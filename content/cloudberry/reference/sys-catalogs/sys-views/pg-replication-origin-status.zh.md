---
title: "pg_replication_origin_status"
description: "`pg_replication_origin_status` 视图提供复制源的进度信息，包括本地和远程日志序列号（LSN）。"
weight: 180
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-replication-origin-status.md"
---

此视图对于监控和管理逻辑复制同步至关重要。

|名称|类型|引用|说明|
|----|----|----------|-----------|
|`local_id`|oid|pg_replication_origin.roident|内部节点标识符。|
|`external_id`|text|pg_replication_origin.roname|外部节点标识符。|
|`remote_lsn`|pg_lsn| |数据已复制到的源节点 LSN。|
|`local_lsn`|pg_lsn| |复制到 remote_lsn 时对应的本节点 LSN。在使用异步提交时，用于在将数据持久化到磁盘之前刷出提交记录。|
