---
title: "pg_statistic_ext"
description: "The `pg_statistic_ext` system catalog table holds definitions of extended planner statistics."
weight: 390
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-statistic-ext.md"
---

Each row in this catalog corresponds to a *statistics object* created with [`CREATE STATISTICS`](/cloudberry/reference/sql-stmts/create-statistics/).

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |The object ID|
|`stxrelid`|oid|[pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid | The table containing the columns described by this object |
|`stxname`|name| | The name of the statistics object |
|`stxnamespace`|oid|[pg_namespace](/cloudberry/reference/sys-catalogs/sys-tables/pg-namespace/).oid| | The object identifier of the namespace that contains this statistics object |
|`stxowner`|oid|[pg_authid](/cloudberry/reference/sys-catalogs/sys-tables/pg-authid/).oid | The owner of the statistics object |
| `stxstattarget` | integer |  | Statistics target for this extended statistics object. Controls the level of detail of statistics collected by ANALYZE for this object. A value of `-1` indicates that the statistics targets of the referenced columns or the system default statistics target should be used. |
|`stxkeys`|ARRAY|[pg_attribute](/cloudberry/reference/sys-catalogs/sys-tables/pg-attribute/).oid | An array of attribute numbers, indicating which table columns are covered by this statistics object; for example, a value of `1 3` would mean that the first and the third table columns are covered |
|`stxkind`|ARRAY| | An array containing codes for the enabled statistics kinds; valid values are: `d` for n-distinct statistics, `f` for functional dependency statistics, and `m` for most common values (MCV) list statistics |
| `stxexprs` | pg_node_tree |   |  If the statistics object is defined on expressions, this column stores the parse tree representation of those expressions. If the statistics object is only defined on simple columns (via `stxkeys`), this field will be `NULL`. |

The `pg_statistic_ext` entry is filled in completely during `CREATE STATISTICS`, but the actual statistical values are not computed then. Subsequent `ANALYZE` commands compute the desired values and populate an entry in the [pg_statistic_ext_data](/cloudberry/reference/sys-catalogs/sys-tables/pg-statistic-ext-data/) catalog.
