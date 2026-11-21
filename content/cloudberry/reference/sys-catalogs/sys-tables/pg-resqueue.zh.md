---
title: "pg_resqueue"
description: "`pg_resqueue` 系统目录表包含 Apache Cloudberry 资源队列的信息，资源队列用于资源管理功能。"
weight: 300
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resqueue.md"
---

> [!NOTE]
> 只有启用基于资源队列的资源管理时，`pg_resqueue` 系统目录表才有效。

此表只在 Coordinator 上填充。它定义在 `pg_global` 表空间中，因此由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID。|
|`rsqname`|name| |资源队列名称。|
|`rsqcountlimit`|real| |资源队列的活动查询数量阈值。|
|`rsqcostlimit`|real| |资源队列的查询代价阈值。|
|`rsqovercommit`|boolean| |允许超过代价阈值的查询在系统空闲时运行。|
|`rsqignorecostlimit`|real| |用于判定“小查询”的查询代价上限。代价低于此值的查询不会排队，而是立即运行。|
