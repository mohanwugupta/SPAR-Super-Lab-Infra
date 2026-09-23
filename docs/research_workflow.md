# Research workflow

## Project minimum

```text
README.md
pixi.toml
pixi.lock
configs/
data/          # when project data fit comfortably in Git
src/ or project modules
experiments/
analysis/
tests/
```

## Normal loop

1. Create a Git branch.
2. Define the experimental config.
3. Identify the canonical data source:
   - GitHub commit/path for ordinary-sized project data; or
   - Hugging Face repo/revision for large ML artifacts.
4. Clone/pull the required inputs onto the Pod.
5. Run tests/smoke tests.
6. Run a small pilot.
7. Record metadata + Git commit.
8. Write working outputs to a run-specific local directory.
9. Inspect results.
10. Persist durable outputs:
    - GitHub for ordinary-sized project results/data;
    - Hugging Face for large artifacts.
11. Scale only after the pilot works.
12. Merge code by pull request.

## Every important run should record

- code Git commit;
- dataset source + exact revision;
- model/checkpoint + revision;
- tokenizer revision;
- inference backend + version;
- Transformers/PyTorch versions;
- dtype/quantization;
- generation parameters;
- seed;
- GPU model;
- experiment config;
- timestamp.

```yaml
dataset:
  source: github
  repo: SPAR-Super-Lab/task-selection
  revision: <GIT_SHA>
  path: data/items.parquet
```

or:

```yaml
dataset:
  source: huggingface
  repo_id: SPAR-Super-Lab/preferences-activations
  revision: <HF_SHA>
```

The starter `spar_inference.metadata` helper records much of the runtime automatically.

## Output directories

Prefer immutable run-specific directories:

```text
results/
  2026-09-23_qwen25-7b_prompt-v4_seed0/
    config.yaml
    metadata.json
    responses.parquet
    summary.csv
```

Do not have multiple Pods overwrite one shared output file.

## Sources of truth

```text
GitHub       -> code/configuration + ordinary-sized datasets/results
Hugging Face -> large datasets + durable ML artifacts
RunPod       -> disposable compute + working storage
```

A production run should be a configuration change, not a rewritten script. The same code path that runs 20 examples should run 200,000 examples.
