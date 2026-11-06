---
title: "带聚合表达式的查询"
description: "聚合表达式对查询选取的行应用聚合函数。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/aggregates-expressions.md"
---

聚合函数对一组值执行计算并返回单个值，例如该组值的总和或平均值。聚合表达式的语法形式如下之一：

- `aggregate_name(expression [ , ... ] ) [ FILTER ( WHERE filter_clause ) ]` — 对所有预期结果值非 null 的输入行执行操作。`ALL` 是默认值。
- `aggregate_name(ALL expression [ , ... ] ) [ FILTER ( WHERE filter_clause ) ]` — 与第一种形式的操作完全相同，因为 `ALL` 是默认值。
- `aggregate_name(DISTINCT expression [ , ... ] ) [ FILTER ( WHERE filter_clause ) ]` — 对输入行的所有不同非 null 值执行操作。
- `aggregate_name(*) [ FILTER ( WHERE filter_clause ) ]` — 对所有行执行操作，包括值为 null 和非 null 的行。通常，这种形式最适合 `count(*)` 聚合函数。

其中，`aggregate_name` 是之前定义的聚合（可能是模式限定的），`expression` 是不包含聚合表达式的任意值表达式。

例如，`count(*)` 得出输入行总数，`count(f1)` 得出 `f1` 非 null 的输入行数，`count(distinct f1)` 则得出 `f1` 的不同非 null 值数量。

如果指定了 `FILTER`，则只有 `filter_clause` 求值为 true 的输入行才会提供给聚合函数；其他行会被丢弃。例如：

```sql
SELECT
    count(*) AS unfiltered,
    count(*) FILTER (WHERE i < 5) AS filtered
FROM generate_series(1,10) AS s(i);
 unfiltered | filtered
------------+----------
         10 |        4
(1 row)
```

还可以添加自定义聚合函数。

Apache Cloudberry 提供 `MEDIAN` 聚合函数，该函数返回 `PERCENTILE_CONT` 结果的第五十百分位数；还为逆分布函数提供以下特殊聚合表达式：

```sql
PERCENTILE_CONT(<percentage>) WITHIN GROUP (ORDER BY <expression>)
```

```sql
PERCENTILE_DISC(<percentage>) WITHIN GROUP (ORDER BY <expression>)
```

目前只能将这两个表达式与关键字 `WITHIN GROUP` 一起使用。

#### 聚合表达式的限制 {#limitations-of-aggregate-expressions}

当前聚合表达式存在以下限制：

- Apache Cloudberry 不支持以下关键字：`ALL`、`DISTINCT` 和 `OVER`。
- 聚合表达式只能出现在 `SELECT` 命令的结果列表或 `HAVING` 子句中。其他子句（例如 `WHERE`）中禁止出现聚合表达式，因为这些子句在聚合结果形成之前按逻辑顺序求值。此限制适用于聚合所属的查询层级。
- 当聚合表达式出现在子查询中时，通常会对该子查询的行求值。如果聚合参数（以及 `filter_clause`，如果有）只包含外层级变量，则聚合属于最近的那个外层级，并对该查询的行求值。聚合表达式整体随后成为其所在子查询的外部引用，并在该子查询的每次求值中充当常量。仅可出现在结果列表或 ``HAVING`` 子句中的限制，适用于聚合出现所在的查询层级。
- Apache Cloudberry 不支持将聚合函数指定为另一个聚合函数的参数。
- Apache Cloudberry 不支持将窗口函数指定为聚合函数的参数。
