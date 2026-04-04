"""Configuration patching for auto remediation loop."""

from __future__ import annotations

from dataclasses import dataclass

from .patterns import match_pattern


@dataclass
class PatchResult:
    changed: bool
    content: str


class ConfigPatcher:
    def patch_dockerfile(self, dockerfile_content: str, build_logs: list[str]) -> PatchResult:
        needs_workdir = False
        needs_apt = False
        missing_packages: set[str] = set()

        for line in build_logs:
            pattern = match_pattern(line)
            if pattern is None:
                continue

            if pattern.action == "ensure_workdir":
                needs_workdir = True
            elif pattern.action == "add_apt_update":
                needs_apt = True
            elif pattern.action == "install_missing_module":
                module_match = pattern.regex.search(line)
                if module_match:
                    missing_packages.add(module_match.group(1).split(".", 1)[0])

        lines = dockerfile_content.splitlines()
        has_workdir = any(line.strip().startswith("WORKDIR ") for line in lines)
        has_apt = any("apt-get update" in line for line in lines)
        installed_packages = self._extract_installed_packages(lines)

        changed = False

        if needs_workdir and not has_workdir:
            insert_idx = self._find_insert_index(lines)
            lines.insert(insert_idx, "WORKDIR /app")
            changed = True

        if needs_apt and not has_apt:
            insert_idx = self._find_insert_index(lines)
            lines.insert(insert_idx, "RUN apt-get update && apt-get install -y --no-install-recommends curl")
            changed = True

        to_install = sorted(pkg for pkg in missing_packages if pkg and pkg not in installed_packages)
        if to_install:
            install_line = f"RUN pip install --no-cache-dir {' '.join(to_install)}"
            insert_idx = self._find_insert_index(lines)
            lines.insert(insert_idx + 1 if insert_idx < len(lines) else insert_idx, install_line)
            changed = True

        content = "\n".join(lines)
        if dockerfile_content.endswith("\n"):
            content += "\n"

        return PatchResult(changed=changed, content=content)

    def _find_insert_index(self, lines: list[str]) -> int:
        for idx, line in enumerate(lines):
            if line.strip().startswith("COPY "):
                return idx
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("CMD ") or stripped.startswith("ENTRYPOINT "):
                return idx
        return len(lines)

    def _extract_installed_packages(self, lines: list[str]) -> set[str]:
        packages: set[str] = set()
        for line in lines:
            stripped = line.strip()
            if not stripped.startswith("RUN ") or "pip install" not in stripped:
                continue

            after_install = stripped.split("pip install", 1)[1].strip()
            tokens = [token for token in after_install.split() if not token.startswith("-")]
            for token in tokens:
                clean = token.split("==", 1)[0].split("[", 1)[0]
                if clean:
                    packages.add(clean)
        return packages
