---
title: "CLUSTER"
description: "根据索引在磁盘上对表进行物理重排序。"
weight: 480
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/cluster.md"
---

## 概要 {#synopsis}

```sql
CLUSTER <indexname> ON <table_name>

CLUSTER [VERBOSE] <table_name> [ USING <index_name> ]

CLUSTER [VERBOSE]
```

## 描述 {#description}

`CLUSTER` 指示 Apache Cloudberry 根据 `<index_name>` 所指定的索引对 `<table_name>` 所指定的表进行排序。该索引必须已经在 `<table_name>` 上定义。

Apache Cloudberry 仅对 B-树索引支持在追加优化表（AO 表）上执行 `CLUSTER` 操作。

> **注意** Apache Cloudberry 不支持对分区表执行 `CLUSTER`。

对表进行聚簇时，会根据索引信息在磁盘上对其进行物理重排序。聚簇是一次性操作：此后更新表时，这些更改不会被聚簇。也就是说，不会尝试按索引顺序存储新行或更新后的行。如果需要，可以通过再次发出该命令来定期重新聚簇。将表的 `FILLFACTOR` 存储参数设置为小于 100% 有助于在更新期间保持聚簇顺序，因为只要所在页上有足够的空间，更新后的行就会保留在同一页上。

使用此命令对表进行聚簇时，Apache Cloudberry 会记住该表是基于哪个索引聚簇的。`CLUSTER <table_name>` 形式会基于该表之前聚簇所用的同一个索引对其重新聚簇。可以使用 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 的 `CLUSTER` 或 `SET WITHOUT CLUSTER` 形式来设置今后的聚簇操作所使用的索引，或者清除任何先前的设置。不带任何参数的 `CLUSTER` 会对当前数据库中调用用户所拥有的所有先前已聚簇的表重新聚簇；如果由超级用户调用，则对所有这类表重新聚簇。这种形式的 `CLUSTER` 不能在事务块内运行。

对表进行聚簇时，会对其获取 `ACCESS EXCLUSIVE` 锁。这会阻止任何其他数据库操作（读和写）在该表上进行，直到 `CLUSTER` 完成。

## 参数 {#parameters}

**`index_name`**

索引的名称。

**`VERBOSE`**

在对每个表进行聚簇时打印进度报告。

**`table_name`**

表的名称（可以带模式限定）。

## 注解 {#notes}

如果所需的记录随机分布在磁盘上，数据库就必须在磁盘上来回寻道才能获取所请求的记录。如果这些记录存储得更紧凑，则从磁盘获取的过程更接近顺序读取。在随机访问表中单行的情况下，表中数据的实际顺序并不重要。但是，如果经常访问某些数据多于其他数据，并且有一个索引可以将它们分组在一起，那么使用 `CLUSTER` 会有好处。如果要从表中请求一段索引值范围，或者请求某个对应多行的索引值，`CLUSTER` 会有帮助，因为一旦索引确定了第一个匹配行所在的表页，其他所有匹配行很可能已经在同一个表页上，从而节省磁盘访问并加快查询。聚簇索引的一个好例子是建立在日期列上的索引，其中数据按日期顺序排列。针对特定日期范围的查询将产生有序的磁盘读取，从而利用更快的顺序访问。

`CLUSTER` 可以使用指定索引上的索引扫描对表重新排序，或者（如果索引是 B-树）使用顺序扫描后再排序。它会根据规划器代价参数和可用的统计信息，尝试选择更快的方法。

使用索引扫描时，会创建表的一个临时副本，其中包含按索引顺序排列的表数据。表上每个索引的临时副本也会同时创建。因此，磁盘上所需的可用空间至少应等于表大小与各索引大小之和。

使用顺序扫描和排序时，还会创建一个临时排序文件，因此临时空间需求的峰值最多可达表大小的两倍，再加上各索引的大小。这种方法通常比索引扫描方法更快，但如果磁盘空间需求无法接受，可以通过暂时将配置参数 enable_sort 设置为 `off` 来停用这一选择。

建议在聚簇之前将配置参数 maintenance_work_mem 设置为一个合理的较大值（但不要超过可专用于 `CLUSTER` 操作的内存量）。

由于查询优化器会记录有关表排序的统计信息，因此建议对刚刚聚簇的表运行 [ANALYZE](/cloudberry/reference/sql-stmts/analyze/)。否则，规划器可能会做出糟糕的查询计划选择。

由于 `CLUSTER` 会记住哪些索引已被聚簇，因此可以在第一次手动对想要聚簇的表进行聚簇，然后设置一个定期维护脚本，运行不带任何参数的 `CLUSTER`，使所需的表被定期重新聚簇。

## 示例 {#examples}

基于索引 `emp_ind` 对表 `employees` 聚簇：

```sql
CLUSTER emp_ind ON emp;
```

使用先前所用的同一个索引对 `employees` 表聚簇：

```sql
CLUSTER employees;
```

对数据库中所有先前已聚簇的表聚簇：

```sql
CLUSTER;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `CLUSTER` 语句。

## 另见 {#see-also}

[CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/)、[CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/)
