---
title: "pg_resgroupcapability"
description: "The `pg_resgroupcapability` system catalog table contains information about the capabilities and limits of defined Apache Cloudberry resource groups."
weight: 280
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resgroupcapability.md"
---

> [!NOTE]
> The `pg_resgroupcapability` system catalog table is valid only when resource group-based resource management is active.

You can join this table to the [pg_resgroup](/cloudberry/reference/sys-catalogs/sys-tables/pg-resgroup/) table by resource group object ID.

The `pg_resgroupcapability` table, defined in the `pg_global` tablespace, is globally shared across all databases in the system.

|column|type|references|description|
|------|----|----------|-----------|
|`resgroupid`|oid|`pg_resgroup.oid`|The object ID of the associated resource group.|
|`reslimittype`|smallint| |The resource group limit type:<br/><br/>1 - Concurrency<br/><br/>2 - CPU_MAX_WEIGHT<br/><br/>3 - CPU_WEIGHT<br/><br/>4 - CPUSET<br/><br/>5 - MEMORY_QUOTA<br/><br/>6 - MIN_COST<br/><br/>7 - IO_LIMIT|
|`value`|opaque type| |The specific value set for the resource limit referenced in this record. This value has the fixed type `text`, and will be converted to a different data type depending upon the limit referenced.|
