---
title: Impact of pg_tde on database operations
linkTitle: Operational impact
description: What changes for applications, database operations, performance, and upgrades.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/index/what-tde-impacts.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 180
upstream_source: percona-20261121
---

This page summarizes how `pg_tde` interacts with core PostgreSQL operations.

| Area | Affected | Notes / Actions |
|------|-----------|-----------------|
| **Backups** | ❌ Yes | Encrypted backups require `pg_tde`-aware tools. See [Backup with WAL encryption](/percona/how-to/backup-wal-enabled/). |
| **Restore** | ❌ Yes | Restored data remains encrypted; `pg_tde` transparently handles decryption. See [Restore encrypted backups](/percona/how-to/restore-backups/). |
| **Streaming replication** | ⚠️ Partial | Replicas must load the `pg_tde` shared library (shared_preload_libraries = 'pg_tde'). Without it, the replica will fail on operations involving `tde_heap`. |
| **Logical replication** | ✅ No | Not affected. |
| **Monitoring and statistics** | ✅ No | Not affected, including `pg_stat_monitor`. |
| **Performance** | ⚠️ Slight | Minor CPU overhead due to enabling encryption, most noticeable on random write workloads. |
