---
title: pg_tde 2.2.0（2026-05-20）
linkTitle: 2.2.0
description: pg_tde 2.2.0：AES-256、pg_tde_upgrade、加密 I/O 优化和兼容性要求。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.2.0.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 830
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

`pg_tde` 现已支持 256 位 AES 加密，并引入简化加密集群升级的工具 [`pg_tde_upgrade`](/zh/percona/command-line-tools/pg-tde-upgrade/)。详见[变更日志](#changelog)。

> [!WARNING]
> `pg_tde` 2.2.0 不兼容低于 17.10 或 18.4 的 Percona Distribution for PostgreSQL。

### 文档更新 {#documentation-updates}

* [pg_tde 的限制](/zh/percona/index/tde-limitations/)新增与 Citus、TimescaleDB 的已知不兼容项，并澄清 `ALTER DATABASE ... SET TABLESPACE` 的行为：启用 `pg_tde` 时该命令可以使用，但受到限制。
* [启用 WAL 加密时的备份](/zh/percona/how-to/backup-wal-enabled/)更清楚地说明了备份期间的密钥轮换限制。

## 已知问题 {#known-issues}

* `pg_rewind` 和 `pg_tde_rewind`

    在使用 `pg_tde` 的集群中，对已经分叉的节点执行 `pg_rewind` 或 `pg_tde_rewind`，可能因集群间内部加密密钥不同而损坏表或索引。

    查询可能报错：

    ```bash
    ERROR: invalid page in block 0 of relation "base/..."
    ```

    这是已知问题。

    详见 [pg_tde 的限制](/zh/percona/index/tde-limitations/)。

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

`pg_tde` 2.2.0 引入以下变更：

### 新功能 {#new-features}

- [PG-1968](https://perconadev.atlassian.net/browse/PG-1968)：支持 AES-256 加密。`pg_tde` 现在支持 256 位 AES，为加密表空间提供更强的密码学保护。
- [PG-2017](https://perconadev.atlassian.net/browse/PG-2017)：`pg_tde_resetwal` 支持 AES-256，可正确处理 AES-256 加密的数据。
- [PG-2018](https://perconadev.atlassian.net/browse/PG-2018)：`pg_tde_basebackup` 完整支持 AES-256，确保使用新算法的数据库具有一致的备份和恢复行为。
- [PG-2240](https://perconadev.atlassian.net/browse/PG-2240)：引入 `pg_tde_upgrade`，自动执行升级启用了 `pg_tde` 的集群所需步骤，使升级更加方便。

### 改进 {#improvements}

- [PG-2278](https://perconadev.atlassian.net/browse/PG-2278)：存储管理器（SMGR）加密复用 OpenSSL 密码上下文，减少开销，提高加密 I/O 吞吐量。

### 缺陷修复 {#bug-fixes}

- [PG-2240](https://perconadev.atlassian.net/browse/PG-2240)：修复对包含加密数据的数据库执行 `pg_upgrade` 时失败的问题。
- [PG-1895](https://perconadev.atlassian.net/browse/PG-1895)：修复 `pg_basebackup` 期间执行 WAL 或 SMGR 密钥轮换可能导致备库无法启动的问题。
- [PG-2125](https://perconadev.atlassian.net/browse/PG-2125)：修复通过 KMIP 使用 HashiCorp Vault 时的密钥创建失败问题。
