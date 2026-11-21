---
title: auto_explain
description: auto_explain 自动记录慢语句的执行计划，无需手动运行 EXPLAIN。
weight: 10
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/auto-explain.md
---

`auto_explain` 模块自动记录慢语句的执行计划，无需手动运行 `EXPLAIN`。

在 Apache Cloudberry 中，`auto_explain` 仅在 Coordinator 上的普通会话中生效。在 Segment 进程或 utility 模式连接中加载此库时，它不会执行任何操作，也不会定义其配置参数。除此之外，其行为与 PostgreSQL 的 `auto_explain` 模块相同。启用 `auto_explain.log_analyze` 时，记录的计划还包含从 Segment 收集的每个切片的执行统计信息。

## 加载模块 {#load-the-module}

Apache Cloudberry 的默认构建会构建并安装 `auto_explain`。它是一个库，不是扩展：它不提供 SQL 对象，无需为其运行 `CREATE EXTENSION`。

要将模块加载到单个会话中，以超级用户身份运行以下命令：

```sql
LOAD 'auto_explain';
```

要在所有会话中加载，将 `auto_explain` 加入 `session_preload_libraries` 或 `shared_preload_libraries`。更改 `shared_preload_libraries` 需要重启集群。预加载可以随时跟踪慢查询，代价是所有查询都会产生一定开销。

## 配置参数 {#configuration-parameters}

只有将 `auto_explain.log_min_duration` 设为 `-1` 之外的值，模块才会执行操作。只有超级用户可以更改这些参数。

| 参数 | 说明 |
|-----------|-------------|
| `auto_explain.log_min_duration` | 记录计划所需的最短语句执行时间，单位为毫秒，超过此时长才记录。`0` 记录所有计划。`-1`（默认值）关闭记录。 |
| `auto_explain.log_analyze` | 记录 `EXPLAIN ANALYZE` 输出，而非 `EXPLAIN` 输出。 |
| `auto_explain.log_buffers` | 记录缓冲区使用情况，仅当 `log_analyze` 开启时生效。 |
| `auto_explain.log_wal` | 记录 WAL 使用情况，仅当 `log_analyze` 开启时生效。 |
| `auto_explain.log_timing` | 收集每个节点的计时信息，仅当 `log_analyze` 开启时生效。 |
| `auto_explain.log_triggers` | 包含触发器统计信息，仅当 `log_analyze` 开启时生效。 |
| `auto_explain.log_verbose` | 记录 `EXPLAIN VERBOSE` 输出。 |
| `auto_explain.log_settings` | 记录影响查询规划且经过修改的配置参数。 |
| `auto_explain.log_format` | 输出格式：`text`、`xml`、`json` 或 `yaml`。 |
| `auto_explain.log_level` | 计划的日志级别。 |
| `auto_explain.log_nested_statements` | 记录函数内运行的语句。 |
| `auto_explain.sample_rate` | 每个会话中需处理的语句比例。 |

## 示例 {#example}

```sql
LOAD 'auto_explain';
SET auto_explain.log_min_duration = 0;
SET auto_explain.log_analyze = true;
SELECT count(*) FROM pg_class;
```

`SELECT` 语句的计划写入 Coordinator 日志。

## 模块文档 {#module-documentation}

各个配置参数的详细信息，参见 PostgreSQL 文档中的 [auto_explain](https://www.postgresql.org/docs/14/auto-explain.html)。
