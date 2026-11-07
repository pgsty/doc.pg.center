---
title: 升级 pg_tde
linkTitle: 升级 pg_tde
description: 在同一 PostgreSQL 大版本内升级 pg_tde；大版本升级应使用 pg_tde_upgrade。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/upgrade.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 570
upstream_source: percona
---

可使用的 `pg_tde` 版本取决于 Percona Distribution for PostgreSQL 的版本。

要使用更新的 `pg_tde`，先确认你的 Percona Distribution for PostgreSQL 版本包含它。

本文介绍同一 PostgreSQL 大版本内的 `pg_tde` 扩展升级。使用 `pg_tde` 的集群要升级 PostgreSQL 大版本，应使用 [pg_tde_upgrade](/zh/percona/command-line-tools/pg-tde-upgrade/)。

## 开始之前 {#before-you-start}

> [!NOTE]
> `pg_tde` 2.2.0 不兼容低于 17.10 或 18.4 的 Percona Distribution for PostgreSQL。升级 `pg_tde` 前应先升级发行版。

> [!WARNING]
> 加密集群不支持 `pg_upgrade`，使用它会导致数据损坏。服务器可能成功启动，但查询加密表会失败。

## 操作步骤 {#procedure}

1. [升级前执行完整备份](/zh/percona/how-to/backup-wal-enabled/)。

2. 通过包管理器升级 `pg_tde` 软件包。

3. 重启 `postgresql` 服务。

4. 连接到每个安装了 `pg_tde` 的数据库，执行：

    ```sql
    ALTER EXTENSION pg_tde UPDATE;
    ```

    > [!NOTE]
    > `pg_tde` 的目录版本在补丁版本之间可能没有变化。无论是否变化，都可以安全执行 `ALTER EXTENSION pg_tde UPDATE`。

5. 验证升级：

```sql
SELECT extname, extversion FROM pg_extension WHERE extname = 'pg_tde';
SELECT pg_tde_version();
```
