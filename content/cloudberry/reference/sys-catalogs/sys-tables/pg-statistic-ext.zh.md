---
title: "pg_statistic_ext"
description: "`pg_statistic_ext` 系统目录表存储规划器扩展统计信息的定义。"
weight: 390
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-statistic-ext.md"
---

此目录中的每一行都对应一个使用 [`CREATE STATISTICS`](/cloudberry/reference/sql-stmts/create-statistics/) 创建的*统计信息对象*。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID|
|`stxrelid`|oid|[pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid |包含此对象所描述列的表|
|`stxname`|name| |统计信息对象的名称|
|`stxnamespace`|oid|[pg_namespace](/cloudberry/reference/sys-catalogs/sys-tables/pg-namespace/).oid| |包含此统计信息对象的名字空间的对象标识符|
|`stxowner`|oid|[pg_authid](/cloudberry/reference/sys-catalogs/sys-tables/pg-authid/).oid |统计信息对象的所有者|
| `stxstattarget` | integer |  |此扩展统计信息对象的统计信息目标值，控制 ANALYZE 为此对象收集统计信息的详细程度。值为 `-1` 表示应使用所引用列的统计信息目标值或系统默认统计信息目标值。|
|`stxkeys`|ARRAY|[pg_attribute](/cloudberry/reference/sys-catalogs/sys-tables/pg-attribute/).oid |属性编号数组，指出此统计信息对象涵盖哪些表列；例如，值为 `1 3` 表示涵盖表的第一列和第三列|
|`stxkind`|ARRAY| |包含已启用统计信息种类代码的数组；有效值包括：`d` 表示不同值组合数量的统计信息，`f` 表示函数依赖统计信息，`m` 表示最常见值（MCV）列表统计信息|
| `stxexprs` | pg_node_tree |   |如果统计信息对象是针对表达式定义的，此列存储这些表达式的解析树表示。如果统计信息对象仅针对普通列定义（通过 `stxkeys`），此字段为 `NULL`。|

`pg_statistic_ext` 条目在执行 `CREATE STATISTICS` 时会完整填入，但此时并不计算实际统计值。后续的 `ANALYZE` 命令会计算所需的值，并填入 [pg_statistic_ext_data](/cloudberry/reference/sys-catalogs/sys-tables/pg-statistic-ext-data/) 目录中的条目。
