---
title: "DROP VIEW"
description: "Removes a view."
weight: 1430
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-view.md"
---

## Synopsis {#synopsis}

```sql
DROP VIEW [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## Description {#description}

`DROP VIEW` removes an existing view. Only the owner of a view can remove it.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the view does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of the view to remove.

**`CASCADE`**

Automatically drop objects that depend on the view (such as other views), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the view if any objects depend on it. This is the default.

## Examples {#examples}

Remove the view `topten`:

```sql
DROP VIEW topten;
```

## Compatibility {#compatibility}

`DROP VIEW` fully conforms to the SQL standard, except that the standard only allows one view to be dropped per command. Also, the `IF EXISTS` option is a Apache Cloudberry extension.

## See also {#see-also}

[`CREATE VIEW`](/cloudberry/reference/sql-stmts/create-view/), [`ALTER VIEW`](/cloudberry/reference/sql-stmts/alter-view/)
