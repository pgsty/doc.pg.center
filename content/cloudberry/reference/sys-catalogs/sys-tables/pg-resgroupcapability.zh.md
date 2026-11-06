---
title: "pg_resgroupcapability"
description: "`pg_resgroupcapability` 系统目录表包含已定义的 Apache Cloudberry 资源组的能力和限制信息。"
weight: 280
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resgroupcapability.md"
---

> [!NOTE]
> 只有启用基于资源组的资源管理时，`pg_resgroupcapability` 系统目录表才有效。

可以通过资源组对象 ID 将此表与 [pg_resgroup](/cloudberry/reference/sys-catalogs/sys-tables/pg-resgroup/) 表连接。

`pg_resgroupcapability` 表定义在 `pg_global` 表空间中，由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`resgroupid`|oid|`pg_resgroup.oid`|关联资源组的对象 ID。|
|`reslimittype`|smallint| |资源组限制类型：<br/><br/>1 — 并发数<br/><br/>2 — CPU_MAX_WEIGHT<br/><br/>3 — CPU_WEIGHT<br/><br/>4 — CPUSET<br/><br/>5 — MEMORY_QUOTA<br/><br/>6 — MIN_COST<br/><br/>7 — IO_LIMIT。|
|`value`|不透明类型| |为此记录引用的资源限制设置的具体值。此值的固定类型为 `text`，会根据所引用的限制转换为不同的数据类型。|
