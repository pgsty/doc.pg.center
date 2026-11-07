---
title: 重建表索引
linkTitle: 重建索引
description: 使用 PostgreSQL REINDEX TABLE 替代 SQL Server 索引维护语句。
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_workaround/rebuilding_table_indexes.md
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

## 重建表索引 {#rebuilding-table-indexes}

在 T-SQL 中，可以通过 [`DBCC DBREINDEX`](https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dbreindex-transact-sql?view=sql-server-ver16) 或 [`ALTER INDEX`](https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16) 重建表的所有索引。原文所述 Babelfish 版本不支持这些语句，可以改用 PostgreSQL 连接执行 `REINDEX TABLE`。详情见 [PostgreSQL 的 REINDEX 文档](https://www.postgresql.org/docs/14/sql-reindex)。

如果 T-SQL 维护脚本中有如下语句：

```sql
DBCC DBREINDEX ('my_database.dbo.my_table');
```

或：

```sql
ALTER INDEX ALL ON my_database.dbo.my_table REBUILD;
```

可以连接启用了 Babelfish 的服务器的 PostgreSQL 端口，执行等价语句：

```sql
REINDEX TABLE my_database_dbo.my_table; -- For servers using multi-database mode
```

或：

```sql
REINDEX TABLE dbo.my_table;             -- For servers using single-database mode
```

为方便使用，可以定义一个 PostgreSQL 存储过程，对指定对象执行 `REINDEX TABLE`，再通过 T-SQL 的 `CALL` 语句调用。务必保证调用过程的权限与对目标表执行 DDL 的权限一致；动态构造 `REINDEX TABLE` 时，要正确引用所有模式名和表名，避免生成格式错误的语句。

关于同时通过 TDS 与 PostgreSQL 端口使用 Babelfish，参见[互操作指南](/zh/babelfish/usage/interoperability/)。
