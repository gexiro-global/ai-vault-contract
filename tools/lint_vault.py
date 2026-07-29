#!/usr/bin/env python3
"""lint_vault.py - structural lint for a vault built on the ai-vault-contract.

Checks the mechanical rules the contract can enforce without judgement:
  * every note carries the required frontmatter fields
  * `type` and `status` are drawn from the closed enums
  * `title` equals the filename stem
  * titles and aliases are unique vault-wide (case-insensitive)
  * dates are ISO YYYY-MM-DD, and no literal `{{date}}` survives
  * no obviously secret-shaped strings were committed

It does NOT judge whether a note is atomic, well-linked or non-duplicative - those
need a model, not a linter. Exit 0 clean, 1 on any violation.
"""

from __future__ import annotations

import datetime as _dt
import pathlib
import re
import sys

TYPE_ENUM = {
    "index", "moc", "project", "infra", "research", "reference",
    "source", "daily", "import", "critique", "adr",
}
STATUS_ENUM = {
    "draft", "active", "verified", "in-flight", "blocked",
    "superseded", "done", "archived", "unprocessed",
}
REQUIRED = ("title", "type", "status", "tags", "created", "updated")
EXCLUDE_DIRS = {".git", ".github", ".obsidian", "_attachments", "tools", "_templates"}
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*\S{8,}")
HEX_RE = re.compile(r"\b[0-9a-f]{32,}\b")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-ish frontmatter reader: flat scalars and inline `[a, b]` lists."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict = {}
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            out[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            out[key] = val.strip("'\"")
    return out


def iter_notes(root: pathlib.Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = pathlib.Path(argv[0]) if argv else pathlib.Path(".")
    errors: list[str] = []
    seen_titles: dict[str, pathlib.Path] = {}
    seen_aliases: dict[str, pathlib.Path] = {}
    note_count = 0

    for path in iter_notes(root):
        note_count += 1
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)

        if not fm:
            # No frontmatter => not a vault note (README, CONTRIBUTING, HANDOFF, ...). Skip.
            note_count -= 1
            continue

        for field in REQUIRED:
            if field not in fm or fm[field] in ("", [], None):
                errors.append(f"{rel}: missing required field '{field}'")

        if fm.get("type") and fm["type"] not in TYPE_ENUM:
            errors.append(f"{rel}: type '{fm['type']}' not in the enum")
        if fm.get("status") and fm["status"] not in STATUS_ENUM:
            errors.append(f"{rel}: status '{fm['status']}' not in the enum")

        stem = path.stem
        if fm.get("title") and fm["title"] != stem:
            errors.append(f"{rel}: title '{fm['title']}' != filename stem '{stem}'")

        for field in ("created", "updated", "valid_as_of"):
            val = fm.get(field)
            if val and not ISO_RE.match(str(val)):
                errors.append(f"{rel}: {field} '{val}' is not ISO YYYY-MM-DD")

        title_key = str(fm.get("title", stem)).lower()
        if title_key in seen_titles and seen_titles[title_key] != path:
            errors.append(f"{rel}: title collides with {seen_titles[title_key].relative_to(root)}")
        seen_titles[title_key] = path
        for alias in fm.get("aliases", []) or []:
            ak = str(alias).lower()
            if ak in seen_aliases and seen_aliases[ak] != path:
                errors.append(f"{rel}: alias '{alias}' collides with {seen_aliases[ak].relative_to(root)}")
            seen_aliases[ak] = path

        fm_block = text[3:text.find(chr(10) + "---", 3)]
        if "{{date}}" in fm_block:
            errors.append(f"{rel}: literal '{{{{date}}}}' left in frontmatter")
        if SECRET_RE.search(text) or HEX_RE.search(text):
            errors.append(f"{rel}: a secret-shaped string was found - do not commit secrets")

    print(f"linted {note_count} note(s), {len(errors)} problem(s)")
    for err in errors:
        print(f"  {err}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
