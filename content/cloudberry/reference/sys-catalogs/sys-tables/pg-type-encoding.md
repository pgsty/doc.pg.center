---
title: "pg_type_encoding"
description: "The `pg_type_encoding` system catalog table contains the column storage type information."
weight: 440
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-type-encoding.md"
---

|column|type|modifers|storage|description|
|------|----|--------|-------|-----------|
|`typeid`|oid|not null|plain|Foreign key to [pg_attribute](/cloudberry/reference/sys-catalogs/sys-tables/pg-attribute/)|
|`typoptions`|ARRAY| |extended|The actual options|
