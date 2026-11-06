---
title: "pg_replication_slots"
description: "`pg_replication_slots` 视图列出数据库集群中当前存在的所有复制槽及其当前状态。"
weight: 190
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-replication-slots.md"
---

其中包括槽名称、类型（物理或逻辑）、关联的数据库、活动状态和 WAL 位置等信息。此视图对于监控复制槽使用情况以及确保复制行为正确至关重要。

|名称|类型|引用|说明|
|----|----|----------|-----------|
|`slot_name`|name| |复制槽在整个集群内的唯一标识符。|
|`plugin`|name| |包含此逻辑槽所用输出插件的共享对象的基本名称；物理槽为 null。|
|`slot_type`|text| |槽类型：physical 或 logical。|
|`datoid`|oid|pg_database.oid|此槽关联的数据库的 OID，或者 null。只有逻辑槽才有关联的数据库。|
|`database`|name|pg_database.datname|此槽关联的数据库的名称，或者 null。只有逻辑槽才有关联的数据库。|
|`temporary`|boolean| |如果这是临时复制槽，则为 true。临时槽不保存到磁盘，并在发生错误或会话结束时自动删除。|
|`active`|boolean| |如果此槽当前正在使用，则为 true。|
|`active_pid`|integer| |如果此槽当前正在使用，则为使用此槽的会话的进程 ID；如果未使用，则为 `NULL`。|
|`xmin`|xid| |此槽要求数据库保留的最旧事务。VACUUM 不能移除任何晚于该事务的事务所删除的元组。|
|`catalog_xmin`|xid| |此槽要求数据库保留的、影响系统目录的最旧事务。VACUUM 不能移除任何晚于该事务的事务所删除的目录元组。|
|`restart_ls`n|pg_lsn| |此槽的消费者可能仍需要的最旧 WAL 的地址（LSN），因此检查点不会自动移除这些 WAL。如果从未为此槽保留 LSN，则为 `NULL`。|
|`confirmed_flush_lsn`|pg_lsn| |逻辑槽的消费者已确认接收到的数据所对应的地址（LSN）。早于此位置的数据不再可用。物理槽为 NULL。|
| `wal_status` | text | |表示复制槽的 WAL 文件可用性。可能的值包括 `reserved`、`extended`、`unreserved` 和 `lost`，反映此槽当前的 WAL 保留状态。|
| `safe_wal_size` | bigint | |表示在此槽面临进入 `lost` 状态的风险之前，还可以写入的 WAL 数据量（以字节为单位）。零或空值表示风险迫近，或此槽已经丢失。|
| `two_phase` | boolean | |表示复制槽是否支持对已准备事务进行解码（两阶段提交）。对于启用两阶段解码的逻辑槽，此值为 `true`；对于物理槽，此值为 `false`。|
