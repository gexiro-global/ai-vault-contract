#!/usr/bin/env python3
"""lint_vault.py - structural lint for a vault built on the ai-vault-contract.

Checks the mechanical rules the contract can enforce without judgement:
  * every note in a vault folder carries the required frontmatter
  * `type` and `status` are drawn from the closed enums
  * `tags` is a list, every tag exists in the registry, and a `type/*` tag is present
  * `title` equals the filename stem, and the note has exactly one H1
  * titles and aliases are unique vault-wide, in one shared namespace
  * dates are real ISO calendar dates, and no literal `{{date}}` survives in frontmatter
  * no obviously secret-shaped strings were committed

It does NOT judge whether a note is atomic, well-linked or non-duplicative - those need a
model, not a linter. Exit 0 clean, 1 on any violation.
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

# Folders whose Markdown files ARE vault notes. A file here without frontmatter is an error,
# not something to skip - otherwise deleting a note's frontmatter silently bypasses every check.
VAULT_DIRS = {
    "00-index", "10-projects", "30-infra", "40-research",
    "50-inbox", "60-daily", "90-imports", "_meta",
}
# Repository documentation and templates are not notes.
EXCLUDE_DIRS = {".git", ".github", ".obsidian", "_attachments", "tools", "_templates"}
EXEMPT_NAMES = {"HANDOFF.md", "log.md", "CHANGELOG.md", ".gitkeep.md"}

MAX_TAGS = 7
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*\S{8,}")
HEX_RE = re.compile(r"\b[0-9a-f]{32,}\b")
H1_RE = re.compile(r"^#\s+\S", re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Minimal YAML-ish frontmatter reader: flat scalars and inline `[a, b]` lists.

    Returns (fields, raw_frontmatter_block). Empty dict when there is no frontmatter.
    """
    if not text.startswith("---"):
        return {}, ""
    end = text.find("\n---", 3)
    if end == -1:
        return {}, ""
    block = text[3:end]
    out: dict = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            out[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            out[key] = val.strip("'\"")
    return out, block


def load_registry(root: pathlib.Path) -> tuple:
    """Read the allowed tags out of 00-index/tag-registry.md.

    Returns (tags, problem). A missing or unreadable registry disables membership checking, so
    it is reported as a problem rather than passing quietly - a vault whose closed vocabulary
    silently stopped being enforced looks exactly like a clean one.
    """
    path = root / "00-index" / "tag-registry.md"
    if not path.is_file():
        return set(), f"tag registry not found at {path.relative_to(root)} - tag membership is NOT enforced"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return set(), f"tag registry unreadable ({exc}) - tag membership is NOT enforced"
    tags = set(re.findall(r"`((?:type|status|domain|project|flow)/[a-z0-9-]+)`", text))
    if not tags:
        return set(), "tag registry contains no recognisable tags - tag membership is NOT enforced"
    return tags, None


def is_note(path: pathlib.Path, root: pathlib.Path) -> bool:
    rel = path.relative_to(root)
    if rel.name in EXEMPT_NAMES:
        return False
    return bool(rel.parts) and rel.parts[0] in VAULT_DIRS


def iter_markdown(root: pathlib.Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = pathlib.Path(argv[0]) if argv else pathlib.Path(".")
    registry, registry_problem = load_registry(root)
    errors: list[str] = []
    # One shared namespace: an alias must not collide with another note's title either.
    seen_names: dict[str, pathlib.Path] = {}
    note_count = 0

    for path in iter_markdown(root):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        fm, fm_block = parse_frontmatter(text)

        if not is_note(path, root):
            continue
        note_count += 1

        if not fm:
            errors.append(f"{rel}: missing or unparseable frontmatter")
            continue

        for field in REQUIRED:
            if field not in fm or fm[field] in ("", [], None):
                errors.append(f"{rel}: missing required field '{field}'")

        if fm.get("type") and fm["type"] not in TYPE_ENUM:
            errors.append(f"{rel}: type '{fm['type']}' not in the enum")
        if fm.get("status") and fm["status"] not in STATUS_ENUM:
            errors.append(f"{rel}: status '{fm['status']}' not in the enum")

        tags = fm.get("tags")
        if tags is not None:
            if not isinstance(tags, list):
                errors.append(f"{rel}: tags must be a list, e.g. [type/research, domain/infra]")
            else:
                if not any(str(t).startswith("type/") for t in tags):
                    errors.append(f"{rel}: no type/* tag")
                if len(tags) > MAX_TAGS:
                    errors.append(f"{rel}: {len(tags)} tags, the contract allows at most {MAX_TAGS}")
                for tag in tags:
                    if registry and str(tag) not in registry:
                        errors.append(f"{rel}: tag '{tag}' is not in the registry")

        stem = path.stem
        if fm.get("title") and fm["title"] != stem:
            errors.append(f"{rel}: title '{fm['title']}' != filename stem '{stem}'")

        # Strip fenced code before counting headings: a `# example` inside a shell snippet is
        # not a heading, and flagging it trains people to ignore the linter.
        body = re.sub(r"^```.*?^```", "", text, flags=re.MULTILINE | re.DOTALL)
        headings = H1_RE.findall(body)
        if len(headings) != 1:
            errors.append(f"{rel}: expected exactly one H1 heading, found {len(headings)}")

        for field in ("created", "updated", "valid_as_of"):
            val = fm.get(field)
            if not val:
                continue
            try:
                _dt.date.fromisoformat(str(val))
            except ValueError:
                errors.append(f"{rel}: {field} '{val}' is not a real ISO date")

        aliases = fm.get("aliases")
        if aliases is not None and not isinstance(aliases, list):
            # A bare scalar would otherwise be iterated character by character, so every letter
            # became an "alias" and real collisions were never detected.
            errors.append(f"{rel}: aliases must be a list, e.g. [first, second]")
            aliases = []
        names = [str(fm.get("title", stem))] + [str(a) for a in (aliases or [])]
        for name in names:
            key = name.lower()
            other = seen_names.get(key)
            if other is not None and other != path:
                errors.append(f"{rel}: name '{name}' collides with {other.relative_to(root)}")
            seen_names[key] = path

        if "{{date}}" in fm_block:
            errors.append(f"{rel}: literal '{{{{date}}}}' left in frontmatter")
        if SECRET_RE.search(text) or HEX_RE.search(text):
            errors.append(f"{rel}: a secret-shaped string was found - do not commit secrets")

    # A vault with no notes needs no registry; one with notes but no registry has silently
    # stopped enforcing its closed vocabulary, which must not look like a clean run.
    if registry_problem and note_count:
        errors.insert(0, registry_problem)

    print(f"linted {note_count} note(s), {len(errors)} problem(s)")
    for err in errors:
        print(f"  {err}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
