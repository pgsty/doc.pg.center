---
title: pg_tde 对数据库操作的影响
linkTitle: 运维影响
description: pg_tde 对备份、恢复、流复制、逻辑复制、监控和性能的影响。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/what-tde-impacts.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 180
upstream_source: percona
---

本页概述 `pg_tde` 与 PostgreSQL 核心操作的关系。

| 领域 | 是否受影响 | 说明与操作 |
|------|-----------|-----------------|
| **备份** | 是 | 加密备份需要支持 `pg_tde` 的工具。见[启用 WAL 加密时的备份](/zh/percona/how-to/backup-wal-enabled/)。 |
| **恢复** | 是 | 恢复后的数据仍然加密，`pg_tde` 透明地处理解密。见[恢复加密备份](/zh/percona/how-to/restore-backups/)。 |
| **流复制** | 部分 | 副本必须加载 `pg_tde` 共享库（shared_preload_libraries = 'pg_tde'）。否则，涉及 `tde_heap` 的操作会在副本上失败。 |
| **逻辑复制** | 否 | 不受影响。 |
| **监控与统计** | 否 | 不受影响，包括 `pg_stat_monitor`。 |
| **性能** | 轻微 | 启用加密会带来少量 CPU 开销，在随机写入负载中最明显。 |
