# SPAR Super Lab Infrastructure

Shared compute, environment, inference, storage, and research-workflow infrastructure for the SPAR Super Lab.

## Stack

1. **RunPod** provides disposable, on-demand GPU Pods.
2. **Pixi** gives each research project a reproducible environment and lockfile.
3. **GitHub** is the default long-term home for code, configs, documentation, small/medium project datasets, and durable project results that fit comfortably in Git.
4. **Hugging Face Hub** is used when datasets or ML artifacts are too large or awkward for GitHub, especially model weights, large generated datasets, adapters, and reusable activation datasets.
5. **RunPod Global Volume** holds the lab's shared hot model pool and can also be used selectively for staging/caching large assets.
6. **Pod-local disk** is fast scratch for caches, activations, temporary shards, and other high-I/O work.
7. **vLLM + an OpenAI-compatible client** is the default shared inference path.

The main principle is that **RunPod is disposable compute, not the long-term source of truth**. Project code and ordinary-sized datasets/results should survive independently of RunPod. Model weights are a special case: their canonical upstream source is Hugging Face, while a shared copy is kept on RunPod persistent storage so lab members do not repeatedly download the same checkpoints.

The reusable inference pieces here were extracted from [PromptControlText](https://github.com/mohanwugupta/PromptControlText), especially its vLLM client, model-registry pattern, vLLM serving configuration, and concurrent generation workflow.

## New mentee?

If this infrastructure is new to you, use the docs in this order:

1. [5-minute quickstart](docs/quickstart.md)
2. **[Build your first experiment](docs/first_experiment.md)** — the beginner end-to-end tutorial
3. **[Shared model pool](docs/model_pool.md)** — what models exist, where they live, and how to use them
4. [RunPod](docs/runpod.md)
5. [GitHub data conventions](docs/github_data.md)
6. [Hugging Face for large ML artifacts](docs/huggingface.md)
7. [Pixi](docs/pixi.md)
8. [Storage](docs/storage.md)
9. [Research workflow](docs/research_workflow.md)
10. [Compute policy](docs/compute_policy.md)
11. [Mechanistic interpretability](docs/mech_interp.md)
12. [Troubleshooting](docs/troubleshooting.md)

The [template](template/) directory is a starter project that can be copied into a new research repository. It includes a complete toy experiment that can be run on RunPod before modifying anything for a real project.

## Design principle

Use the simplest durable storage layer that fits the artifact:

```text
Fits comfortably in Git?        -> GitHub
Too large / ML-specific?        -> Hugging Face
Shared model checkpoint?        -> Hugging Face upstream + RunPod shared model pool
Temporary/high-I/O?             -> Pod-local scratch
```

We centralize the parts that are stable and broadly reused, especially inference, model access, data conventions, and run metadata. We do **not** yet maintain a large shared mech-interp abstraction.
