#!/usr/bin/env python3
"""Tests for lint_vault.py. Runs offline, no dependencies.

Every check gets a case that proves it FAILS on bad input - a linter whose tests only feed it
valid material will happily pass after the check itself is deleted.
"""

import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
LINT = HERE / "lint_vault.py"

GOOD = """---
title: {stem}
aliases: [{aliases}]
type: research
status: active
tags: [type/research]
created: 2026-01-01
updated: 2026-01-01
---

# {stem}

Body.
"""


def run(root):
    proc = subprocess.run(
        [sys.executable, str(LINT), str(root)], capture_output=True, text=True
    )
    return proc.returncode, proc.stdout


def vault(tmp, **notes):
    """Build a throwaway vault: {filename: content} under 40-research/."""
    root = pathlib.Path(tmp)
    (root / "40-research").mkdir(parents=True, exist_ok=True)
    for name, content in notes.items():
        (root / "40-research" / name).write_text(content, encoding="utf-8")
    return root


def test_shipped_vault_is_clean():
    rc, out = run(REPO)
    assert rc == 0, f"the shipped example vault should lint clean:\n{out}"


def test_a_valid_note_passes():
    with tempfile.TemporaryDirectory() as d:
        root = vault(d, **{"ok-note.md": GOOD.format(stem="ok-note", aliases="okn")})
        rc, out = run(root)
        assert rc == 0, out


def test_bad_type_is_caught():
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="broken-note", aliases="bn").replace(
            "type: research", "type: notarealtype"
        )
        rc, out = run(vault(d, **{"broken-note.md": body}))
        assert rc == 1 and "not in the enum" in out, out


def test_title_filename_mismatch_is_caught():
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="a", aliases="aa").replace("title: a", "title: not-a")
        rc, out = run(vault(d, **{"a.md": body}))
        assert rc == 1 and "filename stem" in out, out


def test_impossible_date_is_caught():
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="dated", aliases="dt").replace(
            "updated: 2026-01-01", "updated: 2026-99-99"
        )
        rc, out = run(vault(d, **{"dated.md": body}))
        assert rc == 1 and "not a real ISO date" in out, out


def test_unregistered_tag_is_caught():
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        (root / "00-index").mkdir(parents=True)
        (root / "00-index" / "tag-registry.md").write_text(
            "# Tag Registry\n\n- `type/research` - a note\n", encoding="utf-8"
        )
        body = GOOD.format(stem="tagged", aliases="tg").replace(
            "tags: [type/research]", "tags: [type/research, domain/invented]"
        )
        vault(d, **{"tagged.md": body})
        rc, out = run(root)
        assert rc == 1 and "not in the registry" in out, out


def test_missing_type_tag_is_caught():
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="untyped", aliases="ut").replace(
            "tags: [type/research]", "tags: [domain/infra]"
        )
        rc, out = run(vault(d, **{"untyped.md": body}))
        assert rc == 1 and "no type/* tag" in out, out


def test_alias_colliding_with_another_title_is_caught():
    with tempfile.TemporaryDirectory() as d:
        root = vault(
            d,
            **{
                "first-note.md": GOOD.format(stem="first-note", aliases="fn"),
                "second-note.md": GOOD.format(stem="second-note", aliases="first-note"),
            },
        )
        rc, out = run(root)
        assert rc == 1 and "collides" in out, out


def test_missing_h1_is_caught():
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="headless", aliases="hl").replace("# headless\n", "")
        rc, out = run(vault(d, **{"headless.md": body}))
        assert rc == 1 and "exactly one H1" in out, out


def test_note_without_frontmatter_is_an_error_not_a_skip():
    with tempfile.TemporaryDirectory() as d:
        rc, out = run(vault(d, **{"bare.md": "# bare\n\nno frontmatter here\n"}))
        assert rc == 1 and "missing or unparseable frontmatter" in out, out


def test_secret_shaped_string_is_caught():
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="leaky", aliases="lk") + "\napi_key = abcdef0123456789abcdef0123456789\n"
        rc, out = run(vault(d, **{"leaky.md": body}))
        assert rc == 1 and "secret-shaped" in out, out


def test_scalar_aliases_is_rejected_not_iterated():
    """A bare scalar was iterated character by character, so every letter became an alias."""
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="scalar-alias", aliases="x").replace(
            "aliases: [x]", "aliases: justastring"
        )
        rc, out = run(vault(d, **{"scalar-alias.md": body}))
        assert rc == 1 and "aliases must be a list" in out, out


def test_h1_inside_a_code_fence_is_not_counted():
    """A comment inside a fenced block is not a heading."""
    fence = chr(96) * 3
    with tempfile.TemporaryDirectory() as d:
        body = GOOD.format(stem="fenced", aliases="fnc")
        body += "\n" + fence + "bash\n# not a heading\necho hi\n" + fence + "\n"
        rc, out = run(vault(d, **{"fenced.md": body}))
        assert rc == 0, out


def test_repo_docs_outside_vault_folders_are_ignored():
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        (root / "README.md").write_text("# just prose\n", encoding="utf-8")
        rc, out = run(root)
        assert rc == 0, out


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok   - {name}")
            except AssertionError as exc:
                failures += 1
                print(f"  FAIL - {name}: {exc}")
    print(f"\n{'all tests passed' if not failures else str(failures) + ' failure(s)'}")
    sys.exit(1 if failures else 0)
