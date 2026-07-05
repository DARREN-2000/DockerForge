# API Reference

DockerForge provides internal APIs if you wish to use its components as a library.

## `dockerforge.core.analyzer`

### `PythonAnalyzer`
- `can_handle(file_path: Path) -> bool`
- `analyze_file(file_path: Path, project_root: Path) -> AnalysisResult`
- `analyze_tree(project_root: Path) -> dict[Path, AnalysisResult]`

## `dockerforge.core.generator`

### `DockerfileGenerator`
- `synthesize(entrypoint: str, third_party: set[str] | None = None, python_version: str = "3.12-slim") -> GeneratedArtifacts`

## `dockerforge.remediation.patcher`

### `ConfigPatcher`
- `patch_dockerfile(dockerfile_content: str, build_logs: list[str]) -> PatchResult`
