from __future__ import annotations

import unittest

from dockerforge.core.generator import DockerfileGenerator


class TestGenerator(unittest.TestCase):
    def test_synthesizes_artifacts(self) -> None:
        artifacts = DockerfileGenerator().synthesize("main.py", {"fastapi", "uvicorn"})
        self.assertIn("FROM python:", artifacts.dockerfile)
        self.assertIn("RUN pip install --no-cache-dir fastapi uvicorn", artifacts.dockerfile)
        self.assertIn(".git/", artifacts.dockerignore)


if __name__ == "__main__":
    unittest.main()
