---
title: "pg_stat_progress_copy"
description: "`pg_stat_progress_copy` 视图显示当前正在运行的 `COPY` 命令的进度。"
weight: 290
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-progress-copy.md"
---

每一行表示一个正在执行 `COPY` 操作的后端进程，提供命令类型（`COPY FROM` 或 `COPY TO`）、I/O 类型（例如 `FILE` 和 `PIPE`）、已处理的字节数和元组数，以及被排除或因错误而跳过的元组数等详情。此视图有助于监控长时间运行的 `COPY` 操作。

|列|类型|说明|
|------|----|-----------|
|`gp_segment_id`|integer|Segment（或 Coordinator）实例的唯一标识符。（`gp_stat_progress_copy_summary` 视图中没有此列。）|
| `pid` | integer |后端的进程标识符；在 `gp_stat_progress_copy_summary` 视图中，则为 Coordinator 进程标识符。|
| `datid` | oid |此后端所连接数据库的对象标识符。|
| `datname` | name |此后端所连接数据库的名称。|
| `relid` | oid |执行 `COPY` 命令的表的对象标识符。如果从 `SELECT` 查询复制，则设为 `0`。|
| `command` | text |正在运行的命令：`COPY FROM`、`COPY TO`、`COPY FROM ON SEGMENT` 或 `COPY TO ON SEGMENT`。|
| `type` | text |读取或写入数据的 I/O 类型：`FILE`、`PROGRAM`、`PIPE`（用于 `COPY FROM STDIN` 和 `COPY TO STDOUT`）或 `CALLBACK`（例如用于逻辑复制中的初始表同步）。|
| `bytes_processed` | bigint |`COPY` 命令已处理的字节数。|
| `bytes_total` | bigint |`COPY FROM` 命令的源文件大小，以字节为单位。如果不可用，则设为 `0`。|
| `tuples_processed` | bigint |`COPY` 命令已处理的元组数量。|
| `tuples_excluded` | bigint |因被 `COPY` 命令的 `WHERE` 子句排除而未处理的元组数量。|
