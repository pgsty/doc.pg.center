---
title: 宣布 Babelfish for PostgreSQL 开源：加速 SQL Server 迁移
description: 项目正式开源：T-SQL、TDS 支持与 Compass 兼容性评估工具。
date: '2021-10-28'
weight: 10
type: docs
author: The Babelfish Project Team
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_posts/2021-10-28-babelfish-launch.markdown
upstream_ref: main @ f468c5ed3d38
linkTitle: Babelfish 开源发布
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 历史公告
> 本文保留原始发布日期、作者及版本语境。中文翻译：PGSTY 文档项目。

可扩展性是 PostgreSQL 区别于其他数据库的一大特点。在本文发布时，[PostgreSQL Extension Network](https://pgxn.org/about/) 已登记 329 个开源扩展，涵盖地理空间数据、计算生物学、统计、作业调度、图数据库等功能。

今天，我们发布开源的 Babelfish for PostgreSQL（简称 Babelfish），让 PostgreSQL 能够理解原本为 Microsoft SQL Server 编写的应用查询。Babelfish 是一组扩展，为 PostgreSQL 增加 T-SQL 能力和表格数据流（TDS）监听端口，支持 SQL Server 的 T-SQL 方言，以及保存点、存储过程、嵌套事务等功能。

Babelfish 基于现有 PostgreSQL 构建，采用 Apache 2.0 和 PostgreSQL 开源许可证。按照这些许可证，可以自由使用、修改、分发和销售包含相应许可软件的产品。

在 re:Invent 2020 上，我们[宣布](https://aws.amazon.com/blogs/opensource/want-more-postgresql-you-just-might-like-babelfish/)计划将 Babelfish 开源。今天兑现这一承诺，将代码发布到 GitHub。Babelfish 分为两部分：针对社区版 PostgreSQL 的补丁，计划提交并纳入未来 PostgreSQL 版本；以及建立在该补丁之上的扩展。你可以在自己的环境中克隆、编译、安装并运行 Babelfish，获得 T-SQL 能力。

本次发布的重要组件之一是 Babelfish Compass（[GitHub 仓库](https://github.com/babelfish-for-postgresql/babelfish_compass)）。它分析 Microsoft SQL Server 的 SQL/DDL 代码，判断 Babelfish 的支持程度，并生成报告，帮助决定是否启动使用 Babelfish 从 SQL Server 迁移到 PostgreSQL 的项目。Compass 报告会列出代码中发现的全部 SQL 功能，以及发布时最新 Babelfish 版本是否支持它们。

### Babelfish 的价值 {#benefits-of-babelfish}

Babelfish 降低了 SQL Server 应用迁移到 PostgreSQL 的难度，帮助摆脱昂贵的许可费用。原有应用只需较少代码修改、无需更换数据库驱动，即可直接使用 PostgreSQL。这通过三个层面实现：

- **SQL**。虽然 SQL 是 ANSI 标准，各关系数据库对规范的支持程度和语言扩展仍不同，因此 SQL Server 查询未必能直接在 PostgreSQL 中运行。Babelfish 自带解析器，生成适当的查询节点，使 PostgreSQL 可以原生执行 SQL Server 方言；还提供 PostgreSQL 缺少、或与 SQL Server 行为不同的数据类型、函数和运算符。
- **T-SQL**。SQL Server 的 T-SQL 扩展了 SQL 标准，特别是存储过程所需的变量、异常、控制流等结构。Babelfish 为 PostgreSQL 增加这些结构，并支持 T-SQL 语义。例如，有些错误在 PostgreSQL 中会触发回滚，在 SQL Server 中却不会。通过 TDS 端口使用时，Babelfish 让 PostgreSQL 遵循 SQL Server 的行为，以保证正确性。
- **TDS（SQL Server 线上协议）**。Babelfish 增加对默认运行于 1433 端口的 TDS 协议的支持，因此可以沿用相同的网络协议、端口和连接驱动。该功能通过协议钩子原生实现，不是协议翻译层。

无需更换驱动，修改 SQL 代码的工作量也大幅减少，因此相比完整移植到 PostgreSQL 原生驱动和 PL/pgSQL，使用 Babelfish 可以更快让迁移后的应用运行起来。作为开源项目，社区可以在发现迁移缺口时扩展其功能，进一步增强 PostgreSQL 的可扩展性，覆盖更多场景。

### 如何开始 {#how-to-get-started}

Babelfish 文档提供详细的编译与安装说明，可从 [Babelfish 网站](/zh/babelfish/)访问。

Babelfish 随 PostgreSQL 运行后，服务器默认在 5432 端口监听 PostgreSQL 原生流量，在 1433 端口监听 TDS 流量。

### 这只是开始 {#this-is-only-the-beginning}

Babelfish for PostgreSQL 让 PostgreSQL 理解 SQL Server 的 TDS 线上协议和 T-SQL 语言结构，从而加快 SQL Server 应用迁移。随着未来增加更多 T-SQL 功能支持，这些扩展还将继续演进。希望你喜欢 Babelfish，欢迎来到数据库自由的新阶段！
