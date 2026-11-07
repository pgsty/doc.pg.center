---
title: pg_tde_upgrade
linkTitle: Major upgrade
description: Upgrade PostgreSQL data directories that contain pg_tde-encrypted relations.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-upgrade.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 770
upstream_source: percona
---

`pg_tde_upgrade` is the supported method for performing PostgreSQL major version upgrades on clusters that use `pg_tde`.

Use this tool instead of `pg_upgrade` whenever the cluster uses `pg_tde`, including clusters with encrypted tables or encrypted WAL.

`pg_tde_upgrade` wraps [`pg_upgrade` ](https://www.postgresql.org/docs/current/pgupgrade.html) to simplify upgrading clusters with encrypted relations or WAL. It can also be run safely on clusters without `pg_tde` enabled.

## When to use which upgrade procedure {#when-to-use-which-upgrade-procedure}

| Scenario | Procedure |
|-----------|-----------|
| Upgrade Percona PostgreSQL from one major version to another (for example from 17 to 18) on a cluster that uses `pg_tde` | Use this `pg_tde_upgrade` procedure |
| Upgrade the `pg_tde` extension or package version within the same PostgreSQL major version | Follow the `pg_tde` [upgrade procedure](/percona/how-to/upgrade/) |
| Upgrade PostgreSQL from one major version to another on a cluster that does not use `pg_tde` | Use `pg_upgrade` and follow the [major upgrade procedure](https://docs.percona.com/postgresql/18/major-upgrade.html) |
| Upgrade Percona PostgreSQL to a newer minor version within the same major version (for example from 18.3 to 18.4) | Follow the [minor upgrade procedure ](https://docs.percona.com/postgresql/18/minor-upgrade.html) |

## Implementation {#implementation}

`pg_tde_upgrade` copies the `pg_tde` subdirectory from the old data directory to the new data directory and then runs `pg_upgrade` as normal except for using `pg_tde_resetwal` instead of `pg_resetwal`.

> [!NOTE]
> Ensure that `pg_tde` is included in `shared_preload_libraries` and that you have the right setting for [`pg_tde.wal_encrypt`](/percona/variables/#pgtde-walencrypt) in the new cluster.

## Usage {#usage}

Use `pg_tde_upgrade` in place of `pg_upgrade` when performing a PostgreSQL major version upgrade on a cluster that uses `pg_tde`.

`pg_tde_upgrade` accepts the same command-line arguments as `pg_upgrade`.

Example:

```bash
pg_tde_upgrade \
  --old-bindir ... \
  --new-bindir ... \
  --old-datadir ... \
  --new-datadir ...
```

For more information on how to perform the upgrade for minor versions, see [Minor Upgrade of Percona Distribution for PostgreSQL ](https://docs.percona.com/postgresql/18/minor-upgrade.html?h=pg_tde#before-you-start).

For more information on how to perform the upgrade for the `pg_tde` package version, see [Upgrade pg_tde](/percona/how-to/upgrade/).
