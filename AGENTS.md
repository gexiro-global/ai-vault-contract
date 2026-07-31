# AGENTS.md — the write contract for an AI-first knowledge vault

> Canonical operating contract for this vault. **Codex** reads this file natively; **Claude** reads it via `@AGENTS.md` in `CLAUDE.md`. One source of truth — do not fork these rules into other files. Keep this file lean (≤ ~220 lines / 32 KiB).
>
> This is a **template**. The method is the product; the folder names, `domain/*` and `project/*` values below are examples — replace them with your own. Everything about *how* notes are written is meant to be kept as-is.

This vault is an **AI-first knowledge base** maintained jointly by a human and one or more coding agents (here: Claude + Codex). It is a single, version-controlled source of organized knowledge — not a team wiki and not a dumping ground. Every note earns its place: atomic, self-contained, linked, deduplicated.

## Session start (every session, no exceptions)
1. Read `_meta/HANDOFF.md` — current state + your next task (and any pending sweep/ADR reservation).
2. Read this file + `00-index/tag-registry.md` ([[tag-registry]]) + `00-index/frontmatter-schema.md` ([[frontmatter-schema]]).
3. Read the relevant domain MOC from `00-index/home.md` ([[home]]) before adding to that domain.
Never write blind. If HANDOFF and this contract conflict, the contract wins — then fix HANDOFF.

## Folders (one physical home per note; intelligence lives in links/tags/MOCs)
- `00-index/` — MOCs + companions (`home`, `tag-registry`, `frontmatter-schema`, `moc-holding`, and your domain MOCs)
- `10-projects/` — product/build notes (one subfolder per project; add a local `_moc.md` at >~15 notes)
- `30-infra/` — one note per host/service/stack
- `40-research/` — the atomic knowledge core: one concept per note
- `50-inbox/` — unprocessed captures; triaged to empty (promote → or delete)
- `60-daily/` — `YYYY-MM-DD.md` day/session logs; `## Log` is append-only, `## Captures` are checkboxes
- `90-imports/` — quarantined raw imports; originals are NEVER mutated
- `_meta/` — coordination + audit: `HANDOFF.md`, `CHANGELOG.md`, `log.md`, `decisions/NNNN-*.md` (ADRs)
- `_templates/`, `_attachments/`
Keep the tree shallow (≤3 levels). One note = one folder. Cross-cutting membership = MOCs + tags, never copies.

## Note contract
- **Atomic** — one concept/entity/finding per note: the entirety of that one thing, nothing more. Hard to name = split it.
- **Self-contained** — a reader (human or a future agent) with ONLY this note understands it. Resolve pronouns / "the above" / "as mentioned". No dangling references.
- **Sized for retrieval** — aim ~200–500 tokens ≈ ~150–400 words ≈ ~1,000–2,800 chars of body. Hard-flag >~450 words → split at `##` boundaries into separate atomic notes.
- **Evidence-based** — ground claims in paths, dates, commands, hashes, URLs. Set `status: verified` only after end-to-end confirmation.
- **Uniquely named** - `title` equals the kebab-case filename stem, keyword-rich, a claim/handle; the note carries exactly one H1, which may read as prose. Filenames, titles, and `aliases` are unique vault-wide (case-insensitive): Obsidian resolves `[[link]]` by basename/alias with no uniqueness guarantee, so two `pooling` notes or a duplicated alias silently mis-resolve backlinks. **Qualify generic terms** — `connection-pooling-pgbouncer`, not `pooling`. `aliases:` carries every synonym / acronym / spelled-out form (the dedup + recall lever).

## Frontmatter (full spec: `00-index/frontmatter-schema.md`)
Required on every note: `title, type, status, tags, created, updated`. Add `aliases` whenever the concept has synonyms; `source` for provenance; `related` for `[[wikilinks]]`; `importance` (1–5) and `valid_as_of` where useful. `type`/`status` come from the CLOSED enums in the schema. Property *types* are vault-wide — never write `updated` as text in one note and a Date in another.
**Dates**: MCP/shell writes do NOT run Templater/live-clock, so `{{date}}` persists literally. Source the real date from session/git/deploy context and write a literal ISO `YYYY-MM-DD`. Never fabricate a timestamp and never write a non-date literal (e.g. `unknown`) into a date-typed field — if a date is truly unknown, resolve a real one.

## Tags (`00-index/tag-registry.md` is the closed vocabulary)
Namespaced only: `type/  status/  domain/  project/  flow/`. Pick from the registry — never invent. New tag → add it to the registry with a one-line definition FIRST, then use. Required on every note: a `type/*` tag; add `domain/*`, `project/*`, `flow/*` as they apply; ≤7 total — don't over-tag. The structural namespaces above are closed, intentionally high-cardinality enums and are EXEMPT from any split rule. The "object-tag not topic-tag / split past ~10 notes" rule applies ONLY to any future free-form topic tag: a tag must name a reusable object/attribute, not a one-off. Folders = where it lives; tags = what it's about; MOCs = curated navigation; frontmatter = queryable minutiae.

