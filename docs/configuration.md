# Configuration

DockerForge is designed to be zero-configuration. The core logic dynamically inspects your python environment, abstract syntax trees, and build failure logs to adapt automatically.

Currently, configuration is strictly limited to CLI flags.

```bash
dockerforge --help
```

*   `analyze <path>`: Analyzes dependencies.
*   `generate <entrypoint>`: Generates `Dockerfile` and `.dockerignore`.
*   `build <context> <tag>`: Orchestrates the build process.
*   `remediate <dockerfile> <logfile>`: Applies remediation patches.
