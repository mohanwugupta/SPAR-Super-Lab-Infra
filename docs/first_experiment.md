# Build your first experiment

This tutorial is for someone who can use a terminal at a basic level but has little or no experience with RunPod, Pixi, or vLLM.

The goal is to complete one full research loop:

```text
20 prompts
   ↓
shared model checkpoint
   ↓
RunPod GPU + vLLM
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

## 0. The five concepts you need

- **GitHub** stores project code and ordinary-sized data.
- **RunPod** rents you a GPU computer.
- **RunPod Global Volume** stores the lab's shared model pool.
- **Pixi** installs exactly the software versions the project expects.
- **vLLM** loads a model checkpoint onto the GPU and exposes a local API.

You normally do **not** download a new model for each Pod. You select one from the shared model pool.

## 1. Know what you normally edit

For a real project, you will usually modify:

```text
configs/
data/
experiments/
analysis/
```

You usually should not need to modify:

```text
spar_inference/
scripts/serve_vllm.sh
shared model infrastructure
```

## 2. Choose a GPU

For this tutorial, use a cheap GPU with roughly **16–24 GB VRAM**. The tutorial uses the shared Qwen2.5-1.5B checkpoint.

| Task | Reasonable starting VRAM |
| --- | ---: |
| Debugging / <3B model | 16–24 GB |
| 7–8B inference | ~24 GB |
| 14B inference | ~32–48 GB |
| 30–32B inference | ~48–80 GB or quantization |
| 70B inference | usually multi-GPU / high-memory |
| Basic mech interp on a small model | 24–48 GB |

This is rough planning guidance, not a guarantee.

## 3. Launch a RunPod

Use the shared SPAR RunPod account/API key described in [Quickstart](quickstart.md).

For this tutorial, **attach the Global Volume `spar-super-lab-workspace`**. That is where the shared models live.

Give the Pod a recognizable name:

```text
<your-name>-first-experiment
```

Open a web terminal or SSH in and verify:

```bash
nvidia-smi
ls /workspace/hot-cache/models
```

If the models directory does not exist or the tutorial checkpoint is missing, see [Shared model pool](model_pool.md) and ask the infrastructure maintainer before downloading a separate copy.

## 4. Clone the infrastructure repository

```bash
mkdir -p /root/projects
cd /root/projects

git clone https://github.com/mohanwugupta/SPAR-Super-Lab-Infra.git
cd SPAR-Super-Lab-Infra

pixi run model-list
pixi run model-check qwen25_1_5b
```

This shows whether the tutorial checkpoint is installed and where it lives.

## 5. Enter the project template

```bash
cd /root/projects/SPAR-Super-Lab-Infra/template
pixi install
pixi run test
```

The important files are:

```text
template/
├── configs/first_experiment.yaml
├── data/prompts.csv
├── experiments/run_first_experiment.py
├── spar_inference/
├── scripts/serve_vllm.sh
└── pixi.toml
```

## 6. Inspect the experiment

```bash
cat data/prompts.csv
cat configs/first_experiment.yaml
```

Changing an experimental variable should usually mean changing a config, not rewriting infrastructure code.

## 7. Start the shared model

In terminal 1:

```bash
cd /root/projects/SPAR-Super-Lab-Infra/template

MODEL=/workspace/hot-cache/models/Qwen--Qwen2.5-1.5B-Instruct \
SERVED_MODEL_NAME=Qwen2.5-1.5B-Instruct \
TP=1 \
pixi run serve
```

Wait until vLLM reports that the server is ready. Leave this terminal running.

If loading directly from the Global Volume is a bottleneck, see the optional `model-stage` workflow in [Shared model pool](model_pool.md).

## 8. Run the experiment

Open terminal 2:

```bash
cd /root/projects/SPAR-Super-Lab-Infra/template

curl http://localhost:8000/health

MODEL=Qwen2.5-1.5B-Instruct pixi run experiment
```

The first terminal loads the model checkpoint. The second terminal sends prompts to that running model server.

## 9. Inspect the results

You should now have:

```text
results/first_experiment/
├── config.yaml
├── metadata.json
└── responses.jsonl
```

Inspect:

```bash
head -n 5 results/first_experiment/responses.jsonl
cat results/first_experiment/metadata.json
```

## 10. Change exactly one variable

Change the system prompt in `configs/first_experiment.yaml`, change the output directory so you do not overwrite the first run, and rerun:

```bash
MODEL=Qwen2.5-1.5B-Instruct pixi run experiment
```

Compare the results.

That is the core scientific loop: **hold everything fixed, manipulate the variable you care about, and preserve the exact config + metadata.**

## 11. Moving to a real project

For a real study, copy the template into its own GitHub repository and replace the toy data/config/runner.

For models, choose from the shared catalog rather than hard-coding a new Hugging Face download. See [Shared model pool](model_pool.md).

## 12. Save your work before deleting the Pod

Commit/push scientifically useful ordinary-sized data/results to the project repository. Large artifacts belong on Hugging Face. Temporary high-volume tensors can remain disposable.

Verify that everything worth keeping is off local Pod storage, then terminate the Pod.
