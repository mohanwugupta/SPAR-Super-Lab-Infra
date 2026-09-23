# SPAR Super Lab Infrastructure

Shared compute, environment, inference, storage, and research-workflow infrastructure for the SPAR Super Lab.

## Stack

1. **RunPod** provides on-demand GPU Pods.
2. **Pixi** gives each research project a reproducible environment and lockfile.
3. **GitHub** stores code, configs, documentation, and reviews.
4. **RunPod Global Volume** stores durable shared assets and final outputs.
5. **Pod-local disk** is fast scratch for caches, activations, temporary shards, and other high-I/O work.
6. **vLLM + an OpenAI-compatible client** is the default shared inference path.

The reusable inference pieces here were extracted from [PromptControlText](https://github.com/mohanwugupta/PromptControlText), especially its vLLM client, model-registry pattern, vLLM serving configuration, and concurrent generation workflow. The version here removes benchmark-specific logic and adds stronger reproducibility metadata.

## New mentee?

Read these in order:

1. [5-minute quickstart](docs/quickstart.md)
2. [RunPod](docs/runpod.md)
3. [Pixi](docs/pixi.md)
4. [Storage](docs/storage.md)
5. [Research workflow](docs/research_workflow.md)
6. [Compute policy](docs/compute_policy.md)
7. [Mechanistic interpretability](docs/mech_interp.md)

The [template](template/) directory is a starter project that can be copied into a new research repository.

## Design principle

We centralize the parts that are stable and broadly reused, especially inference and run metadata. We do **not** yet maintain a large shared mech-interp abstraction. Mechanistic-interpretability workflows vary enough that the safer initial pattern is to keep known-good recipes inside each project and promote utilities into shared code only after they recur across multiple projects.
