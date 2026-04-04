from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dockerforge.core.analyzer import PythonAnalyzer


class TestPythonAnalyzer(unittest.TestCase):
    def test_classifies_imports(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "localmod.py").write_text("x = 1\n", encoding="utf-8")
            target = root / "app.py"
            target.write_text(
                "import os\nimport requests\nimport localmod\n",
                encoding="utf-8",
            )

            result = PythonAnalyzer().analyze_file(target, root)

            self.assertIn("os", result.stdlib)
            self.assertIn("localmod", result.local)
            self.assertTrue("requests" in result.third_party or "requests" in result.local)


if __name__ == "__main__":
    unittest.main()
