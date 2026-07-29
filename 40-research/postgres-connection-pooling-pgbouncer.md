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
related: ["[[postgres-max-connections]]"]
---

# Postgres connection pooling with PgBouncer

Each Postgres backend connection costs roughly 5–10 MB of server memory and a process, so a few thousand direct client connections exhaust the server long before they exhaust useful throughput. PgBouncer sits in front of Postgres and multiplexes many short client connections onto a small pool of long-lived server connections.

Three pool modes, cheapest-to-strictest:
- **session** — a server connection is held for the whole client session. Safe for everything, pools the least.
- **transaction** — the server connection is returned to the pool at each transaction boundary. The usual choice for web apps; the highest multiplexing that still keeps transactions intact.
- **statement** — returned after every statement. Highest reuse, but forbids multi-statement transactions.

**Trap:** transaction mode breaks anything that relies on session state across transactions — `SET`, `LISTEN/NOTIFY`, session-level advisory locks, server-side prepared statements. If the app needs those, it must pin the session or use session mode.

## Log
- 2026-01-01 — created; verified pool-mode behaviour against PgBouncer docs.
