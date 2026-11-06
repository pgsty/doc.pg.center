---
title: "pg_attrdef"
description: "`pg_catalog` 模式中的 `pg_attrdef` 表存储列的默认值。"
weight: 150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-attridef.md"
---

列的主要信息存储在 `pg_attribute` 中。只有在创建表或添加列时显式指定了默认值的列，才会在这里有条目。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID。|
|`adrelid`|oid| `pg_class.oid` |此列所属的表。|
|`adnum`|smallint| `pg_attribute.attnum` |列号。|
|`adbin`|pg_node_tree| |列默认值的内部表示。|
