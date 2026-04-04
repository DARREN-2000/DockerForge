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
python -m dockerforge.cli --help
python -m unittest discover -s tests -v
```
