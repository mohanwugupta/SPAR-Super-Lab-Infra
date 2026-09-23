# Hugging Face for large ML artifacts

Hugging Face is **not required for every project**. GitHub is the default long-term home for ordinary-sized project datasets and results.

Use Hugging Face when the artifact is too large or ML-specific for GitHub to be pleasant.

## Good Hugging Face candidates

- large datasets;
- large generated-response datasets;
- model weights;
- adapters;
- reusable activation datasets;
- large checkpoints worth preserving;
- artifacts shared across multiple projects.

A rough lab heuristic is:

```text
< ~1 GB      GitHub by default
~1-10 GB     case-by-case
> ~10 GB     usually Hugging Face
```

These are workflow heuristics, not platform limits.

## Recommended organization setup

Create one Hugging Face organization for the lab, for example:

```text
SPAR-Super-Lab
```

Then create repositories only when a project actually needs them:

```text
SPAR-Super-Lab/common-model-artifacts
SPAR-Super-Lab/preferences-activations
SPAR-Super-Lab/persistence-large-results
```

Use private repositories by default for unpublished work.

Official organization docs:
https://huggingface.co/docs/hub/organizations

## Do not share one lab token

Each lab member should use their own Hugging Face account/token. This gives individual revocation and attribution rather than one shared secret.

Prefer a fine-grained token limited to the resources needed for the project. Never hard-code tokens into Git, configs, or notebooks.

Token docs:
https://huggingface.co/docs/hub/security-tokens

## Authentication

For projects that use Hugging Face:

```bash
hf auth login
hf auth whoami
```

On RunPod, keep the HF cache on fast local storage:

```bash
export SPAR_SCRATCH=/root/scratch
export HF_HOME="$SPAR_SCRATCH/hf"
mkdir -p "$HF_HOME"
```

## Download large data/artifacts

```bash
hf download SPAR-Super-Lab/<repo> \
  --repo-type dataset \
  --local-dir /root/scratch/data
```

For a frozen run, pin the exact revision:

```bash
hf download SPAR-Super-Lab/<repo> \
  --repo-type dataset \
  --revision <FULL_COMMIT_SHA> \
  --local-dir /root/scratch/data
```

## Upload durable large results

```bash
hf upload SPAR-Super-Lab/<artifact-repo> \
  /root/scratch/final-results \
  results/run-001 \
  --repo-type dataset
```

Upload docs:
https://huggingface.co/docs/huggingface_hub/guides/upload

## Record the revision

```yaml
dataset:
  source: huggingface
  repo_id: SPAR-Super-Lab/preferences-activations
  revision: <FULL_COMMIT_SHA>
```

## Relationship to RunPod

```text
Hugging Face = durable source for large artifacts
RunPod local disk = working copy / fast scratch
RunPod Global Volume = optional hot cache
```

Hugging Face storage quotas depend on plan and repository visibility. Check the current limits before moving a very large private collection:

https://huggingface.co/docs/hub/storage-limits
