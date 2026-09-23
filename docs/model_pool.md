# Shared model pool

Most experiments should use the **shared pool of model checkpoints already stored on the RunPod Global Volume** rather than downloading a fresh copy onto every Pod.

The mental model is:

```text
MODEL CATALOG
configs/model_registry.yaml
"What models can I use?"
        |
        v
SHARED MODEL STORAGE
/workspace/hot-cache/models/
"Where are the weights?"
        |
        v
vLLM
"Serve the selected checkpoint"
        |
        v
EXPERIMENT
"Send prompts to localhost:8000"
```

Hugging Face remains the canonical upstream source for the original model weights. The RunPod copy is a shared operational cache that saves setup time and repeated downloads.

## Where models live

When the Global Volume is attached at `/workspace`, the shared pool is:

```text
/workspace/hot-cache/models/
```

Example:

```text
/workspace/hot-cache/models/
├── Qwen--Qwen2.5-1.5B-Instruct/
├── Qwen--Qwen2.5-7B-Instruct/
├── deepseek-ai--DeepSeek-R1-Distill-Qwen-32B/
└── meta-llama--Llama-3.3-70B-Instruct/
```

The exact available set is defined in the canonical registry:

```text
configs/model_registry.yaml
```

Do not assume every model listed in the registry has already been downloaded. Use `model-list` or `model-check`.

## See what is available

From a clone of this infrastructure repository:

```bash
pixi run model-list
```

This shows:
- model slug;
- Hugging Face repo;
- served model name;
- expected GPU count;
- rough VRAM guidance;
- shared path;
- whether the path currently exists.

Check one model:

```bash
pixi run model-check qwen25_7b
```

Print its shared path:

```bash
pixi run model-path qwen25_7b
```

## Normal mentee workflow

For most behavioral/inference experiments:

1. Attach `spar-super-lab-workspace` when launching the Pod.
2. Pick a model marked as installed in the shared pool.
3. Start vLLM from the shared path.
4. Run the experiment in a second terminal.

Example:

```bash
cd /root/projects/my-project

MODEL=/workspace/hot-cache/models/Qwen--Qwen2.5-7B-Instruct \
SERVED_MODEL_NAME=Qwen2.5-7B-Instruct \
TP=1 \
MAX_MODEL_LEN=8192 \
pixi run serve
```

Then in another terminal:

```bash
MODEL=Qwen2.5-7B-Instruct pixi run experiment
```

The first `MODEL` is a **filesystem path used by vLLM to load the checkpoint**.

The second `MODEL` is the **served model name used by the inference client**.

## If direct loading from the Global Volume is slow

The Global Volume is persistent shared/object-backed storage, not fast local scratch. For some models/workloads, it may be better to copy the checkpoint onto Pod-local disk before starting vLLM.

From this infrastructure repository:

```bash
pixi run model-stage qwen25_7b
```

By default that copies the model to:

```text
/root/scratch/models/<model-directory>
```

The command prints the staged local path. Use that path as `MODEL` when starting vLLM.

This pattern is:

```text
Hugging Face
    ↓ one-time shared download
RunPod Global Volume
    ↓ fast staging copy when needed
Pod-local disk
    ↓
vLLM
```

Do not stage by default unless startup/I/O from the shared volume is actually a bottleneck; copying a large model also takes time and requires enough local disk.

## Adding a model to the pool

Lab members should generally **not independently download large models into the shared pool**. Request the model in Slack or coordinate with whoever is maintaining infrastructure.

The maintainer workflow is:

```bash
cd SPAR-Super-Lab-Infra

# Inspect the registry entry
pixi run model-check qwen25_7b

# Download the Hugging Face snapshot into shared storage
pixi run model-download qwen25_7b

# Verify it
pixi run model-check qwen25_7b
```

For gated Hugging Face checkpoints, authenticate first:

```bash
hf auth login
```

After a new model is downloaded, pin the resolved Hugging Face commit SHA in `configs/model_registry.yaml` and commit that registry change. This makes the shared pool reproducible rather than silently tracking an evolving `main` revision.

## Choosing a model and GPU

The registry contains rough resource guidance. It is not a guarantee because VRAM needs depend on dtype, quantization, context length, batching, architecture, and vLLM version.

For development:

- use the smallest model that exercises your code;
- use one GPU unless the experiment requires more;
- scale only after a small pilot works.

If the model you need is not in the shared pool, ask whether an existing checkpoint can answer the scientific question before adding another large copy.
