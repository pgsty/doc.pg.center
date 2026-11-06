---
title: "pg_auth_members"
description: "`pg_catalog` 模式中的 `pg_auth_members` 系统目录表显示角色之间的成员关系。"
weight: 160
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-auth-members.md"
---

允许任何不含环的关系集合。由于角色的作用域是整个系统，`pg_auth_members` 由 Apache Cloudberry 系统中的所有数据库共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`roleid`|oid|`pg_authid.oid`|上级（组）角色的 ID。|
|`member`|oid|`pg_authid.oid`|成员角色的 ID。|
|`grantor`|oid|`pg_authid.oid`|授予此成员资格的角色的 ID。|
|`admin_option`|boolean| |如果成员角色可以将成员资格授予其他角色，则为真。|
