---
title: 技术参考概览
linkTitle: 参考概览
description: pg_tde 的使用参考、SQL 函数、GUC 参数和流复制配置入口。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/advanced-topics/tech-reference.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 610
upstream_source: percona
---

本节介绍支撑 `pg_tde` 的内部组件和工具。

可以通过本节了解加密实现方式、调整配置，并使用高级命令行工具和函数完成诊断与定制。

### 使用参考 {#usage-reference}

介绍 `pg_tde` 的主要操作，包括配置密钥提供商、管理主密钥、设置权限和加密表。

[阅读使用指南](/zh/percona/advanced-topics/usage-guide/)

### 函数 {#functions}

使用内置函数管理密钥提供商、创建和轮换主密钥、验证加密状态。涵盖 Vault、KMIP、本地提供商的命令，以及查询和验证密钥的工具函数。

[浏览可用函数 →](/zh/percona/functions/)

### GUC 参数 {#guc-variables}

配置 `pg_tde` 在 PostgreSQL 中的行为：控制 WAL 加密、强制新表加密，以及管理全局提供商继承。包含作用域、默认值和权限要求。

[配置 GUC 参数](/zh/percona/variables/)

### 流复制 {#streaming-replication}

了解如何通过 `tde_heap` 访问方法配置使用 `pg_tde` 的 PostgreSQL 流复制，涵盖主库和备库配置、密钥管理要求和验证步骤。

[配置 tde_heap 流复制](/zh/percona/replication/)
