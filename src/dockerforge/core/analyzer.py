"""AST-based dependency analyzer."""

from __future__ import annotations

import ast
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass
class AnalysisResult:
    file: Path
    stdlib: set[str] = field(default_factory=set)
    third_party: set[str] = field(default_factory=set)
    local: set[str] = field(default_factory=set)


class AnalyzerPlugin(Protocol):
    def can_handle(self, file_path: Path) -> bool: ...

    def analyze_file(self, file_path: Path, project_root: Path) -> AnalysisResult: ...


class PythonAnalyzer:
    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix == ".py"

    def analyze_file(self, file_path: Path, project_root: Path) -> AnalysisResult:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        result = AnalysisResult(file=file_path)

        for node in ast.walk(tree):
            module_name = None
            if isinstance(node, ast.Import):
                for name in node.names:
                    module_name = name.name.split(".", 1)[0]
                    self._classify(module_name, project_root, result)
            elif isinstance(node, ast.ImportFrom) and node.module:
                module_name = node.module.split(".", 1)[0]
                self._classify(module_name, project_root, result)

        return result

    def analyze_tree(self, project_root: Path) -> dict[Path, AnalysisResult]:
        output: dict[Path, AnalysisResult] = {}
        for py_file in project_root.rglob("*.py"):
            if "site-packages" in py_file.parts:
                continue
            output[py_file] = self.analyze_file(py_file, project_root)
        return output

    def _classify(self, module: str, project_root: Path, result: AnalysisResult) -> None:
        if module in sys.stdlib_module_names:
            result.stdlib.add(module)
            return

        local_pkg = project_root / module
        local_module_file = project_root / f"{module}.py"
        src_local_pkg = project_root / "src" / module
        src_local_module_file = project_root / "src" / f"{module}.py"
        if (
            local_pkg.exists()
            or local_module_file.exists()
            or src_local_pkg.exists()
            or src_local_module_file.exists()
        ):
            result.local.add(module)
            return

        spec = importlib.util.find_spec(module)
        if spec is None:
            result.local.add(module)
            return

        origin = spec.origin or ""
        if "site-packages" in origin or "dist-packages" in origin:
            result.third_party.add(module)
        elif "python" in origin.lower():
            result.stdlib.add(module)
        else:
            result.local.add(module)
