---
title: pg_tde_upgrade
linkTitle: 大版本升级
description: 使用 pg_tde_upgrade 安全升级加密集群的 PostgreSQL 大版本。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-upgrade.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 770
upstream_source: percona
---

`pg_tde_upgrade` 是为使用 `pg_tde` 的集群执行 PostgreSQL 大版本升级的受支持方法。

只要集群使用了 `pg_tde`（包括加密表或加密 WAL），就应使用此工具替代 `pg_upgrade`。

`pg_tde_upgrade` 包装了 [`pg_upgrade`](https://www.postgresql.org/docs/current/pgupgrade.html)，简化包含加密关系或 WAL 的集群升级。它也可以安全地用于未启用 `pg_tde` 的集群。

## 如何选择升级方法 {#when-to-use-which-upgrade-procedure}

| 场景 | 方法 |
|-----------|-----------|
| 使用 `pg_tde` 的集群将 Percona PostgreSQL 从一个大版本升级到另一个，例如 17 升级到 18 | 使用本文的 `pg_tde_upgrade` 流程 |
| 在同一 PostgreSQL 大版本内升级 `pg_tde` 扩展或软件包 | 按照 [pg_tde 升级流程](/zh/percona/how-to/upgrade/)操作 |
| 未使用 `pg_tde` 的集群升级 PostgreSQL 大版本 | 使用 `pg_upgrade`，按照[大版本升级流程](https://docs.percona.com/postgresql/18/major-upgrade.html)操作 |
| 同一大版本内升级 Percona PostgreSQL 小版本，例如 18.3 升级到 18.4 | 按照[小版本升级流程](https://docs.percona.com/postgresql/18/minor-upgrade.html)操作 |

## 实现方式 {#implementation}

`pg_tde_upgrade` 将旧数据目录的 `pg_tde` 子目录复制到新数据目录，然后正常运行 `pg_upgrade`，但使用 `pg_tde_resetwal` 替代 `pg_resetwal`。

> [!NOTE]
> 确保新集群的 `shared_preload_libraries` 包含 `pg_tde`，并正确设置 [`pg_tde.wal_encrypt`](/zh/percona/variables/#pgtde-walencrypt)。

## 用法 {#usage}

对使用 `pg_tde` 的集群执行 PostgreSQL 大版本升级时，以 `pg_tde_upgrade` 替代 `pg_upgrade`。

`pg_tde_upgrade` 接受与 `pg_upgrade` 相同的命令行参数。

示例：

```bash
pg_tde_upgrade \
  --old-bindir ... \
  --new-bindir ... \
  --old-datadir ... \
  --new-datadir ...
```

小版本升级详见 [Percona Distribution for PostgreSQL 小版本升级](https://docs.percona.com/postgresql/18/minor-upgrade.html?h=pg_tde#before-you-start)。

`pg_tde` 软件包升级详见[升级 pg_tde](/zh/percona/how-to/upgrade/)。
