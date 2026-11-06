---
title: "pg_resourcetype"
description: "`pg_resourcetype` 系统目录表包含可分配给 Apache Cloudberry 资源队列的扩展属性信息。"
weight: 290
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resourcetype.md"
---

每行详细描述一个属性及其固有特性，例如默认设置、是否必需，以及停用该属性的值（在允许停用时）。

此表只在 Coordinator 上填充。它定义在 `pg_global` 表空间中，因此由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID。|
|`resname`|name| |资源类型名称。|
|`restypid`|smallint| |资源类型 ID。|
|`resrequired`|boolean| |有效的资源队列是否必须具有此资源类型。|
|`reshasdefault`|boolean| |资源类型是否有默认值。为真时，默认值由 reshasdefaultsetting 指定。|
|`rescandisable`|boolean| |此类型是否可以移除或停用。为真时，默认值由 resdisabledsetting 指定。|
|`resdefaultsetting`|text| |资源类型的默认设置（适用时）。|
|`resdisabledsetting`|text| |停用此资源类型的值（在允许停用时）。|
