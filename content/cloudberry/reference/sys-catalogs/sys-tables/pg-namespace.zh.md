---
title: "pg_namespace"
description: "`pg_namespace` 系统目录表存储名字空间。名字空间是 SQL 模式的底层结构：每个名字空间可以拥有独立的关系、类型等对象集合，而不会产生名称冲突。"
weight: 220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-namespace.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符（隐藏属性，必须显式选择）。|
|`nspname`|name| |名字空间的名称。|
|`nspowner`|oid|pg_authid.oid|名字空间的所有者。|
|`nspacl`|ARRAY| |由 `GRANT` 和 `REVOKE` 指定的访问权限。|
