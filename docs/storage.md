# Storage

The lab uses a four-layer storage model. **GitHub and Hugging Face are the durable sources of truth; RunPod storage is operational infrastructure.**

```text
GitHub                         Hugging Face Hub
code/configs/docs              canonical data/artifacts
        \                       /
         \                     /
          -----> RunPod Pod <---
                 |
                 | local fast scratch
                 v
            experiment
                 |
                 v
       durable outputs -> Hugging Face

RunPod Global Volume = optional hot cache/staging layer
```

## 1. GitHub: code and experiment definitions

Store:
- source code;
- configs;
- Pixi manifests/lockfiles;
- prompts;
- docs;
- small fixtures.

Do not use GitHub for model weights, activation dumps, or large generated datasets.

## 2. Hugging Face: canonical data and artifacts

Hugging Face is the default durable home for:
- datasets;
- generated-response datasets;
- reusable activation datasets;
- adapters/model artifacts;
- important reusable checkpoints;
- final artifacts that should survive a compute-provider change.

Prefer one repository per project/artifact family, and record the exact Hub commit SHA used by important experiments.

See [Hugging Face setup](huggingface.md).

## 3. RunPod Global Volume: hot cache / staging

The Global Volume `spar-super-lab-workspace` is **not the canonical lab filesystem**.

Use it selectively for things that are expensive to repeatedly transfer between Pods, for example:

```text
/workspace/
  hot-cache/
    models/
    datasets/
  staging/
  cross-pod/
```

A useful pattern for a frequently reused large model is:

```text
Hugging Face (canonical)
        |
        v
Global Volume hot copy
        |
        v
copy/stage to Pod-local disk
        |
        v
run inference
```

Do not rely on the Global Volume as the only copy of scientifically important data.

Do not treat it as a POSIX parallel scratch filesystem; avoid concurrent writers to the same file and high-frequency small-file I/O.

## 4. Pod-local disk: fast disposable scratch

```bash
export SPAR_SCRATCH=/root/scratch
export HF_HOME="$SPAR_SCRATCH/hf"
mkdir -p "$SPAR_SCRATCH" "$HF_HOME"
```

Use local disk for:
- Hugging Face/vLLM caches;
- temporary activations;
- intermediate shards;
- probe-training scratch;
- extracted hidden states;
- current experiment working files.

Example:

```bash
# Pull a durable dataset to local scratch
hf download SPAR-Super-Lab/my-project-data \
  --repo-type dataset \
  --local-dir /root/scratch/data

# High-I/O work remains local
pixi run extract-activations --output /root/scratch/acts

# Upload only useful durable outputs
hf upload SPAR-Super-Lab/my-project-artifacts \
  /root/scratch/final-results \
  results/run-001 \
  --repo-type dataset
```

## Failure rule

Assume everything on local Pod storage can disappear when the Pod is deleted.

If an artifact matters scientifically, it should end up in **Hugging Face or GitHub**, not only on RunPod.
