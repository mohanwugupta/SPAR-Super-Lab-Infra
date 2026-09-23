# 5-minute quickstart

> **New to RunPod/Pixi/vLLM?** Follow [Build your first experiment](first_experiment.md) once before using this page as a reference.

## One-time local setup

```bash
curl -fsSL https://pixi.sh/install.sh | bash
pixi global install runpodctl
runpodctl update
runpodctl doctor
```

The lab uses a **shared RunPod API key** so everyone launches compute from the same group account and shared pool of money. Use the key provided privately by the lab and never commit it to GitHub or share it outside the group.

```bash
export RUNPOD_API_KEY="<SPAR_SHARED_RUNPOD_API_KEY>"
```

Hugging Face authentication is needed only for projects that access gated HF assets or for maintainers adding models to the shared pool.

## Start a GPU

```bash
runpodctl gpu list
runpodctl datacenter list
runpodctl pod list
```

Deploy the shared SPAR template, request an appropriate GPU, and name the Pod:

```text
<person>-<project>-<purpose>
```

**Attach `spar-super-lab-workspace` for normal model-based experiments**, because the shared model pool lives on that persistent volume.

## Find a model

Clone or update this infrastructure repo:

```bash
cd /root/projects
git clone https://github.com/mohanwugupta/SPAR-Super-Lab-Infra.git
cd SPAR-Super-Lab-Infra

pixi run model-list
```

The model weights normally live under:

```text
/workspace/hot-cache/models/
```

See [Shared model pool](model_pool.md).

## Work on your project

Clone the project repository onto local Pod storage:

```bash
mkdir -p /root/projects /root/scratch
export SPAR_SCRATCH=/root/scratch

cd /root/projects
git clone <PROJECT_REPO_URL>
cd <PROJECT_REPO>
pixi run --locked test
```

Start an installed shared model, for example:

```bash
MODEL=/workspace/hot-cache/models/Qwen--Qwen2.5-7B-Instruct \
SERVED_MODEL_NAME=Qwen2.5-7B-Instruct \
pixi run serve
```

Then in a second terminal:

```bash
cd /root/projects/<PROJECT_REPO>
MODEL=Qwen2.5-7B-Instruct pixi run experiment
```

## Storage rule

- **GitHub:** code/configs/docs + ordinary-sized datasets/results
- **Hugging Face:** large datasets/artifacts and upstream model source
- **Global Volume:** shared model pool + optional hot cache/staging
- **Pod-local disk:** project checkout, activations, caches, temporary shards

## Finish

Persist anything scientifically important to GitHub/Hugging Face, then delete the Pod:

```bash
runpodctl pod list
runpodctl pod delete <pod-id>
```
