---
title: pg_tde_waldump
linkTitle: WAL inspection
description: Inspect encrypted WAL with a pg_tde-aware version of pg_waldump.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/command-line-tools/pg-tde-waldump.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 760
upstream_source: percona-20261121
---

[`pg_tde_waldump` ](https://www.postgresql.org/docs/current/pgwaldump.html) displays a human-readable rendering of the Write-Ahead Log (WAL) for a PostgreSQL database cluster.

To read encrypted WAL records, `pg_tde_waldump` provides the following additional option:

* `-k, --keyring-path=PATH` is the path to the directory containing the WAL keyring configuration files. This is typically the `pg_tde/` directory inside the PostgreSQL data directory. The following files are included:
    * `wal_keys`
    * `1664_providers`

> [!NOTE]
> `pg_tde_waldump` cannot read encrypted WAL unless `--keyring-path` is specified.

Since [pg_tde 2.3.0](/percona/release-notes/release-notes-v2.3.0/), `pg_tde_waldump` recognizes the `pg_tde` custom resource manager, prints its WAL records correctly, and accepts it in the `--rmgr` filter.
