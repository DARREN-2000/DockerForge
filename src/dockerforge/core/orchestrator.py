"""Docker command orchestration and log streaming."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable


class DockerOrchestrator:
    def build(self, context_dir: Path, tag: str) -> Iterable[str]:
        command = ["docker", "build", "-t", tag, str(context_dir)]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if process.stdout is None:
            raise RuntimeError("Docker build did not provide stdout stream")

        for line in process.stdout:
            yield line.rstrip("\n")

        return_code = process.wait()
        if return_code != 0:
            raise RuntimeError(f"Docker build failed with status {return_code}")
