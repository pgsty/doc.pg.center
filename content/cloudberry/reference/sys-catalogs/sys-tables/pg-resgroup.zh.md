---
title: "pg_resgroup"
description: "`pg_resgroup` 系统目录表包含 Apache Cloudberry 资源组的信息，资源组用于管理并发语句、CPU 和内存资源。"
weight: 270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resgroup.md"
---

> [!NOTE]
> 只有启用基于资源组的资源管理时，`pg_resgroup` 系统目录表才有效。

此表定义在 `pg_global` 表空间中，由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID。|
|`rsgname`|name| |资源组名称。|
|`parent`|oid| |未使用，保留供将来使用。|
