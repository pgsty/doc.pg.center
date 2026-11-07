---
title: 单数据库与多数据库部署
linkTitle: 单库与多库模式
description: 初始化前选择 single-db 或 multi-db，并了解模式名称映射。
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_installation/single-multiple.md
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

## 单数据库与多数据库 {#single-vs-multiple-instances}

Babelfish 提供两种运行模式：

- `single-db`
- `multi-db`

创建 Babelfish 集群时，需要决定只迁移一个 T-SQL 用户数据库，还是同时容纳多个迁移后的用户数据库。这会影响 Babelfish 内部的 T-SQL 模式在 PostgreSQL 中呈现的名称，参见[选择迁移模式](/zh/babelfish/installation/single-multiple/#choosing-a-migration-mode)。

指定 `single-db` 时，只能创建一个 T-SQL 用户数据库，其中的 T-SQL 模式会作为普通 PostgreSQL 模式创建在 Babelfish 数据库中。指定 `multi-db` 时，可以创建多个 T-SQL 数据库，各有自己的模式；为了避免重名，对应 PostgreSQL 模式采用 `<database name>_<schema_name>` 的形式。

迁移模式存储在 `migration_mode` 参数中，初始化 Babelfish 后不能修改。要改变模式，必须创建新集群。如果不指定，默认使用 `single-db`。

以下代码先创建用户和数据库，再设置迁移模式、初始化 Babelfish 扩展。使用 `psql` 连接 PostgreSQL 端口（默认 5432）运行：

```sql
/* Create a user that will own the sample database */
CREATE USER babelfish_user WITH CREATEDB 
	CREATEROLE PASSWORD '<PUT_SECRET_PASSWORD_HERE>' INHERIT;

/* Create a database named demo, owned by the above user */
CREATE DATABASE demo OWNER babelfish_user;
ALTER SYSTEM SET babelfishpg_tsql.database_name = 'demo';
SELECT pg_reload_conf();

/* Specify the migration mode for the database */
ALTER DATABASE demo SET babelfishpg_tsql.migration_mode = 'multi-db';

/* Move into the demo database */
\c demo

/* Create the extension in the demo database and initialize Babelfish */
CREATE EXTENSION IF NOT EXISTS "babelfishpg_tds" CASCADE;
CALL SYS.INITIALIZE_BABELFISH('babelfish_user');
```

示例中的 `ALTER DATABASE` 将模式设为 `multi-db`，随后 `SYS.INITIALIZE_BABELFISH` 按指定模式执行初始化。

连接 TDS 端口时，实际连接的是 `babelfishpg_tsql.database_name` 指定的 PostgreSQL 数据库。初始化过程中，这个参数会设为调用 `SYS.INITIALIZE_BABELFISH` 时所在的数据库名。在 `multi-db` 模式下，可以像 SQL Server 一样通过 TDS 使用 `CREATE DATABASE` 和 `USE`；在 `single-db` 模式下，则通过 TDS 使用唯一的 T-SQL 用户数据库。

### 选择迁移模式 {#choosing-a-migration-mode}

两种模式各有利弊，应根据用户数据库的数量及迁移计划选择。初始化后无法更改，因此还要考虑客户端应用的要求。

初始化时，Babelfish 会创建 `master` 和 `tempdb` 系统数据库。如果曾在 SQL Server 的这两个库中创建或修改对象，需要在新集群中重建。与 SQL Server 不同，Babelfish 不会在集群重启后重新初始化 `tempdb`。

以下情况适合单数据库模式：

- 只迁移一个 SQL Server 数据库。此时，从 PostgreSQL 看到的模式名称与原 SQL Server 中相同。如果最终计划迁移到原生 PostgreSQL，SQL 代码可能只需较少修改。
- 最终目标是完整迁移到原生 PostgreSQL。迁移前将模式合并为单个 `dbo` 模式，再迁入一个集群，可以减少修改量。

以下情况适合多数据库模式：

- 仍在试用 Babelfish，不确定未来需求。
- 需要一起迁移多个用户数据库，且最终目标并非完全迁移到原生 PostgreSQL。
- 未来可能需要向 PostgreSQL 迁移多个数据库。
