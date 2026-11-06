---
title: "pg_statistic_ext_data"
description: "Inspect the catalog fields that store data for extended planner statistics objects in pg_statistic_ext_data."
weight: 400
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-statistic-ext-data.md"
---

The `pg_statistic_ext_data` system catalog table holds data for extended planner statistics defined in [pg_statistic_ext](/cloudberry/reference/sys-catalogs/sys-tables/pg-statistic-ext/). Each row in this catalog corresponds to a *statistics object* created with [`CREATE STATISTICS`](/cloudberry/reference/sql-stmts/create-statistics/).

Like `pg_statistic`, `pg_statistic_ext_data` should not be readable by the public, since the contents might be considered sensitive. (Example: most common combinations of values in columns might be quite interesting.) `pg_stats_ext` is a publicly readable view on `pg_statistic_ext_data` (after joining with `pg_statistic_ext`) that only exposes information about those tables and columns that are readable by the current user.

|column|type|references|description|
|------|----|----------|-----------|
|`stxoid`|oid|[pg_statistic_ext](/cloudberry/reference/sys-catalogs/sys-tables/pg-statistic-ext/).oid | The extended statistic object containing the definition for this data. |
|`stxdndistinct`|pg_ndistinct| | N-distinct counts, serialized as `pg_ndistinct` type. |
|`stxddependencies`|pg_dependencies| | Functional dependency statistics, serialized as `pg_dependencies` type. |
|`stxdmcv`|pg_mcv_list| | MCV (most-common values) list statistics, serialized as `pg_mcv_list` type. |
| `stxdexpr` | ARRAY |  | Stores statistics for expressions defined in the extended statistics object. Each element of the array contains statistical data (similar to what `pg_statistic` holds for a column, such as null fraction, MCV, histogram.) for one of the expressions included in the `CREATE STATISTICS` definition, typically in an internal serialized format. |
