---
title: "pg_backend_memory_contexts"
description: "`pg_backend_memory_contexts` 系统视图显示与当前会话相连的服务器进程正在使用的所有内存上下文。"
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-backend-memory-contexts.md"
---

`pg_backend_memory_contexts` 为每个内存上下文显示一行。

|列|类型|说明|
|------|----|-----------|
| `gp_segment_id` | int4 |内存上下文的 Segment ID。|
|`name`|text|内存上下文的名称。|
|`ident`|text|内存上下文的标识信息。此字段会在 1024 字节处截断。|
|`parent`|text|此内存上下文的父上下文名称。|
|`level`|int4|在上下文树中与 `TopMemoryContext` 的距离。|
|`total_bytes`|int8|为此内存上下文分配的总字节数。|
|`total_nblocks`|int8|为此内存上下文分配的块总数。|
|`free_bytes`|int8|空闲空间，以字节为单位。|
|`free_chunks`|int8|空闲内存片的总数。|
|`used_bytes`|int8|已用空间，以字节为单位。|
