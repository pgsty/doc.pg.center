---
title: "GPORCA 的限制"
description: "在 Apache Cloudberry 中使用默认 GPORCA 优化器时，存在一些限制。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-orca/gporca-limitations.md"
---

由于 GPORCA 尚不支持 Apache Cloudberry 的全部功能，目前它与基于 Postgres 的规划器在 Apache Cloudberry 中共存。

本节介绍这些限制。

- [不支持的 SQL 查询功能](#unsupported-sql-query-features)
- [性能下降](#performance-regressions)

## 不支持的 SQL 查询功能 {#unsupported-sql-query-features}

默认的 GPORCA 优化器不支持某些查询功能。运行不受支持的查询时，Cloudberry 会记录以下提示及查询文本：

```
Falling back to Postgres-based planner because GPORCA does not support the following feature: UTILITY command
```

启用 GPORCA（默认配置）时，不支持以下功能：

- SP-GiST 索引方法。GPORCA 仅支持 B-树、位图、GIN 和 GiST 索引，使用不受支持的方法创建的索引会被忽略。
- `SELECT` 命令的 `TABLESAMPLE` 子句。
- `SELECT` 命令的 `FROM` 子句中，函数调用的可选 `WITH ORDINALITY` 子句。
- 多级分区表。
- 非均匀分区表。
- SortMergeJoin（SMJ）。
- 有序聚合。
- 带多个参数、以 `DISTINCT` 限定的聚合，例如 `SELECT corr(DISTINCT a, b) FROM tbl1;`。
- 在生成空值的分组集规范中，使用重复别名指定多个分组集。此类查询会回退到基于 Postgres 的规划器，除非像下例那样直接将别名强制转换为独立变量：

    ```sql
    CREATE TEMP TABLE tempt AS SELECT i AS ai1, i AS ai2 FROM generate_series(1, 3)i;
    SELECT ai1, ai2 FROM tempt GROUP BY ai2, ROLLUP(ai1) ORDER BY ai1, ai2;
    ```

- 以下标量操作符：
    - ROW
    - ROWCOMPARE
    - FIELDSELECT
- 以集合操作符作为输入参数的聚合函数。
- 默认不支持多个以 Distinct 限定的聚合，例如 `SELECT count(DISTINCT a), sum(DISTINCT b) FROM foo`。可以通过配置参数 `optimizer_enable_multiple_distinct_aggs` 启用。
- `percentile_*` 窗口函数（有序集聚合函数）。
- 逆分布函数。
- 调用带 `ON COORDINATOR` 或 `ON ALL SEGMENTS` 属性的函数的查询。
- 表名等元数据名称包含 UNICODE 字符，且字符与主机系统区域设置不兼容的查询。
- 表名使用 `ONLY` 关键字限定的 `SELECT`、`UPDATE` 和 `DELETE` 命令。
- 按列指定排序规则。只有查询中的所有列使用相同的排序规则时，GPORCA 才支持排序规则。如果列使用不同的排序规则，Cloudberry 会使用基于 Postgres 的规划器。
- 外表上的 DML 和 `COPY ... FROM` 操作。

## 性能下降 {#performance-regressions}

已知启用 GPORCA 后，以下功能可能出现性能下降：

- 短查询——GPORCA 为确定最优查询执行计划而增加的优化能力，可能给运行时间很短的查询带来额外开销。
- ANALYZE——使用 GPORCA 时，ANALYZE 会为分区表生成根分区统计信息；使用基于 Postgres 的规划器时，不生成这些统计信息。
- DML 操作——GPORCA 的 DML 增强功能，包括支持更新分区键和分布键，可能需要额外开销。

此外，对旧版本已有功能的增强，也可能使 GPORCA 执行使用这些功能的 SQL 语句时需要更多时间。
