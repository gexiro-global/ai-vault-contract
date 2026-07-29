---
title: frontmatter-schema
aliases: [frontmatter, schema, yaml, properties, note-schema]
type: reference
status: active
tags: [type/reference, domain/meta]
source: template
created: 2026-01-01
updated: 2026-01-01
---

# Frontmatter Schema

Canonical YAML for every note. Property **types are enforced vault-wide** by Obsidian — keep each field's type identical across all notes or queries silently break. Companion to [[AGENTS]] and [[tag-registry]].

## Field set

| field | type | required | notes |
|---|---|---|---|
| `title` | Text | yes | `== H1 ==` kebab filename stem; keyword-rich claim/handle; unique vault-wide (case-insensitive) |
| `aliases` | List | when synonyms exist | acronyms / synonyms / spelled-out forms; unique vault-wide — qualify generic acronyms (`cache-write-through`, not `cache`) |
| `type` | Text (enum) | yes | one value, see enum below |
| `status` | Text (enum) | yes | one value, see enum below |
| `importance` | Number 1–5 | optional | ranking weight (recency + importance + relevance) |
| `tags` | List | yes | namespaced, from [[tag-registry]]; a `type/*` is required |
| `created` | Date | yes | ISO `YYYY-MM-DD` |
| `updated` | Date | yes | ISO; bump on every edit |
| `valid_as_of` | Date | optional | when the fact was last confirmed true (bi-temporal) |
| `source` | Text | provenance | base URL (strip creds/tokens/query secrets) / repo-relative or sanitized path (NEVER an absolute host path) / commit hash |
| `related` | List | optional | `[[wikilinks]]` to canonical notes — link, don't copy |

**Type-specific extras** (add to the core set, don't replace it):
- `finding`: `severity`, `confidence`
- `research`: `confidence` (optional)
- `reference`/`source`: `source` (required), `author`
- `project`: `project` (link to its MOC)

## `type` enum
`index | moc | project | infra | research | reference | source | daily | import | critique | adr`

## `status` enum
`draft | active | verified | in-flight | blocked | superseded | done | archived | unprocessed`

**ADR status mapping** (Nygard body-state → this enum): Proposed → `draft`; Accepted → `active`; Superseded → `superseded`.

## Dates
ISO `YYYY-MM-DD` only. MCP/shell writes do NOT run Templater, so `{{date}}` persists literally and there is no live clock — source the real date from session/git/deploy context (see [[AGENTS]] Frontmatter). Never fabricate a timestamp and never write a non-date literal (e.g. `unknown`) into a date-typed field.

## Example

```yaml
---
title: postgres-connection-pooling-pgbouncer
aliases: [pgbouncer, connection-pooling, transaction-pooling]
type: research
status: verified
importance: 3
tags: [type/research, domain/infra, project/platform]
created: 2026-01-01
updated: 2026-01-01
valid_as_of: 2026-01-01
source: https://www.pgbouncer.org/features.html
related: ["[[postgres-max-connections]]", "[[database-connection-limits]]"]
---
```

## Rules
- Exactly one `type`; pick the closest.
- `status: verified` only after end-to-end confirmation; otherwise `active`/`draft`.
- ISO dates only; never live `{{date}}`.
- Never store secrets or absolute host paths in any field — see [[AGENTS]] OPSEC.
