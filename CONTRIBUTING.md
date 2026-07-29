# Contributing

This repo is a convention and a starter structure, so the most valuable contributions are
improvements to the *method* — a rule that prevents a failure mode, a sharper wording in
`AGENTS.md`, a check the linter could mechanically enforce.

## Ground rules

- `AGENTS.md` is the single source of truth. Do not restate its rules in other files; link to it.
- Keep `AGENTS.md` lean (≤ ~220 lines). If a rule needs a page of justification, that page is an
  ADR under `_meta/decisions/`, and `AGENTS.md` gets the one-line version.
- The example notes must stay fully synthetic — fictional products, no real hostnames, no secrets.
- Anything you add to the linter needs a case in `tools/test_lint_vault.py`, including a test that
  it *catches* the thing it claims to catch.
- The linter checks only mechanical rules. Do not add checks that require judgement ("is this note
  atomic?") — those belong to the agent, not a regex.

## Scope

This is intentionally small and model-agnostic. Proposals that couple it to one vendor, one plugin,
or one hosting setup will be steered back toward the generic core.

## Support expectations

Best-effort maintenance, no SLA. It is a template — fork it and make it yours.
