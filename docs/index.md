# DockerForge Documentation

Welcome to the official documentation for DockerForge. DockerForge is a production-ready engine for generating and automatically remediating Dockerfiles for Python applications.

## What is DockerForge?

DockerForge analyzes your Python project's Abstract Syntax Tree (AST), maps local and third-party dependencies recursively, and synthesizes an optimized `Dockerfile` and `.dockerignore`. If the resulting build fails (e.g., due to a missing apt package or a C-extension requirement), DockerForge intercepts the build logs, maps the failure to a known pattern, patches the Dockerfile, and rebuilds automatically.

## Navigation

- [Getting Started](getting-started.md)
- [Installation](installation.md)
- [Architecture](architecture.md)
- [Design Principles](design.md)
- [Internals](internals.md)
