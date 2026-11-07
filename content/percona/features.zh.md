---
title: 功能
linkTitle: 功能
description: pg_tde 的表加密、单租户与多租户、表级控制和密钥管理功能。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/features.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 120
upstream_source: percona
---

`pg_tde` 可用于 [Percona Server for PostgreSQL](https://docs.percona.com/postgresql/17/)。Percona Server for PostgreSQL 提供扩展的存储管理器 API，允许集成自定义存储管理器。

该扩展提供以下功能：

* [表加密](/zh/percona/test/#encrypt-data-in-a-new-table)，包括：
    * 数据表
    * 加密表的索引数据
    * TOAST 表
    * 临时表

> [!NOTE]
> 这些表的元数据不加密。

* 通过[全局 keyring 提供商](/zh/percona/global-key-provider-configuration/set-principal-key/)支持单租户
* [多租户支持](/zh/percona/how-to/multi-tenant-setup/)
* 表级粒度的加密和访问控制
* 多种[密钥管理选项](/zh/percona/global-key-provider-configuration/overview/)

## 下一步 {#next-steps}

进一步了解 `pg_tde` 如何实现透明数据加密：

[关于透明数据加密](/zh/percona/index/about-tde/)
