---
title: "pg_type_encoding"
description: "The `pg_type_encoding` system catalog table contains the column storage type information."
weight: 440
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-type-encoding.md"
---

|column|type|modifers|storage|description|
|------|----|--------|-------|-----------|
|`typeid`|oid|not null|plain|Foreign key to [pg_attribute](/cloudberry/reference/sys-catalogs/sys-tables/pg-attribute/)|
|`typoptions`|ARRAY| |extended|The actual options|
