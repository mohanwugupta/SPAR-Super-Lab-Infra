from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import yaml

from spar_inference import GenerationConfig, VLLMClient, write_run_metadata


def main() -> None:
    config_path = Path(os.environ.get("EXPERIMENT_CONFIG", "configs/first_experiment.yaml"))
    config = yaml.safe_load(config_path.read_text())

    model = os.environ.get("MODEL")
    if not model:
        raise SystemExit(
            "Set MODEL to the vLLM served model name, e.g. "
            "MODEL=Qwen2.5-1.5B-Instruct pixi run experiment"
        )

    generation = config["generation"]
    gen_config = GenerationConfig(
        temperature=float(generation.get("temperature", 0.0)),
        max_tokens=int(generation.get("max_tokens", 64)),
        top_p=float(generation.get("top_p", 1.0)),
        seed=int(generation.get("seed", 0)),
        repetition_penalty=float(generation.get("repetition_penalty", 1.0)),
    )

    input_path = Path(config["input_file"])
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Freeze the exact experiment config next to the outputs.
    (output_dir / "config.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False)
    )

    client = VLLMClient(model_name=model, enable_cache=False)
    output_path = output_dir / "responses.jsonl"

    count = 0
    with input_path.open(newline="", encoding="utf-8") as source, output_path.open(
        "w", encoding="utf-8"
    ) as sink:
        for row in csv.DictReader(source):
            text, request_metadata = client.generate(
                system_prompt=config.get("system_prompt"),
                user_prompt=row["prompt"],
                config=gen_config,
            )
            record = {
                "id": row["id"],
                "prompt": row["prompt"],
                "response": text,
                "request_metadata": request_metadata,
            }
            sink.write(json.dumps(record, ensure_ascii=False) + "\n")
            sink.flush()
            count += 1
            print(f"[{count}] {row['id']}: {text[:100]!r}")

    write_run_metadata(
        output_dir / "metadata.json",
        extra={
            "experiment": "first_experiment",
            "model": model,
            "input_file": str(input_path),
            "n_items": count,
            "experiment_config": config,
        },
    )

    print(f"\nCompleted {count} prompts.")
    print(f"Responses: {output_path}")
    print(f"Metadata:  {output_dir / 'metadata.json'}")


if __name__ == "__main__":
    main()
