---
title: "窗口函数查询"
description: "窗口表达式允许应用程序开发人员使用标准 SQL 命令更轻松地组合复杂的在线分析处理（OLAP）查询。"
weight: 130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/window-functions.md"
---

例如，借助窗口表达式，用户可以计算不同时间间隔上的移动平均值或总和，在所选列值变化时重置聚合和排名，并用简单的方式表达复杂的比率。

窗口表达式表示将一个 `<window function>` 应用于一个 `<window frame>`，后者通过 `OVER()` 子句定义。这类似于使用聚合函数和 `GROUP BY` 子句进行的计算。聚合函数为每组行返回一个结果值，而窗口函数为每一行返回一个结果值；但窗口函数返回的值是根据该行所属窗口帧中的行集计算的。`OVER()` 子句允许将行划分为*分区*，然后通过指定分区中当前行之前或之后哪些行应纳入计算，进一步限制窗口帧。

Apache Cloudberry 不支持将窗口函数作为另一个窗口函数的参数。

窗口表达式的语法如下：

```sql
<window_function> ( [<expression> [, ...]] ) [ FILTER ( WHERE <filter_clause> ) ] OVER ( <window_specification> )
```

其中，`<window_function>` 可以是用户定义的窗口函数，`<expression>` 是不包含窗口表达式的任意值表达式，`<window_specification>` 的形式如下：

```sql
[<window_name>]
[PARTITION BY <expression> [, ...]]
[[ORDER BY <expression> [ASC | DESC | USING operator] [NULLS {FIRST | LAST}] [, ...]
[ <frame_clause> ]
```

可选的 `<frame_clause>` 可以是以下形式之一：

```sql
{ RANGE | ROWS | GROUPS } <frame_start> [ <frame_exclusion> ]
{ RANGE | ROWS | GROUPS } BETWEEN <frame_start> AND <frame_end> [ <frame_exclusion> ]
```

其中，`<frame_start>` 和 `<frame_end>` 可以是以下形式之一：

```sql
UNBOUNDED PRECEDING
<offset> PRECEDING
CURRENT ROW
<offset> FOLLOWING
UNBOUNDED FOLLOWING
```

`<frame_exclusion>` 可以是以下形式之一：

```sql
EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```

窗口表达式只能出现在 `SELECT` 命令的选择列表中。例如：

```sql
SELECT count(*) OVER(PARTITION BY customer_id), * FROM sales;
```

如果指定了 `FILTER`，则只有 `<filter_clause>` 求值为 true 的输入行才会传递给窗口函数；其他行会被丢弃。在窗口表达式中，`FILTER` 子句只能与作为聚合函数的 `<window_function>` 一起使用。

在窗口表达式中，该表达式必须包含 `OVER` 子句。`OVER` 子句指定窗口帧，即窗口函数要处理的行。它在语法上将该函数与普通函数或聚合函数区分开来。

在窗口表达式中使用的窗口聚合函数不支持带多个输入表达式的 `DISTINCT` 子句。

窗口定义具有以下特征：

- `PARTITION BY` 子句定义应用窗口函数的窗口分区。如果省略，则将整个结果集视为一个分区。
- `ORDER BY` 子句定义在窗口分区内对行排序所依据的表达式。窗口定义中的 `ORDER BY` 子句与普通查询表达式中的 `ORDER BY` 子句彼此独立且不同。对于计算排名的窗口函数，必须使用 `ORDER BY` 子句，因为它确定排名值所依据的指标。对于 OLAP 聚合，只有使用窗口帧（`ROWS`、`RANGE` 或 `GROUPS` 子句）时才要求使用 `ORDER BY` 子句。

> [!NOTE]
> 没有一致排序关系的数据类型（例如 `time`）的列，不适合用作窗口定义中的 `ORDER BY` 子句。无论是否指定时区，`Time` 都缺乏一致的排序关系，因为加法和减法不会产生预期效果。例如，以下表达式通常并不成立：`x::time < x::time + '2 hour'::interval`

- `<frame_clause>` 指定组成 `<window frame>` 的行集。对于作用于窗口帧而不是整个分区的窗口函数，窗口帧是当前分区的子集。窗口帧中的行集可能随当前行的变化而变化。窗口帧可以使用 `RANGE`、`ROWS` 或 `GROUPS` 模式指定；每种模式都从 `<frame_start>` 运行到 `<frame_end>`。如果省略 `<frame_end>`，其默认值为 `CURRENT ROW`。

