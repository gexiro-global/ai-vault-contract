---
title: tag-registry
aliases: [tag-registry, tags, taxonomy, vocabulary]
type: reference
status: active
tags: [type/reference, domain/meta]
source: template
created: 2026-01-01
updated: 2026-01-01
---

# Tag Registry

The ONLY valid tags. **Pick from this list — never invent.** Add a new tag here (with a one-line definition) FIRST, then use it. Namespaced and hierarchical (`/`). Companion to [[AGENTS]] and [[frontmatter-schema]].

> The `domain/*` and `project/*` values below are **examples** — replace them with the subject areas and products of your own vault. The `type/`, `status/` and `flow/` namespaces are part of the method; keep them.

## Governance
- Required on every note: a `type/*` tag. Add `domain/*`, `project/*`, `flow/*` as they apply. ≤7 total — don't over-tag.
- The structural namespaces here (`type/ status/ domain/ project/ flow/`) are closed, intentionally high-cardinality enums — **EXEMPT from any split rule**. `domain/infra` or `project/platform` matching hundreds of notes is by design.
- The "object-tag not topic-tag / split past ~10 notes" rule applies ONLY to any future free-form topic tag: a tag must name a reusable object/attribute, not a one-off.
- A parent-tag search matches all nested children (`tag:type` finds `type/research`, `type/reference`, …), so nest deliberately.

## type/* (note kind — mirrors frontmatter `type`)
- `type/index` — the root map (`home`)
- `type/moc` — map of content / domain index
- `type/project` — product/build note
- `type/infra` — host/service/stack note
- `type/research` — atomic knowledge note
- `type/reference` — stable reference/contract
- `type/source` — literature/source note (one per external source)
- `type/daily` — day/session log
- `type/import` — imported raw material
- `type/critique` — external critique/review
- `type/adr` — architecture/decision record (`_meta/decisions/`)

## status/* (OPTIONAL retrieval mirror)
Frontmatter `status` is authoritative. Add a `status/*` tag ONLY when you want to filter/group by status in search or the graph — it is not required. Values mirror the enum:
`status/draft` · `status/active` · `status/verified` · `status/in-flight` · `status/blocked` · `status/superseded` · `status/done` · `status/archived` · `status/unprocessed`

## domain/* (subject area — EXAMPLE object-tags; replace with your own)
`domain/meta` · `domain/engineering` · `domain/infra` · `domain/product` · `domain/research` · `domain/ops` · `domain/ai`

## project/* (owning product — EXAMPLE values; replace with your own)
`project/platform` · `project/webapp` · `project/mobile` · `project/second-brain`

## flow/* (pipeline state the invariant jobs act on)
- `flow/inbox` — captured, not yet triaged
- `flow/to-distill` — needs rewrite into an atomic note
- `flow/orphan` — no MOC/backlink home yet (parked in `[[moc-holding]]`)
- `flow/dupe-candidate` — flagged as a possible duplicate, awaiting merge decision

## Controlled frontmatter enums (authoritative copy in [[frontmatter-schema]])
- `type`: index | moc | project | infra | research | reference | source | daily | import | critique | adr
- `status`: draft | active | verified | in-flight | blocked | superseded | done | archived | unprocessed
