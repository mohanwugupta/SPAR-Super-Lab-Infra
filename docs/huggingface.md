# Hugging Face Hub

Hugging Face is the lab's **canonical storage layer for reusable datasets and durable ML artifacts**. RunPod is compute, not the source of truth.

## Recommended organization setup

Create one Hugging Face organization for the lab, for example:

```text
SPAR-Super-Lab
```

Then create separate repositories by project or artifact family:

```text
SPAR-Super-Lab/common-data                  dataset repo
SPAR-Super-Lab/task-selection-data          dataset repo
SPAR-Super-Lab/preferences-data             dataset repo
SPAR-Super-Lab/persistence-artifacts        dataset repo
SPAR-Super-Lab/shared-adapters              model repo
```

Use private repositories by default for unpublished work. Public repos are appropriate only when the project is ready to release the data/artifact.

Official organization docs:
https://huggingface.co/docs/hub/organizations

## Do not share one lab token

Each lab member should:

1. have their own Hugging Face account;
2. join the lab organization;
3. create their own token;
4. authenticate their own laptop/Pod.

This gives us individual revocation and attribution rather than one shared secret.

Prefer a **fine-grained token** limited to the organization/resources needed for the project. Read-only work should use read access; upload workflows need write access.

Token docs:
https://huggingface.co/docs/hub/security-tokens

## Organization roles

Hugging Face organization roles include read, contributor, write, and admin.

For a simple lab where everyone can see the same unpublished datasets:
- most members can be **read** if they only consume shared data;
- give **write** only to people who need to update shared repositories;
- keep **admin** limited to mentors/infra maintainers.

Fine-grained repository isolation inside one organization is available through Hugging Face Resource Groups on Team/Enterprise plans. A free organization should not be treated as strong project-by-project access isolation.

Access-control docs:
https://huggingface.co/docs/hub/organizations-security

## One-time authentication

Install/use a recent Hugging Face CLI and log in:

```bash
hf auth login
hf auth whoami
```

The browser/token login is stored locally. On RunPod, keep Hugging Face's cache on fast local Pod storage:

```bash
export SPAR_SCRATCH=/root/scratch
export HF_HOME="$SPAR_SCRATCH/hf"
mkdir -p "$HF_HOME"
```

For non-interactive automation, `HF_TOKEN` can be supplied as a secret/environment variable. Never hard-code it into code, YAML, notebooks, or Git.

Authentication docs:
https://huggingface.co/docs/huggingface_hub/quick-start

## Download data to a Pod

For an entire dataset repository:

```bash
mkdir -p /root/scratch/task-selection-data

hf download SPAR-Super-Lab/task-selection-data \
  --repo-type dataset \
  --local-dir /root/scratch/task-selection-data
```

For a frozen publication/reproduction run, pin a revision:

```bash
hf download SPAR-Super-Lab/task-selection-data \
  --repo-type dataset \
  --revision <FULL_COMMIT_SHA> \
  --local-dir /root/scratch/task-selection-data
```

The important principle is:

```text
HF Hub = source of truth
local Pod disk = working copy
```

## Upload durable results

Upload only artifacts worth keeping, rather than every temporary tensor:

```bash
hf upload SPAR-Super-Lab/persistence-artifacts \
  /root/scratch/final-results \
  results/run-001 \
  --repo-type dataset
```

The current `hf upload` flow supports large/resumable folder uploads. If an upload is interrupted, rerun it rather than inventing a second destination.

Upload docs:
https://huggingface.co/docs/huggingface_hub/guides/upload

## Record the Hub revision

Important runs should record the exact Hugging Face commit used. For example:

```bash
python - <<'PY'
from huggingface_hub import HfApi

info = HfApi().repo_info(
    "SPAR-Super-Lab/task-selection-data",
    repo_type="dataset",
)
print(info.sha)
PY
```

Put that SHA in the experiment config/metadata:

```yaml
dataset:
  repo_id: SPAR-Super-Lab/task-selection-data
  revision: <FULL_COMMIT_SHA>
```

This is the data equivalent of pinning a Git commit.

## Repository conventions

Dataset repositories should prefer stable, machine-friendly formats:

```text
README.md
data/
  train-00000-of-00004.parquet
  train-00001-of-00004.parquet
metadata/
  schema.json
  provenance.json
artifacts/
  <optional reusable derived artifacts>
```

Avoid thousands of tiny files when a small number of Parquet/JSONL shards will do.

## What belongs where

### Hugging Face
- canonical datasets;
- frozen/generated response datasets;
- reusable activation datasets;
- adapters/model artifacts;
- durable checkpoints worth sharing;
- release artifacts.

### RunPod Global Volume
- optional hot copies of frequently reused large assets;
- staging data that would be expensive to download repeatedly;
- temporary cross-Pod handoff when HF is inconvenient.

### Pod-local disk
- HF/vLLM cache;
- activations currently being computed;
- temporary checkpoint shards;
- intermediate tensors;
- high-I/O mech-interp work.

### GitHub
- code;
- prompts/configs;
- Pixi lockfiles;
- documentation;
- small test fixtures.

## Storage limits

Hugging Face's storage quotas depend on account/organization plan and repository visibility. As of September 2026, a free user/org includes limited private storage, while paid organization plans provide larger private quotas and paid expansion. Check the current storage page before moving a very large private artifact collection:

https://huggingface.co/docs/hub/storage-limits
