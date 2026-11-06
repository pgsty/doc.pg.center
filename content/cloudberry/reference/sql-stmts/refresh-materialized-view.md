---
title: "REFRESH MATERIALIZED VIEW"
description: "Replaces the contents of a materialized view."
weight: 1580
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/refresh-materialized-view.md"
---

## Synopsis {#synopsis}

```sql
REFRESH MATERIALIZED VIEW [ CONCURRENTLY ] <name>
    [ WITH [ NO ] DATA ]
```

## Description {#description}

`REFRESH MATERIALIZED VIEW` completely replaces the contents of a materialized view. The old contents are discarded. To run this command you must be the owner of the materialized view. If `WITH DATA` is specified (or defaults), the backing query is executed to provide the new data, and the materialized view is left in a scannable state. If `WITH NO DATA` is specified, no new data is generated, and the materialized view is left in an unscannable state.

You may not specify `CONCURRENTLY` and `WITH NO DATA` together.

## Parameters {#parameters}

**`CONCURRENTLY`**

Refresh the materialized view without locking out concurrent selects on the materialized view. Without this option, a refresh that affects a lot of rows tends to use fewer resources and completes more quickly, but could block other connections which are trying to read from the materialized view. This option might be faster in cases where a small number of rows are affected.

This option is only allowed if there is at least one `UNIQUE` index on the materialized view which uses only column names and includes all rows; that is, it must not index on any expressions nor include a `WHERE` clause.

You can not use this option when the materialized view is not already populated.

Even with this option, only one `REFRESH` at a time may run against any one materialized view.

**`name`**

The name (optionally schema-qualified) of the materialized view to refresh.

**`WITH [ NO ] DATA`**

`WITH DATA` is the default and specifies that the materialized view query is run to provide new data, and the materialized view is left in a scannable state. If `WITH NO DATA` is specified, no new data is generated and the materialized view is left in an unscannable state.

## Notes {#notes}

If there is an `ORDER BY` clause in the materialized view's defining query, the original contents of the materialized view will be ordered that way; but `REFRESH MATERIALIZED VIEW` does not guarantee to preserve that ordering.

## Examples {#examples}

This command replaces the contents of the materialized view `order_summary` using the query from the materialized view's definition, and leaves it in a scannable state.

```sql
REFRESH MATERIALIZED VIEW order_summary;
```

This command frees storage associated with the materialized view `annual_statistics_basis` and leaves it in an unscannable state.

```sql
REFRESH MATERIALIZED VIEW annual_statistics_basis WITH NO DATA;
```

## Compatibility {#compatibility}

`REFRESH MATERIALIZED VIEW` is a Apache Cloudberry extension of the SQL standard.

## See also {#see-also}

[ALTER MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/alter-materialized-view/), [CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/), [DROP MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/drop-materialized-view/)
