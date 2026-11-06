---
title: "pg_shdescription"
description: "`pg_shdescription` 系统目录表存储共享数据库对象的可选描述（注释）。"
weight: 350
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-shdescription.md"
---

可以使用 `COMMENT` 命令操作描述，并使用 `psql` 的 `d` 元命令查看描述。另请参阅 [pg_description](/cloudberry/reference/sys-catalogs/sys-tables/pg-description/)，它为单个数据库内的对象描述提供类似功能。与大多数系统目录不同，`pg_shdescription` 由 Cloudberry 系统中的所有数据库共享：每个系统只有一份 `pg_shdescription`，而不是每个数据库一份。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`objoid`|oid|任意 OID 列|此描述所属对象的 OID。|
|`classoid`|oid|pg_class.oid|此对象所在系统目录的 OID|
|`description`|text| |用作此对象描述的任意文本。|
