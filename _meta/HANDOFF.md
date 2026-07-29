# HANDOFF

> The single coordination file. Every agent reads this FIRST at session start and rewrites it before STOP. Keep it short and current — it is state, not history (history goes to `_meta/log.md` and note `## Log` sections).

## Current status
Starter vault. Contract, schema, tag registry and a small worked example are in place. Nothing project-specific yet.

## Recent decisions
- [[0001-atomic-notes-over-long-documents]] — atomic notes over long documents (Accepted).

## Verification evidence
- Example notes [[postgres-connection-pooling-pgbouncer]] and [[postgres-max-connections]] link to each other and are curated in [[moc-research]]; no orphans.

## Known limits
- `domain/*` and `project/*` in [[tag-registry]] are placeholder values — replace before real use.

## Next task
- Replace the example domains/projects with your own, then delete the two example research notes (or keep them as a reference until your first real notes exist).

## Reservations
- Next ADR number: 0002.
