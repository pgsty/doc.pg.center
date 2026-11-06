---
title: "DROP MATERIALIZED VIEW"
description: "Removes a materialized view."
weight: 1150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-materialized-view.md"
---

## Synopsis {#synopsis}

```sql
DROP MATERIALIZED VIEW [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP MATERIALIZED VIEW` drops an existing materialized view. To run this command, you must be the owner of the materialized view.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the materialized view does not exist. A notice is issued in this case.

**`name`**

The name (optionally schema-qualified) of a materialized view to be dropped.

**`CASCADE`**

Automatically drop objects that depend on the materialized view (such as other materialized views, or regular views), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the materialized view if any objects depend on it. This is the default.

## Examples {#examples}

This command removes the materialized view called `order_summary`.

```sql
DROP MATERIALIZED VIEW order_summary;
```

## Compatibility {#compatibility}

`DROP MATERIALIZED VIEW` is a Apache Cloudberry extension of the SQL standard.

## See also {#see-also}

[`ALTER MATERIALIZED VIEW`](/cloudberry/reference/sql-stmts/alter-materialized-view/), [`CREATE MATERIALIZED VIEW`](/cloudberry/reference/sql-stmts/create-materialized-view/), [`REFRESH MATERIALIZED VIEW`](/cloudberry/reference/sql-stmts/refresh-materialized-view/)
