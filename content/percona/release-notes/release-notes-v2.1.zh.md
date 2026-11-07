---
title: pg_tde 2.1.0（2025-11-28）
linkTitle: 2.1.0
description: pg_tde 2.1.0：PostgreSQL 18.1、AIO、独立打包、专用工具和命名空间支持。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 860
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

### 支持 PostgreSQL 18.1 {#added-support-for-postgresql-18-1}

`pg_tde` 完整支持 Postgres 18.1。

### PostgreSQL 18 的打包变更 {#packaging-changes-for-postgresql-18}

从 PostgreSQL 18 开始，RPM 和 DEB 安装中的 `pg_tde` 以**独立软件包**发布。

它不再包含于 PostgreSQL 服务器主软件包中。

如果 PostgreSQL 18 部署使用 `pg_tde`，必须单独安装与之匹配的软件包。

Percona PostgreSQL **Docker 镜像仍然默认包含 `pg_tde`**，容器部署无需额外操作。

各 PostgreSQL 版本的提供方式见[安装 pg_tde](/zh/percona/install/)。

### 支持 AIO {#added-support-for-aio}

增加**异步 I/O（AIO）**支持，它现在是默认 I/O 机制。

### 支持 Vault Enterprise 和 OpenBao 命名空间 {#added-namespace-support-for-vault-enterprise-and-openbao}

增加 HashiCorp Vault 和 OpenBao 命名空间支持。[添加或修改 Vault 提供商](/zh/percona/functions/#add-or-modify-vault-providers)现已记录并完整支持 `namespace` 参数。

### 拆分仓库以支持多个 PostgreSQL 版本 {#repository-split-for-multi-version-postgresql-support}

将项目重组为多仓库结构，以更高效地支持多个 PostgreSQL 版本。

### 工具变更 {#tooling-changes}

标准 PostgreSQL 命令行工具不再能够操作由 `pg_tde` 加密的集群。为安全管理加密数据，应使用 Percona 提供的对应 `pg_tde_` 工具：

* pg_basebackup → pg_tde_basebackup
* pg_checksums → pg_tde_checksums
* pg_resetwal → pg_tde_resetwal
* pg_rewind → pg_tde_rewind
* pg_waldump → pg_tde_waldump

> [!WARNING]
>
> 非 pg_tde_* 版本无法用于加密集群，使用时可能报错。处理启用了 TDE 的数据时，始终使用 `pg_tde_` 版本。

### 增加 Akeyless 支持 {#added-akeyless-support}

`pg_tde` 现在通过 KMIP 协议兼容 Akeyless CipherTrust Manager。详见[密钥管理概览](/zh/percona/global-key-provider-configuration/overview/)。

### 支持 Vault 和 OpenBao 的命名空间 {#added-support-for-vault-and-openbao-namespaces}

实现 Vault Enterprise 和 OpenBao 的 "namespace" 功能，可通过命令行使用，也可以在 HTTP 接口中通过 `X-Vault-Namespace` 请求头使用。

### 文档更新 {#documentation-updates}

- 新增 [Akeyless](/zh/percona/global-key-provider-configuration/kmip-akeyless/) 文档。
- 新增 [pg_tde 对数据库操作的影响](/zh/percona/index/what-tde-impacts/)，概述与 PostgreSQL 核心操作的关系。
- 更新 [FAQ](/zh/percona/faq/)，说明逻辑复制是否让订阅端数据保持加密。
- 更新[安装 pg_tde](/zh/percona/install/)，增加不同 PostgreSQL 版本提供方式的表格。
- 更新[添加或修改 Vault 提供商](/zh/percona/functions/#add-or-modify-vault-providers)，增加 `namespace` 参数。

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
