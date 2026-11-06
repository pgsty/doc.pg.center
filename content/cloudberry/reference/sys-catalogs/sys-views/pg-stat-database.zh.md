---
title: "pg_stat_database"
description: "`pg_stat_database` 视图提供集群中各数据库的累积统计信息。"
weight: 230
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-database.md"
---

其中包括已提交和已回滚的事务数量、磁盘块读取次数和缓存命中次数、返回或获取的元组数量，以及插入、更新和删除的行数等指标。此视图有助于监控数据库的整体活动和性能。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`gp_segment_id`|integer| |Segment（或 Coordinator）实例的唯一标识符。|
|`datid`|oid| |此数据库的 OID；对于属于共享关系的对象，为 0。|
|`datname`|name| |此数据库的名称；对于共享对象，为 NULL。|
|`numbackends`|integer| |当前连接到此数据库的后端数量；对于共享对象，为 NULL。这是此视图中唯一反映当前状态的列；其他所有列返回的都是自上次重置以来的累积值。|
|`xact_commit`|bigint| |此数据库中已提交的事务数量。|
|`xact_rollback`|bigint| |此数据库中已回滚的事务数量。|
|`blks_read`|bigint| |此数据库中读取的磁盘块数量。|
|`blks_hit`|bigint| |在缓冲区缓存中找到磁盘块而无需读取磁盘的次数（仅包括 PostgreSQL 缓冲区缓存中的命中，不包括操作系统的文件系统缓存）。|
|`tup_returned`|bigint| |此数据库中顺序扫描获取的存活行数与索引扫描返回的索引项数量之和。|
|`tup_fetched `|bigint| |此数据库中索引扫描获取的存活行数。|
|`tup_inserted`|bigint| |此数据库中查询插入的行数。|
|`tup_updated`|bigint| |此数据库中查询更新的行数。|
|`tup_deleted | bigint`|bigint| |此数据库中查询删除的行数。|
|`conflicts`|bigint| |此数据库中因与恢复发生冲突而取消的查询数量。|
|`temp_files`|bigint| |此数据库中查询创建的临时文件数量。所有临时文件都计入统计，不论创建原因（例如排序或哈希），也不受 `log_temp_files` 设置影响。|
|`temp_bytes`|bigint| |此数据库中查询写入临时文件的数据总量。所有临时文件都计入统计，不论创建原因，也不受 log_temp_files 设置影响。|
|`deadlocks`|bigint| |此数据库中检测到的死锁数量。|
|`checksum_failures`|bigint| |此数据库中（或共享对象上）检测到的数据页校验和失败次数；如果未启用数据校验和，则为 NULL。|
|`checksum_last_failure`|timestamp with time zone| |此数据库中（或共享对象上）上次检测到数据页校验和失败的时间；如果未启用数据校验和，则为 NULL。|
|`blk_read_time`|double precision| |此数据库中的后端读取数据文件块所花费的时间，以毫秒为单位（启用 track_io_timing 时才记录，否则为零）。|
|`session_time`|double precision| |此数据库中数据库会话花费的时间，以毫秒为单位（请注意，仅在会话状态发生变化时才更新统计信息，因此会话长时间空闲时，这段空闲时间不会计入）。|
|`active_time`|double precision| |此数据库中执行 SQL 语句花费的时间，以毫秒为单位（对应 pg_stat_activity 中的 active 和 fastpath function call 状态）。|
|`idle_in_transaction_time`|double precision| |此数据库中处于事务内空闲状态的时间，以毫秒为单位（对应 `gp_stat_activity` 中的 idle in transaction 和 idle in transaction (aborted) 状态）|
|`sessions`|bigint| |与此数据库建立的会话总数。|
|`sessions_abandoned`|bigint| |与此数据库建立的会话中，因客户端连接丢失而终止的会话数量。|
|`sessions_fatal`|bigint| |与此数据库建立的会话中，因致命错误而终止的会话数量。|
|`sessions_killed`|bigint| |与此数据库建立的会话中，因操作人员干预而终止的会话数量。|
|`stats_reset`|timestamp with time zone| |这些统计信息最后一次重置的时间。|
