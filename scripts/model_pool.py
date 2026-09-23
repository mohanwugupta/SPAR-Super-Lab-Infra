#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "configs" / "model_registry.yaml"
DEFAULT_STAGE_ROOT = Path(os.environ.get("SPAR_SCRATCH", "/root/scratch")) / "models"


def load_registry(path: Path) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load(path.read_text())
    models = data.get("models", {})
    if not isinstance(models, dict):
        raise ValueError("registry must contain a mapping named 'models'")
    return models


def get_model(models: dict[str, dict[str, Any]], slug: str) -> dict[str, Any]:
    try:
        return models[slug]
    except KeyError as exc:
        raise SystemExit(
            f"Unknown model slug: {slug}\nAvailable: {', '.join(sorted(models))}"
        ) from exc


def installed(entry: dict[str, Any]) -> bool:
    path = Path(entry["shared_path"])
    return path.is_dir() and any(path.iterdir())


def marker_path(entry: dict[str, Any]) -> Path:
    return Path(entry["shared_path"]) / ".spar_model.json"


def print_table(models: dict[str, dict[str, Any]]) -> None:
    headers = ["slug", "installed", "gpus", "min_vram", "served_name", "repo_id"]
    rows = []
    for slug, entry in models.items():
        rows.append([
            slug,
            "yes" if installed(entry) else "no",
            str(entry.get("gpus", "?")),
            str(entry.get("min_vram_gb", "?")),
            str(entry.get("served_model_name", "")),
            str(entry.get("repo_id", "")),
        ])

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]
    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(value.ljust(widths[i]) for i, value in enumerate(row)))


def cmd_check(entry: dict[str, Any], slug: str) -> int:
    path = Path(entry["shared_path"])
    print(f"slug:          {slug}")
    print(f"repo_id:       {entry['repo_id']}")
    print(f"revision:      {entry.get('revision', 'main')}")
    print(f"served_name:   {entry.get('served_model_name', '')}")
    print(f"shared_path:   {path}")
    print(f"gpus:          {entry.get('gpus', '?')}")
    print(f"min_vram_gb:   {entry.get('min_vram_gb', '?')}")
    print(f"installed:     {'yes' if installed(entry) else 'no'}")

    marker = marker_path(entry)
    if marker.exists():
        try:
            metadata = json.loads(marker.read_text())
            print(f"resolved_sha:  {metadata.get('resolved_revision', '?')}")
            print(f"downloaded_at: {metadata.get('downloaded_at_unix', '?')}")
        except Exception as exc:
            print(f"marker_error:  {exc}")

    return 0 if installed(entry) else 1


def cmd_download(entry: dict[str, Any], slug: str) -> int:
    from huggingface_hub import HfApi, snapshot_download

    destination = Path(entry["shared_path"])
    destination.mkdir(parents=True, exist_ok=True)

    repo_id = entry["repo_id"]
    revision = entry.get("revision", "main")
    token = os.environ.get("HF_TOKEN")

    print(f"Downloading {repo_id}@{revision}")
    print(f"Destination: {destination}")

    info = HfApi(token=token).model_info(repo_id, revision=revision)
    resolved = info.sha

    snapshot_download(
        repo_id=repo_id,
        revision=resolved,
        local_dir=str(destination),
        token=token,
    )

    marker = {
        "slug": slug,
        "repo_id": repo_id,
        "requested_revision": revision,
        "resolved_revision": resolved,
        "downloaded_at_unix": time.time(),
    }
    marker_path(entry).write_text(json.dumps(marker, indent=2) + "\n")

    print(f"Installed {slug}")
    print(f"Resolved Hugging Face revision: {resolved}")
    if revision == "main":
        print(
            "IMPORTANT: replace revision: main with the resolved SHA in "
            "configs/model_registry.yaml and commit it."
        )
    return 0


def cmd_stage(entry: dict[str, Any], slug: str, force: bool) -> int:
    source = Path(entry["shared_path"])
    if not installed(entry):
        raise SystemExit(
            f"{slug} is not installed at {source}. "
            "Use an installed model or ask the infra maintainer to add it."
        )

    destination = DEFAULT_STAGE_ROOT / entry["local_dir_name"]
    DEFAULT_STAGE_ROOT.mkdir(parents=True, exist_ok=True)

    if destination.exists() and force:
        print(f"Removing existing staged copy: {destination}")
        shutil.rmtree(destination)

    if destination.exists():
        print(f"Already staged: {destination}")
        print(destination)
        return 0

    print(f"Staging {slug}")
    print(f"  from: {source}")
    print(f"  to:   {destination}")
    print("This may take a while for a large model.")

    shutil.copytree(source, destination)
    print(destination)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage the SPAR shared model pool.")
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_REGISTRY),
        help="Path to model registry YAML.",
    )

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List registered models and installation status.")

    p_check = sub.add_parser("check", help="Inspect one model.")
    p_check.add_argument("slug")

    p_path = sub.add_parser("path", help="Print one model's shared path.")
    p_path.add_argument("slug")

    p_download = sub.add_parser(
        "download",
        help="Download one model from Hugging Face to shared storage (maintainers).",
    )
    p_download.add_argument("slug")

    p_stage = sub.add_parser(
        "stage",
        help="Copy one installed shared model to Pod-local scratch.",
    )
    p_stage.add_argument("slug")
    p_stage.add_argument("--force", action="store_true")

    args = parser.parse_args()
    models = load_registry(Path(args.registry))

    if args.command == "list":
        print_table(models)
        return 0

    entry = get_model(models, args.slug)

    if args.command == "check":
        return cmd_check(entry, args.slug)
    if args.command == "path":
        print(entry["shared_path"])
        return 0
    if args.command == "download":
        return cmd_download(entry, args.slug)
    if args.command == "stage":
        return cmd_stage(entry, args.slug, args.force)

    return 2


if __name__ == "__main__":
    sys.exit(main())
