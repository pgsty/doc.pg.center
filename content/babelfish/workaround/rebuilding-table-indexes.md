---
title: Rebuilding Table Indexes
linkTitle: Rebuild indexes
description: Use PostgreSQL REINDEX TABLE for SQL Server index-maintenance scripts.
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_workaround/rebuilding_table_indexes.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Rebuilding Table Indexes {#rebuilding-table-indexes}


In T-SQL, you reindex all the indexes in the table using the [`DBCC DBREINDEX` statement](https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dbreindex-transact-sql?view=sql-server-ver16) or [`ALTER INDEX` statement](https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16). Currently, Babelfish doesn’t support those statements. Instead, you can run the PostgreSQL `REINDEX TABLE` statement from a Postgres connection. For information about the PostgreSQL statement, see [`REINDEX` in the PostgreSQL documentation](https://www.postgresql.org/docs/14/sql-reindex).

If your T-SQL maintenance scripts have a statement like one of the following:

```sql
DBCC DBREINDEX ('my_database.dbo.my_table');
```
or

```sql
ALTER INDEX ALL ON my_database.dbo.my_table REBUILD;
```

then run this equivalent statement, while connected to the PostgreSQL port of your Babelfish-enabled server:

```sql
REINDEX TABLE my_database_dbo.my_table; -- For servers using multi-database mode
```
or

```sql
REINDEX TABLE dbo.my_table;             -- For servers using single-database mode
```

For convenience, you can define a PostgreSQL stored procedure that runs the `REINDEX TABLE` statement for a specified statement, and call the stored procedure using the T-SQL `CALL` statement. If you do so, make sure that the permissions to call the procedure are consistent with the permissions to perform DDL operations on the table, and that any dynamically created `REINDEX TABLE` statements quote all the schema and table names to avoid a malformed statement.

For information about using Babelfish from both the TDS port and the PostgreSQL port, [visit the Babelfish website](/babelfish/usage/interoperability/).
