"""Recursive dependency tracing."""

from __future__ import annotations

from pathlib import Path

from .analyzer import AnalysisResult, PythonAnalyzer


class DependencyTracer:
    def __init__(self, analyzer: PythonAnalyzer | None = None) -> None:
        self.analyzer = analyzer or PythonAnalyzer()

    def trace(self, entry_file: Path, project_root: Path) -> dict[Path, AnalysisResult]:
        visited: set[Path] = set()
        graph: dict[Path, AnalysisResult] = {}
        self._walk(entry_file.resolve(), project_root.resolve(), visited, graph)
        return graph

    def _walk(
        self,
        current_file: Path,
        project_root: Path,
        visited: set[Path],
        graph: dict[Path, AnalysisResult],
    ) -> None:
        if current_file in visited or not current_file.exists():
            return
        if not self.analyzer.can_handle(current_file):
            return

        visited.add(current_file)
        result = self.analyzer.analyze_file(current_file, project_root)
        graph[current_file] = result

        for local_mod in result.local:
            candidates = [
                project_root / f"{local_mod}.py",
                project_root / local_mod / "__init__.py",
                project_root / "src" / local_mod / "__init__.py",
                project_root / "src" / f"{local_mod}.py",
            ]
            for candidate in candidates:
                if candidate.exists():
                    self._walk(candidate.resolve(), project_root, visited, graph)
                    break
