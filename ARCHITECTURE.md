# Architecture Overview

DockerForge is designed as a pipeline that analyzes Python code, generates container definitions, attempts a build, and recursively remediates any failures until success.

## Core Components

### 1. Analyzer (`src/dockerforge/core/analyzer.py`)
Uses Python's `ast` module to statically analyze source files. It classifies imports into `stdlib`, `third_party`, and `local` dependencies by inspecting the environment and project structure.

### 2. Tracer (`src/dockerforge/core/tracer.py`)
Recursively walks through local dependencies starting from an entrypoint file, building a complete dependency graph of the application.

### 3. Generator (`src/dockerforge/core/generator.py`)
Synthesizes a `Dockerfile` and a `.dockerignore` file based on the extracted dependency graph (e.g., ensuring all necessary third-party packages are installed).

### 4. Orchestrator (`src/dockerforge/core/orchestrator.py`)
Executes `docker build`, capturing the streaming output and identifying failure points.

### 5. Remediation Engine (`src/dockerforge/remediation/`)
When a build fails, this engine analyzes the error logs against a set of known `PATTERNS` (e.g., missing APT packages, missing Python modules, incorrect working directories) and applies precise patches to the `Dockerfile`.

## Execution Flow

1. **Analyze**: The user specifies an entrypoint. The Analyzer and Tracer map the dependencies.
2. **Generate**: Initial `Dockerfile` and `.dockerignore` are synthesized.
3. **Build**: The Orchestrator attempts to build the image.
4. **Remediate**: If the build fails, the Remediation Engine analyzes the logs, patches the `Dockerfile`, and triggers a rebuild. This loop continues until the build succeeds or a maximum retry count is reached.
