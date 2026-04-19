from __future__ import annotations

import unittest

from dockerforge.remediation.patcher import ConfigPatcher


class TestPatcher(unittest.TestCase):
    def test_adds_missing_module_install(self) -> None:
        dockerfile = "FROM python:3.12-slim\nCOPY . /app\nCMD [\"python\", \"app.py\"]\n"
        logs = ['ModuleNotFoundError: No module named "pydantic"']
        patched = ConfigPatcher().patch_dockerfile(dockerfile, logs)
        self.assertTrue(patched.changed)
        self.assertIn("RUN pip install --no-cache-dir pydantic", patched.content)


if __name__ == "__main__":
    unittest.main()
