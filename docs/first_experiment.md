# Build your first experiment

This tutorial is for someone who can use a terminal at a basic level but has little or no experience with RunPod, Pixi, or vLLM.

The goal is to complete one full research loop:

```text
20 prompts
   ↓
RunPod GPU
   ↓
vLLM model server
   ↓
Python experiment
   ↓
responses.jsonl + metadata.json
   ↓
save useful work
   ↓
delete GPU
```

Do this once before starting a real experiment.

## 0. The four concepts you need

You do not need to understand the infrastructure deeply yet.

- **GitHub** stores the project code and ordinary-sized data.
- **RunPod** rents you a GPU computer.
- **Pixi** installs exactly the software versions the project expects.
- **vLLM** loads the language model onto the GPU and exposes a local interface that our Python code sends prompts to.

A command such as:

```bash
pixi run experiment
```

means: "run the project's named `experiment` command inside its reproducible environment."

An environment variable such as:

```bash
export MODEL=Qwen2.5-1.5B-Instruct
```

is a temporary setting available to programs launched from that terminal.

## 1. Know what you normally edit

For a real project, you will usually modify:

```text
configs/
data/
experiments/
analysis/
```

You usually should **not** need to modify:

```text
spar_inference/
scripts/serve_vllm.sh
Pixi infrastructure
```

If you think you need to change the shared inference code just to run a normal experiment, ask first.

## 2. Choose a GPU

For this tutorial, use a cheap GPU with roughly **16–24 GB VRAM**. The included 1.5B model is intentionally small.

A rough starting guide:

| Task | Reasonable starting VRAM |
| --- | ---: |
| Debugging / <3B model | 16–24 GB |
| 7–8B inference | ~24 GB |
| 14B inference | ~32–48 GB |
| 30–32B inference | ~48–80 GB or quantization |
| 70B inference | usually multi-GPU / high-memory |
| Basic mech interp on a small model | 24–48 GB |
| Large activation extraction | calculate model + activation requirements first |

This is a rough planning guide, not a guarantee. Context length, batch size, dtype, quantization, and the model architecture all affect memory.

When debugging code, use the **smallest model and cheapest GPU that exercise the code path**.

## 3. Launch a RunPod

Use the shared SPAR RunPod account/API key described in [Quickstart](quickstart.md).

Give the Pod a recognizable name, for example:

```text
mohan-first-experiment
```

For this tutorial, you do not need the Global Volume.

Once the Pod is running, open its web terminal or SSH into it.

Verify the GPU:

```bash
nvidia-smi
```

If you see the GPU and its memory, the machine is ready.

## 4. Copy the project template

For this tutorial you can work directly from this infrastructure repository:

```bash
mkdir -p /root/projects
cd /root/projects

git clone https://github.com/mohanwugupta/SPAR-Super-Lab-Infra.git
cd SPAR-Super-Lab-Infra/template
```

The important files are:

```text
template/
├── configs/
│   └── first_experiment.yaml
├── data/
│   └── prompts.csv
├── experiments/
│   └── run_first_experiment.py
├── spar_inference/
├── scripts/
│   └── serve_vllm.sh
└── pixi.toml
```

## 5. Install the environment

From `template/`:

```bash
pixi install
pixi run test
```

The first install may take several minutes. Later runs are faster because the environment is cached.

If `pixi run test` passes, the project environment is working.

## 6. Look at the experiment before running it

The input data are in:

```text
data/prompts.csv
```

The experimental settings are in:

```text
configs/first_experiment.yaml
```

View them:

```bash
cat data/prompts.csv
cat configs/first_experiment.yaml
```

The configuration controls the system prompt, temperature, token limit, seed, input file, and output directory.

This separation is intentional: **changing an experimental variable should usually mean changing a config, not rewriting infrastructure code.**

## 7. Start the model server

In your first terminal:

```bash
export SPAR_SCRATCH=/root/scratch
mkdir -p "$SPAR_SCRATCH"

MODEL=Qwen/Qwen2.5-1.5B-Instruct \
SERVED_MODEL_NAME=Qwen2.5-1.5B-Instruct \
pixi run serve
```

You will see model-loading logs. Wait until vLLM reports that the server is ready.

**Leave this terminal running.** It is now the model server.

## 8. Open a second terminal

Open another web terminal tab or SSH into the same Pod again.

Go back to the template:

```bash
cd /root/projects/SPAR-Super-Lab-Infra/template
```

Confirm that the server responds:

```bash
curl http://localhost:8000/health
```

If that succeeds, run the experiment:

```bash
MODEL=Qwen2.5-1.5B-Instruct pixi run experiment
```

The experiment will send all 20 prompts to the local vLLM server and save each response as it finishes.

## 9. Inspect the results

You should now have:

```text
results/first_experiment/
├── config.yaml
├── metadata.json
└── responses.jsonl
```

Inspect the first few responses:

```bash
head -n 5 results/first_experiment/responses.jsonl
```

Inspect the reproducibility metadata:

```bash
cat results/first_experiment/metadata.json
```

The metadata records information such as the Git commit, software versions, GPU, model, and experiment settings.

## 10. Change exactly one variable

Now make a small scientific manipulation.

For example, change:

```yaml
system_prompt: "Answer each question in one short sentence."
```

to:

```yaml
system_prompt: "Answer each question cautiously and explain uncertainty."
```

Also change the output directory so the new run does not overwrite the old one:

```yaml
output_dir: results/first_experiment_cautious
```

Then rerun:

```bash
MODEL=Qwen2.5-1.5B-Instruct pixi run experiment
```

Compare the two output directories.

That is the basic experimental loop: **hold everything fixed, manipulate the variable you care about, and preserve the exact config + metadata for each run.**

## 11. Moving to a real project

For a real study, copy the contents of `template/` into its own GitHub repository, then replace:

- `data/prompts.csv` with your project data;
- `configs/first_experiment.yaml` with your experimental configs;
- `experiments/run_first_experiment.py` with the project runner.

Keep the shared `spar_inference/` and `scripts/serve_vllm.sh` infrastructure unless the project genuinely requires different behavior.

## 12. Save your work before deleting the Pod

For ordinary-sized results, commit/push the scientifically useful files to the project's GitHub repository.

Do **not** blindly commit every temporary output. Preserve inputs, frozen configs, important result tables, analysis-ready outputs, and anything needed to reproduce the result.

Large artifacts belong on Hugging Face; high-volume temporary tensors can remain disposable.

Finally, verify that everything worth keeping is off the Pod, then terminate it.

## You are ready for a real experiment when

You can do all of these without guessing:

- launch and identify your RunPod;
- clone the project;
- run `pixi install` / `pixi run test`;
- start vLLM;
- run the experiment in another terminal;
- find and inspect the outputs;
- identify which config changed between two runs;
- preserve useful results;
- terminate the GPU.

If one of those steps fails, use [Troubleshooting](troubleshooting.md) before scaling up.
