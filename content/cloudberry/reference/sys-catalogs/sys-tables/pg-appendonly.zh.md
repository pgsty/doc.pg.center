---
title: "pg_appendonly"
description: "`pg_catalog` 模式中的 `pg_appendonly` 表包含 AO 表的存储选项及其他特征信息。"
weight: 120
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-appendonly.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`relid`|oid| |表的对象标识符（OID）。|
| `blocksize` | integer |  |AO 表压缩所用的块大小。有效值为 8K–2M，默认为 `32K`。|
| `compresslevel`|smallint| |压缩级别，从 1 到 19 压缩比逐渐提高。指定 zlib 时，有效值为 1–9；指定 zstd 时，有效值为 1–19。|
| `checksum`|boolean| |存储的校验和值，用于比较压缩时与扫描时数据块的状态，以确保数据完整性。|
| `compresstype`|name| |AO 表使用的压缩类型。有效值为：<br />- `none`（不压缩）<br />- `rle_type`（游程编码压缩）<br />- `zlib`（gzip 压缩）<br />- `zstd`（Zstandard 压缩）。|
| `columnstore` | boolean |  |`1` 表示列存储，`0` 表示行存储。|
| `segrelid` | oid | |表在磁盘上的段文件 ID。|
| `segfilecount` |  smallint| |段文件数量。|
| `version`  | smallint | |AO 表的版本。|
| `blkdirrelid` | oid | |磁盘上列存表文件所用的块。|
| `blkdiridxid` | oid | |磁盘上列存索引文件所用的块。|
| `visimaprelid` | oid | |表的可见性映射。|
| `visimapidxid` | oid | |可见性映射上的 B-树索引。|
