---
title: "gp_stat_archiver"
description: "`gp_stat_archiver` 视图提供 Apache Cloudberry 集群中每个 Segment 的 WAL 归档进程信息。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-stat-archiver.md"
---

其中包括成功归档的 WAL 文件数量、最后一个已归档 WAL 文件的名称和归档时间、归档失败次数以及最近一次失败的详细信息等指标。此视图有助于监控和诊断整个集群的 WAL 归档情况。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`gp_segment_id`|integer| |Segment（或 Coordinator）实例的唯一标识符。|
|`archived_count`|bigint| |已成功归档的 WAL 文件数量。|
|`last_archived_wal`|text| |最近一次成功归档的 WAL 文件名称。|
|`last_archived_time `|timestamp with time zone| |最近一次成功归档操作的时间。|
|`failed_count`|bigint| |尝试归档 WAL 文件失败的次数。|
|`last_failed_wal`|timestamp with time zone| |最近一次归档失败的 WAL 文件名称。|
|`last_failed_time`|bigint| |最近一次归档失败的时间。|
|`stats_reset`|timestamp with time zone| |这些统计信息最后一次重置的时间。|

此系统视图的信息汇总在 `gp_stat_archiver_summary` 系统视图中。
