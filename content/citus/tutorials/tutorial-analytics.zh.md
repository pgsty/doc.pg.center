---
title: 分析与仪表盘
description: 使用 Citus 设计、导入、聚合和查询实时事件与时序数据。
weight: 20
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/tutorial-analytics?view=citus-14
upstream_ref: citus-14; 8445a2831f01
translation_status: translated
---

本指南介绍如何：（1）设计并分布事件流；（2）大规模导入；（3）执行低延迟分析；（4）汇总数据并清理过期数据；（5）使用近似去重计数（HLL）；（6）加入半结构化 JSONB 数据。

> [!NOTE]
> 本文假定你已经有正在运行的 Citus 集群（Azure Database for PostgreSQL 弹性集群或自建集群），并能访问 `psql`。如果还没有本地环境，请先阅读[快速入门](/citus/installation/getting-started/)。

## 1. 场景与架构 {#1-use-case-and-architecture}

实时仪表盘需要快速查询近期事件的切片和趋势，同时高效保留更长时间的历史数据。典型要求如下：

| 要求 | 挑战 | Citus 方法 |
| --- | --- | --- |
| 分钟级指标的低延迟 | 高速写入与频繁聚合 | 按租户或分区哈希分片，并在本地聚合 |
| 从分钟到数年的时间窗口图表 | 反复扫描大型原始表 | 预聚合的多粒度汇总表 |
| 控制成本 | 原始事件无限增长 | 保留窗口、汇总与分区 |
| 去重计数（访客/IP） | 精确计数成本高 | 概率型 HLL 草图 |
| 半结构化属性 | 模式频繁变更且列稀疏 | JSONB 与按需建立的索引 |

本文使用两个可以映射到同一设计的示例领域：HTTP 请求遥测与 GitHub 事件。你可以替换为自己的事件流和维度。

## 2. 基础事件模型 {#2-base-event-model}

示例使用类似 GitHub 的高吞吐事件流中的一部分数据。核心表是用户表与事件表：

```sql
CREATE TABLE github_users (
  user_id bigint PRIMARY KEY,
  url text,
  login text,
  avatar_url text,
  gravatar_id text,
  display_login text
);

CREATE TABLE github_events (
  event_id bigint,
  event_type text,
  event_public boolean,
  repo_id bigint,
  payload jsonb,
  repo jsonb,
  user_id bigint,
  org jsonb,
  created_at timestamp
);

CREATE INDEX event_type_index ON github_events (event_type);
CREATE INDEX payload_index ON github_events USING GIN (payload jsonb_path_ops);
```

### 选择分布列 {#choose-a-distribution-column}

选择高基数、访问均衡且经常出现在过滤条件中的列（这里是 `user_id`）。两张表都按它分布，可以实现连接与汇总的共置：

```sql
SELECT create_distributed_table('github_users',  'user_id');
SELECT create_distributed_table('github_events', 'user_id');
```

### 替代方案：HTTP 请求流 {#alternate-http-request-stream}

面向单站点仪表盘时，可使用 `site_id`：

```sql
CREATE TABLE http_request (
  site_id INT,
  ingest_time timestamptz DEFAULT now(),
  url text,
  request_region text,
  ip_address text,
  status_code int,
  response_time_msec int
);
SELECT create_distributed_table('http_request', 'site_id');
```

## 3. 加载数据 {#3-loading-data}

示例 CSV 导入（GitHub）：

```psql
\copy github_users  from 'users.csv'  with csv
\copy github_events from 'events.csv' with csv
```

## 4. 即时查询（原始层） {#4-immediate-querying-raw-layer}

```sql
-- count users
SELECT count(*) FROM github_users;

-- commits per minute (PushEvent)
SELECT date_trunc('minute', created_at) AS minute,
       sum((payload->>'distinct_size')::int) AS num_commits
FROM github_events
WHERE event_type = 'PushEvent'
GROUP BY minute
ORDER BY minute;

-- top repo creators
SELECT login, count(*)
FROM github_events ge
JOIN github_users  gu USING (user_id)
WHERE event_type = 'CreateEvent'
  AND payload @> '{"ref_type":"repository"}'
GROUP BY login
ORDER BY count(*) DESC
LIMIT 10;
```

## 5. 汇总设计（性能层） {#5-rollup-design-performance-layer}

仪表盘会反复按时间桶扫描原始事件表，因此需要引入按 1 分钟（也可按 1 小时或 1 天）的汇总表，并以相同的分布列与时间桶为键。

HTTP 示例汇总表（按分钟）：

```sql
CREATE TABLE http_request_1min (
  site_id INT,
  ingest_time timestamptz, -- truncated minute
  error_count INT,
  success_count INT,
  request_count INT,
  average_response_time_msec INT,
  CHECK (request_count = error_count + success_count),
  CHECK (ingest_time = date_trunc('minute', ingest_time))
);
SELECT create_distributed_table('http_request_1min', 'site_id');
CREATE INDEX ON http_request_1min (site_id, ingest_time);
```

