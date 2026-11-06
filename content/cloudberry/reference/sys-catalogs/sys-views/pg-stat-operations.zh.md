---
title: "pg_stat_operations"
description: "`pg_stat_operations` 视图显示对数据库对象（例如表、索引、视图或数据库）或全局对象（例如角色）执行的最后一次操作的详细信息。"
weight: 250
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-operations.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`classname`|text| |存储此对象记录的系统表在 `pg_catalog` 模式中的名称（`pg_class`=关系，`pg_database`=数据库，`pg_namespace`=模式，`pg_authid`=角色）|
|`objname`|name| |对象的名称。|
|`objid`|oid| |对象的 OID。|
|`schemaname`|name| |对象所在模式的名称。|
|`usestatus`|text| |对对象执行最后一次操作的角色的状态（`CURRENT`=系统中当前活动的角色，`DROPPED`=系统中已不存在的角色，`CHANGED`=系统中存在的角色名，但自上次执行操作以来已更改）。|
|`usename`|name| |对此对象执行操作的角色名称。|
|`actionname`|name| |对此对象执行的动作。|
|`subtype`|text| |操作的对象类型或所执行操作的子类型。|
|`statime`|timestamptz| |操作的时间戳。此时间戳与写入 Apache Cloudberry 服务器日志文件的时间戳相同，可据此在日志中查找操作的更多详细信息。|
