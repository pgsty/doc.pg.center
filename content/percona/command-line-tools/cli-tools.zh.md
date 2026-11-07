---
title: pg_tde 命令行工具概览
linkTitle: 工具概览
description: 用于加密集群的 pg_tde 归档、恢复、备份、校验、WAL 和升级工具。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/cli-tools.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 710
upstream_source: percona
---

`pg_tde` 扩展提供一组专门处理加密数据和集群的命令行工具。它们与标准 PostgreSQL 工具并存，但操作由 `pg_tde` 加密的数据时，**必须**使用这些工具。

> [!NOTE]
> 标准 PostgreSQL 工具无法操作 `pg_tde` 加密的 WAL 或表。

## 新增的 pg_tde 专用工具 {#new-pgtde-specific-tools}

以下工具由 `pg_tde` 专门引入，用于支持密钥轮换和 WAL 加密流程：

* [pg_tde_change_key_provider](/zh/percona/command-line-tools/pg-tde-change-key-provider/)：修改数据库的加密密钥提供商。
* [pg_tde_archive_decrypt](/zh/percona/command-line-tools/pg-tde-archive-decrypt/)：归档前解密 WAL。
* [pg_tde_restore_encrypt](/zh/percona/command-line-tools/pg-tde-restore-encrypt/)：自定义恢复命令，确保恢复的 WAL 处于加密状态。

## 处理 pg_tde 加密数据的工具 {#tools-for-working-with-pgtde-encrypted-data}

以下工具是在标准 PostgreSQL 工具基础上增加 `pg_tde` 支持的版本。处理加密 WAL 或表时，必须使用 `pg_tde_*` 版本：

* [pg_tde_checksums](/zh/percona/command-line-tools/pg-tde-checksums/)：验证数据校验和。
* [pg_tde_waldump](/zh/percona/command-line-tools/pg-tde-waldump/)：查看并解密 WAL 文件。
* [pg_tde_basebackup](/zh/percona/how-to/backup-wal-enabled/)：创建包含加密数据的基础备份。
* pg_tde_resetwal：为使用 `pg_tde` 的集群重置 WAL。
* pg_tde_rewind：回退使用加密 WAL 的集群。
* [pg_tde_upgrade](/zh/percona/command-line-tools/pg-tde-upgrade/)：为使用 `pg_tde` 的集群执行大版本升级。
