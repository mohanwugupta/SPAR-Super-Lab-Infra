# Research workflow

## Project minimum

```text
README.md
pixi.toml
pixi.lock
configs/
src/ or project modules
experiments/
tests/
```

## Normal loop

1. Create a Git branch.
2. Define the experimental config.
3. Pin or record the Hugging Face dataset/artifact revision.
4. Pull required data to local Pod scratch.
5. Run tests/smoke tests.
6. Run a small pilot.
7. Record metadata + Git commit.
8. Write working outputs to a run-specific local directory.
9. Inspect results.
10. Upload durable/reusable outputs to Hugging Face.
11. Record the resulting Hub revision.
12. Scale only after the pilot works.
13. Merge code by pull request.

## Every important run should record

- model/checkpoint + revision;
- dataset/artifact Hugging Face repo + revision;
- tokenizer revision;
- inference backend + version;
- Transformers/PyTorch versions;
- dtype/quantization;
- generation parameters;
- seed;
- GPU model;
- Git commit;
- experiment config;
- timestamp.

The starter `spar_inference.metadata` helper records much of the runtime automatically.

## Output directories

Prefer immutable run-specific directories:

```text
results/
  2026-09-23_qwen25-7b_prompt-v4_seed0/
    config.yaml
    metadata.json
    responses.jsonl
    summary.csv
```

Do not have multiple Pods overwrite one shared output file.

## Sources of truth

```text
GitHub       -> code/configuration
Hugging Face -> datasets + durable ML artifacts
RunPod       -> disposable compute + working storage
```

A production run should be a configuration change, not a rewritten script. The same code path that runs 20 examples should run 200,000 examples.
