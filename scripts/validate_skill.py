#!/usr/bin/env python3
"""Lint the public APEX Tool Evaluator package with only the stdlib.

This project-specific linter checks package structure, stable metadata, eval
fixtures, and a limited set of accidental-publication indicators. It is not a
complete secret scanner or a replacement for the Agent Skills reference
validator.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "PROVENANCE.md",
    "THIRD_PARTY_NOTICES.md",
    "SECURITY.md",
    "references/evaluation-form.md",
    "evals/evals.json",
)
PUBLIC_BOUNDARY_PATTERNS = (
    ("absolute home path", re.compile(r"/(?:Users|home)/[^/\s]+/")),
    ("Windows user path", re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+(?:\\|\b)")),
    ("private file URI", re.compile(r"(?i)\b(?:file|smb|ssh)://")),
    (
        "private key header",
        re.compile(r"-" * 5 + r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY" + r"-" * 5),
    ),
    (
        "credential assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9_./+~-]{8,}"
        ),
    ),
    (
        "credential-like token",
        re.compile(
            r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
            r"sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"
        ),
    ),
)


def fail(message: str) -> None:
    raise ValueError(message)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    values: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([a-z][a-z0-9-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    return values


def validate_required_files(root: Path = ROOT) -> None:
    missing = [path for path in REQUIRED if not (root / path).is_file()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def validate_skill(root: Path = ROOT) -> None:
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    name = metadata.get("name", "")
    if name != "apex-tool-evaluator":
        fail("Skill name must be apex-tool-evaluator")
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("Skill name must be 1-64 lowercase letters, digits, or hyphens")
    if root.name != name:
        fail("Skill directory name must match frontmatter name")
    description = metadata.get("description", "")
    if not description:
        fail("Skill description is required")
    if len(description) > 1024:
        fail("Skill description must be at most 1024 characters")
    if len(metadata.get("compatibility", "")) > 500:
        fail("Skill compatibility must be at most 500 characters")
    if metadata.get("license") != "Apache-2.0":
        fail("Skill license must be Apache-2.0")
    if len(text.splitlines()) >= 500:
        fail("SKILL.md must stay below 500 lines")


def validate_evals(root: Path = ROOT) -> None:
    data = json.loads((root / "evals/evals.json").read_text(encoding="utf-8"))
    if data.get("skill_name") != "apex-tool-evaluator":
        fail("evals.skill_name must match the Skill name")
    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 5:
        fail("At least five evals are required")
    ids = [item.get("id") for item in evals]
    if len(ids) != len(set(ids)):
        fail("Eval IDs must be unique")
    for item in evals:
        for field in ("prompt", "expected_output", "files", "expectations"):
            if field not in item:
                fail(f"Eval {item.get('id')} is missing {field}")
        if not item["expectations"]:
            fail(f"Eval {item.get('id')} needs expectations")


def validate_public_boundary(root: Path = ROOT) -> None:
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or path.suffix.lower() in {".pyc", ".pyo"}:
            findings.append(f"{relative}: cache or bytecode file is not allowed")
            continue
        raw = path.read_bytes()
        if b"\x00" in raw:
            findings.append(f"{relative}: binary file is not allowed")
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(f"{relative}: non-UTF-8 or binary file is not allowed")
            continue
        for label, pattern in PUBLIC_BOUNDARY_PATTERNS:
            if pattern.search(content):
                findings.append(f"{relative}: {label}")
    if findings:
        fail("Public-boundary violations found: " + "; ".join(findings))


def main() -> int:
    try:
        validate_required_files(ROOT)
        validate_skill(ROOT)
        validate_evals(ROOT)
        validate_public_boundary(ROOT)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"VALIDATION_FAILED: {exc}", file=sys.stderr)
        return 1
    print("VALIDATION_OK: structure, metadata, eval fixtures, and limited public-boundary checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
