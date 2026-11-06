---
title: "pg_description"
description: "`pg_description` 系统目录表为各个数据库对象存储可选的描述（注释）。"
weight: 190
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-description.md"
---

可以使用 `COMMENT` 命令管理描述，并通过 `psql` 的 `\d` 元命令查看。`pg_description` 的初始内容提供了许多内置系统对象的描述。另见 [pg_shdescription](/cloudberry/reference/sys-catalogs/sys-tables/pg-shdescription/)，它对 Cloudberry 系统共享对象的描述提供类似功能。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`objoid`|oid|任意 OID 列|此描述所属对象的 OID。|
|`classoid`|oid|pg_class.oid|包含此对象的系统目录的 OID。|
|`objsubid`|integer| |对于表列的注释，此值为列号。对于其他所有对象类型，此列为零。|
|`description`|text| |用作对象描述的任意文本。|
