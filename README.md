# ai-vault-contract

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Lint](https://github.com/gexiro-global/ai-vault-contract/actions/workflows/lint.yml/badge.svg)](https://github.com/gexiro-global/ai-vault-contract/actions/workflows/lint.yml)

A starter [Obsidian](https://obsidian.md) vault and write-contract for a knowledge base that **coding agents maintain alongside you** — built for Claude and Codex, usable by any agent that can read Markdown and run a shell.

The hard part of an AI-maintained knowledge base is not storage. It is stopping the agent from quietly writing the fourth slightly-different note about the same thing. This repo is the set of rules that prevents that, plus the folder structure and templates that make the rules enforceable.

## What you get

- **`AGENTS.md`** — the write contract. One file, read natively by Codex and by Claude via `CLAUDE.md`. It defines what a note *is*, how notes are named and linked, how frontmatter and tags are constrained, and — crucially — the search-before-create discipline that keeps the vault from duplicating itself.
- **`00-index/`** — the closed [tag registry](00-index/tag-registry.md) and [frontmatter schema](00-index/frontmatter-schema.md), a [home MOC](00-index/home.md), and an orphan-catcher.
- **`_templates/`** — a note template and an ADR template.
- **A small worked example** — two linked research notes, one ADR, one daily log, and the MOC that curates them, so you can see the pattern in a live vault rather than in prose.

## The ideas worth stealing

Even if you never open Obsidian, these are the parts that make an agent-maintained vault work:

1. **Atomic notes.** One concept per note, ~200–500 tokens, uniquely named with rich aliases. Retrieval is sharp because each note is *about* one thing. ([ADR 0001](_meta/decisions/0001-atomic-notes-over-long-documents.md) explains why.)
2. **Search before you create.** Duplication is the number-one failure of an AI vault. The contract makes the agent search the title, every alias, and key terms — and *merge* rather than add — before writing anything new.
3. **Closed vocabularies.** `type` and `status` are fixed enums; tags come from a registry, never invented. Property types are uniform vault-wide so queries never silently break.
4. **Supersede, never delete.** Decisions become ADRs; replaced notes are marked `superseded` with a redirect. History is a feature.
5. **Bi-temporal facts.** `updated` tracks the note; `valid_as_of` tracks when the fact was last confirmed true. An agent can tell a stale note from an unchanged one.
6. **A cold-resume handoff.** One `HANDOFF.md` is rewritten before every stop, so a different agent (or the same one next week) resumes without guessing.
7. **OPSEC as a hard rule.** A versioned, mirrored vault keeps writes forever, so secrets never go in — not even redacted. The contract says how to prevent, and how to respond if one slips in.

## Use it

```bash
git clone https://github.com/gexiro-global/ai-vault-contract.git my-vault
cd my-vault
```

1. Open the folder as a vault in Obsidian (or just edit the Markdown — nothing here needs Obsidian to *run*).
2. Point your agent at it: Codex reads `AGENTS.md` natively; Claude reads it through `CLAUDE.md`.
3. In [`00-index/tag-registry.md`](00-index/tag-registry.md), replace the example `domain/*` and `project/*` values with your own. The `type/`, `status/` and `flow/` namespaces are part of the method — keep them.
4. Delete the two example research notes and the sample daily log once your own notes exist, or keep them as a reference.

## What this is NOT

- It is not an application or a plugin. It is a **convention plus a starting structure**; the notes and the contract are the product. The one executable here is
  `tools/lint_vault.py`, a dependency-free structural linter you can run or ignore.
- It does not lint your vault for you out of the box. The contract specifies the checks (schema, size, orphans, dedup, secret scan); wiring them to a specific tool or a pre-commit hook is left to you, because the right tool depends on your setup. The included CI does a minimal structural check as a starting point.
- It is not tied to a specific model or agent. Claude and Codex are the reference pair; the rules are model-agnostic.
- It is not a Zettelkasten purity project. It borrows atomicity and linking from that tradition and drops the ceremony.

## Layout

```
AGENTS.md                 the write contract (start here)
CLAUDE.md                 pointer to AGENTS.md for Claude tooling
00-index/                 home MOC, tag registry, frontmatter schema, orphan catcher
10-projects/  30-infra/   your notes live here (examples in 40-research/)
40-research/              atomic knowledge core — worked example inside
50-inbox/  60-daily/      capture and day logs
90-imports/               quarantined raw imports (never mutated)
_meta/                    HANDOFF, log, and ADRs (decisions/)
_templates/               note and ADR templates
```

## License

[MIT](LICENSE) — use it, adapt it, ship your own vault from it.

Built and maintained by Gexiro Global Enterprises Ltd.
