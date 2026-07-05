# Project Internals

This section provides a deep dive into the inner workings of DockerForge's specific modules.

## Remediation Patterns

The core of the remediation engine lives in `src/dockerforge/remediation/patterns.py`. It defines a `RemediationPattern` dataclass with a regex and an action.

Currently supported patterns:
1. `missing_workdir`: Detects "workdir not set" and injects `WORKDIR /app`.
2. `module_not_found`: Extracts missing module names from `ModuleNotFoundError` and appends them to a `pip install` command.
3. `apt_index_missing`: Detects "unable to locate package" and injects an `apt-get update`.

## AST Classification

The `PythonAnalyzer` class ensures accuracy by checking:
1. Is it in `sys.stdlib_module_names`? (Standard Library)
2. Does a local `.py` or package directory exist? (Local)
3. Does `importlib` resolve it to a `site-packages` path? (Third Party)
