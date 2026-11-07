---
title: pg_tde_waldump
linkTitle: WAL inspection
description: Inspect encrypted WAL with a pg_tde-aware version of pg_waldump.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-waldump.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 760
upstream_source: percona
---

[`pg_tde_waldump` ](https://www.postgresql.org/docs/current/pgwaldump.html) displays a human-readable rendering of the Write-Ahead Log (WAL) for a PostgreSQL database cluster.

To read encrypted WAL records, `pg_tde_waldump` provides the following additional option:

* `-k, --keyring-path=PATH` is the path to the directory containing the WAL keyring configuration files. This is typically the `pg_tde/` directory inside the PostgreSQL data directory. The following files are included:
    * `wal_keys`
    * `1664_providers`

> [!NOTE]
> `pg_tde_waldump` cannot read encrypted WAL unless `--keyring-path` is specified.
