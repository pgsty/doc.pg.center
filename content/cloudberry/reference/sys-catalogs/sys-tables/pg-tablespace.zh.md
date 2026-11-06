---
title: "pg_tablespace"
description: "`pg_tablespace` 系统目录表存储可用表空间的信息。"
weight: 410
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-tablespace.md"
---

可以将表放入特定的表空间，以便管理磁盘布局。与大多数系统目录不同，`pg_tablespace` 由 Cloudberry 系统中的所有数据库共享：每个系统只有一份 `pg_tablespace`，而不是每个数据库一份。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID|
|`spcname`|name| |表空间名称。|
|`spcowner`|oid|pg_authid.oid|表空间的所有者，通常是创建它的用户。|
|`spcacl`|ARRAY| |表空间访问权限。|
|`spcoptions`|ARRAY| |表空间的 contentID 位置。|
