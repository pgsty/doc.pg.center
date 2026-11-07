---
title: pg_tde 1.0.0（2025-06-30）
linkTitle: 1.0.0
description: pg_tde 1.0.0：关系数据加密正式可用，WAL 加密仍为 Beta，不兼容此前版本。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v1.0.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 880
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

* **pg_tde 1.0 正式可用（GA）**

使用[透明数据加密（TDE）](/zh/percona/index/about-tde/)加密 PostgreSQL 关系数据的能力已达到**稳定**状态，为 PostgreSQL 工作负载提供生产级数据保护。

* **WAL 加密仍处于 Beta 阶段**

WAL 加密当时仍为 Beta，必须显式启用才生效。**尚不适合生产环境，请勿在生产环境启用。**

## 升级注意事项 {#upgrade-considerations}

由于代码发生重大变化，`pg_tde` 1.0 **不向后兼容** RC2 等旧版本，**不能**直接升级，必须**全新安装** `pg_tde`。

## 已知问题 {#known-issues}

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

### 新功能 {#new-features}

- [PG-1257](https://perconadev.atlassian.net/browse/PG-1257)：增加移除当前主密钥的 SQL 函数。

### 改进 {#improvements}

- [PG-1617](https://perconadev.atlassian.net/browse/PG-1617)：移除关系密钥缓存。
- [PG-1635](https://perconadev.atlassian.net/browse/PG-1635)：面向用户的 TDE 函数现在返回 void。
- [PG-1605](https://perconadev.atlassian.net/browse/PG-1605)：移除 `pg_tde_grant_database_key_management_to_role()` 中未声明的依赖。

### 缺陷修复 {#bugs-fixed}

- [PG-1581](https://perconadev.atlassian.net/browse/PG-1581)：修复重启后 KMIP 密钥不可用时，访问表导致 PostgreSQL 崩溃的问题。
- [PG-1583](https://perconadev.atlassian.net/browse/PG-1583)：修复修改 keyring 文件后，通过 CASCADE 删除 `pg_tde` 扩展导致崩溃的问题。
- [PG-1585](https://perconadev.atlassian.net/browse/PG-1585)：修复服务器使用新令牌重启后，重新添加 Vault 提供商失败的问题。
- [PG-1592](https://perconadev.atlassian.net/browse/PG-1592)：改进服务器密钥尚未创建时请求其信息的错误日志。
- [PG-1593](https://perconadev.atlassian.net/browse/PG-1593)：修复创建提供商时接受无效 Vault 令牌所导致的运行时失败。
- [PG-1600](https://perconadev.atlassian.net/browse/PG-1600)：修复提供商不可用时删除表导致 Postmaster 错误的问题。
- [PG-1606](https://perconadev.atlassian.net/browse/PG-1606)：修复角色授权函数缺少超级用户检查而产生误导性错误的问题。
- [PG-1607](https://perconadev.atlassian.net/browse/PG-1607)：改进 CA 参数顺序和相关文档，使含义更清楚。
- [PG-1608](https://perconadev.atlassian.net/browse/PG-1608)：更新并修正文档中的全局密钥配置参数。
- [PG-1613](https://perconadev.atlassian.net/browse/PG-1613)：测试并改进 `pg_tde_change_key_provider` 命令行工具。
- [PG-1637](https://perconadev.atlassian.net/browse/PG-1637)：修复密钥文件中的未使用密钥在 OID 回卷后引发问题。
- [PG-1651](https://perconadev.atlassian.net/browse/PG-1651)：修复命令行工具处理 Vault 密钥导入导出的问题。
- [PG-1652](https://perconadev.atlassian.net/browse/PG-1652)：修复通过命令行修改提供商后服务器找不到加密密钥的问题。
- [PG-1662](https://perconadev.atlassian.net/browse/PG-1662)：修复修改分区表时生成不一致加密状态的问题。
- [PG-1663](https://perconadev.atlassian.net/browse/PG-1663)：修复分区表上的索引未加密的问题。
- [PG-1700](https://perconadev.atlassian.net/browse/PG-1700)：修复主密钥缺失时的错误提示。
