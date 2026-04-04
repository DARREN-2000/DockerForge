from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

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

            fake_spec = SimpleNamespace(origin="/tmp/site-packages/requests/__init__.py")
            with patch("dockerforge.core.analyzer.importlib.util.find_spec", return_value=fake_spec):
                result = PythonAnalyzer().analyze_file(target, root)

            self.assertIn("os", result.stdlib)
            self.assertIn("requests", result.third_party)
            self.assertIn("localmod", result.local)


if __name__ == "__main__":
    unittest.main()
