---
title: "pg_attribute_encoding"
description: "`pg_catalog` 模式中的 `pg_attribute_encoding` 系统目录表包含列存储信息。"
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-attribute-encoding.md"
---

|列|类型|修饰符|存储|说明|
|------|----|--------|-------|-----------|
|`attrelid`|oid|not null|plain|指向 `pg_attribute.attrelid` 的外键。|
|`attnum`|smallint|not null|plain|指向 `pg_attribute.attnum` 的外键。|
| `filenum` | smallint | not null | plain |列文件编号。|
|`attoptions`|text [ ]| |extended|选项。|

对于 `filenum = f` 的列，磁盘上列文件使用的后缀为 `(f - 1)*128 to f*128 - 1`。例如：

- `filenum = 1` 的列对应文件 `relfilenode`、`relfilenode.1` .. `relfilenode.127`。
- `filenum = 2` 的列对应文件 `relfilenode.128`、`relfilenode.129` .. `relfilenode.255`。
- `filenum = 3` 的列对应文件 `relfilenode.256`、`relfilenode.257` .. `relfilenode.383`。
