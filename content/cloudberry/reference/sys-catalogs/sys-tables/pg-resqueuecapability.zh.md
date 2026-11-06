---
title: "pg_resqueuecapability"
description: "`pg_resqueuecapability` 系统目录表包含现有 Apache Cloudberry 资源队列的扩展属性（也称能力）信息。"
weight: 310
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resqueuecapability.md"
---

> [!NOTE]
> 只有启用基于资源队列的资源管理时，`pg_resqueuecapability` 系统目录表才有效。

此表只记录分配了扩展能力（例如优先级设置）的资源队列。通过资源队列对象 ID，可以将此表与 [pg_resqueue](/cloudberry/reference/sys-catalogs/sys-tables/pg-resqueue/) 表连接；通过资源类型 ID（`restypid`），可以与 [pg_resourcetype](/cloudberry/reference/sys-catalogs/sys-tables/pg-resourcetype/) 表连接。

此表只在 Coordinator 上填充。它定义在 `pg_global` 表空间中，因此由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`rsqueueid`|oid|`pg_resqueue.oid`|关联资源队列的对象 ID。|
|`restypid`|smallint|`pg_resourcetype. restypid`|资源类型，来源于 [pg_resqueuecapability](/cloudberry/reference/sys-catalogs/sys-tables/pg-resourcetype/) 系统表。|
|`resetting`|text| |为此记录引用的能力设置的具体值。根据实际资源类型，此值可以具有不同的数据类型。|