## Before you CREATE (anti-duplication — the #1 failure mode of an AI vault)
1. **SEARCH first** — full-text search the title, each intended alias, and 2–3 key terms, then check backlinks / unlinked-mentions. (Codex: `rg`/grep over the vault. Claude: an Obsidian MCP's BM25 search + backlinks.)
2. If a canonical note exists → **UPDATE or LINK** it. If two near-duplicates exist → **MERGE** (rewrite backlinks, archive the absorbed note `status: superseded` with a redirect link). Never leave two notes on one concept.
3. Only genuinely-new concepts get a new note. Cheap generation makes hoarding easy — **distill, don't accumulate**.

## Linking & MOCs (no orphans)
- Link with intent toward the more-canonical note; `[[wikilink]]` the first mention of any entity that has (or should have) a note. Backlinks are free.
- Every new note is linked from ≥1 MOC and ≥1 sibling. Zero inbound links = a bug — fix it in the same write session. No home yet → link it from `[[moc-holding]]` (orphan catcher) and move on.
- A MOC is curated/generated `[[wikilinks]]` under `##` headings, not a dump. Append a new note's link to the right MOC in the SAME session you create it. Split a MOC section into a sub-MOC past ~20–30 links.

## Update, log, supersede
- Bump `updated` on every edit (and `valid_as_of` when you re-confirm a fact).
- Material change → append `- YYYY-MM-DD — <what>` to the note's `## Log`, terse and evidence-based.
- NEVER hard-delete or silently overwrite a decision → set `status: superseded`, link the replacement. Structural / architecture / schema / taxonomy changes → write an ADR in `_meta/decisions/` (Nygard: Title / Status / Context / Decision / Consequences).
- **ADR/slug numbering (avoid collisions between two agents)**: before writing an ADR, compute `next = max(existing NNNN) + 1`, then reserve it by committing an `ADR NNNN reserved by <agent>` line in `_meta/HANDOFF.md` FIRST; the other agent sees it at session start. Same reserve-first pattern for any same-day numbered slug. Numbers are monotonic, never reused.
- `60-daily/` `## Log` is append-only; `## Captures` are checkboxes toggled during triage (`- [x] … → [[note]]`).

## OPSEC (hard — a versioned + mirrored vault means writes persist forever)
**Prevent (absolute).** NEVER write into any note / frontmatter / log: passwords, API keys, tokens, bearer/JWT/session cookies, private or SSH keys, seed phrases / mnemonics / wallet keystores, `.env` contents, DB/connection strings, or private personal data. Store the shape/placeholder (`<TOKEN>`), never the value; redact in capture-prone sections. Reference a secret by its role and store location, never its value.
**Own infrastructure.** Never record your OWN public IPs / ranges (use hostnames). Internal hostnames, ports, paths and container names may be documented ONLY in `30-infra/` notes, where that is the point — and only if the vault itself is private and access-gated. Keep them out of anything you intend to share or export.
**Respond** (if a secret ever lands in the vault): redaction does NOT remove it (it stays in git history + every mirror). So (1) treat it as compromised and rotate/revoke it out-of-band IMMEDIATELY — this is the primary control; (2) THEN scrub history (`git filter-repo`/BFG) and force-push ALL mirrors; (3) record the incident in an ADR + `_meta/log.md`.
**Enforce.** A pre-commit secret scan (gitleaks/trufflehog) is the teeth of the schema lint; `.gitignore` excludes `.obsidian/plugins/*/data.json`, `.obsidian/workspace*.json`, caches, `*.bak`.

## Git discipline
- Commit before AND after each batch. Small, atomic commits. Conventional Commits (`feat/fix/docs/chore/refactor(scope): …`).
- Hot shared files (`_meta/HANDOFF.md`, `_meta/log.md`) are append-oriented and **one-writer-at-a-time** — commit immediately so the diff is the lock record.
- Keep co-author trailers so history is attributable (which agent, or the human). `git rerere` is on.
- Never commit secrets or the ignored editor-state files.

## Handoff protocol (cold-resume across agents)
Before you STOP: rewrite `_meta/HANDOFF.md` (Current status / Recent decisions / Verification evidence / Known limits / Next task), append one line to `_meta/log.md`, then commit. The next agent reads HANDOFF first. Always leave the vault resumable cold.

## Retrieval model (why the rules above exist)
Recall leans on keyword-rich titles, rich `aliases`, explicit links, and consistent terminology, so full-text search + backlinks stay sharp. (Tooling example: Claude via an Obsidian MCP using BM25 + the backlink graph, embeddings OFF; Codex via ripgrep.) Below ~200k tokens the whole vault can be read directly — keep notes high-signal.

## Keeping the vault healthy (wired checks, not hopes)
**Every session-end, over the notes you touched:** run the zero-orphan check, MOC-upkeep, and schema/size lint; fix or park in `[[moc-holding]]`. Then do the handoff + commit.
**Full-vault sweep on a cadence** (a scheduled agent job runs all five below and appends an evidence line to `_meta/log.md`). If the last sweep is >7 days old, HANDOFF flags it and the next session runs it first.
1. **Inbox/daily triage** — promote captures to atomic notes, dedup, empty `50-inbox/`.
2. **Zero-orphan** — every note reachable from ≥1 MOC, else → `[[moc-holding]]`.
3. **MOC upkeep** — append new notes; split oversized MOCs (~20–30 links).
4. **Schema + size lint** — frontmatter complete, tags ⊆ registry, filenames/titles/aliases unique (case-insensitive), flag >~450-word notes; run the secret scan.
5. **Dedup** — for each note, full-text-search its title + each alias + top key terms; if a DIFFERENT note ranks high on ≥2 overlapping terms, tag both `flow/dupe-candidate`, list them in HANDOFF, and MERGE (rewrite backlinks, absorb, `status: superseded` + redirect).
