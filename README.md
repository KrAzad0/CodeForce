# ContestForge-R

ContestForge-R is a dependency-free Python starter for defining and
evaluating programming-contest problems. It makes each experiment auditable:
define a typed `ProblemSpec`, compare an executable reference against a
brute-force oracle, measure a population of candidate solvers, and turn the
signals into a reward score.

The project includes a static project site at
**https://krazad0.github.io/CodeForce/**. Its source is in [`docs/`](docs/);
the Pages workflow deploys that directory on pushes to `main`.

## Local setup

Python 3.10 or newer is required. The package has no runtime dependencies.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -e ".[test]"
```

## CLI

Solvers use a small JSON-in/JSON-out protocol: one JSON value on stdin and
one JSON value on stdout. The bundled example is a count-target-pairs
problem.

```bash
# Print the JSON Schema and validate a spec can be loaded
contestforge validate examples/sum_pairs.json

# Verify reference and brute-force programs on the bundled cases
contestforge verify examples/sum_pairs.json examples/cases.json

# Estimate difficulty from the solver population in the spec metadata
contestforge estimate examples/sum_pairs.json examples/cases.json
```

The Python API exposes the same building blocks:
`ProblemSpec`, `run_solver`, `verify_problem`, `estimate_difficulty`,
`score_submission`, and `evaluate_pipeline`.

## Development and tests

```bash
python -m pytest -q
python -m compileall -q src examples
```

Design decisions and follow-up research ideas are documented in
[`docs/design.md`](docs/design.md) and [`docs/research.md`](docs/research.md).
The subprocess timeout is a correctness guard, not a security boundary; use
container or sandbox isolation for untrusted code.

## GitHub Pages

The repository workflow is [`.github/workflows/pages.yml`](.github/workflows/pages.yml).
It uploads `docs/` with the official Pages artifact/deploy actions. Before the
first deployment, set **Settings → Pages → Build and deployment → Source** to
**GitHub Actions** once. The workflow uses the default `GITHUB_TOKEN`, which
cannot enable Pages through the action; after the one-time setting, pushes to
`main` that change `docs/` or the workflow deploy the site. You can also run
the workflow manually with **Actions → Deploy Pages site → Run workflow**.
