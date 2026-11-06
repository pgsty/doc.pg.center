---
title: "pg_statistic_ext_data"
description: "查看 pg_statistic_ext_data 中存储规划器扩展统计信息对象数据的目录字段。"
weight: 400
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-statistic-ext-data.md"
---

`pg_statistic_ext_data` 系统目录表存储在 [pg_statistic_ext](/cloudberry/reference/sys-catalogs/sys-tables/pg-statistic-ext/) 中定义的规划器扩展统计信息的数据。此目录中的每一行都对应一个使用 [`CREATE STATISTICS`](/cloudberry/reference/sql-stmts/create-statistics/) 创建的*统计信息对象*。

与 `pg_statistic` 一样，`pg_statistic_ext_data` 不应允许所有用户读取，因为其内容可能属于敏感信息。（例如，列中最常见的值组合可能会引人关注。）`pg_stats_ext` 是基于 `pg_statistic_ext_data`（与 `pg_statistic_ext` 连接后）的公开可读视图，仅暴露当前用户可读取的表和列的信息。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`stxoid`|oid|[pg_statistic_ext](/cloudberry/reference/sys-catalogs/sys-tables/pg-statistic-ext/).oid |包含此数据定义的扩展统计信息对象。|
|`stxdndistinct`|pg_ndistinct| |不同值组合的数量，序列化为 `pg_ndistinct` 类型。|
|`stxddependencies`|pg_dependencies| |函数依赖统计信息，序列化为 `pg_dependencies` 类型。|
|`stxdmcv`|pg_mcv_list| |MCV（最常见值）列表统计信息，序列化为 `pg_mcv_list` 类型。|
| `stxdexpr` | ARRAY |  |存储扩展统计信息对象中所定义表达式的统计信息。数组中的每个元素都包含 `CREATE STATISTICS` 定义中的一个表达式的统计数据（类似于 `pg_statistic` 为列存储的数据，例如空值比例、MCV、直方图），通常采用内部序列化格式。|
