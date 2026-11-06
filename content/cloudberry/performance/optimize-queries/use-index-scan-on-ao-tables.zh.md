---
title: "在 AO 表上使用 IndexScan"
description: "在 Apache Cloudberry 的 AO 表上使用索引扫描，加速选择性强的查询。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-index-scan-on-ao-tables.md"
---

Apache Cloudberry 支持在查询 AO 表时使用 IndexScan，以提高特定场景中的查询效率，例如以下查询：

```sql
SELECT * FROM tbl WHERE val > 100 ORDER BY val LIMIT 10;
```

> [!TIP]
> AO 表是一种针对批量插入场景优化的存储方式，适用于大数据分析、数据仓库等场景。向 AO 表插入新数据时，Apache Cloudberry 会将数据追加到表的末尾，而不像普通表那样寻找可用空间进行插入。这意味着向 AO 表插入数据只需对文件执行追加操作，因此插入效率更高。

对于上述查询语句：

- 如果使用堆表存储，Apache Cloudberry 会通过 IndexScan 查找 10 个 `val` 大于 `100` 的元组来执行查询。只需从索引和表中读取大约 10 个元组。
- 如果使用 AO 表存储，假设 `tbl` 表有 10 亿行元组，并通过 `LIMIT` 子句指定只返回 10 个元组：

    - Apache Cloudberry 支持使用 IndexScan 扫描 AO 表，可以大幅减少待扫描的数据量，显著提高扫描效率。这种扫描方式优于 SeqScan 和 BitmapScan。SeqScan 或 BitmapScan 扫描的数据量是 IndexScan 的 1 亿倍。

## 适用场景 {#applicable-scenarios}

此功能适用于查询大型表，并通过 `ORDER BY` 和 `LIMIT` 子句限制返回结果集大小的场景：

```sql
SELECT * FROM tbl WHERE val > 100 ORDER BY val LIMIT 10;
```

> [!NOTE]
> “大型表”是指表的数据量约为待查询数据量的 3000 倍。例如，使用 `LIMIT 10` 返回 10 条记录时，超过 30,000 条记录的表就可以视为大型表。

根据数据规模的不同，优化程度也有所不同。在最适合的场景中，原本需要执行几十分钟的查询可以在 1 秒内返回。

## 使用示例 {#usage-example}

要启用 AO IndexScan，需要运行 `SET optimizer TO off;` 禁用 GPORCA 优化器，并将系统参数 `gp_enable_ao_indexscan` 设为 `ON`。

以下示例中，未启用 AO IndexScan 时的执行时间为 5888.235 ms，远长于启用后的 15.462 ms。

```sql
SET optimizer TO off; -- To enable AO IndexScan, first disable the GPORCA optimizer.

-- Creates the test table, generates 100 million records of data, and builds index on the val column.
CREATE TABLE tbl (id int, val int) WITH (orientation='column', appendonly=true);
INSERT INTO tbl SELECT i, i FROM generate_series(1, 100000000) s(i);

-- Creates an index on the val column.
CREATE INDEX idx_val ON tbl(val);

-- Directly runs a query.
EXPLAIN ANALYZE SELECT * FROM tbl WHERE val > 100 ORDER BY val LIMIT 10;

(Execution Time: 5888.235 ms)


-- Runs the query again after enabling AO IndexScan.
SET gp_enable_ao_indexscan TO on;
EXPLAIN ANALYZE SELECT * FROM tbl WHERE val > 100 ORDER BY val LIMIT 10;

(Execution Time: 15.462 ms)
```

目前，此功能仅适用于 PostgreSQL 优化器。此外，某些机械硬盘的随机 I/O 效率可能比顺序 I/O 低 30,000 倍。在性能较差的机械硬盘上启用 AO IndexScan，其执行效率可能不尽如人意。
