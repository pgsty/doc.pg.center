---
title: "gp_fastsequence"
description: "`pg_catalog` 模式中的 `gp_fastsequence` 表记录 AO 表和列存表的信息。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-fastsequence.md"
---

`last_sequence` 值表示表当前使用的最大行号。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`objid`|oid| `pg_class.oid` |用于跟踪 AO 文件段的 `pg_aoseg.pg_aocsseg_*` 表的对象 ID。|
|`objmod`|bigint| |对象修饰符。|
|`last_sequence`|bigint| |对象最后使用的序列号。|
