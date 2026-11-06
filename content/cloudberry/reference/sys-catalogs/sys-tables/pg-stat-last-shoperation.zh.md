---
title: "pg_stat_last_shoperation"
description: "pg_stat_last_shoperation 表包含用于跟踪角色、表空间等全局对象的元数据信息。"
weight: 370
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-stat-last-shoperation.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`classid`|oid|pg_class.oid|包含此对象的系统目录的 OID|
|`objid`|oid|任意 OID 列|此对象在其系统目录中的 OID|
|`staactionname`|name| |对此对象执行的动作|
|`stasysid`|oid| |对此对象执行操作的角色 OID|
|`stausename`|name| |对此对象执行操作的角色名称|
|`stasubtype`|text| |操作的对象类型或所执行操作的子类型|
|`statime`|timestamp with timezone| |操作的时间戳。此时间戳与写入 Apache Cloudberry 服务器日志文件的时间戳相同，可据此在日志中查找操作的更多详细信息。|
