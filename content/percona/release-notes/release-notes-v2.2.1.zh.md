---
title: pg_tde 2.2.1（2026-07-06）
linkTitle: 2.2.1
description: pg_tde 2.2.1：PostgreSQL 16 支持、pg_rewind 与基础备份修复、转向 Meson。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.2.1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 820
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

`pg_tde` 2.2.1 重点改进稳定性与兼容性，提高 `pg_rewind` 的可靠性。详见[变更日志](#changelog)。

> [!WARNING]
> `pg_tde` 2.2.1 不兼容低于 17.10.2 或 18.4.2 的 Percona Distribution for PostgreSQL。

## 已知问题 {#known-issues}

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

`pg_tde` 2.2.1 引入以下变更：

### 新功能 {#new-features}

- [PG-2398](https://perconadev.atlassian.net/browse/PG-2398)：支持 PostgreSQL 16。

### 缺陷修复 {#bug-fixes}

- [PG-2407](https://perconadev.atlassian.net/browse/PG-2407)：修复影响 `pg_tde` 集群中 `pg_rewind` 的多个问题，提高回退与恢复操作的可靠性。
- [PG-2258](https://perconadev.atlassian.net/browse/PG-2258)：修复 `pg_tde_basebackup` 报出 "could not find server principal key" 的问题。

### 变更 {#changes}

- 移除使用 `make` 构建 `pg_tde` 的支持，现在只能使用 Meson 构建。
