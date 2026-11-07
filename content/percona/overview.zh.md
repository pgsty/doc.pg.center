---
title: pg_tde 文档
linkTitle: 项目介绍
description: Percona PostgreSQL 透明数据加密：安装、功能、架构与最新发布说明。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 110
upstream_source: percona
---

Percona Transparent Data Encryption for PostgreSQL（`pg_tde`）是一个开源、由社区驱动且面向长期发展的 PostgreSQL 扩展，通过透明数据加密（TDE）保护静态数据。`pg_tde` 确保磁盘上的数据以加密形式存储；即使有人取得物理存储介质，没有相应的加密密钥也无法读取数据。

`pg_tde` 是 Percona Server for PostgreSQL 的组成部分，需要其补丁才能工作。它随 Percona Distribution for PostgreSQL 17+ 提供，以确保兼容性和正常运行。详见 [Percona Distribution for PostgreSQL 18 文档](https://docs.percona.com/postgresql/18/)。

### 安装指南 {#installation-guide}

按照分步安装说明快速开始。

[安装 `pg_tde`](/zh/percona/install/)

### 功能 {#rocket-features}

了解 Percona 的 `pg_tde` 扩展为 PostgreSQL 提供哪些功能。

[查看 `pg_tde` 的功能](/zh/percona/features/)

### 架构 {#architecture}

了解 `pg_tde` 如何通过 Percona 的架构集成到 PostgreSQL，以及密钥管理、加密应用方式和兼顾性能与安全的设计。

[了解 `pg_tde` 的内部机制](/zh/percona/architecture/overview/)

### 最新动态 {#loudspeaker-what-s-new}

了解 `pg_tde` 的版本发布和变更。

[查看最新版本的变更](/zh/percona/release-notes/release-notes-v2.2.2/)
