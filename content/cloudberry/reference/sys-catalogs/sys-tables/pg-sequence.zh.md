---
title: "pg_sequence"
description: "`pg_sequence` 系统目录表包含序列的信息。"
weight: 330
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-sequence.md"
---

序列的部分信息（例如名称和模式）存储在 [pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/) 系统表中。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`seqrelid`|oid|`pg_class.oid` |此序列对应的 `pg_class` 条目的 OID|
|`seqtypid`|oid|`pg_type.oid`|序列的数据类型|
|`seqstart`|bigint| |序列的起始值|
|`seqincrement`|bigint| |序列的步长|
|`seqmax`|bigint| |序列的最大值|
|`seqmin`|bigint| |序列的最小值|
|`seqcache`|bigint| |序列的缓存大小|
|`seqcycle`|boolean| |序列是否循环|
