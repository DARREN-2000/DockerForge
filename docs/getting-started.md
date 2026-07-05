# Getting Started

This guide will walk you through analyzing a Python project and generating a `Dockerfile`.

## 1. Analyze Your Project

Use the `analyze` command to inspect a Python file and map its dependencies:

```bash
dockerforge analyze path/to/your/app.py
```
This outputs a breakdown of `stdlib`, `third_party`, and `local` imports.

## 2. Generate a Dockerfile

To generate a `Dockerfile` and `.dockerignore` for your application:

```bash
dockerforge generate path/to/your/app.py
```

## 3. Build and Remediate

To build the image and stream the logs:

```bash
dockerforge build . your-image-tag
```

If the build fails, you can manually trigger the remediation loop (or use our planned auto-remediate wrapper):

```bash
dockerforge remediate Dockerfile build.log
```
