---
title: 密钥管理概览
linkTitle: 选择提供商
description: 选择本地或外部密钥提供商，配置全局主密钥，并遵守备份期间禁止轮换密钥的限制。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/overview.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 310
upstream_source: percona
---

> [!NOTE] 本站勘误
> 本概览保留了早期对 Vault KMIP 的验证状态说明；2.2.2 发布说明已明确宣布支持 Vault Enterprise KMIP，具体版本状态请以对应发布说明为准。 详见[勘误记录](/zh/percona/site/errata/)。


在生产环境中，将加密密钥保存在 PostgreSQL 服务器本地可能带来安全风险。为增强安全性，`pg_tde` 通过全局密钥提供商接口支持外部密钥管理系统（KMS）。

本节介绍如何配置 `pg_tde` 使用本地和外部密钥提供商。

要让 `pg_tde` 使用外部 KMS：

1. 配置密钥提供商。
2. 设置[全局主密钥](/zh/percona/global-key-provider-configuration/set-principal-key/)。

> [!NOTE]
> **本地**或**测试环境**可以使用密钥文件，但生产部署建议集成 KMS。

> [!IMPORTANT]
> 使用 HashiCorp Vault 时，**KV v2 是推荐且受支持的集成方式**。
>
> Vault 的 KMIP 引擎尚不是经过验证的 `pg_tde` 配置，不建议用于生产部署。

> [!WARNING]
> 备份运行期间不要轮换加密密钥，否则可能造成备份不一致并导致恢复失败。这适用于所有备份工具。
>
> 将密钥轮换安排在备份窗口之外。轮换密钥后，重新执行一次完整备份。
>
> 详见 [pg_tde 的限制](/zh/percona/index/tde-limitations/#limitations-when-using-pgtde)。

`pg_tde` 已对以下密钥提供商进行测试：

| KMS 提供商 | 说明 | 文档 |
|--------------------|-------------------------------------------------------|---------------|
| **KMIP** | 标准密钥管理互操作协议。 | [配置 KMIP →](/zh/percona/global-key-provider-configuration/kmip-server/) |
| **Vault** | HashiCorp Vault 集成（KV v2 API）。 | [配置 Vault →](/zh/percona/global-key-provider-configuration/vault/) |
| **Fortanix** | Fortanix DSM 密钥管理。 | [配置 Fortanix →](/zh/percona/global-key-provider-configuration/kmip-fortanix/) |
| **Thales** | Thales CipherTrust Manager 和 DSM。 | [配置 Thales →](/zh/percona/global-key-provider-configuration/kmip-thales/) |
| **OpenBao** | Vault 的社区分支，支持 KV v2。 | [配置 OpenBao →](/zh/percona/global-key-provider-configuration/openbao/) |
| **Akeyless** | 云端秘密管理平台，用于安全存储和访问凭据及加密密钥。 | [配置 Akeyless →](/zh/percona/global-key-provider-configuration/kmip-akeyless/) |
| **Keyring 文件**（不推荐） | 仅供开发和测试使用的本地密钥文件。 | [配置 keyring 文件 →](/zh/percona/global-key-provider-configuration/keyring/) |
