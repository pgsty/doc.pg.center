---
title: "pg_resqueue"
description: "The `pg_resqueue` system catalog table contains information about Apache Cloudberry resource queues, which are used for the resource management feature."
weight: 300
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-resqueue.md"
---

> [!NOTE]
> The `pg_resqueue` system catalog table is valid only when resource queue-based resource management is active.

This table is populated only on the coordinator. This table is defined in the `pg_global` tablespace, meaning it is globally shared across all databases in the system.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |The object id|
|`rsqname`|name| |The name of the resource queue|
|`rsqcountlimit`|real| |The active query threshold of the resource queue|
|`rsqcostlimit`|real| |The query cost threshold of the resource queue|
|`rsqovercommit`|boolean| |Allows queries that exceed the cost threshold to run when the system is idle|
|`rsqignorecostlimit`|real| |The query cost limit of what is considered a 'small query'. Queries with a cost under this limit will not be queued and run immediately.|
