---
title: "pg_stat_database_conflicts"
description: "`pg_stat_database_conflicts` 视图提供 PostgreSQL 备库上因恢复冲突而取消查询的统计信息。"
weight: 220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-database-conflicts.md"
---

每一行对应一个数据库，包含由各种冲突类型导致的取消次数，例如表空间被删除、锁超时、旧快照、缓冲区被钉住以及死锁。此视图有助于监控和诊断备库上与复制冲突有关的问题。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`datid`|oid| |数据库的 OID。|
|`datname`|name| |此数据库的名称。|
|`confl_tablespace`|bigint| |此数据库中因表空间被删除而取消的查询数量。|
|`confl_lock`|bigint| |此数据库中因锁超时而取消的查询数量。|
|`confl_snapshot`|bigint| |此数据库中因旧快照而取消的查询数量。|
|`confl_bufferpin`|bigint| |此数据库中因缓冲区被钉住而取消的查询数量。|
|`confl_deadlock`|bigint| |此数据库中因死锁而取消的查询数量。|
