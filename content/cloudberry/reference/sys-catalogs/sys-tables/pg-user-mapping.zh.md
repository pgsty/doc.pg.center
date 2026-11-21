---
title: "pg_user_mapping"
description: "`pg_user_mapping` 系统目录表存储本地用户到远程用户的映射。"
weight: 450
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-user-mapping.md"
---

查看此目录需要管理员权限。普通用户无法访问此目录，应改用 `pg_user_mappings` 视图。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID|
|`umuser`|oid|pg_authid.oid|被映射的本地角色的 OID；如果用户映射是公共映射，则为 0。|
|`umserver`|oid|pg_foreign_server.oid|包含此映射的外部服务器的 OID|
|`umoptions`|ARRAY| |用户映射专用选项，以“keyword=value”字符串表示。|
