---
title: "pg_tablespace"
description: "The `pg_tablespace` system catalog table stores information about the available tablespaces."
weight: 410
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-tablespace.md"
---

Tables can be placed in particular tablespaces to aid administration of disk layout. Unlike most system catalogs, `pg_tablespace` is shared across all databases of a Cloudberry system: there is only one copy of `pg_tablespace` per system, not one per database.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |The object ID|
|`spcname`|name| |Tablespace name.|
|`spcowner`|oid|pg_authid.oid|Owner of the tablespace, usually the user who created it.|
|`spcacl`|ARRAY| |Tablespace access privileges.|
|`spcoptions`|ARRAY| |Tablespace contentID locations.|
