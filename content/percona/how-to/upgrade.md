---
title: Upgrade pg_tde
linkTitle: Upgrade pg_tde
description: Plan extension upgrades and major PostgreSQL upgrades for encrypted clusters.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/upgrade.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 570
upstream_source: percona
---

The version of `pg_tde` available to you depends on your version of Percona Distribution for PostgreSQL.

To use a newer `pg_tde` release, first ensure that your Percona Distribution for PostgreSQL version includes it.

This document describes upgrading the `pg_tde` extension within the same PostgreSQL major version. For PostgreSQL major version upgrades on clusters that use `pg_tde`, use [pg_tde_upgrade](/percona/command-line-tools/pg-tde-upgrade/).

## Before you start {#before-you-start}

> [!NOTE]
> `pg_tde` 2.2.0 is not compatible with Percona Distribution for PostgreSQL older than 17.10 or 18.4. Upgrade your distribution first before upgrading `pg_tde`.

> [!WARNING]
> Using `pg_upgrade` on an encrypted cluster is not supported and will result in data corruption. The server may start successfully but queries against encrypted tables will fail.

## Procedure {#procedure}

1. Take a full [backup before upgrading](/percona/how-to/backup-wal-enabled/).

2. Upgrade the `pg_tde` package via your package manager.

3. Restart the `postgresql` service.

4. Connect to each database where `pg_tde` is installed and run:

    ```sql
    ALTER EXTENSION pg_tde UPDATE;
    ```

    > [!NOTE]
    > The catalog version of `pg_tde` may not change between patch releases. You can run `ALTER EXTENSION pg_tde UPDATE` safely regardless.

5. Verify the upgrade:

```sql
SELECT extname, extversion FROM pg_extension WHERE extname = 'pg_tde';
SELECT pg_tde_version();
```
