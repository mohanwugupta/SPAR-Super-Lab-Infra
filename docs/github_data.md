# GitHub data conventions

GitHub is the **default long-term home for project data and results when they fit comfortably in Git**. This keeps a project self-contained after the fellowship: code, configs, data, analyses, and documentation can live together without depending on RunPod storage.

## Good GitHub candidates

Examples:

- benchmark inputs;
- prompt sets;
- annotations;
- small/medium CSV, JSONL, or Parquet files;
- generated behavioral results;
- analysis-ready tables;
- experiment summaries;
- publication data releases.

A typical project can therefore look like:

```text
project/
  README.md
  pixi.toml
  pixi.lock
  configs/
  data/
    raw/
    processed/
  results/
    frozen/
  src/
  experiments/
  analysis/
  tests/
```

Cloning the repository onto a RunPod Pod then brings the code and ordinary-sized data together:

```bash
git clone <REPO_URL>
cd <REPO>
pixi run --locked experiment
```

## Size heuristic

These are **lab heuristics, not GitHub hard limits**:

```text
< ~1 GB total project data
    GitHub by default

~1-10 GB
    case-by-case:
    GitHub if stable and reasonably sharded;
    Hugging Face if frequently updated or ML-artifact-heavy

> ~10 GB
    usually Hugging Face
```

The more important question is not only the current file size but also **Git history**. Git stores previous versions. Repeatedly replacing a large binary file can make the repository much larger than the latest checkout appears.

## Prefer compact, stable files

Prefer:

- Parquet for tables that would otherwise be large CSVs;
- JSONL for streamable records;
- stable shards rather than repeatedly rewriting one huge binary;
- derived data that are difficult or expensive to regenerate.

Avoid committing:

- model weights;
- hundreds of GB of activations;
- cache directories;
- temporary checkpoints;
- high-churn intermediate tensors.

## Git LFS

Git LFS can be useful for occasional files that are too large for normal Git but still belong closely with the project.

Treat LFS as an escape hatch, not the default storage architecture. LFS storage/bandwidth quotas are different from ordinary GitHub repository storage, and very large ML datasets are generally cleaner on Hugging Face.

GitHub documentation:
- https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits
- https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage

## Reproducibility

For important runs, record the Git commit containing or referencing the exact input data:

```bash
git rev-parse HEAD
```

If data live in the same repository, this can pin code + config + dataset together. If a dataset lives in a separate GitHub repository, record both repository URL and commit SHA in the experiment config.

```yaml
dataset:
  source: github
  repo: SPAR-Super-Lab/task-selection
  revision: 0123456789abcdef...
  path: data/processed/items.parquet
```
