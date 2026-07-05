# Security Policy

## Supported Versions

Currently, DockerForge is in active development. Security updates are provided for the latest stable release.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

We take the security of DockerForge seriously. If you discover a security vulnerability, please bring it to our attention right away!

Please **DO NOT** file a public issue for security vulnerabilities. Instead, send an email to security@dockerforge.io.

We will acknowledge receipt of your vulnerability report within 48 hours and strive to send you regular updates about our progress. If you're curious about the status of your report, feel free to follow up by email.

### What to include in your report

* A description of the vulnerability and its impact.
* Steps to reproduce the vulnerability. This is extremely helpful!
* Any proof-of-concept (PoC) scripts or code.

### Scope

The scope of this policy includes:
* The core DockerForge analyzer, generator, and remediation loops.
* CLI entrypoints.
* Default generated `Dockerfile` and `.dockerignore` configurations.

If you find a vulnerability in a third-party dependency, we recommend reporting it to the maintainers of that dependency. However, we appreciate being notified so we can update our dependencies or provide mitigations.
