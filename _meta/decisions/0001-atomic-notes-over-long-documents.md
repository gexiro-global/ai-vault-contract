---
title: 0001-atomic-notes-over-long-documents
aliases: [adr-0001, atomic-notes-decision]
type: adr
status: active
tags: [type/adr, domain/meta]
source: template
created: 2026-01-01
updated: 2026-01-01
---

# ADR 0001 — Atomic notes over long documents

**Status:** Accepted

## Context
The vault is read by coding agents through full-text search and a backlink graph, not by a human scrolling. Long, multi-topic documents rank ambiguously (many terms, no single focus), return oversized chunks, and accumulate duplicated sub-sections that drift out of sync. The dominant failure mode of an AI-maintained vault is duplication, and long documents make duplication invisible.

## Decision
One concept per note, ~200–500 tokens, uniquely and descriptively named, with rich `aliases`. Cross-cutting membership is expressed through MOCs and tags, never by copying content between notes. Notes over ~450 words are split at `##` boundaries.

## Consequences
- **Good:** sharper retrieval (a note is *about* one thing), cheap dedup (search a title + its aliases before creating), and safe merges (rewrite backlinks, supersede the absorbed note).
- **Cost:** more notes and more linking discipline; a new note must be linked from a MOC and a sibling in the same session, or the zero-orphan check flags it.
- **Follow-on:** the health sweep in [[AGENTS]] enforces this (schema/size lint + dedup pass).
