---
title: "pg_stat_all_tables"
description: "`pg_stat_all_tables` 视图为当前数据库中的每个表（包括 TOAST 表）显示一行，其中包含对该表的访问统计信息。"
weight: 200
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-all-tables.md"
---

`pg_stat_user_tables` 和 `pg_stat_sys_table` 视图包含相同的信息，但经过筛选，分别仅显示用户表和系统表。

|列|类型|说明|
|------|----|-----------|
|`relid`|oid|表的 OID|
|`schemaname`|name|此表所在模式的名称|
|`relname`|name|此表的名称|
|`seq_scan`|bigint|所有 Segment 实例在此表上发起的顺序扫描总次数|
|`seq_tup_read`|bigint|顺序扫描获取的存活行数|
|`idx_scan`|bigint|所有 Segment 实例在此表上发起的索引扫描总次数|
|`idx_tup_fetch`|bigint|索引扫描获取的存活行数|
|`n_tup_ins`|bigint|插入的行数|
|`n_tup_upd`|bigint|更新的行数（包括 HOT 更新的行）|
|`n_tup_del`|bigint|删除的行数|
|`n_tup_hot_upd`|bigint|通过 HOT 更新的行数（即无需单独更新索引的行）|
|`n_live_tup`|bigint|存活行数的估计值|
|`n_dead_tup`|bigint|死亡行数的估计值|
|`n_mod_since_analyze`|bigint|自上次分析此表以来修改的行数的估计值|
|`last_vacuum`|timestamp with time zone|上次手动清理此表的时间（不计 `VACUUM FULL`）|
|`last_autovacuum`|timestamp with time zone|autovacuum 守护进程上次清理此表的时间|
|`last_analyze`|timestamp with time zone|上次手动分析此表的时间|
|`last_autoanalyze`|timestamp with time zone|autovacuum 守护进程上次分析此表的时间|
|`vacuum_count`|bigint|手动清理此表的次数（不计 `VACUUM FULL`）|
|`autovacuum_count`|bigint|autovacuum 守护进程清理此表的次数|
|`analyze_count`|bigint|手动分析此表的次数|
|`autoanalyze_count`|bigint|autovacuum 守护进程分析此表的次数|
