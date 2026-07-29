---
title: postgres-max-connections
aliases: [max_connections, postgres-connection-limit]
type: research
status: active
importance: 2
tags: [type/research, domain/infra, project/platform]
created: 2026-01-01
updated: 2026-01-01
source: https://www.postgresql.org/docs/current/runtime-config-connection.html
related: ["[[postgres-connection-pooling-pgbouncer]]"]
---

# Postgres max_connections

`max_connections` caps concurrent connections to a Postgres cluster (default 100). Raising it is tempting under connection pressure and usually the wrong lever: each allowed connection reserves memory whether or not it is active, and past a few hundred the per-connection overhead and lock contention cost more than the extra concurrency buys.

The scalable answer is a connection pooler in front of the database — see [[postgres-connection-pooling-pgbouncer]] — sized so the pool's server-side connection count stays comfortably under `max_connections`, leaving headroom for superuser and maintenance connections (`superuser_reserved_connections`).

## Log
- 2026-01-01 — created as the counterpart to the pooling note.
