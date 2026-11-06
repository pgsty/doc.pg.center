---
title: "使用动态表加速查询并自动刷新数据"
linkTitle: "使用动态表"
description: "动态表是类似物化视图的数据库对象，可以自动刷新数据并加速查询。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/use-dynamic-tables.md"
---

Apache Cloudberry 引入动态表，以加快查询处理并自动更新数据。

动态表可以基于基表、外部表或物化视图创建。它们按照计划自动更新数据，使数据保持最新。

## 使用场景 {#use-cases}

动态表适用于以下场景：

- **加速湖仓环境中的查询**：以动态表查询替代外部表查询，提高性能。
- **自动更新数据**：安排刷新任务，无需人工操作即可保持数据更新。
- **实时分析**：适用于需要频繁查询最新数据的场景，例如财务分析或运营监控。

## 与物化视图的比较 {#comparison-with-materialized-views}

动态表与[使用物化视图回答查询](/cloudberry/performance/optimize-queries/use-auto-materialized-view-to-answer-queries/)有以下区别：

| **特性** | 动态表 | AQUMV |
|----------------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| **用途** | 一种自动刷新的特殊表，用于处理数据流水线并简化 ETL。 | 使用物化视图提高查询效率，并自动改写查询。 |
| **基础与结构** | 可以基于普通表、外部表和物化视图。 | 基于物化视图，通常面向单表。 |
| **查询改写** | 不支持 | 支持单表改写 |
| **数据刷新机制** | 用户可以通过 SQL 定义自动刷新间隔 | 需要手动刷新物化视图数据 |

## 用法 {#usage}

### 创建动态表 {#create-a-dynamic-table}

使用 `CREATE DYNAMIC TABLE` 语句创建动态表：

``` sql
CREATE DYNAMIC TABLE table_name AS <select_query> [WITH NO DATA] [SCHEDULE '<cron_string>'] [DISTRIBUTED BY <distribution_key>];
```

参数说明：

