# Storage

The lab uses a **GitHub-first durable storage policy**, Hugging Face for larger ML artifacts/upstream model sources, a RunPod shared model pool, and Pod-local storage for active work.

```text
GitHub                         Hugging Face
code/data/results              large artifacts + upstream models
      \                             /
       \                           /
        ---- durable sources -------
                    |
                    v
       RunPod Global Volume
       shared model pool / hot cache
                    |
                    v
              RunPod Pod
                    |
             local fast scratch
```

## 1. GitHub: default source of truth

GitHub is preferred when project data/results fit comfortably in Git: code, configs, prompts, benchmark inputs, small/medium datasets, generated behavioral results, and analysis-ready tables.

## 2. Hugging Face: large / ML-specific durable artifacts

Use Hugging Face for large datasets, adapters, activation datasets, large results, and as the canonical upstream source for model checkpoints.

## 3. RunPod Global Volume: shared model pool + hot cache

The Global Volume `spar-super-lab-workspace` has one especially important role: **the common model pool**.

When mounted at `/workspace`:

```text
/workspace/
  hot-cache/
    models/
      <shared checkpoints>
    datasets/
  staging/
  cross-pod/
```

Most model-based experiments should attach this volume and load an existing shared checkpoint rather than redownloading it.

See [Shared model pool](model_pool.md).

The Global Volume is still not the canonical source of scientifically unique project results. If the fellowship ends or RunPod storage is removed, code/results should remain on GitHub/Hugging Face, and model checkpoints can be reconstructed from their pinned Hugging Face revisions.

## 4. Pod-local disk: fast disposable scratch

```bash
export SPAR_SCRATCH=/root/scratch
mkdir -p "$SPAR_SCRATCH"
```

Use local disk for cloned repos, vLLM caches, temporary activations, intermediate shards, probe-training scratch, and optionally staged copies of shared model checkpoints.

Assume unique local Pod data can disappear. Anything scientifically important should eventually live in GitHub or Hugging Face.
