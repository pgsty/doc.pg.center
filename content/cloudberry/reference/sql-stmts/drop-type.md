---
title: "DROP TYPE"
description: "Removes a data type."
weight: 1400
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-type.md"
---

## Synopsis {#synopsis}

```sql
DROP TYPE [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## Description {#description}

`DROP TYPE` will remove a user-defined data type. Only the owner of a type can remove it.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the type does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of the data type to remove.

**`CASCADE`**

Automatically drop objects that depend on the type (such as table columns, functions, operators), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the type if any objects depend on it. This is the default.

## Examples {#examples}

Remove the data type `box`:

```sql
DROP TYPE box;
```

## Compatibility {#compatibility}

This command is similar to the corresponding command in the SQL standard, apart from the `IF EXISTS` option, which is a Apache Cloudberry extension. But note that much of the `CREATE TYPE` command and the data type extension mechanisms in Apache Cloudberry differ from the SQL standard.

## See also {#see-also}

[`ALTER TYPE`](/cloudberry/reference/sql-stmts/alter-type/), [`CREATE TYPE`](/cloudberry/reference/sql-stmts/create-type/)
