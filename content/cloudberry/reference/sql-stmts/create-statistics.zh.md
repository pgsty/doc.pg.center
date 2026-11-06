---
title: "CREATE STATISTICS"
description: "定义扩展统计信息。"
weight: 810
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-statistics.md"
---

## 概要 {#synopsis}

```sql
CREATE STATISTICS [ IF NOT EXISTS ] <statistics_name>
    [ ( <statistics_kind> [, ... ] ) ]
    ON <column_name>, <column_name> [, ...]
    FROM <table_name>
```

## 描述 {#description}

`CREATE STATISTICS` 创建新的扩展统计信息对象，跟踪指定表、外表或物化视图的数据。统计信息对象创建在当前数据库中，归发出命令的用户所有。

如果给出模式名（例如 `CREATE STATISTICS myschema.mystat ...`），则在指定模式中创建统计信息对象；否则在当前模式中创建。统计信息对象的名称必须不同于同一模式中其他统计信息对象的名称。

## 参数 {#parameters}

**`IF NOT EXISTS`**

如果同名统计信息对象已经存在，不报错；Apache Cloudberry 会发出一条提示。注意，此处只考虑统计信息对象的名称，不考虑其定义细节。

**`statistics_name`**

要创建的统计信息对象名称（可带模式限定）。

**`statistics_kind`**

此统计信息对象中要计算的统计信息种类。当前支持 `ndistinct`（启用不同值数量统计信息）、`dependencies`（启用函数依赖统计信息）和 `mcv`（启用最常见值列表）。如果省略此子句，统计信息对象将包含所有支持的统计信息种类。

**`column_name`**

计算统计信息时要涵盖的表列名称。必须指定至少两个列名，列名顺序无关紧要。

**`table_name`**

包含统计信息所针对列的表名称（可带模式限定）；继承和分区的处理方式见 [ANALYZE](/cloudberry/reference/sql-stmts/analyze/)。

## 注意事项 {#notes}

必须是表所有者才能创建读取该表的统计信息对象。不过，创建后统计信息对象的所有权与底层表的所有权相互独立。

## 示例 {#examples}

创建表 `t1`，其中两列之间存在函数依赖，即知道第一列的值就足以确定另一列的值。然后为这些列构建函数依赖统计信息：

```sql
CREATE TABLE t1 (
    a   int,
    b   int
);

INSERT INTO t1 SELECT i/100, i/500
                 FROM generate_series(1,1000000) s(i);

ANALYZE t1;

-- the number of matching rows will be drastically underestimated:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);

CREATE STATISTICS s1 (dependencies) ON a, b FROM t1;

ANALYZE t1;

-- now the row count estimate is more accurate:
EXPLAIN ANALYZE SELECT * FROM t1 WHERE (a = 1) AND (b = 0);
```

没有函数依赖统计信息时，规划器会假定两个 `WHERE` 条件相互独立，将它们的选择率相乘，从而得出过低的行数估计。有了这些统计信息，规划器就能识别 `WHERE` 条件中的冗余，不再低估行数。

创建表 `t2`，其中两列完全相关（包含相同数据），并为这些列创建 MCV 列表：

```sql
CREATE TABLE t2 (
    a   int,
    b   int
);

INSERT INTO t2 SELECT mod(i,100), mod(i,100)
                 FROM generate_series(1,1000000) s(i);

CREATE STATISTICS s2 (mcv) ON a, b FROM t2;

ANALYZE t2;

-- valid combination (found in MCV)
EXPLAIN ANALYZE SELECT * FROM t2 WHERE (a = 1) AND (b = 1);

-- invalid combination (not found in MCV)
EXPLAIN ANALYZE SELECT * FROM t2 WHERE (a = 1) AND (b = 2);
```

MCV 列表向规划器提供表中常见具体值的更详细信息，以及未出现在表中的值组合的选择率上界，使规划器在这两种情况下都能给出更好的估计。

## 兼容性 {#compatibility}

SQL 标准中没有 `CREATE STATISTICS` 语句。

## 另见 {#see-also}

[ALTER STATISTICS](/cloudberry/reference/sql-stmts/alter-statistics/), [DROP STATISTICS](/cloudberry/reference/sql-stmts/drop-statistics/)
