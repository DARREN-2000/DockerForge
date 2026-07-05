# Design Principles

DockerForge is built on the following core design principles:

## 1. Zero Configuration by Default
Users should not need to write complex configuration files. The tool should infer as much as possible directly from the codebase (AST analysis) and the build environment.

## 2. Deterministic and Safe Remediation
Remediation patches must be applied predictably based on explicit regular expression patterns and known build failure signatures. We favor explicit rules over non-deterministic AI generation for the core loop to ensure build stability and security.

## 3. Transparency
The build orchestration process streams logs directly to the user. When a remediation step is taken, it is explicitly logged so the user understands exactly *why* their Dockerfile was modified.

## 4. Extensibility
The architecture is decoupled. The analyzer, generator, and remediation engine communicate via well-defined dataclasses, making it easy to swap out components or add support for new languages in the future.
