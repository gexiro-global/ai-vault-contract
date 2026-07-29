# Changelog

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - Unreleased

### Added
- Initial public release.
- `AGENTS.md` write contract for an AI-first knowledge vault, with `CLAUDE.md` pointer.
- `00-index/` companions: home MOC, closed tag registry, frontmatter schema, orphan catcher.
- `_templates/` note and ADR templates.
- A worked example: two linked research notes, an ADR, a daily log, and the research MOC.
- `tools/lint_vault.py` structural linter (frontmatter, enums, title/filename, uniqueness, dates,
  secret-shaped strings) with an offline test suite.
- CI that lints the example vault and tests the linter.
