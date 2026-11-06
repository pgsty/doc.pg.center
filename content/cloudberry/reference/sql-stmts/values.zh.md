---
title: "VALUES"
description: "计算一组行。"
weight: 1800
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/values.md"
---

## 语法概要 {#synopsis}

```sql
VALUES ( <expression> [, ...] ) [, ...]
   [ORDER BY <sort_expression> [ ASC | DESC | USING <operator> ] [, ...] ]
   [LIMIT { <count> | ALL } ] 
   [OFFSET <start> [ ROW | ROWS ] ]
   [FETCH { FIRST | NEXT } [<count> ] { ROW | ROWS } ONLY ]
```

## 说明 {#description}

`VALUES` 计算由值表达式指定的行值或一组行值。它最常用于在较大命令中生成“常量表”，但也可以独立使用。

指定多行时，所有行必须具有相同数量的元素。结果表各列的数据类型通过组合该列中各表达式显式指定或推断出的类型来确定，所用规则与 `UNION` 相同。

在较大的命令中，语法上凡是允许 `SELECT` 的地方都允许 `VALUES`。由于语法将它视为 `SELECT`，因此可以在 `VALUES` 命令中使用 `ORDER BY`、`LIMIT`（或等价的 `FETCH FIRST`）和 `OFFSET` 子句。

## 参数 {#parameters}

**`expression`**

要计算并插入到结果表（行集）指定位置的常量或表达式。在 `INSERT` 顶层出现的 `VALUES` 列表中，可以用 `DEFAULT` 替代表达式，表示应插入目标列的默认值。当 `VALUES` 出现在其他上下文中时，不能使用 `DEFAULT`。

**`sort_expression`**

表示如何对结果行排序的表达式或整数常量。该表达式可以用 `column1`、`column2` 等名称引用 `VALUES` 结果的列。详情请参见 [SELECT](/cloudberry/reference/sql-stmts/select/) 参数中的“ORDER BY 子句”。

**`operator`**

排序操作符。详情请参见 [SELECT](/cloudberry/reference/sql-stmts/select/) 参数中的“ORDER BY 子句”。

**`LIMIT count`**<br />
**`OFFSET start`**

要返回的最大行数。详情请参见 [SELECT](/cloudberry/reference/sql-stmts/select/) 参数中的“LIMIT 子句”。

## 注意事项 {#notes}

应避免包含大量行的 `VALUES` 列表，否则可能遇到内存不足错误或性能问题。出现在 `INSERT` 内的 `VALUES` 是特殊情况（因为所需列类型可从 `INSERT` 的目标表得知，无需扫描 `VALUES` 列表来推断），因此它可以处理比其他上下文中实际可用的列表更大的列表。

## 示例 {#examples}

独立的 `VALUES` 命令：

```sql
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

这将返回一个两列三行的表。它实际上等价于：

```sql
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

更常见的用法是在较大的 SQL 命令中使用 `VALUES`。最常用于 `INSERT`：

```sql
INSERT INTO films (code, title, did, date_prod, kind)
    VALUES ('T_601', 'Yojimbo', 106, '1961-06-16', 'Drama');
```

在 `INSERT` 上下文中，`VALUES` 列表项可以使用 `DEFAULT`，表示此处使用列默认值，而不指定具体值：

```sql
INSERT INTO films VALUES
    ('UA502', 'Bananas', 105, DEFAULT, 'Comedy', '82 
minutes'),
    ('T_601', 'Yojimbo', 106, DEFAULT, 'Drama', DEFAULT);
```

也可以在允许编写子 `SELECT` 的位置使用 `VALUES`，例如 `FROM` 子句中：

```sql
SELECT f.* FROM films f, (VALUES('MGM', 'Horror'), ('UA', 
'Sci-Fi')) AS t (studio, kind) WHERE f.studio = t.studio AND 
f.kind = t.kind;
UPDATE employees SET salary = salary * v.increase FROM 
(VALUES(1, 200000, 1.2), (2, 400000, 1.4)) AS v (depno, 
target, increase) WHERE employees.depno = v.depno AND 
employees.sales >= v.target;
```

请注意，与 `SELECT` 一样，在 `FROM` 子句中使用 `VALUES` 时必须提供 `AS` 子句。`AS` 子句不必指定所有列的名称，但这样做是良好实践。Apache Cloudberry 中 `VALUES` 的默认列名为 `column1`、`column2` 等，但其他数据库系统中的名称可能不同。

在 `INSERT` 中使用 `VALUES` 时，所有值会自动转换为相应目标列的数据类型。在其他上下文中使用时，可能需要指定正确的数据类型。如果所有条目都是用引号括起的字面常量，只需转换第一个，就能确定所有条目的假定类型：

```sql
SELECT * FROM machines WHERE ip_address IN 
(VALUES('192.168.0.1'::inet), ('192.168.0.10'), 
('192.0.2.43'));
```

> **注意** 对于简单的 `IN` 测试，使用 `IN` 的标量列表形式比编写上述 `VALUES` 查询更好。标量列表方式书写更少，通常也更高效。

## 兼容性 {#compatibility}

`VALUES` 符合 SQL 标准。`LIMIT` 和 `OFFSET` 是 Apache Cloudberry 的扩展；另请参见 [SELECT](/cloudberry/reference/sql-stmts/select/)。

## 另请参阅 {#see-also}

[INSERT](/cloudberry/reference/sql-stmts/insert/), [SELECT](/cloudberry/reference/sql-stmts/select/)
