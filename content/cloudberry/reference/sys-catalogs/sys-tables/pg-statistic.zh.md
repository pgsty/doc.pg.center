---
title: "pg_statistic"
description: "`pg_statistic` 系统目录表存储数据库内容的统计数据。"
weight: 380
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-statistic.md"
---

这些条目由 [`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/) 创建，随后供查询规划器使用。请注意，即使统计数据是最新的，它们本质上也都是近似值。

通常，每个已分析的表列都有一个 `stainherit = false` 的条目。如果该表有继承子表，Apache Cloudberry 还会创建第二个条目，其 `stainherit = true`。这一行表示该列在整个继承树上的统计信息，例如通过 `SELECT column FROM table*` 可以看到的数据的统计信息；而 `stainherit = false` 的行则表示 `SELECT column FROM ONLY table` 的结果。

`pg_statistic` 还存储索引表达式值的统计数据。这些表达式被当作实际的数据列来描述；具体来说，`starelid` 引用的是索引。不过，普通的非表达式索引列不会生成条目，因为它会与底层表列的条目重复。目前，索引表达式的条目始终具有 `stainherit = false`。

不同类型的数据可能适用不同种类的统计信息，因此 `pg_statistic` 在设计上尽量不预设所存储统计信息的种类。只有极为通用的统计信息（例如空值情况）才在 `pg_statistic` 中设有专用列。其他信息都存储在槽中；每个槽是一组相关列，其内容由槽内某一列中的数字代码标识。

`pg_statistic` 不应允许所有用户读取，因为即使是表内容的统计信息也应视为敏感信息。（例如，工资列的最小值和最大值。）`pg_stats` 是基于 `pg_statistic` 的公开可读视图，仅暴露当前用户可读取的表的信息。

> [!WARNING]
> `gpsd` 和 `minirepro` 等诊断工具会以清晰可读的形式从 `pg_statistic` 收集敏感信息，例如直方图边界。务必检查这些工具的输出文件，确保按照所在组织的要求，这些内容可以传送到数据库外部。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`starelid`|oid|[pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid|所描述列所属的表或索引|
|`staattnum`|smallint|[pg_attribute](/cloudberry/reference/sys-catalogs/sys-tables/pg-attribute/).attnum|所描述列的编号|
|`stainherit`|boolean| |如果为 true，统计信息包含继承子表的列，而不仅限于指定关系中的值。|
|`stanullfrac`|real| |该列中空值所占的比例|
|`stawidth`|integer| |非空项的平均存储宽度，以字节为单位|
|`stadistinct`|real| |列中不同非空数据值的数量。大于零的值表示不同值的实际数量。小于零的值表示相对于表行数的倍数取负值（例如，如果一列中约 80% 的值非空，且每个非空值平均出现约两次，则可以用 `stadistinct` = -0.4 表示）。零表示不同值的数量未知。|
|`stakind*N*`|smallint| |标识 `pg_statistic` 行的第 `N` 个槽中存储的统计信息种类的数字代码|
|`staop*N*`|oid|[pg_operator](/cloudberry/reference/sys-catalogs/sys-tables/pg-operator/).oid|用于推导第 `N` 个槽中统计信息的操作符。例如，直方图槽会显示定义数据排序顺序的 `<` 操作符。|
|`stacoll*N*`|oid|pg_collation.oid|用于推导第 `N` 个槽中统计信息的排序规则。例如，可排序列的直方图槽会显示定义数据排序顺序的排序规则。对于不可排序的数据，此值为零。|
|`stanumbers*N*`|ARRAY| |适用于第 `N` 个槽的数值统计信息；如果该槽的种类不涉及数值，则为 NULL。|
|`stavalues*N*`|anyarray| |适用于第 `N` 个槽的列数据值；如果该槽的种类不存储任何数据值，则为 NULL。每个数组的元素值实际上采用特定列的数据类型，或数组元素类型等相关类型，因此无法将这些列的类型定义为比 `anyarray` 更具体的类型。|
