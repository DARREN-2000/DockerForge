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
        updated = dockerfile_content
        changed = False

        for line in build_logs:
            pattern = match_pattern(line)
            if pattern is None:
                continue

            if pattern.action == "ensure_workdir" and "WORKDIR" not in updated:
                updated = updated.replace("COPY . /app\n", "WORKDIR /app\nCOPY . /app\n")
                changed = True

            elif pattern.action == "add_apt_update" and "apt-get update" not in updated:
                insertion = "RUN apt-get update && apt-get install -y --no-install-recommends curl\n"
                updated = updated.replace("COPY . /app\n", f"{insertion}COPY . /app\n")
                changed = True

            elif pattern.action == "install_missing_module":
                module = pattern.regex.search(line)
                if module:
                    pkg = module.group(1).split(".", 1)[0]
                    install_line = f"RUN pip install --no-cache-dir {pkg}\n"
                    if install_line not in updated:
                        updated = updated.replace("COPY . /app\n", f"COPY . /app\n{install_line}")
                        changed = True

        return PatchResult(changed=changed, content=updated)
