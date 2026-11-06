---
title: "连接查询"
description: "在 Apache Cloudberry 中，`JOIN` 子句根据相关列值组合两个或多个表中的行。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/join-queries.md"
---

`JOIN` 子句是 `SELECT` 语句中 `FROM` 子句的一部分。

`JOIN` 子句的语法如下：

```sql
table1_name join_type table2_name [join_condition]
```

其中：

- `table1_name`、`table2_name`：要连接的表的名称。

- `join_type`：连接类型，可以是以下类型之一：

    - `[INNER] JOIN`
    - `LEFT [OUTER] JOIN`
    - `RIGHT [OUTER] JOIN`
    - `FULL [OUTER] JOIN`
    - `NATURAL JOIN`

- `join_condition`：可选条件，用于指定如何匹配两个表中的行。可以采用以下形式之一：

    - `ON <join_condition>`
    - `USING ( <join_column> [, ...] )`
    - `LATERAL`

> [!NOTE]
> 对于 `FULL JOIN` 查询，ORCA 优化器会根据成本估算自动在 `Merge Join` 和 `Hash Join` 之间选择，因此用户无需手动指定连接方法。

## 连接类型 {#join-types}

Apache Cloudberry 支持以下连接类型：

`INNER JOIN` 返回满足连接条件的两个表的行的交集。换句话说，它只返回两个表中都具有匹配值的行。如果在 `JOIN` 前省略 `INNER`，则默认为 `INNER JOIN`。

```sql
SELECT *
FROM table1
INNER JOIN table2
ON table1.column_name = table2.column_name;
```

### 左外连接 {#left-outer-join}

`LEFT OUTER JOIN`（或简称 `LEFT JOIN`）返回左表中的所有行以及右表中匹配的行。如果右表中没有匹配项，结果会为右表的列包含 `NULL` 值。

```sql
SELECT *
FROM table1
LEFT OUTER JOIN table2
ON table1.column_name = table2.column_name;
```

### 右外连接 {#right-outer-join}

`RIGHT OUTER JOIN`（或简称 `RIGHT JOIN`）与 `LEFT OUTER JOIN` 相反。它返回右表中的所有行以及左表中匹配的行。如果左表中没有匹配项，结果会为左表的列包含 `NULL` 值。

```sql
SELECT *
FROM table1
RIGHT OUTER JOIN table2
ON table1.column_name = table2.column_name;
```

> [!NOTE]
> 从 v2.0.0 开始，当满足分区剪枝条件时，`Hash Right Join` 查询也可以触发动态分区消除（DPE），从而减少分区扫描并提高性能。

### 全外连接 {#full-outer-join}

`FULL OUTER JOIN`（或简称 `FULL JOIN`）返回左表和右表中的所有行。对于左表中没有匹配项的行，右表列会填充 `NULL`。对于右表中没有匹配项的行，左表列会填充 `NULL`。

```sql
SELECT *
FROM table1
FULL OUTER JOIN table2
ON table1.column_name = table2.column_name;
```

### 交叉连接 {#cross-join}

`CROSS JOIN` 返回两个表的笛卡尔积。它将左表中的每一行与右表中的每一行组合。如果没有 `WHERE` 子句过滤结果，输出行数将等于左表行数乘以右表行数。

```sql
SELECT *
FROM table1
CROSS JOIN table2;
```

### 自然连接 {#natural-join}

`NATURAL` 子句是 `USING` 子句的进一步简写。当两个表中所有名称相同的列都应参与连接时，可以使用它。如果两个表中没有名称相同的列，`NATURAL JOIN` 的行为与 `CROSS JOIN` 相同。请谨慎使用 `NATURAL JOIN`，因为它依赖列名，可能产生意外结果。

```sql
SELECT *
FROM table1
NATURAL JOIN table2;
```

## 连接条件 {#join-conditions}

连接条件定义了如何匹配两个表中的行。连接条件有三种类型：

### ON 子句 {#on-clause}

