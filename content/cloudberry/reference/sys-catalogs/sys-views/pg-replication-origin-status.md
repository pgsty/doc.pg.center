---
title: "pg_replication_origin_status"
description: "The `pg_replication_origin_status` view provides information about the progress of replication origins, including the local and remote log sequence numbers (LSNs)."
weight: 180
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-replication-origin-status.md"
---

This view is essential for monitoring and managing logical replication synchronization.

|name|type|references|description|
|----|----|----------|-----------|
|`local_id`|oid|pg_replication_origin.roident|Internal node identifier.|
|`external_id`|text|pg_replication_origin.roname|External node identifier.|
|`remote_lsn`|pg_lsn| |The origin node's LSN up to which data has been replicated.|
|`local_lsn`|pg_lsn| |This node's LSN at which remote_lsn has been replicated. Used to flush commit records before persisting data to disk when using asynchronous commits.|
