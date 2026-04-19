# DockerForge

Production-ready prototype for a **Deep Analyzer Engine** and **Auto Remediation Loop**.

## Features

- AST-based import analysis and classification
- Recursive local dependency tracing
- Dockerfile and `.dockerignore` synthesis
- Docker build orchestration with streaming output
- Pattern-based remediation and Dockerfile patching
- CLI entrypoint for analyze/generate/build/remediate workflows

## Project Layout

```text
dockerforge/
├── pyproject.toml
├── src/
│   └── dockerforge/
│       ├── __init__.py
│       ├── cli.py
│       ├── core/
│       │   ├── analyzer.py
│       │   ├── tracer.py
│       │   ├── generator.py
│       │   └── orchestrator.py
│       ├── remediation/
│       │   ├── patterns.py
│       │   └── patcher.py
│       └── utils/
│           └── logger.py
└── tests/
```

## Local Usage

```bash
python -m pip install -e .
dockerforge --help
python -m unittest discover -s tests -v
```

## Web App (GitHub Pages)

A production-oriented static web app is available in `/docs` with:

- Import analysis
- Dockerfile + `.dockerignore` generation
- Dockerfile remediation simulation from build logs

### Run locally

Open `/docs/index.html` in a browser, or serve it:

```bash
cd docs
python -m http.server 8000
```

Then open `http://localhost:8000`.

### Deploy to GitHub Pages

This repository includes `.github/workflows/deploy-pages.yml` which deploys `/docs` on pushes to `main`.

In repository settings, set **Pages** source to **GitHub Actions**. After the workflow runs, the site will be available at:

`https://DARREN-2000.github.io/DockerForge/`
