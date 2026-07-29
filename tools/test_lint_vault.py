#!/usr/bin/env python3
"""Tests for lint_vault.py. Runs offline, no dependencies.

Proves two things: the shipped example vault passes, and a deliberately broken note
is actually caught (a linter that never fails is worse than none).
"""

import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
LINT = HERE / "lint_vault.py"


def run(root):
    proc = subprocess.run(
        [sys.executable, str(LINT), str(root)], capture_output=True, text=True
    )
    return proc.returncode, proc.stdout


def test_shipped_vault_is_clean():
    rc, out = run(REPO)
    assert rc == 0, f"the shipped example vault should lint clean:\n{out}"


def test_bad_type_is_caught():
    with tempfile.TemporaryDirectory() as d:
        note = pathlib.Path(d) / "broken-note.md"
        note.write_text(
            "---\n"
            "title: broken-note\n"
            "type: notarealtype\n"
            "status: active\n"
            "tags: [type/research]\n"
            "created: 2026-01-01\n"
            "updated: 2026-01-01\n"
            "---\n\n# broken-note\n",
            encoding="utf-8",
        )
        rc, out = run(d)
        assert rc == 1 and "not in the enum" in out, out


def test_title_filename_mismatch_is_caught():
    with tempfile.TemporaryDirectory() as d:
        note = pathlib.Path(d) / "a.md"
        note.write_text(
            "---\ntitle: not-a\ntype: research\nstatus: active\n"
            "tags: [type/research]\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n",
            encoding="utf-8",
        )
        rc, out = run(d)
        assert rc == 1 and "filename stem" in out, out


def test_secret_shaped_string_is_caught():
    with tempfile.TemporaryDirectory() as d:
        note = pathlib.Path(d) / "leaky.md"
        note.write_text(
            "---\ntitle: leaky\ntype: research\nstatus: active\n"
            "tags: [type/research]\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n\n"
            "api_key = abcdef0123456789abcdef0123456789\n",
            encoding="utf-8",
        )
        rc, out = run(d)
        assert rc == 1 and "secret-shaped" in out, out


def test_non_note_files_are_ignored():
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "README.md").write_text("# just prose\n", encoding="utf-8")
        rc, out = run(d)
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
