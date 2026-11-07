---
title: pg_tde_waldump
linkTitle: 查看 WAL
description: 通过指定 WAL keyring 路径，使用 pg_tde_waldump 查看加密 WAL。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-waldump.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 760
upstream_source: percona
---

[`pg_tde_waldump`](https://www.postgresql.org/docs/current/pgwaldump.html) 以便于阅读的格式显示 PostgreSQL 数据库集群的预写式日志（WAL）。

为读取加密 WAL 记录，`pg_tde_waldump` 提供以下额外选项：

* `-k, --keyring-path=PATH`：包含 WAL keyring 配置文件的目录路径，通常是 PostgreSQL 数据目录内的 `pg_tde/` 目录，其中包括：
    * `wal_keys`
    * `1664_providers`

> [!NOTE]
> 不指定 `--keyring-path`，`pg_tde_waldump` 就无法读取加密 WAL。
