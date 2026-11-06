---
title: "堆表与 AO 表格式"
description: "Apache Cloudberry 支持两种存储模型：堆存储和追加优化（AO）存储。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/heap-and-ao-table-formats.md"
---

存储模型应根据数据类型和查询类型选择。本文介绍这两种存储模型，并为选择最优模型提供建议。

## 堆存储 {#heap-storage}

默认情况下，Apache Cloudberry 使用与 PostgreSQL 相同的堆存储模型。堆表存储最适合 OLTP 类工作负载，这类负载中的数据在初次加载后经常修改。`UPDATE` 和 `DELETE` 操作需要存储行级版本信息，以确保数据库事务处理的可靠性。堆表最适合维度表等较小的表，这些表在初次加载后经常更新。

## 追加优化存储 {#append-optimized-storage}

追加优化表（AO 表）存储最适合数据仓库环境中的反规范化事实表。反规范化事实表通常是系统中最大的表。事实表通常批量加载，并由只读查询访问。将大型事实表改用追加优化存储模型，可以省去每行更新可见性信息的存储开销，使页结构更加精简，也更容易优化。AO 表的存储模型针对批量数据加载进行了优化，不建议使用单行 `INSERT` 语句。

### 创建堆表 {#to-create-a-heap-table}

行存堆表是默认的存储类型。

```sql
=> CREATE TABLE foo (a int, b text) DISTRIBUTED BY (a);
```

使用 `CREATE TABLE` 命令的 `WITH` 子句声明表的存储选项。默认创建普通的行存堆表。例如，创建不压缩的 AO 表：

```sql
=> CREATE TABLE bar (a int, b text) 
    WITH (appendoptimized=true)
    DISTRIBUTED BY (a);
```

> [!NOTE] 注意
> 使用 `appendoptimized=value` 语法指定 AO 表存储类型。`appendoptimized` 只是旧存储选项 `appendonly` 的别名。Apache Cloudberry 在系统目录中存储的是 `appendonly`，列出 AO 表的存储选项时显示的也是它。

在可重复读或可串行化事务中，不允许对 AO 表执行 `UPDATE` 和 `DELETE`；执行这些操作会导致事务提前结束。

## 选择行存或列存 {#choose-row-or-column-oriented-storage}

Apache Cloudberry 提供行存、列存或两者结合的存储方式。本节给出为表选择合适存储方式的一般指导原则。请使用自己的数据和查询工作负载评估性能。

- 行存：适合包含大量反复执行的事务、且需要一次访问某一行中多列数据的 OLTP 类工作负载，检索效率较高。
- 列存：适合只对少数列进行聚合计算的数据仓库工作负载，也适合需要定期更新单列而不修改其他列数据的情况。

对于大多数通用或混合工作负载，行存能够最好地兼顾灵活性与性能。不过，在某些场景下，列存模型的 I/O 和存储效率更高。为表选择存储方式时，应考虑以下需求：

- **表数据更新。** 如果频繁加载和更新表数据，请选择行存堆表。只有 AO 表支持列存。

    更多信息请参阅[堆存储](#heap-storage)。

- **频繁插入。** 如果频繁向表中插入行，请考虑行存模型。列存表没有针对写入操作进行优化，因为一行中各列的值必须写入磁盘上的不同位置。
- **查询所需的列数。** 如果查询的 `SELECT` 列表或 `WHERE` 子句通常需要全部或大部分列，请考虑行存模型。列存表最适合对单列的大量值进行聚合、且 `WHERE` 或 `HAVING` 谓词也作用于该聚合列的查询。例如：

    ```sql
    SELECT SUM(salary)...
    ```

    ```sql
    SELECT AVG(salary)... WHERE salary > 10000
    ```

    或者，`WHERE` 谓词作用于单列，且返回的行数相对较少。例如：

    ```sql
    SELECT salary, dept ... WHERE state='CA'
    ```

- **表中的列数。** 如果需要同时访问多列，或表的行大小相对较小，行存的效率更高。如果表包含很多列，而查询只访问其中的一小部分，列存表可以提供更好的查询性能。
- **压缩。** 同一列的数据具有相同的数据类型，因此列存可以采用行存无法采用的存储空间优化方法。例如，许多压缩方案利用相邻数据的相似性进行压缩。不过，相邻数据的压缩程度越高，随机访问可能越困难，因为读取数据前必须先解压。

### 创建列存表 {#to-create-a-column-oriented-table}

`CREATE TABLE` 命令的 `WITH` 子句用于指定表的存储选项，默认创建行存堆表。采用列存的表必须是 AO 表。例如，创建列存表：

```sql
=> CREATE TABLE bar (a int, b text) WITH (appendoptimized=true, orientation=column) DISTRIBUTED BY (a);
```
