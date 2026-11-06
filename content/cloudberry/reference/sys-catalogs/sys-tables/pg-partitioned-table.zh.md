---
title: "pg_partitioned_table"
description: "`pg_partitioned_table` 系统目录存储表如何分区的信息。"
weight: 240
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-partitioned-table.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`partrelid`|oid|[pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid|此分区表的 `pg_class` 条目的对象标识符。|
|`partstrat`|char| |分区策略：`h` = 哈希分区表，`l` = 列表分区表，`r` = 范围分区表。|
|`partnatts`|smallint| |分区键中的列数。|
|`partdefid`|oid|[pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid |此分区表默认分区的 `pg_class` 条目的对象标识符；如果没有默认分区，则为零。|
|`partattrs`|int2vector|[pg_attribute](/cloudberry/reference/sys-catalogs/sys-tables/pg-attribute/).attnum |包含 `partnatts` 个值的数组，指示哪些表列属于分区键。例如，值 `1 3` 表示表的第一列和第三列构成分区键。数组中的零表示对应的分区键列是表达式，而不是简单的列引用。|
|`partclass`|ARRAY|[pg_opclass](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid|对分区键中的每一列，包含所用操作符类的对象标识符。|
|`partcollation`|ARRAY|[pg_opclass](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid |对分区键中的每一列，包含分区所用排序规则的对象标识符；如果列的数据类型不支持排序规则，则为零。|
|`partexprs`|pg_node_tree| |不是简单列引用的分区键列所对应的表达式树（以 `nodeToString()` 表示）。此列表为 `partattrs` 中的每个零项包含一个元素。如果所有分区键列都是简单引用，则为 NULL。Apache Cloudberry 的经典分区语法不支持在分区键中指定表达式。|
