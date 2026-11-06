---
title: "pg_resgroup"
description: "The `pg_resgroup` system catalog table contains information about Apache Cloudberry resource groups, which are used for managing concurrent statements, CPU, and memory resources."
weight: 270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resgroup.md"
---

> [!NOTE]
> The `pg_resgroup` system catalog table is valid only when resource group-based resource management is active.

This table, defined in the `pg_global` tablespace, is globally shared across all databases in the system.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |The object ID|
|`rsgname`|name| |The name of the resource group.|
|`parent`|oid| |Unused; reserved for future use.|
