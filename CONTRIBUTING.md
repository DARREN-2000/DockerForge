# Contributing to DockerForge

First off, thank you for considering contributing to DockerForge. It's people like you that make DockerForge such a great tool for generating Dockerfiles and remediating builds automatically.

## Where do I go from here?

If you've noticed a bug or have a feature request, make one! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

If you'd like to dive right in, feel free to pick up any of the issues with the "good first issue" or "help wanted" labels.

## Setting up your environment

DockerForge requires Python 3.10+.

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dockerforge.git
   cd dockerforge
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   # Create a virtual environment and activate it
   # pip install -e ".[dev]"
   ```

3. Run the tests to ensure everything is working:
   ```bash
   PYTHONPATH=src python -m unittest discover -s tests -v
   ```

## Development Workflow

1. Create a branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes. Ensure you adhere to the project's coding standards.

3. Write tests for your changes. We aim for 100% test coverage for the core analysis, generation, and remediation engines.

4. Run the test suite and ensure all tests pass:
   ```bash
   PYTHONPATH=src python -m unittest discover -s tests -v
   ```

5. Commit your changes. Write a descriptive commit message.
   ```bash
   git commit -m "feat: add support for parsing pyproject.toml"
   ```

6. Push your branch to your fork and open a Pull Request against the `main` branch of the DockerForge repository.

## Architecture Overview

If you're modifying the core logic, familiarizing yourself with the following files is recommended:
- `src/dockerforge/core/analyzer.py` - AST-based dependency analyzer.
- `src/dockerforge/core/tracer.py` - Recursive dependency tracing.
- `src/dockerforge/core/generator.py` - Dockerfile and `.dockerignore` synthesis.
- `src/dockerforge/remediation/patcher.py` - Pattern-based remediation logic.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md).

Thank you for your contributions!
