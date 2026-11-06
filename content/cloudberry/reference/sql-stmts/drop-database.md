---
title: "DROP DATABASE"
description: "Removes a database."
weight: 1050
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-database.md"
---

## Synopsis {#synopsis}

```sql
DROP DATABASE [IF EXISTS] <name>
```

## Description {#description}

`DROP DATABASE` drops a database. It removes the catalog entries for the database and deletes the directory containing the data. It can only be run by the database owner. Also, it cannot be run while you or anyone else are connected to the target database. (Connect to `postgres` or any other database to issue this command.)

> [!WARNING]
> `DROP DATABASE` cannot be undone. Use it with care!

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the database does not exist. A notice is issued in this case.

**`name`**

The name of the database to remove.

## Notes {#notes}

`DROP DATABASE` cannot be run inside a transaction block.

This command cannot be run while connected to the target database. Thus, it might be more convenient to use the program dropdb instead, which is a wrapper around this command.

## Examples {#examples}

Drop the database named `testdb`:

```sql
DROP DATABASE testdb;
```

## Compatibility {#compatibility}

There is no `DROP DATABASE` statement in the SQL standard.

## See also {#see-also}

[`ALTER DATABASE`](/cloudberry/reference/sql-stmts/alter-database/), [`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/)
