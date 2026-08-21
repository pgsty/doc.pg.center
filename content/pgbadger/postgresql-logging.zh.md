---
title: "PostgreSQL 日志配置"
linkTitle: "PostgreSQL 日志"
weight: 40
description: "为 pgBadger 配置查询日志、log_line_prefix、消息语言与运行统计"
icon: fa-solid fa-database
module: [PGBADGER]
categories: [任务]
aliases: [/docs/pgbadger/postgresql-logging/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger 只能报告 PostgreSQL 实际写入日志的信息。应先确定可解析的日志前缀与清晰的语句记录策略，再按需要加入检查点、锁、临时文件和自动清理等运行事件。

## 最小查询日志配置 {#minimum-query-logging}

若报告需要查询文本与执行耗时，请启用按时长记录语句：

```postgresql
log_min_duration_statement = 0
```

`0` 会记录每一条执行完毕的语句。繁忙服务器应使用更高的毫秒阈值来控制日志量；在生产环境使用较低阈值前，应先评估开销与存储增长。

若只需要耗时与查询数量，不需要查询文本，可使用：

```postgresql
log_min_duration_statement = -1
log_duration = on
```

需要“最慢查询”和“查询总耗时”报告时，应优先使用 `log_min_duration_statement`。

## 日志前缀的必需字段 {#required-prefix-fields}

自定义 `log_line_prefix` 必须同时包含：

- 一个时间字段：`%t`、`%m` 或 `%n`；
- 一个进程或会话字段：`%p` 或 `%c`。

最小的 `stderr` 前缀如下：

```postgresql
log_line_prefix = '%t [%p]: '
```

更实用的前缀还会记录用户、数据库、应用与客户端：

```postgresql
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

使用 syslog 作为目标时，时间与进程信息由 syslog 提供，对应前缀可写为：

```postgresql
log_line_prefix = 'user=%u,db=%d,app=%a,client=%h '
```

pgBadger 也支持另一种键顺序：

```postgresql
log_line_prefix = '%t [%p]: db=%d,user=%u,app=%a,client=%h '
```

如果前缀不属于 pgBadger 能自动识别的形式，请用 `--prefix` 传入与 `postgresql.conf` **完全一致**的值，不要在命令行中自行简化或改写。

## 建议记录的运行事件 {#recommended-event-settings}

按报告需求启用相应事件：

```postgresql
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

这些设置可能产生大量日志。尤其是 `log_temp_files = 0` 与 `log_autovacuum_min_duration = 0` 会记录每一个符合条件的事件，应根据工作负载和日志保留预算调整阈值。

## 保持服务端消息为英文 {#message-locale}

上游解析器识别英文 PostgreSQL 服务端消息。可使用：

```postgresql
lc_messages = 'en_US.UTF-8'
```

或：

```postgresql
lc_messages = 'C'
```

上游解析器不支持 `fr_FR.UTF-8` 等其他消息语言。

## 避免互相冲突的语句设置 {#statement-setting-conflicts}

不要同时启用 `log_min_duration_statement`、`log_duration` 和 `log_statement = 'all'`。同一次执行可能被重复记录，既会放大 pgBadger 统计值，也会显著增加日志量。

| 目标 | 建议设置 |
|---|---|
| 查询文本与耗时 | `log_min_duration_statement = 0` 或选定的阈值 |
| 仅统计耗时与次数 | `log_min_duration_statement = -1`，`log_duration = on` |
| 广泛记录全部语句 | 将 `log_statement` 视为独立的日志策略；用于 pgBadger 统计时不要把三项全部同时打开 |

重新加载 PostgreSQL 配置后，应先检查几条真实日志，再开始大规模分析。确认时间、进程/会话标识、用户、数据库、应用与客户端字段都符合选定格式。

