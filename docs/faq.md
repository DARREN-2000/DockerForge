# Frequently Asked Questions

**Does DockerForge support non-Python dependencies?**
Currently, DockerForge is optimized for Python applications, utilizing AST parsing and Python standard library tools to trace dependencies.

**Is my code sent to a server?**
No. DockerForge runs entirely locally. It does not use external APIs or LLMs for its core execution and remediation loop. All analysis is deterministic and runs on your machine.

**Can I use it in my CI/CD pipeline?**
Yes! The CLI is designed to return non-zero exit codes on failure and can be easily wrapped in standard bash scripts within GitHub Actions or GitLab CI.
