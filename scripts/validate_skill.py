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
RELEASE_VERSION = "0.1.3"
RELEASE_DATE = "2026-08-29"
SOCIAL_PREVIEW_ASSET = f"apex-tool-evaluator-social-preview-v{RELEASE_VERSION}.jpg"
SOCIAL_PREVIEW_SHA = "baaa5708f6fec725689a436f315a629481f1b6a03b74f5566b592f39f4089780"
REQUIRED = (
    "SKILL.md",
    "README.md",
    "EVALUATION.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "NOTICE",
    "PROVENANCE.md",
    "THIRD_PARTY_NOTICES.md",
    "SECURITY.md",
    "SOCIAL_PREVIEW.md",
    "SUPPORT.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "examples/evidence-backed-evaluation.md",
    "references/evaluation-form.md",
    "evals/evals.json",
    "evals/trigger-evals.json",
)
ALLOWED_EVAL_CATEGORIES = {"normal", "edge", "negative"}
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
    if not re.search(
        rf'^\s+version:\s*["\']{re.escape(RELEASE_VERSION)}["\']\s*$',
        text,
        re.MULTILINE,
    ):
        fail(f"Skill metadata version must be {RELEASE_VERSION}")
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
        for field in ("category", "prompt", "expected_output", "files", "expectations"):
            if field not in item:
                fail(f"Eval {item.get('id')} is missing {field}")
        if item["category"] not in ALLOWED_EVAL_CATEGORIES:
            fail(f"Eval {item.get('id')} has an invalid category")
        if not item["expectations"]:
            fail(f"Eval {item.get('id')} needs expectations")
    counts = {
        category: sum(item["category"] == category for item in evals)
        for category in ALLOWED_EVAL_CATEGORIES
    }
    if counts["normal"] < 3 or counts["edge"] < 1 or counts["negative"] < 1:
        fail("Evals must include at least 3 normal, 1 edge, and 1 negative case")


def validate_trigger_evals(root: Path = ROOT) -> None:
    data = json.loads((root / "evals/trigger-evals.json").read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) != 20:
        fail("Trigger evals must contain exactly 20 queries")

    queries: list[str] = []
    labels: list[bool] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            fail(f"Trigger eval {index} must be an object")
        if set(item) != {"query", "should_trigger"}:
            fail(f"Trigger eval {index} must contain only query and should_trigger")
        query = item["query"]
        if not isinstance(query, str) or not query.strip():
            fail(f"Trigger eval {index} needs a non-empty query")
        if not isinstance(item["should_trigger"], bool):
            fail(f"Trigger eval {index} should_trigger must be a boolean")
        queries.append(query.strip())
        labels.append(item["should_trigger"])

    if len(queries) != len(set(queries)):
        fail("Trigger eval queries must be unique")
    if labels.count(True) != 10 or labels.count(False) != 10:
        fail("Trigger evals must have a 10:10 should-trigger balance")


def validate_version_consistency(root: Path = ROOT) -> None:
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    skill_match = re.search(
        r'^\s+version:\s*["\']([^"\']+)["\']\s*$', skill_text, re.MULTILINE
    )
    if not skill_match or skill_match.group(1) != RELEASE_VERSION:
        fail(f"SKILL.md release version must be {RELEASE_VERSION}")

    citation_text = (root / "CITATION.cff").read_text(encoding="utf-8")
    citation_match = re.search(
        r'^version:\s*["\']?([^"\'\s]+)["\']?\s*$', citation_text, re.MULTILINE
    )
    if not citation_match or citation_match.group(1) != RELEASE_VERSION:
        fail("CITATION.cff version must match SKILL.md")
    if f"/releases/tag/v{RELEASE_VERSION}" not in citation_text:
        fail("CITATION.cff release URL must match SKILL.md")
    if not re.search(
        rf"^date-released:\s*{re.escape(RELEASE_DATE)}\s*$",
        citation_text,
        re.MULTILINE,
    ):
        fail(f"CITATION.cff release date must be {RELEASE_DATE}")

    readme_text = (root / "README.md").read_text(encoding="utf-8")
    readme_versions = set(re.findall(r"\bv\d+\.\d+\.\d+\b", readme_text))
    if readme_versions != {f"v{RELEASE_VERSION}"}:
        fail("README release references must match SKILL.md")
    expected_asset = f"apex-tool-evaluator-v{RELEASE_VERSION}.skill"
    if expected_asset not in readme_text:
        fail("README must name the versioned .skill release asset")
    if f"apex-tool-evaluator-v{RELEASE_VERSION}.zip" in readme_text:
        fail("README release asset must use .skill instead of .zip")

    changelog_text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    latest = re.search(
        r"^## (\d+\.\d+\.\d+) - (\d{4}-\d{2}-\d{2})\s*$",
        changelog_text,
        re.MULTILINE,
    )
    if not latest or latest.groups() != (RELEASE_VERSION, RELEASE_DATE):
        fail("CHANGELOG latest release must match SKILL.md and CITATION.cff")

    social_text = (root / "SOCIAL_PREVIEW.md").read_text(encoding="utf-8")
    if f"v{RELEASE_VERSION}" not in social_text:
        fail("SOCIAL_PREVIEW.md release tag must match SKILL.md")
    if SOCIAL_PREVIEW_ASSET not in social_text:
        fail("SOCIAL_PREVIEW.md asset name must match the versioned preview")
    sha_match = re.search(r"^- SHA-256:\s*`([^`]+)`\s*$", social_text, re.MULTILINE)
    if not sha_match or sha_match.group(1) != SOCIAL_PREVIEW_SHA:
        fail("SOCIAL_PREVIEW.md SHA-256 must match the final release preview")


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
        validate_trigger_evals(ROOT)
        validate_version_consistency(ROOT)
        validate_public_boundary(ROOT)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"VALIDATION_FAILED: {exc}", file=sys.stderr)
        return 1
    print(
        "VALIDATION_OK: structure, release metadata, behavior and trigger fixtures, "
        "and limited public-boundary checks passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
