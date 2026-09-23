# SPAR Super Lab Infrastructure

Shared compute, environment, inference, storage, and research-workflow infrastructure for the SPAR Super Lab.

## Stack

1. **RunPod** provides disposable, on-demand GPU Pods.
2. **Pixi** gives each research project a reproducible environment and lockfile.
3. **GitHub** is the canonical home for code, configs, documentation, and reviews.
4. **Hugging Face Hub** is the canonical home for reusable datasets, model artifacts, and durable research artifacts.
5. **RunPod Global Volume** is an optional hot cache / staging layer for large assets that are expensive to download repeatedly.
6. **Pod-local disk** is fast scratch for caches, activations, temporary shards, and other high-I/O work.
7. **vLLM + an OpenAI-compatible client** is the default shared inference path.

This makes the compute provider disposable: code lives on GitHub, durable data/artifacts live on Hugging Face, and RunPod supplies GPUs and temporary working storage.

The reusable inference pieces here were extracted from [PromptControlText](https://github.com/mohanwugupta/PromptControlText), especially its vLLM client, model-registry pattern, vLLM serving configuration, and concurrent generation workflow. The version here removes benchmark-specific logic and adds stronger reproducibility metadata.

## New mentee?

Read these in order:

1. [5-minute quickstart](docs/quickstart.md)
2. [RunPod](docs/runpod.md)
3. [Hugging Face](docs/huggingface.md)
4. [Pixi](docs/pixi.md)
5. [Storage](docs/storage.md)
6. [Research workflow](docs/research_workflow.md)
7. [Compute policy](docs/compute_policy.md)
8. [Mechanistic interpretability](docs/mech_interp.md)

The [template](template/) directory is a starter project that can be copied into a new research repository.

## Design principle

We centralize the parts that are stable and broadly reused, especially inference, data conventions, and run metadata. We do **not** yet maintain a large shared mech-interp abstraction. Mechanistic-interpretability workflows vary enough that the safer initial pattern is to keep known-good recipes inside each project and promote utilities into shared code only after they recur across multiple projects.
