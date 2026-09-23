# 5-minute quickstart

## One-time local setup

```bash
curl -fsSL https://pixi.sh/install.sh | bash
pixi global install runpodctl
runpodctl update
runpodctl doctor
```

Each person should use their own RunPod credentials. Do not share API keys.

Hugging Face authentication is needed **only for projects that use large HF-hosted datasets/models/artifacts**:

```bash
hf auth login
hf auth whoami
```

## Start a GPU

```bash
runpodctl gpu list
runpodctl datacenter list
runpodctl pod list
```

Deploy the shared SPAR template, request **one inexpensive appropriate GPU**, and name the Pod:

```text
<person>-<project>-<purpose>
```

Attach `spar-super-lab-workspace` only when the project benefits from the shared hot cache/staging layer.

## Work on the Pod

Most projects should start simply by cloning their GitHub repository:

```bash
mkdir -p /root/projects /root/scratch
export SPAR_SCRATCH=/root/scratch
export HF_HOME="$SPAR_SCRATCH/hf"

cd /root/projects
git clone <REPO_URL>
cd <REPO>

pixi run --locked test
pixi run --locked <project-task>
```

If the project's dataset is in the GitHub repository, that is all you need.

If the project has a large Hugging Face dataset/artifact:

```bash
hf download SPAR-Super-Lab/<dataset-repo> \
  --repo-type dataset \
  --local-dir /root/scratch/data
```

For the starter inference stack:

```bash
MODEL=<served-model-name> pixi run inference-smoke
```

## Storage rule

- **GitHub:** code/configs/docs + ordinary-sized datasets/results
- **Hugging Face:** large datasets/models/activation artifacts
- **Global Volume:** optional hot cache/staging
- **Pod-local disk:** caches, activations, temporary shards, fast scratch

## Finish

Persist anything scientifically important to its canonical GitHub/Hugging Face location, then delete the Pod:

```bash
runpodctl pod list
runpodctl pod delete <pod-id>
```
