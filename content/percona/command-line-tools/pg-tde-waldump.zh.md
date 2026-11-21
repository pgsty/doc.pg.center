---
title: pg_tde_waldump
linkTitle: 查看 WAL
description: 通过指定 WAL keyring 路径，使用 pg_tde_waldump 查看加密 WAL。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/command-line-tools/pg-tde-waldump.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 760
upstream_source: percona-20261121
---

[`pg_tde_waldump`](https://www.postgresql.org/docs/current/pgwaldump.html) 以便于阅读的格式显示 PostgreSQL 数据库集群的预写式日志（WAL）。

为读取加密 WAL 记录，`pg_tde_waldump` 提供以下额外选项：

* `-k, --keyring-path=PATH`：包含 WAL keyring 配置文件的目录路径，通常是 PostgreSQL 数据目录内的 `pg_tde/` 目录，其中包括：
    * `wal_keys`
    * `1664_providers`

> [!NOTE]
> 不指定 `--keyring-path`，`pg_tde_waldump` 就无法读取加密 WAL。

从 [pg_tde 2.3.0](/zh/percona/release-notes/release-notes-v2.3.0/) 开始，`pg_tde_waldump` 能够识别 `pg_tde` 自定义资源管理器，正确输出其 WAL 记录，并允许在 `--rmgr` 过滤器中指定它。
