---
title: 架构概览
linkTitle: 架构概览
description: pg_tde 的可定制加密模型、服务器内核改动、扩展与 keyring API。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/architecture/overview.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 410
upstream_source: percona
---

`pg_tde` 是一个**可定制、完整的静态数据加密扩展**。“扩展”指 `pg_tde` 以 PostgreSQL 扩展的形式交付。

> [!NOTE]
> `pg_tde` 依赖 PostgreSQL 内核中为提高可扩展性而做的改动。目前，它只能运行在包含这些改动的 [Percona Server for PostgreSQL](https://docs.percona.com/postgresql/17/index.html) 上。

以下介绍这一设计的主要架构组成。

**a. 可定制**，意味着 `pg_tde` 支持多种使用场景：

* 加密所有数据库中的全部表，或只加密选定的表。
* 将加密密钥保存在不同的外部密钥存储服务器中，列表见[密钥管理概览](/zh/percona/global-key-provider-configuration/overview/)。
* 为集群使用一个密钥，或为不同集群使用不同密钥。
* 将全部密钥集中在一个提供商中，或分散到多个提供商。
* 控制权限：谁可以管理密钥，谁可以创建加密或未加密的表。

**b. 完整**，意味着 `pg_tde` 的目标是加密静态数据。

**c. 静态数据**，指写入磁盘的所有内容，包括：

* 表数据文件
* 索引
* 序列
* 临时表
* 预写式日志（WAL）

## 主要组件 {#main-components}

`pg_tde` 的主要组件包括：

* **服务器内核改动**主要用于提高服务器的可扩展性，让 `pg_tde` 的主要逻辑能够作为扩展独立存在。内核改动还为部分需要直接操作加密表或加密 WAL 文件的命令行工具增加了加密支持。

    源码见[这里](https://github.com/percona/postgres/tree/release-2.2.2)。

* **`pg_tde` 扩展**通过接入内核改动引入的扩展点，以及 PostgreSQL 服务器已有的扩展点，实现加密逻辑。

    与其他扩展类似，所有行为都可以通过 GUC 参数和 SQL 语句控制。

* **Keyring API 和库**通过不同密钥提供商实现密钥存储逻辑。API 仅供内部使用；keyring 库目前属于主代码库，未来可能拆分为共享库。
