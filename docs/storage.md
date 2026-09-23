# Storage

The lab uses a **GitHub-first durable storage policy**, with Hugging Face for larger ML artifacts and RunPod for compute/working storage.

```text
                      DURABLE
          GitHub                    Hugging Face
 code/configs/docs/data/results     large datasets/models/activations
              \                     /
               \                   /
                ----> RunPod Pod <---
                      |
                      | fast local scratch
                      v
                   experiment

RunPod Global Volume = optional hot cache / staging layer
```

## 1. GitHub: default source of truth

GitHub is preferred when the project's durable data fit comfortably in Git.

Store:
- source code;
- configs;
- Pixi manifests/lockfiles;
- prompts;
- documentation;
- benchmark inputs;
- small/medium processed datasets;
- generated behavioral results;
- analysis-ready tables;
- publication data.

This has a major long-term advantage: after the fellowship, the project remains self-contained without paying for RunPod storage.

See [GitHub data conventions](github_data.md).

## 2. Hugging Face: large / ML-specific durable artifacts

Use Hugging Face when GitHub becomes awkward, especially for:
- multi-GB datasets;
- model weights/adapters;
- large activation datasets;
- large generated datasets;
- reusable ML artifacts.

A practical rule of thumb:

```text
< ~1 GB      GitHub by default
~1-10 GB     decide based on churn/format/use
> ~10 GB     usually Hugging Face
```

These are operational heuristics rather than hard platform limits.

See [Hugging Face](huggingface.md).

## 3. RunPod Global Volume: optional hot cache / staging

The Global Volume `spar-super-lab-workspace` is **not the canonical lab filesystem**.

Use it selectively for:
- a hot copy of a large model repeatedly loaded by multiple Pods;
- a dataset repeatedly reused across short-lived Pods;
- temporary cross-Pod handoff;
- staging before upload to GitHub/Hugging Face.

Do not rely on the Global Volume as the only copy of scientifically important data.

## 4. Pod-local disk: fast disposable scratch

```bash
export SPAR_SCRATCH=/root/scratch
export HF_HOME="$SPAR_SCRATCH/hf"
mkdir -p "$SPAR_SCRATCH" "$HF_HOME"
```

Use local disk for:
- cloned Git repositories;
- Hugging Face/vLLM caches;
- temporary activations;
- intermediate shards;
- probe-training scratch;
- extracted hidden states;
- current experiment working files.

## Common case: everything fits in GitHub

```bash
git clone <PROJECT_REPO>
cd <PROJECT_REPO>
pixi run --locked experiment
```

No Hugging Face or Global Volume is required.

## Large-artifact case

```bash
git clone <PROJECT_REPO>
cd <PROJECT_REPO>

hf download SPAR-Super-Lab/<large-data-repo> \
  --repo-type dataset \
  --local-dir /root/scratch/data

pixi run --locked experiment

hf upload SPAR-Super-Lab/<artifact-repo> \
  /root/scratch/final-results \
  results/run-001 \
  --repo-type dataset
```

## Failure rule

Assume everything unique on RunPod can disappear.

If an artifact matters scientifically, its canonical copy should eventually live in **GitHub or Hugging Face**, not only on RunPod.