`ON` 子句指定一个布尔表达式，用于确定两个表中的哪些行应被视为匹配。它的工作方式类似于 `WHERE` 子句，但专门应用于 `JOIN`。

```sql
SELECT *
FROM table1
JOIN table2
ON table1.column_name = table2.column_name;
```

### USING 子句 {#using-clause}

当两个表有一个或多个名称相同的列时，`USING` 子句是 `ON` 子句的简写形式。它指定用于连接的公共列。结果中每个匹配列只包含一个实例，而不是同时包含两份。

```sql
SELECT *
FROM table1
JOIN table2
USING (column_name);
```

## LATERAL {#lateral}

`LATERAL` 关键字可以放在 `FROM` 子句中的子查询前。它允许子查询引用 `FROM` 列表中位于它之前的项目。如果没有 `LATERAL`，Apache Cloudberry 会独立计算子查询，不允许引用其他 `FROM` 项。

## 示例 {#example}

假设有两个表：`customers` 和 `orders`。

`customers` 表：

```sql
customer_id | customer_name
------------+---------------
1           | John Doe
2           | Jane Smith
3           | Bob Johnson
```

`orders` 表：

```sql
order_id | customer_id | order_date
---------+-------------+------------
1        | 1           | 2023-01-15
2        | 2           | 2023-02-20
3        | 1           | 2023-03-10
4        | 4           | 2024-05-01
```

下面是使用不同 `JOIN` 类型的示例：

### INNER JOIN 示例 {#inner-join-example}

此查询返回所有客户及其订单，只包含客户 ID 在两个表中都匹配的行。

```sql
SELECT customers.customer_name, orders.order_id
FROM customers
INNER JOIN orders
ON customers.customer_id = orders.customer_id;
```

结果：

```sql
customer_name | order_id
--------------+----------
John Doe      | 1
Jane Smith    | 2
John Doe      | 3
```

### LEFT OUTER JOIN 示例 {#left-outer-join-example}

此查询返回所有客户及其订单。即使某个客户没有订单，也仍会包含该客户的信息。

```sql
SELECT customers.customer_name, orders.order_id
FROM customers
LEFT OUTER JOIN orders
ON customers.customer_id = orders.customer_id;
```

结果：

```sql
customer_name | order_id
--------------+----------
John Doe      | 1
Jane Smith    | 2
Bob Johnson   | NULL
John Doe      | 3
```

### RIGHT OUTER JOIN 示例 {#right-outer-join-example}

此查询返回所有订单以及下单的客户。即使某个订单没有关联客户，也仍会包含该订单。在此示例中，`order_id` 为 4 的订单没有匹配的客户。

```sql
SELECT customers.customer_name, orders.order_id
FROM customers
RIGHT OUTER JOIN orders
ON customers.customer_id = orders.customer_id;
```

结果：

```sql
customer_name | order_id
--------------+----------
John Doe      | 1
Jane Smith    | 2
John Doe      | 3
NULL          | 4
```

### FULL OUTER JOIN 示例 {#full-outer-join-example}

此查询返回所有客户和所有订单。如果某个客户没有订单，或某个订单没有客户，结果仍会包含该客户或订单。

```sql
SELECT customers.customer_name, orders.order_id
FROM customers
FULL OUTER JOIN orders
ON customers.customer_id = orders.customer_id;
```

结果：

```sql
customer_name | order_id
--------------+----------
John Doe      | 1
Jane Smith    | 2
Bob Johnson   | NULL
John Doe      | 3
NULL          | 4
```

### CROSS JOIN 示例 {#cross-join-example}

此查询返回 customers 和 orders 表的笛卡尔积。

```sql
SELECT customers.customer_name, orders.order_id
FROM customers
CROSS JOIN orders;
```

结果（部分输出；共 3 × 4 = 12 行）：

```sql
customer_name | order_id
--------------+----------
John Doe      | 1
John Doe      | 2
John Doe      | 3
John Doe      | 4
Jane Smith    | 1
Jane Smith    | 2
...
```
