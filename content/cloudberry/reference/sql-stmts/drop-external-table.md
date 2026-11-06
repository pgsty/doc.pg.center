---
title: "DROP EXTERNAL TABLE"
description: "Removes an external table definition."
weight: 1080
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-external-table.md"
---

## Synopsis {#synopsis}

```sql
DROP EXTERNAL [WEB] TABLE [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP EXTERNAL TABLE` drops an existing external table definition from the database system. The external data sources or files are not deleted. To run this command you must be the owner of the external table.

## Parameters {#parameters}

**`WEB`**

Optional keyword for dropping external web tables.

**`IF EXISTS`**

Do not throw an error if the external table does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of an existing external table.

**`CASCADE`**

Automatically drop objects that depend on the external table (such as views).

**`RESTRICT`**

Refuse to drop the external table if any objects depend on it. This is the default.

## Examples {#examples}

Remove the external table named `staging` if it exists:

```sql
DROP EXTERNAL TABLE IF EXISTS staging;
```

## Compatibility {#compatibility}

There is no `DROP EXTERNAL TABLE` statement in the SQL standard.

## See also {#see-also}

[`CREATE EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/create-external-table/), [`ALTER EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/alter-external-table/)
