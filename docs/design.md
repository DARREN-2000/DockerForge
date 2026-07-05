# Design Decisions

## Why AST over `pip freeze`?
Traditional tools rely on `requirements.txt` or `pip freeze`, which often contain bloated, unused dependencies, or environment-specific packages. DockerForge statically analyzes the actual code being executed to build a minimal, exact dependency graph.

## Why Regex over LLMs?
While Large Language Models (LLMs) are excellent for generalized code generation, they lack determinism. Build infrastructure must be predictable. By using explicit Regex patterns (`src/dockerforge/remediation/patterns.py`), we ensure that a missing module error always results in a specific `pip install` command, guaranteeing build reproducibility.

## Why a modular pipeline?
By decoupling the Analyzer, Generator, and Patcher, users can leverage DockerForge as an SDK. You can use the Tracer just to visualize your dependencies without ever generating a Dockerfile.
