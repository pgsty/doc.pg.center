---
title: "pg_am"
description: "`pg_catalog` 模式中的 `pg_am` 表存储索引访问方法的信息。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-am.md"
---

系统支持的每种索引访问方法在此表中各有一行。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符（隐藏属性，必须显式选择）。|
|`amname`|name| |访问方法的名称。|
|`amhandler`|regproc| |负责提供访问方法信息的处理函数的 OID。|
|`amtype`|char| |`t` 表示表（包括物化视图），`i` 表示索引。|
