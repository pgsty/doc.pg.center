---
title: "pg_stat_bgwriter"
description: "`pg_stat_bgwriter` 视图提供后台写入进程的累积统计信息，该进程负责在后台将脏缓冲区写入磁盘。"
weight: 210
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-bgwriter.md"
---

此视图有助于监控后台写入进程的效率以及整体缓冲区管理情况。其中包括检查点期间写入的缓冲区数量、后台写入进程清理的缓冲区数量，以及后端进程直接写入的缓冲区数量等指标。这些统计信息有助于调优数据库性能以及了解写入活动的规律。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`checkpoints_timed`|bigint| |已执行的定时检查点数量。|
|`checkpoints_req`|bigint| |已执行的请求检查点数量。|
|`checkpoint_write_time`|double precision| |检查点处理过程中将文件写入磁盘所花费的总时间，以毫秒为单位。|
|`checkpoint_sync_time`|double precision| |检查点处理过程中将文件同步到磁盘所花费的总时间，以毫秒为单位。|
|`buffers_checkpoint`|bigint| |检查点期间写入的缓冲区数量。|
|`buffers_clean`|bigint| |后台写入进程写入的缓冲区数量。|
|`maxwritten_clean` | bigint| |后台写入进程因写入过多缓冲区而停止清理扫描的次数。|
|`buffers_backend`|  bigint| |后端直接写入的缓冲区数量。|
|`buffers_backend_fsync` | bigint| |后台写入进程因写入过多缓冲区而停止清理扫描的次数。|
|`buffers_alloc`|bigint| |已分配的缓冲区数量。|
|`stats_reset`|timestamp with time zone| |这些统计信息最后一次重置的时间。|
