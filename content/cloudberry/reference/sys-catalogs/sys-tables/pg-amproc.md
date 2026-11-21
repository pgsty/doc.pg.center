---
title: "pg_amproc"
description: "The `pg_amproc` table in the `pg_catalog` schema stores information about support procedures associated with index access method operator classes."
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-amproc.md"
---

There is one row for each support procedure belonging to an operator class.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |Row identifier (hidden attribute; must be explicitly selected)|
|`amprocfamily`|oid|`pg_opfamily.oid`|The operator family this entry is for|
|`amproclefttype`|oid|`pg_type.oid`|Left-hand input data type of associated operator|
|`amprocrighttype`|oid|`pg_type.oid`|Right-hand input data type of associated operator|
|`amprocnum`|smallint| |Support procedure number|
|`amproc`|regproc|`pg_proc.oid`|OID of the procedure|
