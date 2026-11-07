---
title: 支持的 PostgreSQL 部署
linkTitle: 支持的版本
description: 正式支持的 Percona PostgreSQL 版本与 PostgreSQL 16 技术预览的适用范围。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/supported-versions.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 190
upstream_source: percona
---

`pg_tde` 扩展可用于 Percona Server for PostgreSQL [17.5](https://docs.percona.com/postgresql/17/) 及后续版本。Percona Server for PostgreSQL 是 PostgreSQL 社区版的开源兼容替代品。这些版本提供 `tde_heap` 访问方法，具备完整加密能力，包括表、索引和 WAL 数据加密。

需要在 PostgreSQL 16 上使用 `pg_tde` 的用户可以使用[技术预览版本](https://docs.percona.com/postgresql/16/percona-ext.html#tech-preview-pg_tde-built-into-percona-server-for-postgresql-16)。该版本不受正式支持，不建议用于生产环境，发布节奏也不同于受支持的 PostgreSQL [17.5](https://docs.percona.com/postgresql/17/) 及后续版本。

该扩展与 Percona Server for PostgreSQL 紧密集成，提供社区版构建不具备的增强加密功能。

## 为什么选择 Percona Server for PostgreSQL？ {#why-choose-percona-server-for-postgresql}

使用 Percona 的 PostgreSQL 发行版可以获得：

- 通过 `tde_heap` 访问方法提供的**完整加密支持**，涵盖表、索引和 WAL 数据。
- 社区版构建不具备的**性能改进和企业功能**。
- 由 Percona 专家支持团队提供保障的**定期更新和安全补丁**。
- 面向安全 PostgreSQL 部署的**专业支持**与指导。

> [!NOTE]
> 早期或功能受限的 `pg_tde` 版本（例如 `tde_heap_basic`）已被弃用。

如果还不确定哪种部署适合你的需求，可以[联系 Percona 专家](https://www.percona.com/about/contact)，为你的环境选择合适的方案。

[开始安装](/zh/percona/install/)
