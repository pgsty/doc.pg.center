---
title: "在 Apache Cloudberry 中创建和管理表"
linkTitle: "创建和管理表"
description: "Apache Cloudberry 中的表与任何关系数据库中的表相似，但表行会分布到系统中的不同 Segment 上。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-tables.md"
---

创建表时，需要指定表的分布策略。

## 创建表 {#create-a-table}

`CREATE TABLE` 命令创建表并定义其结构。创建表时，需要定义：

- 表的列及其关联的数据类型。请参见[选择列数据类型](#choose-column-data-types)。
- 用于限制列或表可以包含的数据的表约束或列约束。请参见[设置表约束和列约束](#set-table-and-column-constraints)。
- 表的分布策略，该策略决定 Apache Cloudberry 如何在各 Segment 之间划分数据。
- 表在磁盘上的存储方式。
- 大型表的分区策略。

### 选择列数据类型 {#choose-column-data-types}

列的数据类型决定该列可以包含的数据值类型。选择占用空间尽可能小、同时能够容纳数据并能对数据形成最佳约束的数据类型。例如，对字符串使用字符数据类型，对日期使用 date 或 timestamp 数据类型，对数字使用数值数据类型。

对于包含文本数据的表列，请指定 `VARCHAR` 或 `TEXT` 数据类型。不建议指定 `CHAR` 数据类型。在 Apache Cloudberry 中，`VARCHAR` 或 `TEXT` 数据类型会将添加到数据中的填充（最后一个非空格字符之后添加的空格字符）视为有意义的字符，而 `CHAR` 数据类型不会。

使用能够容纳数值数据并为未来扩展留出空间的最小数值数据类型。例如，对于适合 `INT` 或 `SMALLINT` 的数据使用 `BIGINT` 会浪费存储空间。如果预计数据值会随时间增长，请考虑：在加载大量数据后从较小数据类型改为较大数据类型的代价很高。例如，如果当前数据值适合 `SMALLINT`，但很可能会增长，那么 `INT` 是更好的长期选择。

计划用于跨表连接的列应使用相同的数据类型。跨表连接通常使用一个表中的主键和另一个表中的外键。如果数据类型不同，数据库必须转换其中一种类型，才能正确比较数据值，这会增加不必要的开销。

### 设置表约束和列约束 {#set-table-and-column-constraints}

可以在列和表上定义约束，以限制表中的数据。Apache Cloudberry 对约束的支持与 PostgreSQL 相同，但存在一些限制，包括：

- `CHECK` 约束只能引用定义该约束的表。
- `UNIQUE` 和 `PRIMARY KEY` 约束必须与表的分布键以及分区键（如果有）兼容。

  > [!NOTE]
  > AO 表不允许使用 `UNIQUE` 和 `PRIMARY KEY` 约束，因为这些约束创建的 `UNIQUE` 索引不允许用于 AO 表。

- 允许使用 `FOREIGN KEY` 约束，但不会强制执行。
- 在分区表上定义的约束适用于整个分区表。不能在表的单个分区上定义约束。

#### 检查约束 {#check-constraints}

检查约束允许指定某列的值必须满足布尔（真值）表达式。例如，要求产品价格为正数：

```sql
=> CREATE TABLE products 
            ( product_no integer, 
              name text, 
              price numeric CHECK (price > 0) );
```

#### 非空约束 {#not-null-constraints}

非空约束指定某列不得取 null 值。非空约束总是作为列约束书写。例如：

```sql
=> CREATE TABLE products 
       ( product_no integer NOT NULL,
         name text NOT NULL,
         price numeric );
```

#### 唯一约束 {#unique-constraints}

唯一约束确保某列或一组列中包含的数据相对于表中的所有行都是唯一的。表必须是哈希分布表或复制表（不能是 `DISTRIBUTED RANDOMLY`）。如果表是哈希分布表，约束列必须与表的分布键相同，或是分布键的超集。例如：

```sql
=> CREATE TABLE products 
       ( product_no integer `UNIQUE`, 
         name text, 
         price numeric)
      DISTRIBUTED BY (product_no);
```

#### 主键 {#primary-keys}

主键约束是 `UNIQUE` 约束与 `NOT NULL` 约束的组合。表必须是哈希分布表（不能是 `DISTRIBUTED RANDOMLY`），主键列必须与表的分布键相同，或是分布键的超集。如果表有主键，则默认将该列（或列组）选作表的分布键。例如：

```sql
=> CREATE TABLE products 
       ( `product_no` integer `PRIMARY KEY`, 
         name text, 
         price numeric)
`      DISTRIBUTED BY (``product_no``)`;

```

#### 外键 {#foreign-keys}

不支持外键。可以声明外键，但不会强制执行参照完整性。

外键约束指定某列或一组列中的值必须与另一个表某行中出现的值匹配，从而维护两个相关表之间的参照完整性。Apache Cloudberry 的分布式表 Segment 之间无法执行参照完整性检查。

#### 排他约束 {#exclusion-constraints}

排他约束确保：如果使用指定操作符比较任意两行的指定列或表达式，则至少有一个操作符比较结果为 false 或 null。语法如下：

``` sql
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
) DISTRIBUTED REPLICATED;
```

与唯一约束类似，只有复制表，或分布键列属于约束的一部分时，才允许使用排他约束；并且分布键列必须使用与分布键哈希操作符类中相同的 `=` 操作符。

分区表不支持排他约束。

详情请参见 [`CREATE TABLE ... CONSTRAINT ... EXCLUDE`](/cloudberry/reference/sql-stmts/create-table/)。

添加排他约束会自动创建约束声明中指定类型的索引。