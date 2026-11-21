---
title: "pg_backend_memory_contexts"
description: "The `pg_backend_memory_contexts` system view displays all of the memory contexts in use by the server process attached to the current session."
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-backend-memory-contexts.md"
---

`pg_backend_memory_contexts` contains one row for each memory context.

|column|type|description|
|------|----|-----------|
| `gp_segment_id` | int4 | The segment ID of the memory context.|
|`name`|text| The name of the memory context.|
|`ident`|text| Identification information of the memory context. This field is truncated at 1024 bytes.|
|`parent`|text| The name of the parent of this memory context.|
|`level`|int4| The distance from `TopMemoryContext` in context tree.|
|`total_bytes`|int8| The total number of bytes allocated for this memory context.|
|`total_nblocks`|int8| The total number of blocks allocated for this memory context.|
|`free_bytes`|int8| Free space in bytes.|
|`free_chunks`|int8| The total number of free chunks.|
|`used_bytes`|int8| Used space in bytes.|
