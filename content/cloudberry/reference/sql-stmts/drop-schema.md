---
title: "DROP SCHEMA"
description: "Removes a schema."
weight: 1280
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-schema.md"
---

## Synopsis {#synopsis}

```sql
DROP SCHEMA [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## Description {#description}

`DROP SCHEMA` removes schemas from the database.

A schema can be dropped only by its owner or a superuser. Note that the owner can drop the schema (and thereby all contained objects) even if they do not own some of the objects within the schema.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the schema does not exist. A notice is issued in this case.

**`name`**

The name of the schema to remove.

**`CASCADE`**

Automatically drop objects (tables, functions, etc.) that are contained in the schema, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the schema if it contains any objects. This is the default.

## Notes {#notes}

Using the `CASCADE` option may result in the command removing objects in other schemas besides the one(s) named.

## Examples {#examples}

Remove the schema `mystuff` from the database, along with everything it contains:

```sql
DROP SCHEMA mystuff CASCADE;
```

## Compatibility {#compatibility}

`DROP SCHEMA` is fully conforming with the SQL standard, except that the standard only allows one schema to be dropped per command. Also, the `IF EXISTS` option is a Apache Cloudberry extension.

## See also {#see-also}

[`CREATE SCHEMA`](/cloudberry/reference/sql-stmts/create-schema/), [`ALTER SCHEMA`](/cloudberry/reference/sql-stmts/alter-schema/)