- `<frame_start>` 为 `UNBOUNDED PRECEDING` 表示窗口帧从分区的第一行开始；同样，`<frame_end>` 为 `UNBOUNDED FOLLOWING` 表示窗口帧在分区的最后一行结束。

- 在 `RANGE` 或 `GROUPS` 模式下，`<frame_start>` 为 `CURRENT ROW` 表示窗口帧从当前行的第一条对等行开始（对等行是指窗口的 `ORDER BY` 子句将其排序为与当前行等价的行）；而 `<frame_end>` 为 `CURRENT ROW` 表示窗口帧在当前行的最后一条对等行结束。在 `ROWS` 模式下，`CURRENT ROW` 就表示当前行。

- 在 `<offset> PRECEDING` 和 `<offset> FOLLOWING` 窗口帧选项中，`<offset>` 必须是一个不包含变量、聚合函数或窗口函数的表达式。`<offset>` 的含义取决于窗口帧模式：
    - 在 `ROWS` 模式下，`<offset>` 必须生成非空的非负整数；该选项表示窗口帧在当前行之前或之后指定数量的行处开始或结束。
    - 在 `GROUPS` 模式下，`<offset>` 同样必须生成非空的非负整数；该选项表示窗口帧在当前行所属对等组之前或之后指定数量的对等组处开始或结束，其中对等组是指在 `ORDER BY` 排序中彼此等价的一组行。（窗口定义中必须有 `ORDER BY` 子句才能使用 `GROUPS` 模式。）
    - 在 `RANGE` 模式下，这些选项要求 `ORDER BY` 子句恰好指定一列。`<offset>` 指定当前行中该列的值与窗口帧中前置或后续行的该列值之间的最大差值。`<offset>` 表达式的数据类型取决于排序列的数据类型。对于数值排序列，它通常与排序列的类型相同；对于日期时间排序列，它是 `interval`。例如，如果排序列的类型是 `date` 或 `timestamp`，可以写成 `RANGE BETWEEN '1 day' PRECEDING AND '10 days' FOLLOWING`。`<offset>` 仍必须非空且非负，但“非负”的含义取决于其数据类型。
    在任何情况下，窗口帧末端的距离都受分区末端距离的限制，因此靠近分区两端的行，其窗口帧包含的行数可能少于其他位置。

- 请注意，在 `ROWS` 和 `GROUPS` 模式中，`0 PRECEDING` 和 `0 FOLLOWING` 等价于 `CURRENT ROW`。在 `RANGE` 模式中，对于合适的特定数据类型“零”含义，通常也成立。

- `<frame_exclusion>` 选项允许从窗口帧中排除当前行附近的行，即使根据窗口帧开始和结束选项这些行本应被包含。`EXCLUDE CURRENT ROW` 将当前行从窗口帧中排除。`EXCLUDE GROUP` 将当前行及其排序对等行从窗口帧中排除。`EXCLUDE TIES` 将当前行的所有对等行从窗口帧中排除，但不排除当前行本身。`EXCLUDE NO OTHERS` 只是明确指定默认行为，即不排除当前行或其对等行。

- 默认的窗口帧选项是 `RANGE UNBOUNDED PRECEDING`，这与 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` 相同。在有 `ORDER BY` 时，这会将窗口帧设置为从分区开头到当前行最后一条 `ORDER BY` 对等行的所有行。在没有 `ORDER BY` 时，这表示分区中的所有行都包含在窗口帧中，因为所有行都成为当前行的对等行。

- 限制包括：`<frame_start>` 不能是 `UNBOUNDED FOLLOWING`，`<frame_end>` 不能是 `UNBOUNDED PRECEDING`，并且 `<frame_end>` 的选项在上面列表中的位置不能早于 `<frame_start>` 的选项。例如，不允许使用 `RANGE BETWEEN CURRENT ROW AND value PRECEDING`。

## 窗口示例 {#window-examples}

以下示例展示如何将窗口函数与分区和窗口帧结合使用。

### 示例 1 – 分区上的聚合窗口函数 {#example-1--aggregate-window-function-over-a-partition}

`OVER` 子句中的 `PARTITION BY` 列表将具有指定表达式相同值的行划分为组或分区。

本示例将员工薪资与其所在部门的平均薪资进行比较：

```sql
SELECT depname, empno, salary, avg(salary) OVER(PARTITION BY depname)
FROM empsalary;
  depname  | empno | salary |          avg          
