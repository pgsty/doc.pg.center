---
title: "pg_resourcetype"
description: "The `pg_resourcetype` system catalog table contains information about the extended attributes that can be assigned to Apache Cloudberry resource queues."
weight: 290
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resourcetype.md"
---

Each row details an attribute and inherent qualities such as its default setting, whether it is required, and the value to deactivate it (when allowed).

This table is populated only on the coordinator. This table is defined in the `pg_global` tablespace, meaning it is globally shared across all databases in the system.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |The object ID|
|`resname`|name| |The name of the resource type|
|`restypid`|smallint| |The resource type ID|
|`resrequired`|boolean| |Whether the resource type is required for a valid resource queue|
|`reshasdefault`|boolean| |Whether the resource type has a default value. When true, the default value is specified in reshasdefaultsetting.|
|`rescandisable`|boolean| |Whether the type can be removed or deactivated. When true, the default value is specified in resdisabledsetting.|
|`resdefaultsetting`|text| |Default setting for the resource type, when applicable|
|`resdisabledsetting`|text| |The value that deactivates this resource type (when allowed)|
