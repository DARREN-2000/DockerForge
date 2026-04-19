"""DockerForge CLI entrypoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from dockerforge.core.analyzer import PythonAnalyzer
from dockerforge.core.generator import DockerfileGenerator
from dockerforge.core.orchestrator import DockerOrchestrator
from dockerforge.core.tracer import DependencyTracer
from dockerforge.remediation.patcher import ConfigPatcher
from dockerforge.utils.logger import get_logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dockerforge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("path", type=Path)

    generate = subparsers.add_parser("generate")
    generate.add_argument("entrypoint")

    remediate = subparsers.add_parser("remediate")
    remediate.add_argument("dockerfile", type=Path)
    remediate.add_argument("logfile", type=Path)

    build = subparsers.add_parser("build")
    build.add_argument("context", type=Path)
    build.add_argument("tag")

    return parser


def main() -> int:
    logger = get_logger()
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        tracer = DependencyTracer(PythonAnalyzer())
        graph = tracer.trace(args.path, Path.cwd())
        for file, result in graph.items():
            logger.info(
                "file=%s stdlib=%s third_party=%s local=%s",
                file,
                sorted(result.stdlib),
                sorted(result.third_party),
                sorted(result.local),
            )
        return 0

    if args.command == "generate":
        artifacts = DockerfileGenerator().synthesize(args.entrypoint)
        Path("Dockerfile").write_text(artifacts.dockerfile, encoding="utf-8")
        Path(".dockerignore").write_text(artifacts.dockerignore, encoding="utf-8")
        logger.info("Generated Dockerfile and .dockerignore")
        return 0

    if args.command == "remediate":
        dockerfile = args.dockerfile.read_text(encoding="utf-8")
        logs = args.logfile.read_text(encoding="utf-8").splitlines()
        patched = ConfigPatcher().patch_dockerfile(dockerfile, logs)
        if patched.changed:
            args.dockerfile.write_text(patched.content, encoding="utf-8")
            logger.info("Applied remediation patches")
        else:
            logger.info("No remediation needed")
        return 0

    if args.command == "build":
        orchestrator = DockerOrchestrator()
        for line in orchestrator.build(args.context, args.tag):
            logger.info(line)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
