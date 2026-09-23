# SPAR Super Lab Infrastructure

Shared compute, environment, inference, storage, and research-workflow infrastructure for the SPAR Super Lab.

## Stack

1. **RunPod** provides disposable, on-demand GPU Pods.
2. **Pixi** gives each research project a reproducible environment and lockfile.
3. **GitHub** is the default long-term home for code, configs, documentation, small/medium project datasets, and durable project results that fit comfortably in Git.
4. **Hugging Face Hub** is used when datasets or ML artifacts are too large or awkward for GitHub, especially model weights, large generated datasets, adapters, and reusable activation datasets.
5. **RunPod Global Volume** is an optional hot cache / staging layer for large assets that are expensive to download repeatedly.
6. **Pod-local disk** is fast scratch for caches, activations, temporary shards, and other high-I/O work.
7. **vLLM + an OpenAI-compatible client** is the default shared inference path.

The main principle is that **RunPod is disposable compute, not the long-term source of truth**. After the fellowship ends, project code and ordinary-sized datasets/results should still live in durable repositories that do not depend on keeping RunPod storage online.

The reusable inference pieces here were extracted from [PromptControlText](https://github.com/mohanwugupta/PromptControlText), especially its vLLM client, model-registry pattern, vLLM serving configuration, and concurrent generation workflow. The version here removes benchmark-specific logic and adds stronger reproducibility metadata.

## New mentee?

If this infrastructure is new to you, use the docs in this order:

1. [5-minute quickstart](docs/quickstart.md)
2. **[Build your first experiment](docs/first_experiment.md)** — the beginner end-to-end tutorial
3. [RunPod](docs/runpod.md)
4. [GitHub data conventions](docs/github_data.md)
5. [Hugging Face for large ML artifacts](docs/huggingface.md)
6. [Pixi](docs/pixi.md)
7. [Storage](docs/storage.md)
8. [Research workflow](docs/research_workflow.md)
9. [Compute policy](docs/compute_policy.md)
10. [Mechanistic interpretability](docs/mech_interp.md)
11. [Troubleshooting](docs/troubleshooting.md)

The [template](template/) directory is a starter project that can be copied into a new research repository. It includes a complete toy experiment that can be run on RunPod before modifying anything for a real project.

## Design principle

Use the simplest durable storage layer that fits the artifact:

```text
Fits comfortably in Git?        -> GitHub
Too large / ML-specific?        -> Hugging Face
Needed repeatedly during runs?  -> optional RunPod hot cache
Temporary/high-I/O?             -> Pod-local scratch
```

We centralize the parts that are stable and broadly reused, especially inference, data conventions, and run metadata. We do **not** yet maintain a large shared mech-interp abstraction.