- `<select_query>`：定义动态表所用的 SQL 查询。支持与基表、物化视图或其他动态表连接。
- `WITH NO DATA`：创建表时不填充初始数据。
- `SCHEDULE '<cron_string>'`：使用 Linux cron 表达式设置刷新计划。详情参见 [Cron 表达式](https://crontab.guru/)。
- `DISTRIBUTED BY`：定义分布键，以提高查询性能。

完整语法：

``` sql
CREATE DYNAMIC TABLE [ IF NOT EXISTS ] table_name
   [ (column_name [, ...] ) ]
   [ USING method ]
   [ WITH ( storage_parameter [= value] [, ... ] ) ]
   [ TABLESPACE tablespace_name ]
   [ SCHEDULE schedule_string ]
   AS query
   [ WITH [ NO ] DATA ]
   [ DISTRIBUTED BY (keys [, ...]) ];
```

示例：

``` sql
CREATE DYNAMIC TABLE dt0 SCHEDULE '5 * * * *' AS SELECT a, b, sum(c) FROM t1 GROUP BY a, b WITH NO DATA DISTRIBUTED BY(b);

\d dt0

             List of relations
Schema | Name |     Type      |  Owner  | Storage
--------+------+---------------+---------+---------
public | dt0  | dynamic table | gpadmin | heap
(1 rows)
```

本例创建动态表 `dt0`，并安排它每 5 分钟刷新一次。

### 刷新动态表 {#refresh-a-dynamic-table}

动态表根据 `SCHEDULE` 设置自动刷新。要手动刷新表，请使用 `REFRESH DYNAMIC TABLE` 语句。将 `table_name` 替换为实际表名：

``` sql
REFRESH DYNAMIC TABLE table_name;
```

要清空表并使其不可读取，请使用 `WITH NO DATA` 选项。将 `table_name` 替换为实际表名：

``` sql
REFRESH DYNAMIC TABLE table_name WITH NO DATA;
```

### 查看调度信息 {#view-schedule-information}

使用 `pg_get_dynamic_table_schedule` 函数查看动态表的刷新计划。将 `table_name` 替换为实际表名：

``` sql
SELECT pg_get_dynamic_table_schedule('table_name'::regclass::oid);
```

### 删除动态表 {#drop-a-dynamic-table}

要删除动态表及其关联的刷新任务，请使用 `DROP DYNAMIC TABLE` 语句。将 `table_name` 替换为实际表名：

``` sql
DROP DYNAMIC TABLE table_name;
```

### 查看分布键 {#view-distribution-key}

创建动态表时，可以指定分布键以优化查询性能。使用 `\d+` 命令查看分布键和查询定义。

示例：

``` sql
\d+ dt0
```

输出：

``` sql
Dynamic table "public.dt0"
Column |  Type   | Collation | Nullable | Default | Storage | Compression | Stats target | Description
--------+---------+-----------+----------+---------+---------+-------------+--------------+-------------
a      | integer |           |          |         | plain   |             |              |
b      | integer |           |          |         | plain   |             |              |
sum    | bigint  |           |          |         | plain   |             |              |
View definition:
SELECT t1.a,
   t1.b,
   sum(t1.c) AS sum
   FROM t1
   GROUP BY t1.a, t1.b;
Distributed by: (b)
Access method: heap
```

本例中，动态表 `dt0` 使用列 `b` 作为分布键。数据根据 `b` 分布到各节点，从而保障查询和聚合操作的效率。

## 示例 {#examples}

### 示例 1：加速湖仓架构中的外部表查询 {#example-1-accelerate-external-table-queries-in-lake-house-architecture}

处理数据湖或外部存储中的数据时，Apache Cloudberry 会自动将外部表查询替换为动态表查询，从而加快查询过程。

1. 创建可读外部表 `ext_r`，其数据来自指定文件 `dynamic_table_text_file.txt`。

    ``` sql
    CREATE READABLE EXTERNAL TABLE ext_r(id int)
       LOCATION('demoprot://dynamic_table_text_file.txt')
    FORMAT 'text';
    ```

    在上述创建外部表的语句中，`demoprot://dynamic_table_text_file.txt` 是示例协议和文件路径。

2. 使用 `EXPLAIN` 查看查询条件为 `id > 5` 的表查询执行计划。

    ``` sql
    EXPLAIN(COSTS OFF, VERBOSE)
    SELECT sum(id) FROM ext_r WHERE id > 5;
    ```

    查询计划输出如下。计划中出现了 `Foreign Scan on dynamic_table_schema.ext_r`，说明规划器直接扫描了外部表 `ext_r`。

    ``` sql
    QUERY PLAN
    --------------------------------------------------------------
    Finalize Aggregate
    Output: sum(id)
    ->  Gather Motion 3:1  (slice1; segments: 3)
          Output: (PARTIAL sum(id))
          ->  Partial Aggregate
                Output: PARTIAL sum(id)
                ->  Foreign Scan on dynamic_table_schema.ext_r
                      Output: id
                      Filter: (ext_r.id > 5)
    ```

3. 创建动态表 `dt_external`，存储从外部表 `ext_r` 过滤出的数据，并执行 `ANALYZE` 更新表统计信息。

    ``` sql
    CREATE DYNAMIC TABLE dt_external AS
    SELECT * FROM ext_r WHERE id > 5;
    ANALYZE dt_external;
    ```

4. 在事务中设置参数，启用动态表查询加速。

    ``` sql
    BEGIN;
    SET optimizer = OFF;
    SET LOCAL enable_answer_query_using_materialized_views = ON;
    SET LOCAL aqumv_allow_foreign_table = ON;
    ```

5. 再次使用 `EXPLAIN` 查看查询条件为 `id > 5` 的表查询执行计划。

    利用动态表自动替代外部表查询，将对外部表 `ext_r` 的查询替换为对动态表 `dt_external` 的查询，从而加速查询。

    ``` sql
    EXPLAIN(COSTS OFF, VERBOSE)
    SELECT sum(id) FROM ext_r WHERE id > 5;
    
    COMMIT;
    ```

    查询计划输出如下。其中的 `Seq Scan on dynamic_table_schema.dt_external` 表明，规划器已自动将外部表查询替换为对动态表 `dt_external` 的查询。

    ``` sql
    QUERY PLAN
    ---------------------------------------------------------------
    Finalize Aggregate
    Output: sum(id)
    ->  Gather Motion 3:1  (slice1; segments: 3)
          Output: (PARTIAL sum(id))
          ->  Partial Aggregate
                Output: PARTIAL sum(id)
                ->  Seq Scan on dynamic_table_schema.dt_external
                      Output: id
    Settings: enable_answer_query_using_materialized_views = 'on',
    optimizer = 'off'
    Optimizer: Postgres query optimizer
    (10 rows)
    ```

通过这一过程，原本需要扫描外部表的操作被扫描动态表取代，从而提高查询效率并缩短响应时间。

### 示例 2：创建空动态表 {#example-2-create-an-empty-dynamic-table}

1. 创建基表 `existing_table` 并插入数据：

    ``` sql
    CREATE TABLE existing_table (
       id INT,
       name VARCHAR(100),
       value INT
    );

    INSERT INTO existing_table (id, name, value) VALUES
    (1, 'Alice', 100),
    (2, 'Bob', 150),
    (3, 'Charlie', 200);
    ```

2. 创建空动态表：

    ``` sql
    CREATE DYNAMIC TABLE empty_table AS 
    SELECT * FROM existing_table 
    WITH NO DATA;
    ```

    此语句创建一个空动态表，之后可以通过手动刷新填充数据。

3. 检查该表是否为空：

    ``` sql
    SELECT * FROM empty_table;
    
    -- ERROR:  materialized view "empty_table" has not been populated
    -- HINT:  Use the REFRESH MATERIALIZED VIEW command.
    ```

## 注意事项 {#notes}

- 刷新策略：应设置合适的刷新间隔。刷新过于频繁可能增加系统负载；间隔过长则可能使查询到的数据不够及时。
- 查询替换：动态表的性能优势在于自动替代外部表查询，适用于经常需要读取外部表数据的查询场景。
- 数据一致性：动态表是一种物化视图，需要注意刷新策略与数据一致性之间的平衡，确保应用逻辑正确。
