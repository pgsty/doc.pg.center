---
title: "pg_stat_last_shoperation"
description: "The pg_stat_last_shoperation table contains metadata tracking information about global objects (roles, tablespaces, etc.)."
weight: 370
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-stat-last-shoperation.md"
---

|column|type|references|description|
|------|----|----------|-----------|
|`classid`|oid|pg_class.oid|OID of the system catalog containing the object|
|`objid`|oid|any OID column|OID of the object within its system catalog|
|`staactionname`|name| |The action that was taken on the object|
|`stasysid`|oid| |The OID of the role that performed the operation in this object |
|`stausename`|name| |The name of the role that performed the operation on this object|
|`stasubtype`|text| |The type of object operated on or the subclass of operation performed|
|`statime`|timestamp with timezone| |The timestamp of the operation. This is the same timestamp that is written to the Apache Cloudberry server log files in case you need to look up more detailed information about the operation in the logs.|
