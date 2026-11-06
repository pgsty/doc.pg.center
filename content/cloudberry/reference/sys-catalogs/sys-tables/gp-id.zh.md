---
title: "gp_id"
description: "`pg_catalog` 模式中的 `gp_id` 系统目录表标识 Apache Cloudberry 系统的名称及其 Segment 数量。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-id.md"
---

它还记录该表所在数据库实例（Segment 或 Coordinator）的 `local` 值。此表定义在 `pg_global` 表空间中，因此由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`gpname`|name| |此 Apache Cloudberry 系统的名称。|
|`numsegments`|smallint| |Apache Cloudberry 系统中的 Segment 数量。|
|`dbid`|smallint| |此 Segment（或 Coordinator）实例的唯一标识符。|
|`content`|smallint| |此 Segment 实例上所存储数据分片的 ID。主实例及其镜像具有相同的内容 ID。<br/><br/>对于 Segment，取值为 0–*N-1*，其中 *N* 是 Apache Cloudberry 中的 Segment 数量。<br/><br/>对于 Coordinator，值为 -1。|
