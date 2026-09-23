# Troubleshooting

Start here before changing infrastructure code.

## `pixi: command not found`

Pixi is not installed or your shell has not reloaded its PATH.

```bash
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.bashrc
pixi --version
```

## `runpodctl` cannot authenticate

Confirm the shared lab key is set in your current local shell:

```bash
echo "${RUNPOD_API_KEY:+RUNPOD_API_KEY is set}"
runpodctl pod list
```

Never print the actual key into Slack, logs, screenshots, or GitHub.

## vLLM says CUDA out of memory

Typical fixes, in roughly this order:

1. use a smaller model for debugging;
2. shorten the context length;
3. reduce concurrent sequences / batching;
4. use quantization when scientifically acceptable;
5. choose a GPU with more VRAM;
6. use tensor parallelism across multiple GPUs when the experiment genuinely requires it.

Do not scale to expensive GPUs before confirming that the experiment code itself works on a small model.

## `Connection refused` on `localhost:8000`

The inference client cannot reach vLLM.

Check:

```bash
curl http://localhost:8000/health
```

If it fails:

- confirm `pixi run serve` is still running in another terminal;
- wait for the model to finish loading;
- inspect the server terminal for an error;
- confirm the port is 8000.

## The model name is not found

The name sent by the client must match the model name served by vLLM.

For the tutorial:

```bash
MODEL=Qwen/Qwen2.5-1.5B-Instruct \
SERVED_MODEL_NAME=Qwen2.5-1.5B-Instruct \
pixi run serve
```

Then the experiment terminal uses:

```bash
MODEL=Qwen2.5-1.5B-Instruct pixi run experiment
```

## Hugging Face says the model is gated / unauthorized

Some models require you to accept a license or authenticate.

```bash
hf auth login
hf auth whoami
```

Then confirm your Hugging Face account has access to the model.

## `pixi.lock` or dependency mismatch

For an existing project/reproduction run, do not casually regenerate the environment.

Use:

```bash
pixi run --locked test
```

If the lockfile and manifest disagree, ask the project lead whether this is an intentional dependency change before running `pixi update`.

## The Pod disappeared and my files are gone

Pod-local storage is disposable.

Important work must be pushed to GitHub or Hugging Face before the Pod is deleted. RunPod storage should not be the only copy of a scientific artifact.

## Git rejects a large file

Do not immediately force it into Git.

Ask:

1. Can the file be converted to a compact Parquet/JSONL representation?
2. Is it actually necessary to preserve?
3. Is it a large ML artifact that belongs on Hugging Face?
4. Would Git LFS be appropriate?

See [GitHub data conventions](github_data.md).

## The experiment runs but outputs look wrong

Before assuming an infrastructure problem, inspect:

- the exact input rows;
- the checked-in config;
- the served model name;
- temperature/seed/token limit;
- system prompt;
- response metadata;
- Git commit.

Run a 5–20 item pilot and manually inspect outputs before launching a large run.

## Still stuck?

When asking for help, include:

```text
Pod name:
GPU:
Git commit:
Command you ran:
Exact error:
What you expected:
What happened instead:
```

Do not include API keys or other secrets.
