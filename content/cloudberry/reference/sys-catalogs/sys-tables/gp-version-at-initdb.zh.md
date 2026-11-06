---
title: "gp_version_at_initdb"
description: "`pg_catalog` 模式中的 `gp_version_at_initdb` 表在 Apache Cloudberry 系统的 Coordinator 和每个 Segment 上都有数据。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-version-at-initdb.md"
---

它标识首次初始化系统时使用的 Apache Cloudberry 版本。此表定义在 `pg_global` 表空间中，因此由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`schemaversion`|smallint| |模式版本号。|
|`productversion`|text| |产品版本号。|
