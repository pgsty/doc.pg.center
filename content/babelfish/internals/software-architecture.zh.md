---
title: 软件架构
linkTitle: 软件架构
description: 理解服务器补丁、扩展，以及 SQL Server 数据库到 PostgreSQL 模式的映射。
weight: 40
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/software-architecture.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 文档快照
> 本文译自上游网站，中文翻译由 PGSTY 文档项目整理。上游自 2023 年起将新文档迁至 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)；请结合所用版本的[发行说明](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)核对功能支持。

Babelfish 通过[钩子](/zh/babelfish/internals/postgresql-hooks/)在 PostgreSQL 服务器中实现 Microsoft SQL Server 的行为。这让 PostgreSQL 服务器能够理解多种语言，使部署更灵活，也更易于管理。

运行 Babelfish 的 PostgreSQL 数据库在两个可配置的 TCP 端口上接受连接，分别使用两种方言：

- SQL Server 方言（TDS）。
- PostgreSQL 方言。

TDS 处理程序接受并处理从 TDS 端口传入的请求后，会将请求交给 PostgreSQL 后端。后端使用经过修改、能够理解 SQL Server 方言的自定义解析器来解析请求。

![Babelfish 系统架构](/babelfish/assets/images/babelfish-architecture.png)
{width="800" caption="Babelfish 系统架构（上游原图）"}

PostgreSQL 优化器和执行器没有显著变化。

Babelfish 随附的 PostgreSQL 内核经过修改，以支持触发器处理、事务处理以及其他与 SQL Server 不同的行为。因此，这个数据库服务器与社区版 PostgreSQL 并非完全相同。

### 数据库与模式 {#databases-vs-schemas}

PostgreSQL 支持以下对象层次：

- 实例：正在运行的 PostgreSQL 服务器（PostgreSQL 社区文档称之为集群）。
- 数据库：用户连接的对象。
- 模式：数据库中表和其他对象的逻辑分组。
- 表：存放数据的对象。

SQL Server 也支持这些对象。

与 PostgreSQL 不同，SQL Server 允许查询另一个数据库中的表，或连接不同数据库中的表。要启用跨数据库连接，应在 Babelfish 中使用 `multi-db` 部署模式。

在 `multi-db` 模式下，使用 `USE` 从一个数据库切换到另一个数据库时，连接仍然指向同一个 PostgreSQL 数据库，只是切换到了不同的模式。如果计划通过两种协议查询同一张表，理解这种关系会有所帮助。

关于单数据库和多数据库部署的详细说明，见[相应文档](/zh/babelfish/installation/single-multiple/)。

### Babelfish 扩展 {#babelfish-extensions}

Babelfish 使用扩展为 PostgreSQL 提供 SQL Server 兼容能力：

- `babelfishpg_common`：SQL Server 数据类型。
- `babelfishpg_money`：固定精度数值类型。
- `babelfishpg_tds`：TDS 协议扩展。
- `babelfishpg_tsql`：T-SQL 扩展。

下面分别介绍这些扩展。

#### `babelfishpg_common`：SQL Server 数据类型 {#babelfishpgcommon-sql-server-data-types}

数据类型往往十分相似，但不一定完全相同。因此，Babelfish 开发团队提供了专门的数据类型，用来模拟 SQL Server 行为。

#### `babelfishpg_money`：money 数据类型 {#babelfishpgmoney-money-data-type}

`babelfishpg_money` 扩展实现 money 数据类型。

#### `babelfishpg_tds`：TDS 协议扩展 {#babelfishpgtds-tds-protocol-extension}

这个扩展实现 TDS 客户端/服务器协议。需要修改 `postgresql.conf` 中的 `shared_preload_libraries` 参数，以确保服务器启动时加载该扩展。

#### `babelfishpg_tsql`：T-SQL 扩展 {#babelfishpgtsql-t-sql-extension}

这个扩展提供处理 T-SQL 语法的代码，包括函数、[系统视图](/zh/babelfish/internals/system-views/)以及实现 SQL Server 功能所需的其他基础设施。
