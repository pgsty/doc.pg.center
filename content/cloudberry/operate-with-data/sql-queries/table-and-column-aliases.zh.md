---
title: "表别名和列别名"
description: "可以为表和复杂的表引用指定临时名称，以便在查询的其余部分引用派生表。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/table-and-column-aliases.md"
---

这称为表别名。

要创建表别名，请写成：

```sql
FROM table_reference AS alias
```

或者：

```sql
FROM table_reference alias
```

`AS` 关键字是可选的冗余词。`alias` 可以是任意标识符。

表别名的一个典型用途是为较长的表名指定较短的标识符，使连接子句易于阅读。例如：

```sql
SELECT * FROM some_very_long_table_name s JOIN another_fairly_long_name a ON s.id = a.num;
```

就当前查询而言，别名会成为表引用的新名称——不能在查询的其他位置使用原始名称引用该表。因此，以下写法无效：

```sql
SELECT * FROM my_table AS m WHERE my_table.a > 5;    -- wrong
```

表别名主要是为了记法方便，但将表与自身连接时必须使用表别名。例如：

```sql
SELECT * FROM people AS mother JOIN people AS child ON mother.id = child.mother_id;
```

此外，如果表引用是子查询，则必须使用别名。

括号用于消除歧义。在以下示例中，第一个语句为 `my_table` 的第二个实例指定别名 b，但第二个语句为连接结果指定别名：

```sql
SELECT * FROM my_table AS a CROSS JOIN my_table AS b ...
SELECT * FROM (my_table AS a CROSS JOIN my_table) AS b ...
```

表别名还有另一种形式，可以同时为表的列和表本身指定临时名称：

```sql
FROM table_reference [AS] alias ( column1 [, column2 [, ...]] )
```

如果指定的列别名少于表的实际列数，则其余列不会重命名。这种语法对自连接或子查询尤其有用。

将别名应用于 `JOIN` 子句的输出时，别名会隐藏 `JOIN` 内部的原始名称。例如：

```sql
SELECT a.* FROM my_table AS a JOIN your_table AS b ON ...
```

是有效的 SQL，但：

```sql
SELECT a.* FROM (my_table AS a JOIN your_table AS b ON ...) AS c
```

无效；表别名 a 在别名 `c` 的外部不可见。