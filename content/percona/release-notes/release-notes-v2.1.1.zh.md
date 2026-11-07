---
title: pg_tde 2.1.1（2026-01-22）
linkTitle: 2.1.1
description: pg_tde 2.1.1：HashiCorp Vault 命名空间集成和密钥配置文档更新。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.1.1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 850
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

### 集成 HashiCorp Vault 命名空间 {#integrated-hashicorp-vault-namespace}

通过 `pg_tde_add_global_key_provider_vault_v2` 参数，将 HashiCorp Vault 命名空间集成到 `pg_tde`。

### 文档更新 {#documentation-updates}

更新[全局主密钥配置](/zh/percona/global-key-provider-configuration/set-principal-key/)与[配置 WAL 加密](/zh/percona/wal-encryption/)章节的安装步骤，移除过时的 KMS 配置信息。

## 已知问题 {#known-issues}

* 在 `pg_tde_basebackup` 运行期间创建、修改或轮换全局密钥提供商（或其密钥），可能导致从备份初始化的备库或独立集群在 WAL 重放时失败，还可能损坏加密数据（表、索引及其他关系）。

    不要在备份窗口内执行这些操作。完成密钥轮换或提供商更新后，重新执行完整备份。

* 使用 `--wal-method=fetch` 运行 `pg_tde_basebackup` 会产生警告。

    这是预期行为，将在后续版本处理。

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

### 新功能 {#new-features}

* [PG-1959](https://perconadev.atlassian.net/browse/PG-1959)：将 HashiCorp Vault 命名空间集成到 `pg_tde`。
