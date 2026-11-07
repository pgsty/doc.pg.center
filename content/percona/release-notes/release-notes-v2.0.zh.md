---
title: 中文文档
linkTitle: 2.0.0
description: pg_tde 2.0.0：WAL 加密正式可用、历史升级限制与完整变更日志。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.0.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 870
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

### WAL 加密正式可用 {#wal-encryption-is-now-generally-available}

WAL（预写式日志）加密现已获得完整支持，可用于生产环境。该功能使用与数据加密相同的密钥基础设施，安全、透明地加密预写式日志，扩大 Percona PostgreSQL 的加密覆盖范围。

### WAL 加密升级限制 {#wal-encryption-upgrade-limitation}

在 Beta 阶段（`pg_tde` 1.0 或更早版本）启用了 WAL 加密的集群，不能升级到 `pg_tde` 2.0。以下错误表明曾启用 WAL 加密：

```sql
FATAL: principal key not configured
HINT: Use pg_tde_set_server_key_using_global_key_provider() to configure one.
```

Beta 阶段未使用 WAL 加密的集群可以正常升级。

### 文档更新 {#documentation-updates}

* 更新[限制](/zh/percona/index/tde-limitations/)，包含 WAL 加密限制及支持和不支持的工具。
* [PG-1858](https://perconadev.atlassian.net/browse/PG-1858)：新增[启用 WAL 加密时的备份](/zh/percona/how-to/backup-wal-enabled/)，包括恢复这类备份的方法。
* [PG-1832](https://perconadev.atlassian.net/browse/PG-1858)：增加 `pg_tde_archive_decrypt` 和 `pg_tde_restore_encrypt` 的文档，在[命令行工具](/zh/percona/command-line-tools/cli-tools/)中介绍如何安全归档和恢复加密 WAL 段。
* [PG-1740](https://perconadev.atlassian.net/browse/PG-1740)：更新启用 WAL 加密时[卸载 pg_tde](/zh/percona/how-to/uninstall/) 的说明，并补充 TDE 已关闭但 WAL 加密仍然启用的情况。

## 已知问题 {#known-issues}

* 在 `pg_basebackup` 运行期间创建、修改或轮换全局密钥提供商（或其密钥），可能导致从备份初始化的备库或独立集群在 WAL 重放时失败，还可能损坏加密数据（表、索引及其他关系）。

    不要在备份窗口内执行这些操作。完成密钥轮换或提供商更新后，重新执行完整备份。

* 使用 `--wal-method=fetch` 运行 `pg_basebackup` 会产生警告。

    这是预期行为，将在后续版本处理。

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

### 新功能 {#new-features}

* [PG-1497](https://perconadev.atlassian.net/browse/PG-1497)：WAL 加密正式可用（GA）。
* [PG-1037](https://perconadev.atlassian.net/browse/PG-1037)：`pg_rewind` 支持加密 WAL。
* [PG-1411](https://perconadev.atlassian.net/browse/PG-1497)：`pg_resetwal` 支持加密 WAL。
* [PG-1603](https://perconadev.atlassian.net/browse/PG-1603)：`pg_basebackup` 支持加密 WAL。
* [PG-1710](https://perconadev.atlassian.net/browse/PG-1710)：支持加密 WAL 的归档。
* [PG-1711](https://perconadev.atlassian.net/browse/PG-1711)：支持加密 WAL 的增量备份，已验证与 `pg_combinebackup` 和 WAL 汇总工具的兼容性。
* [PG-1712](https://perconadev.atlassian.net/browse/PG-1712)：`pg_createsubscriber` 支持加密 WAL。
* [PG-1833](https://perconadev.atlassian.net/browse/PG-1833)：增加经验证的 `pg_waldump` 加密 WAL 支持。
* [PG-1834](https://perconadev.atlassian.net/browse/PG-1834)：验证 `pg_upgrade` 与加密的兼容性。

### 改进 {#improvements}

* [PG-1661](https://perconadev.atlassian.net/browse/PG-1661)：验证从提供商获取的密钥材料。
* [PG-1667](https://perconadev.atlassian.net/browse/PG-1667)：验证 Vault keyring 引擎类型。

### 缺陷修复 {#bugs-fixed}

* [PG-1391](https://perconadev.atlassian.net/browse/PG-1391)：修复使用加密密钥的副本上检查点段未加密的问题。
* [PG-1412](https://perconadev.atlassian.net/browse/PG-1412)：修复 PITR 和 `pg_rewind` 期间 `XLogFileCopy` 处理加密 WAL 失败的问题。
* [PG-1452](https://perconadev.atlassian.net/browse/PG-1452)：修复即使设置了 `PGDATA`，未提供 `-D` 时 `pg_tde_change_key_provider` 仍无法运行的问题。
* [PG-1485](https://perconadev.atlassian.net/browse/PG-1485)：修复启用 `wal_encryption` 时，流复制因 WAL magic number 无效而失败的问题。
* [PG-1604](https://perconadev.atlassian.net/browse/PG-1604)：修复备库提升时，重放 WAL 中的两阶段事务因 magic number 无效而崩溃的问题。
* [PG-1658](https://perconadev.atlassian.net/browse/PG-1658)：修复服务器重启后无法删除全局密钥提供商的问题。
* [PG-1835](https://perconadev.atlassian.net/browse/PG-1835)：修复 `pg_resetwal` 损坏加密 WAL，导致 PostgreSQL 启动时检查点无效的问题。
* [PG-1842](https://perconadev.atlassian.net/browse/PG-1842)：修复流复制环境中含加密表的副本启动延迟问题。
* [PG-1843](https://perconadev.atlassian.net/browse/PG-1843)：修复创建加密表时的性能问题。
* [PG-1863](https://perconadev.atlassian.net/browse/PG-1863)：修复创建临时表时生成不必要 WAL 的问题。
* [PG-1866](https://perconadev.atlassian.net/browse/PG-1866)：修复启用 WAL 加密时，崩溃后自动重启偶尔失败的问题。
* [PG-1867](https://perconadev.atlassian.net/browse/PG-1867)：修复加密 WAL 的归档恢复。
