---
title: "在 Apache Cloudberry 中插入、更新和删除行数据"
linkTitle: "插入、更新和删除行"
description: "在 Apache Cloudberry 中插入、更新和删除表行、截断表，并使用 VACUUM 回收存储空间。"
weight: 140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/insert-update-delete-rows.md"
---

本文介绍如何在 Apache Cloudberry 中操作行数据，包括：

- [插入行](#insert-rows)
- [更新现有行](#update-existing-rows)
- [删除行](#delete-rows)
- [截断表](#truncate-a-table)
- [清理数据库](#vacuum-the-database)

## 插入行 {#insert-rows}

使用 `INSERT` 命令在表中创建行。此命令需要表名以及表中每一列的值；也可以选择按任意顺序指定列名。如果不指定列名，请按照表中列的顺序列出数据值，并以逗号分隔。

例如，指定要插入的列名和值：
插入
```sql
INSERT INTO products (name, price, product_no) VALUES ('Cheese', 9.99, 1);
```

仅指定要插入的值：

```sql
INSERT INTO products VALUES (1, 'Cheese', 9.99);
```

通常，数据值是字面量（常量），但也可以使用标量表达式。例如：

```sql
INSERT INTO films SELECT * FROM tmp_films WHERE date_prod < 
'2016-05-07';
```

可以在一条命令中插入多行。例如：

```sql
INSERT INTO products (product_no, name, price) VALUES
    (1, 'Cheese', 9.99),
    (2, 'Bread', 1.99),
    (3, 'Milk', 2.99);
```

### 向分区表插入行 {#insert-rows-into-partitioned-tables}

要向分区表插入数据，应指定使用 `CREATE TABLE` 命令创建的根分区表。不支持在 `INSERT` 命令中直接指定叶子分区；这样做会导致错误，因为叶子分区对用户不可见，数据插入由数据库系统自动管理。

如果插入的数据不符合任何现有分区的范围（例如，指定的键值不匹配任何分区规则），则会返回错误。

要确保数据正确插入分区表，只需在 `INSERT` 语句中指定根分区表。数据库系统会根据分区键，自动将数据行插入相应的叶子分区。如果数据行不符合任何叶子分区的范围，数据库会返回错误。

示例：

```sql
-- Inserting data into the root partitioned table
INSERT INTO sales (sale_id, product_no, year, amount) VALUES (1, 'Cheese', 2021, 9.99);
```

上述语句会根据 year 列的值，自动将数据行插入正确的分区。不应也无需尝试在插入数据时直接指定任何叶子分区。

### 向 AO 表插入行 {#insert-rows-into-append-optimized-tables}

要插入大量数据，请使用外部表或 `COPY` 命令。插入大量行时，这些加载机制比 `INSERT` 更高效。

Apache Cloudberry 中 AO 表的存储模型旨在高效执行批量数据加载，而不是执行单行 `INSERT` 语句。对于大批量数据插入，建议使用 `COPY` 命令等批量加载方法。Apache Cloudberry 支持在 AO 表上并发执行多个 `INSERT` 事务；但这种能力通常用于批量插入，而不是单行操作。

## 更新现有行 {#update-existing-rows}

`UPDATE` 命令更新表中的行。可以更新表中的所有行、部分行或单个行。可以分别更新每一列，而不影响其他列。

要执行更新，需要：

- 要更新的表名和列名。
- 列的新值。
- 一个或多个用于指定要更新的行的条件。

例如，以下命令将所有价格为 *5* 的产品更新为价格 *10*：

```sql
UPDATE products SET price = 10 WHERE price = 5;
```

## 删除行 {#delete-rows}

`DELETE` 命令从表中删除行。指定 `WHERE` 子句可以删除符合特定条件的行。如果不指定 `WHERE` 子句，则删除表中的所有行。结果是一个有效但为空的表。例如，要从 products 表中删除价格为 *10* 的所有行：

```sql
DELETE FROM products WHERE price = 10;
```

要删除表中的所有行：

```sql
DELETE FROM products;
```

### 截断表 {#truncate-a-table}

使用 `TRUNCATE` 命令快速删除表中的所有行。例如：

```sql
TRUNCATE mytable;
```

此命令一次操作即可清空表中的所有行。请注意，在 Apache Cloudberry 中，即使不使用 `CASCADE` 选项，`TRUNCATE` 命令默认也会影响继承的子表。此外，由于 Apache Cloudberry 不支持外键约束，`TRUNCATE` 命令不会触发任何 `ON DELETE` 操作或重写规则。该命令只截断指定表中的行。

## 清理数据库 {#vacuum-the-database}

删除或更新的数据行会占用磁盘上的物理空间，即使新事务无法看到它们。定期运行 `VACUUM` 命令可以删除这些过期行。例如：

```sql
VACUUM mytable;
```

`VACUUM` 命令收集表级统计信息，例如行数和页数。加载数据后对所有表执行 VACUUM，包括 AO 表。

要维护 Apache Cloudberry 中的数据，需要使用 `VACUUM`、`VACUUM FULL` 和 `VACUUM ANALYZE` 命令；尤其是在数据库中的数据经常更新和删除时。

## 另请参见 {#see-also}

- [使用事务](/cloudberry/operate-with-data/work-with-transactions/)
- [事务并发控制](/cloudberry/operate-with-data/transactional-concurrency-control/)
