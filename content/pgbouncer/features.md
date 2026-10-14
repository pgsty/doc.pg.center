---
title: "Features"
weight: 10
description: "PgBouncer features — pooling modes and SQL compatibility"
icon: fa-solid fa-wand-magic-sparkles
module: [PGBOUNCER]
categories: [Concept]
upstream_link: "https://www.pgbouncer.org/features.html"
---

- Several levels of brutality when rotating connections:

  **Session pooling**
  : Most polite method. When a client connects, a server connection will be assigned to it for the whole duration it stays connected. When the client disconnects, the server connection will be put back into pool. This mode supports all PostgreSQL features.

  **Transaction pooling**
  : A server connection is assigned to a client only during a transaction. When PgBouncer notices that the transaction is over, the server will be put back into the pool. This mode breaks a few session-based features of PostgreSQL. You can use it only when the application cooperates by not using features that break. See the table below for incompatible features.

  **Statement pooling**
  : Most aggressive method. This is transaction pooling with a twist: Multi-statement transactions are disallowed. This is meant to enforce "autocommit" mode on the client, mostly targeted at PL/Proxy.

- Low memory requirements (2 kB per connection by default). This is because PgBouncer does not need to see full packets at once.

- It is not tied to one backend server. The destination databases can reside on different hosts.

- Supports online reconfiguration for most settings.

- Supports [rolling restarts and upgrades](/pgbouncer/usage/#shutdown-wait_for_clients) using multiple processes with [`so_reuseport`](/pgbouncer/config/#so_reuseport). The legacy online restart (`-R`) was removed in 1.26.0.

--------

## SQL feature map for pooling modes

The following table lists various PostgreSQL features and whether they are compatible with PgBouncer pooling modes. Note that "transaction" pooling breaks client expectations of the server *by design* and can be used only if the application cooperates by not using non-working features.

| Feature                          | Session pooling  |  Transaction pooling  |
|----------------------------------|:----------------:|:---------------------:|
| Startup parameters [^0]          | Yes              |          Yes          |
| SET/RESET                        | Yes              | For tracked parameters [^0] |
| LISTEN                           | Yes              |         Never         |
| NOTIFY                           | Yes              |          Yes          |
| WITHOUT HOLD CURSOR              | Yes              |          Yes          |
| WITH HOLD CURSOR                 |       Yes        |         Never         |
| Protocol-level prepared plans    | Yes              |       Yes [^1]        |
| PREPARE / DEALLOCATE             | Yes              |         Never         |
| ON COMMIT DROP temp tables       | Yes              |          Yes          |
| PRESERVE/DELETE ROWS temp tables | Yes              |         Never         |
| Cached plan reset                | Yes              |          Yes          |
| LOAD statement                   | Yes              |         Never         |
| Session-level advisory locks     | Yes              |         Never         |

[^0]: Since 1.26.0, PgBouncer tracks all server-reported parameters that clients can change: `application_name`, `client_encoding`, `DateStyle`, `default_transaction_read_only` (PostgreSQL 14+), `IntervalStyle`, `scram_iterations` (PostgreSQL 16+), `search_path` (PostgreSQL 18+), `session_authorization`, `standard_conforming_strings`, and `TimeZone`. For parameters that the server does not report, only startup values are tracked; later `SET` changes are not. See [`track_extra_parameters`](/pgbouncer/config/#track_extra_parameters) and [`ignore_startup_parameters`](/pgbouncer/config/#ignore_startup_parameters) for details and extension-provided parameters.

[^1]: Protocol-level prepared statement support is enabled when [`max_prepared_statements`](/pgbouncer/config/#max_prepared_statements) is non-zero. The default is 200; setting it to 0 disables this support. SQL-level `PREPARE` / `DEALLOCATE` remains incompatible with transaction pooling, except for `DEALLOCATE ALL` and `DISCARD ALL` when tracking is enabled.