-----------+-------+--------+-----------------------
 develop   |     9 |   4500 | 5020.0000000000000000
 develop   |    10 |   5200 | 5020.0000000000000000
 develop   |    11 |   5200 | 5020.0000000000000000
 develop   |     7 |   4200 | 5020.0000000000000000
 develop   |     8 |   6000 | 5020.0000000000000000
 personnel |     5 |   3500 | 3700.0000000000000000
 personnel |     2 |   3900 | 3700.0000000000000000
 sales     |     1 |   5000 | 4866.6666666666666667
 sales     |     3 |   4800 | 4866.6666666666666667
 sales     |     4 |   4800 | 4866.6666666666666667
(10 rows)
```

前 3 个输出列来自 `empsalary` 表，并且表中的每一行对应一个输出行。第 4 列是根据与当前行具有相同 `depname` 值的所有行计算出的平均值。共享同一 `depname` 值的行构成一个分区；本示例中有三个分区。`avg` 函数与普通的 `avg` 聚合函数相同，但 `OVER` 子句使它作为窗口函数应用。

也可以将窗口定义放在 `WINDOW` 子句中，并在选择列表中引用它。下面的示例与前一个查询等价：

```sql
SELECT depname, empno, salary, avg(salary) OVER(mywindow)
FROM empsalary
WINDOW mywindow AS (PARTITION BY depname);
```

当选择列表中有多个窗口函数使用相同窗口定义时，定义一个命名窗口很有用。

### 示例 2 – 带 ORDER BY 子句的排名窗口函数 {#example-2--ranking-window-function-with-an-order-by-clause}

`OVER` 子句中的 `ORDER BY` 子句控制窗口函数处理行的顺序。窗口函数的 `ORDER BY` 列表不必与查询的输出顺序一致。本示例使用 `rank()` 窗口函数对各部门内的员工薪资进行排名：

```sql
SELECT depname, empno, salary,
    rank() OVER (PARTITION BY depname ORDER BY salary DESC)
FROM empsalary;
  depname  | empno | salary | rank 
-----------+-------+--------+------
 develop   |     8 |   6000 |    1
 develop   |    11 |   5200 |    2
 develop   |    10 |   5200 |    2
 develop   |     9 |   4500 |    4
 develop   |     7 |   4200 |    5
 personnel |     2 |   3900 |    1
 personnel |     5 |   3500 |    2
 sales     |     1 |   5000 |    1
 sales     |     4 |   4800 |    2
 sales     |     3 |   4800 |    2
(10 rows)
```

### 示例 3 – 行窗口帧上的聚合函数 {#example-3--aggregate-function-over-a-row-window-frame}

`RANGE`、`ROWS` 或 `GROUPS` 子句定义窗口帧，即窗口函数在计算中包含的分区内行集。`ROWS` 指定要处理的物理行集，例如从分区开头到当前行的所有行。

本示例使用 `sum()` 函数按部门计算员工薪资的累计总和，将从分区开头到当前行的行相加：

```sql
SELECT depname, empno, salary,
    sum(salary) OVER (PARTITION BY depname ORDER BY salary
        ROWS between UNBOUNDED PRECEDING AND CURRENT ROW)
FROM empsalary ORDER BY depname, sum;
  depname  | empno | salary |  sum  
-----------+-------+--------+-------
 develop   |     7 |   4200 |  4200
 develop   |     9 |   4500 |  8700
 develop   |    11 |   5200 | 13900
 develop   |    10 |   5200 | 19100
 develop   |     8 |   6000 | 25100
 personnel |     5 |   3500 |  3500
 personnel |     2 |   3900 |  7400
 sales     |     4 |   4800 |  4800
 sales     |     3 |   4800 |  9600
 sales     |     1 |   5000 | 14600
(10 rows)
```

### 示例 4 – 范围或组窗口帧上的聚合函数 {#example-4--aggregate-function-for-a-range-or-groups-window-frame}

`RANGE` 和 `GROUPS` 模式根据 `OVER` 子句中 `ORDER BY` 表达式的值指定逻辑值。本示例展示 `ROWS` 与 `RANGE` 或 `GROUPS` 的区别。窗口帧包含薪资值小于或等于当前行的所有行。与前一个示例不同，薪资相同的员工得到相同的总和，并且总和包含这些员工的全部薪资。

```sql
SELECT depname, empno, salary,
    sum(salary) OVER (PARTITION BY depname ORDER BY salary
        RANGE between UNBOUNDED PRECEDING AND CURRENT ROW)
