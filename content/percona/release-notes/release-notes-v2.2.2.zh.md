---
title: pg_tde 2.2.2（2026-08-20）
linkTitle: 2.2.2
description: pg_tde 2.2.2：Vault Enterprise KMIP 支持、WAL 性能改进和归档修复。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.2.2.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 810
upstream_source: percona
---

Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

`pg_tde` 2.2.2 重点修复 WAL 加密性能问题，并增加对 HashiCorp Vault Enterprise KMIP 的支持。此前已支持通过 Vault V2 协议使用 Vault Enterprise，现在也可以使用 KMIP。

> [!WARNING]
> `pg_tde` 2.2.2 不兼容低于 17.10.2 或 18.4.2 的 Percona Distribution for PostgreSQL。

## 已知问题 {#known-issues}

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

`pg_tde` 2.2.2 引入以下变更：

### 新功能 {#new-features}

- [PG-2125](https://perconadev.atlassian.net/browse/PG-2125)：支持通过 KMIP 使用 HashiCorp Vault Enterprise。
- [PG-2473](https://perconadev.atlassian.net/browse/PG-2473)：初步支持在 Windows 上使用 Microsoft Visual C++ 构建。

### 改进 {#improvements}

- [PG-2494](https://perconadev.atlassian.net/browse/PG-2494)：改进 WAL 加密性能。

### 缺陷修复 {#bug-fixes}

- [PG-2492](https://perconadev.atlassian.net/browse/PG-2492)：修复向 `pg_tde_add_global_key_provider_kmip()` 或 `pg_tde_add_database_key_provider_kmip()` 传入空证书参数时发生的崩溃。
- [PG-2608](https://perconadev.atlassian.net/browse/PG-2608)：修复 fork 后多个进程访问同一 cURL 句柄时，Vault 密钥提供商可能出现的竞态条件。
- [PG-2609](https://perconadev.atlassian.net/browse/PG-2609)：修复 pg_wal 目录为符号链接时的 WAL 归档问题，涉及 `pg_tde_archive_decrypt` 和 `pg_tde_restore_encrypt`。
- 合入 PostgreSQL 16.15、17.11 和 18.5 的前端工具缺陷修复。
