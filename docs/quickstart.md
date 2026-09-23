# 5-minute quickstart

## One-time local setup

```bash
curl -fsSL https://pixi.sh/install.sh | bash
pixi global install runpodctl
runpodctl update
runpodctl doctor
```

Each person should use their own RunPod credentials. Do not share API keys.

You will also need your own Hugging Face account/token with access to the SPAR organization:

```bash
hf auth login
hf auth whoami
```

Do not share a common Hugging Face token.

## Start a GPU

Inspect capacity first:

```bash
runpodctl gpu list
runpodctl datacenter list
runpodctl pod list
```

For interactive work, deploy the shared SPAR template, request **one inexpensive appropriate GPU**, and name the Pod:

```text
<person>-<project>-<purpose>
```

Attach `spar-super-lab-workspace` only when you need the shared hot-cache/staging layer; it is not required for every job.

## Work on the Pod

Keep the repo and high-I/O working files on local Pod disk:

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

Pull project data from Hugging Face into local scratch:

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

- **GitHub:** code/configs/docs
- **Hugging Face:** canonical datasets and reusable/durable artifacts
- **Global Volume:** optional hot cache/staging
- **Pod-local disk:** caches, activations, temporary shards, fast scratch

## Finish

Upload anything worth keeping to its Hugging Face repository, confirm the upload, then delete the Pod:

```bash
runpodctl pod list
runpodctl pod delete <pod-id>
```