### 汇总函数 {#rollup-function}

```plpgsql
CREATE TABLE latest_rollup (
  minute timestamptz PRIMARY KEY CHECK (minute = date_trunc('minute', minute))
);
INSERT INTO latest_rollup VALUES ('1901-01-01');

CREATE OR REPLACE FUNCTION rollup_http_request() RETURNS void LANGUAGE plpgsql AS $$
DECLARE
  curr_rollup_time timestamptz := date_trunc('minute', now() - interval '1 minute');
  last_rollup_time timestamptz := minute FROM latest_rollup;
BEGIN
  INSERT INTO http_request_1min (
    site_id, ingest_time, request_count,
    success_count, error_count, average_response_time_msec
  )
  SELECT site_id,
         date_trunc('minute', ingest_time),
         COUNT(*) request_count,
         SUM(CASE WHEN status_code BETWEEN 200 AND 299 THEN 1 ELSE 0 END) success_count,
         SUM(CASE WHEN status_code BETWEEN 200 AND 299 THEN 0 ELSE 1 END) error_count,
         SUM(response_time_msec) / COUNT(*) average_response_time_msec
  FROM http_request

    WHERE ingest_time <@ tstzrange(last_rollup_time, curr_rollup_time, '(]')
  GROUP BY 1,2;

  UPDATE latest_rollup SET minute = curr_rollup_time;
END;$$;
```

使用 cron 或 `pg_cron` 每分钟调度一次。

### 仪表盘查询（汇总层） {#dashboard-query-rollup-layer}

```sql
SELECT site_id, ingest_time AS minute, request_count,
       success_count, error_count, average_response_time_msec
FROM http_request_1min
WHERE ingest_time > date_trunc('minute', now()) - interval '5 minutes';
```

## 6. 数据保留与分区 {#6-data-retention-and-partitioning}

应用 TTL 策略限制存储使用量：

```sql
DELETE FROM http_request      WHERE ingest_time < now() - interval '1 day';
DELETE FROM http_request_1min WHERE ingest_time < now() - interval '1 month';
```

为加快清理，可在 Citus 哈希分片之上，再按 `ingest_time` 使用原生范围分区（见[时序数据](/citus/tutorials/tutorial-time-series/)）。

## 7. 近似去重计数 HLL {#7-approximate-distinct-counts-hll}

安装或启用 HLL（[Azure Database for PostgreSQL 灵活服务器](https://learn.microsoft.com/en-us/azure/postgresql/extensions/concepts-extensions-versions#hll)已提供）：

```sql
CREATE EXTENSION IF NOT EXISTS hll;
ALTER TABLE http_request_1min ADD COLUMN distinct_ip_addresses hll;
```

在汇总表的 `INSERT` 中加入：

```sql
 , hll_add_agg(hll_hash_text(ip_address)) AS distinct_ip_addresses
```

查询时间区间内的去重计数：

```sql
SELECT hll_cardinality(hll_union_agg(distinct_ip_addresses)) AS unique_ips
FROM http_request_1min
WHERE ingest_time > now() - interval '5 minutes';
```

## 8. 半结构化聚合 JSONB {#8-semi-structured-aggregations-jsonb}

加入按区域统计：

```sql
ALTER TABLE http_request_1min ADD COLUMN region_counters jsonb;
```

扩展汇总逻辑（时间窗口 + `jsonb_object_agg`）：

```sql
 , jsonb_object_agg(request_region, region_count) AS region_counters
FROM (
  SELECT *, count(*) OVER (
    PARTITION BY site_id, date_trunc('minute', ingest_time), request_region
  ) AS region_count
  FROM http_request
) h
```

仪表盘提取示例：

```sql
SELECT request_count,
       success_count,
       error_count,
       average_response_time_msec,
       COALESCE(region_counters->>'USA','0')::int AS us_visitors
FROM http_request_1min
WHERE ingest_time > now() - interval '5 minutes';
```

## 9. 运维 {#9-maintenance-and-operations}

| 任务 | 说明 |
| --- | --- |
| 分片再平衡 | 添加工作节点后执行 `SELECT citus_rebalance_start();`。 |
| 模式演进 | 协调节点上的标准 DDL 会传播；将汇总逻辑保存在版本化函数中。 |
| 监控 | 跟踪导入延迟（`now - latest_rollup.minute`）。 |
| 回填 | 临时扩大汇总窗口，避免 cron 任务重叠。 |
| 大租户或热点键 | 如果单个键占据主要负载，可考虑二次分片，或使用 `isolate_tenant_to_new_shard` 隔离。 |

## 10. 相关内容 {#10-related-content}

- [教程：时序数据](/citus/tutorials/tutorial-time-series/)
- [教程：多租户应用](/citus/tutorials/tutorial-multi-tenant/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
