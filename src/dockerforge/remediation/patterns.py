"""Known remediation signatures for build failures."""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class RemediationPattern:
    name: str
    regex: re.Pattern[str]
    action: str


PATTERNS = [
    RemediationPattern(
        name="missing_workdir",
        regex=re.compile(r"(?i)workdir.*not set|no working directory"),
        action="ensure_workdir",
    ),
    RemediationPattern(
        name="module_not_found",
        regex=re.compile(r"(?i)ModuleNotFoundError: No module named ['\"]([\w\-\.]+)['\"]"),
        action="install_missing_module",
    ),
    RemediationPattern(
        name="apt_index_missing",
        regex=re.compile(r"(?i)unable to locate package"),
        action="add_apt_update",
    ),
]


def match_pattern(log_line: str) -> RemediationPattern | None:
    for pattern in PATTERNS:
        if pattern.regex.search(log_line):
            return pattern
    return None
