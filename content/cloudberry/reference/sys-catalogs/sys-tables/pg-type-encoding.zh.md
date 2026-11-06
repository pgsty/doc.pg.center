---
title: "pg_type_encoding"
description: "`pg_type_encoding` 系统目录表包含列的存储类型信息。"
weight: 440
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-type-encoding.md"
---

|列|类型|修饰符|存储|说明|
|------|----|--------|-------|-----------|
|`typeid`|oid|not null|plain|引用 [pg_attribute](/cloudberry/reference/sys-catalogs/sys-tables/pg-attribute/) 的外键|
|`typoptions`|ARRAY| |extended|实际选项|
