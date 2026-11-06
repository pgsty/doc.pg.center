---
title: "gp_stat_activity"
description: "`pg_stat_activity` 是一个集群级视图，显示每个主 Segment 的 `pg_stat_activity` 信息。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-stat-activity.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`gp_segment_id`|integer| |Segment（或 Coordinator）实例的唯一标识符。|
|`datid`|oid|pg_database.oid|数据库 OID|
|`datname`|name| |数据库名称|
|`pid`|integer| |此后端的进程 ID|
|`sess_id`|integer| |会话 ID|
| `leader_pid` | integer | |会话领导进程的进程 ID。|
|`usesysid`|oid|pg_authid.oid|登录此后端的用户的 OID|
|`usename`|name| |登录此后端的用户的名称|
|`application_name`|text| |连接到此后端的应用程序名称|
|`client_addr`|inet| |连接到此后端的客户端 IP 地址。如果此字段为空，表示客户端通过服务器机器上的 Unix 套接字连接，或这是 autovacuum 等内部进程。|
|`client_hostname`|text| |连接的客户端的主机名，由对 `client_addr` 的反向 DNS 查询得到。仅对于 IP 连接且启用 log_hostname 时，此字段才可能非空。|
|`client_port`|integer| |客户端与此后端通信所使用的 TCP 端口号；如果使用 Unix 套接字，则为 -1|
|`backend_start`|timestamptz| |后端进程的启动时间|
|`xact_start`|timestamptz| |事务开始时间|
|`query_start`|timestamptz| |查询开始执行的时间|
|`state_change`|timestampz| |`state` 最后一次更改的时间|
|`wait_event_type`|text| |后端正在等待的事件类型|
|`wait_event`|text| |如果后端当前正在等待，则为等待事件名称|
|`state`|text| |此后端当前的总体状态。可能的值包括：<br/><br/>- `active`：后端正在运行查询。<br/><br/>- `idle`：后端正在等待新的客户端命令。<br/><br/>- `idle in transaction`：后端处于事务中，但当前未运行查询。<br/><br/>- `idle in transaction (aborted)`：此状态类似于 idle in transaction，但事务中的某条语句引发了错误。<br/><br/>- `fastpath function call`：后端正在运行快速路径函数。<br/><br/>- `disabled`：如果在此后端中停用了 `track_activities`，则报告此状态。|
| `backend_xid` | xid | |此后端当前执行的事务的事务 ID（XID）（如果有）。|
|`backend_xmin`|xid| |此后端需要保留的最小事务 ID。|
|  `query_id` | bigint | |当前正在执行的查询的查询 ID。|
|`query`|text| |此后端最近一次查询的文本。如果 `state` 为 active，此字段显示当前运行的查询。在所有其他状态下，它显示最后运行的查询。|
| `backend_type` | text  |描述后端进程的类型（例如 "client backend"、"worker process"、"autovacuum worker"）。|
|`rsgid`|oid|pg_resgroup.oid|资源组 OID 或 `0`。|
|`rsgname`|text|pg_resgroup.rsgname|资源组名称或 `unknown`。|
