---
title: "DROP TABLE"
description: "Removes a table."
weight: 1320
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-table.md"
---

## Synopsis {#synopsis}

```sql
DROP TABLE [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## Description {#description}

`DROP TABLE` removes tables from the database. Only the table owner, the schema owner, and superuser can drop a table. To empty a table of rows without removing the table definition, use [`DELETE`](/cloudberry/reference/sql-stmts/delete/) or [`TRUNCATE`](/cloudberry/reference/sql-stmts/truncate/).

`DROP TABLE` always removes any indexes, rules, triggers, and constraints that exist for the target table. However, to drop a table that is referenced by a view, `CASCADE` must be specified. `CASCADE` removes a dependent view entirely.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the table does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of the table to remove.

**`CASCADE`**

Automatically drop objects that depend on the table (such as views), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the table if any objects depend on it. This is the default.

## Examples {#examples}

Remove the table `mytable`:

```sql
DROP TABLE mytable;
```

Remove two tables, `films` and `distributors`:

```sql
DROP TABLE films, distributors;
```

## Compatibility {#compatibility}

`DROP TABLE` conforms to the SQL standard, except that the standard allows only one table to be dropped per command. Also, the `IF EXISTS` option is a Apache Cloudberry extension.

## See also {#see-also}

[`ALTER TABLE`](/cloudberry/reference/sql-stmts/alter-table/), [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/)
