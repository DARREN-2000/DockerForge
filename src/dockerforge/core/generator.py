"""Dockerfile and .dockerignore synthesis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GeneratedArtifacts:
    dockerfile: str
    dockerignore: str


class DockerfileGenerator:
    def synthesize(
        self,
        entrypoint: str,
        third_party: set[str] | None = None,
        python_version: str = "3.12-slim",
    ) -> GeneratedArtifacts:
        third_party = third_party or set()
        req_block = ""
        if third_party:
            sorted_deps = " ".join(sorted(third_party))
            req_block = f"RUN pip install --no-cache-dir {sorted_deps}\n"

        dockerfile = (
            f"FROM python:{python_version}\n"
            "ENV PYTHONDONTWRITEBYTECODE=1\n"
            "ENV PYTHONUNBUFFERED=1\n"
            "WORKDIR /app\n"
            "COPY . /app\n"
            f"{req_block}"
            f"CMD [\"python\", \"{entrypoint}\"]\n"
        )

        dockerignore = "\n".join(
            [
                "__pycache__/",
                "*.pyc",
                ".git/",
                ".venv/",
                "venv/",
                ".pytest_cache/",
                "dist/",
                "build/",
            ]
        ) + "\n"

        return GeneratedArtifacts(dockerfile=dockerfile, dockerignore=dockerignore)