FROM empsalary ORDER BY depname, sum;
  depname  | empno | salary |  sum  
-----------+-------+--------+-------
 develop   |     7 |   4200 |  4200
 develop   |     9 |   4500 |  8700
 develop   |    11 |   5200 | 19100
 develop   |    10 |   5200 | 19100
 develop   |     8 |   6000 | 25100
 personnel |     5 |   3500 |  3500
 personnel |     2 |   3900 |  7400
 sales     |     4 |   4800 |  9600
 sales     |     3 |   4800 |  9600
 sales     |     1 |   5000 | 14600
(10 rows)
```

在本示例中，由于 `<frame_start>` 和 `<frame_end>` 未使用 `<offset>`，`RANGE` 和 `GROUPS` 模式会产生相同结果：

```sql
SELECT depname, empno, salary,
    sum(salary) OVER (PARTITION BY depname ORDER BY salary
        GROUPS between UNBOUNDED PRECEDING AND CURRENT ROW)
FROM empsalary ORDER BY depname, sum;
  depname  | empno | salary |  sum
-----------+-------+--------+-------
 develop   |     7 |   4200 |  4200
 develop   |     9 |   4500 |  8700
 develop   |    11 |   5200 | 19100
 develop   |    10 |   5200 | 19100
 develop   |     8 |   6000 | 25100
 personnel |     5 |   3500 |  3500
 personnel |     2 |   3900 |  7400
 sales     |     4 |   4800 |  9600
 sales     |     3 |   4800 |  9600
 sales     |     1 |   5000 | 14600
(10 rows)
```

### 示例 5 – 范围和组窗口帧上的聚合函数 {#example-5--aggregate-function-for-a-range-and-a-groups-window-frame}

本示例展示 `RANGE` 与 `GROUPS` 的区别。`sales` 表列出了某家公司两家商店在四天期间的销售额。

使用 `GROUPS` 模式时，`<offset>` 的值表示当前行所属对等组之前的对等组数量。不同的对等组由 `ORDER BY` 子句确定，在此例中是日期。由于查询未指定 `<frame_end>` 的值，末端默认值为 `CURRENT ROW`。

```sql
SELECT date, shop, total, sum(total) OVER (PARTITION BY shop ORDER BY date asc GROUPS 2 PRECEDING) 
FROM sales ORDER BY shop, date;
    date    |  shop  |  total  |   sum    
------------+--------+---------+----------
 2022-01-07 | Shop 1 | 3000.00 |  3000.00
 2022-01-08 | Shop 1 | 1000.00 |  4000.00
 2022-01-09 | Shop 1 | 5000.00 | 11000.00
 2022-01-09 | Shop 1 | 2000.00 | 11000.00
 2022-01-07 | Shop 2 | 4000.00 | 10000.00
 2022-01-07 | Shop 2 | 6000.00 | 10000.00
 2022-01-09 | Shop 2 | 7000.00 | 21000.00
 2022-01-09 | Shop 2 | 4000.00 | 21000.00
 2022-01-10 | Shop 2 | 2000.00 | 23000.00
(9 rows)
```

要在 `RANGE` 模式下获得等价结果，`<frame_clause>` 必须指定一个使用与排序列相同数据类型的 `<offset>`，此处为 `date`。使用数值 `2` 将返回错误。

```sql
SELECT date, shop, total, sum(total) OVER (PARTITION BY shop ORDER BY date asc RANGE '2 days' PRECEDING) 
FROM sales ORDER BY shop, date;
    date    |  shop  |  total  |   sum    
------------+--------+---------+----------
 2022-01-07 | Shop 1 | 3000.00 |  3000.00
 2022-01-08 | Shop 1 | 1000.00 |  4000.00
 2022-01-09 | Shop 1 | 5000.00 | 11000.00
 2022-01-09 | Shop 1 | 2000.00 | 11000.00
 2022-01-07 | Shop 2 | 4000.00 | 10000.00
 2022-01-07 | Shop 2 | 6000.00 | 10000.00
 2022-01-09 | Shop 2 | 7000.00 | 21000.00
 2022-01-09 | Shop 2 | 4000.00 | 21000.00
 2022-01-10 | Shop 2 | 2000.00 | 13000.00
(9 rows)
```

请注意，上述输出在最后一行有所不同：`RANGE` 模式使用前两天的条目，而 Shop 2 在 `2022-01-08` 没有条目；`GROUPS` 模式则使用前两个对等组，即 `2022-01-07` 和 `2022-01-09`。
