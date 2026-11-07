---
title: pg_tde 的价值
linkTitle: TDE 的用途
description: pg_tde 为组织、DBA 和工程师提供数据保护、精细控制和集中密钥管理。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/how-tde-helps.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 150
upstream_source: percona
---

以下介绍使用 `pg_tde` 为不同用户和组织带来的益处。

## 对组织的益处 {#benefits-for-organizations}

* **数据安全：** 即使备份文件或存储设备失窃或泄露，也能防止未经授权地访问已存储的数据。
* **适用于企业的架构：** 同时支持单租户和多租户，为 SaaS 提供商或内部多用户系统提供灵活选择。

## 对 DBA 和工程师的益处 {#benefits-for-dbas-and-engineers}

* **精细控制：** 可以只加密特定表或数据库，无需加密整个系统，从而减少性能开销。
* **简化运维：** 透明运行，不需要大幅修改应用程序。
* **纵深防御：** 在 TLS（传输加密）、访问控制和基于角色的权限等现有措施之外，再增加一层保护。

结合外部密钥管理系统（KMS），`pg_tde` 支持集中控制、审计和轮换加密密钥，这些能力对于安全的生产环境至关重要。

> [!NOTE] 另请参阅
>
> 关于透明数据加密（TDE）的更多信息，见[这篇文章](https://www.percona.com/blog/transparent-data-encryption-tde/)。

[了解 pg_tde 的工作原理](/zh/percona/index/how-does-tde-work/)
