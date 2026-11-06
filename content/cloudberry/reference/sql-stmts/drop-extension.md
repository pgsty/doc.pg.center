---
title: "DROP EXTENSION"
description: "Removes an extension from a Apache Cloudberry."
weight: 1070
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-extension.md"
---

## Synopsis {#synopsis}

```sql
DROP EXTENSION [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP EXTENSION` removes extensions from the database. Dropping an extension causes its component objects to be dropped as well.

> [!NOTE]
> The supporting extension files that were installed to create the extension (for example, the library and `.control` files) are not deleted. The files must be manually removed from the Apache Cloudberry hosts.

You must own the extension to use `DROP EXTENSION`.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the extension does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name of an installed extension.

**`CASCADE`**

Automatically drop objects that depend on the extension, and in turn all objects that depend on those objects. Refer to the PostgreSQL [Dependency Tracking](https://www.postgresql.org/docs/14/ddl-depend.html) documentation for more information.

> [!TIP]
> Before issuing a `DROP EXTENSION` with the `CASCADE` keyword, you should be aware of all object that depend on the extension to avoid unintended consequences.

**`RESTRICT`**

Refuse to drop an extension if any objects depend on it (other than its own member objects and other extensions listed in the same `DROP` command). This is the default.

## Examples {#examples}

To remove the extension `hstore` from the current database:

```sql
DROP EXTENSION hstore;
```

This command fails if any of the extension objects are in use in the database. For example, if a table is defined with columns of the `hstore` type. Add the `CASCADE` option to forcibly remove those dependent objects.

## Compatibility {#compatibility}

`DROP EXTENSION` is a Apache Cloudberry extension.

## See also {#see-also}

[`CREATE EXTENSION`](/cloudberry/reference/sql-stmts/create-extension/), [`ALTER EXTENSION`](/cloudberry/reference/sql-stmts/alter-extension/)
