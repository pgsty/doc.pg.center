---
title: "gp_partition_template"
description: "`pg_catalog` 模式中的 `gp_partition_template` 系统目录表描述分区表与分区层次结构中各层定义的子分区模板之间的关系。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-partition-template.md"
---

> [!NOTE]
> Apache Cloudberry 仅对使用经典语法创建的分区表支持子分区模板。

每个子分区模板都依赖于层次结构中下一层模板的存在。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`relid`| oid | `pg_class.oid` |根分区表的对象标识符。|
|`level`|smallint| |分区在层次结构中的层级。层级编号如下：第 `0` 层是根分区表本身，第 `1` 层表示根分区表的直接子分区，以此类推。叶子分区的层级编号最大。|
|`template`| `pg_node_tree` | |为层次结构中此层各分区定义的子分区模板的表达式表示。|
