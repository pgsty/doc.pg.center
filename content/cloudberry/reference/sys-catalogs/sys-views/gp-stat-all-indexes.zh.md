---
title: "pg_stat_all_indexes"
description: "`pg_stat_all_indexes` 视图为当前数据库中的每个索引显示一行，其中包含对该索引的访问统计信息。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-stat-all-indexes.md"
---

`pg_stat_user_indexes` 和 `pg_stat_sys_indexes` 视图包含相同的信息，但经过筛选，分别仅显示用户索引和系统索引。

|列|类型|说明|
|------|----|-----------|
|`relid`|oid|此索引所属表的 OID|
|`indexrelid`|oid|此索引的 OID|
|`schemaname`|name|此索引所在模式的名称|
|`relname`|name|此索引所属表的名称|
|`indexrelname`|name|此索引的名称|
|`idx_scan`|bigint|所有 Segment 实例在此索引上发起的索引扫描总次数|
|`idx_tup_read`|bigint|对此索引进行扫描所返回的索引项数量|
|`idx_tup_fetch`|bigint|使用此索引进行简单索引扫描所获取的存活表行数|
