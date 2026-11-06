---
title: "值表达式"
description: "值表达式是查询中用于计算、转换和引用数据的核心组成部分。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/value-expressions.md"
---

定义查询时，理解这些表达式是编写灵活、高效 SQL 的关键。

本文介绍列引用、位置参数、数组和行构造器、函数调用以及类型转换等表达式。这些表达式分别在查询结果的处理和表示中发挥特定作用。

## 列引用 {#column-references}

列引用的形式如下：

```sql
<correlation>.<columnname>
```

其中，`<correlation>` 是表的名称（可以带模式名限定），或者是在 `FROM` 子句中定义的表别名，也可以是关键字 `NEW` 或 `OLD`。`NEW` 和 `OLD` 只能出现在重写规则中，但其他关联名可以用于任何 SQL 语句。如果列名在查询涉及的所有表中都是唯一的，则可以省略列引用中的 `<correlation>` 部分。

## 位置参数 {#positional-parameters}

位置参数是 SQL 语句或函数的参数，通过它们在参数序列中的位置来引用。例如，`$1` 表示第一个参数，`$2` 表示第二个参数，依此类推。位置参数的值来自 SQL 语句外部提供的参数，或在调用 SQL 函数时提供的参数。某些客户端库支持将数据值与 SQL 命令分开指定，此时参数指的是 SQL 命令之外的数据值。参数引用的形式如下：

```sql
$number
```

例如：

```sql
CREATE FUNCTION dept(text) RETURNS dept
    AS $$ SELECT * FROM dept WHERE name = $1 $$
    LANGUAGE SQL;
```

这里，`$1` 在函数每次被调用时都引用第一个函数参数的值。

## 下标 {#subscripts}

如果一个表达式生成数组类型的值，可以按如下方式提取数组值中的特定元素：

```sql
<expression>[<subscript>]

```

可以提取多个相邻元素，这称为数组切片，形式如下（包括方括号）：

```sql
<expression>[<lower_subscript>:<upper_subscript>]

```

每个下标都是一个表达式，并生成一个整数值。

数组表达式通常必须放在圆括号中，但当要设置下标的表达式是列引用或位置参数时，可以省略圆括号。当原数组是多维数组时，可以连接多个下标。例如（包括圆括号）：

```sql
mytable.arraycolumn[4]
```

```sql
mytable.two_d_column[17][34]
```

```sql
$1[10:42]
```

```sql
(arrayfunction(a,b))[42]
```

## 字段选择 {#field-selection}

如果一个表达式生成复合类型（行类型）的值，可以按如下方式提取行中的特定字段：

```sql
<expression>.<fieldname>
```

行表达式通常必须放在圆括号中，但当要从中选择字段的表达式是表引用或位置参数时，可以省略这些圆括号。例如：

```sql
mytable.mycolumn
```

```sql
$1.somecolumn
```

```sql
(rowfunction(a,b)).col3
```

限定列引用是字段选择语法的一种特殊情况。

## 运算符调用 {#operator-invocations}

运算符调用可以采用以下语法：

```sql
<expression operator expression>(binary infix operator)
```

```sql
<operator expression>(unary prefix operator)
```

```sql
<expression operator>(unary postfix operator)
```

其中，`operator` 是运算符词元、关键字 `AND`、`OR` 或 `NOT` 之一，或者是形式如下的限定运算符名称：

```sql
OPERATOR(<schema>.<operatorname>)
```

可用的运算符以及运算符是一元还是二元，取决于系统或用户定义了哪些运算符。

## 函数调用 {#function-calls}

函数调用的语法是：函数名称（可以用模式名限定），后跟用圆括号括起的参数列表：

```sql
function ([expression [, expression ... ]])
```

例如，以下函数调用计算 2 的平方根：

```sql
sqrt(2)
```

## 类型转换 {#type-casts}

类型转换指定从一种数据类型到另一种数据类型的转换。对已知类型的值表达式应用类型转换，就是运行时类型转换。只有定义了适当的类型转换时，转换才会成功。这与对常量使用类型转换不同。对字符串字面量应用类型转换表示为字面量常量初始指定一种类型，因此只要字符串字面量的内容符合该数据类型可接受的输入语法，转换就会成功。

Apache Cloudberry 支持对值表达式应用以下三种类型转换：

- *显式类型转换* —— 当显式指定两种数据类型之间的转换时，Apache Cloudberry 会应用该转换。Apache Cloudberry 接受两种等价的显式类型转换语法：

    ```sql
    CAST ( expression AS type )
    expression::type
    ```

    `CAST` 语法符合 SQL 标准；使用 `::` 的语法是历史沿用的 PostgreSQL 用法。

- *赋值转换* —— 在赋值上下文中向目标数据类型的列赋值时，Apache Cloudberry 会隐式调用类型转换。例如，带有 `AS ASSIGNMENT` 子句的 [`CREATE CAST`](/cloudberry/reference/sql-stmts/create-cast/) 命令会创建一个在赋值上下文中隐式应用的转换。此赋值转换示例假定 `tbl1.f1` 是 `text` 类型的列。`INSERT` 命令之所以允许执行，是因为该值会从 `integer` 类型隐式转换为 `text` 类型。

    ```sql
    INSERT INTO tbl1 (f1) VALUES (42);
    ```

- *隐式转换* —— 在赋值或表达式上下文中，Apache Cloudberry 会隐式调用类型转换。例如，带有 `AS IMPLICIT` 子句的 `CREATE CAST` 命令会创建隐式转换，该转换会在赋值上下文和表达式上下文中自动应用。此隐式转换示例假定 `tbl1.c1` 是 `int` 类型的列。在谓词中进行计算时，`c1` 的值会从 `int` 类型隐式转换为 `decimal` 类型。

    ```sql
    SELECT * FROM tbl1 WHERE tbl1.c2 = (4.3 + tbl1.c1) ;
    ```

如果值表达式必须生成的类型没有歧义（例如，将其赋给表列时），通常可以省略显式类型转换；系统会自动应用类型转换。Apache Cloudberry 只会隐式应用系统目录中定义为赋值上下文或显式上下文的类型转换。其他类型转换必须使用显式类型转换语法调用，以防在用户不知情的情况下发生意外转换。

可以使用 `psql` 元命令 `dC` 显示类型转换信息。类型转换信息存储在目录表 `pg_cast` 中，类型信息存储在目录表 `pg_type` 中。

## 数组构造器 {#array-constructors}

数组构造器是一种表达式，它根据成员元素的值构造数组值。简单数组构造器由关键字 `ARRAY`、左方括号 `[`、一个或多个以逗号分隔的数组元素值表达式，以及右方括号 `]` 组成。例如：

```sql
SELECT ARRAY[1,2,3+4];
  array
---------
 {1,2,7}
```

数组元素类型是其成员表达式的公共类型，使用与 `UNION` 或 `CASE` 构造相同的规则确定。

通过嵌套数组构造器，可以构造多维数组值。在内部构造器中，可以省略关键字 `ARRAY`。例如，下面两个 `SELECT` 语句生成相同结果：

```sql
SELECT ARRAY[ARRAY[1,2], ARRAY[3,4]];
SELECT ARRAY[[1,2],[3,4]];
     array
---------------
 {{1,2},{3,4}}
```

这是因为多维数组必须是矩形的，同一级别的内部构造器必须生成维度相同的子数组。

多维数组构造器的元素不局限于子 `ARRAY` 构造；任何能够生成适当类型数组的表达式都可以作为元素。例如：

```sql
CREATE TABLE arr(f1 int[], f2 int[]);
INSERT INTO arr VALUES (ARRAY[[1,2],[3,4]], 
ARRAY[[5,6],[7,8]]);
SELECT ARRAY[f1, f2, '{{9,10},{11,12}}'::int[]] FROM arr;
                     array
------------------------------------------------
 {{{1,2},{3,4}},{{5,6},{7,8}},{{9,10},{11,12}}}
```

可以根据子查询的结果构造数组。数组构造器应使用关键字 `ARRAY`，后跟一个放在圆括号中的子查询。例如：

```sql
SELECT ARRAY(SELECT oid FROM pg_proc WHERE proname LIKE 'bytea%');
                          ?column?
-----------------------------------------------------------
 {2011,1954,1948,1952,1951,1244,1950,2005,1949,1953,2006,31}
```

子查询必须返回单列。生成的一维数组为子查询结果中的每一行包含一个元素，元素类型与子查询输出列的类型匹配。使用 `ARRAY` 构建的数组值，其下标始终从 `1` 开始。

## 行构造器 {#row-constructors}

行构造器是一种表达式，它根据成员字段的值构造行值（也称为复合值）。例如：

```sql
SELECT ROW(1,2.5,'this is a test');
```

行构造器使用 `rowvalue.*` 语法，该语法会展开为行值元素的列表，就像在 `SELECT` 列表顶层使用 `.*` 语法一样。例如，如果表 `t` 有列 `f1` 和 `f2`，以下查询等价：

```sql
SELECT ROW(t.*, 42) FROM t;
SELECT ROW(t.f1, t.f2, 42) FROM t;
```

默认情况下，`ROW` 表达式创建的值具有匿名 record 类型。如有必要，可以将其转换为命名的复合类型——可以是表的行类型，也可以是使用 `CREATE TYPE AS` 创建的复合类型。为避免歧义，需要时可以显式转换该值。例如：

```sql
CREATE TABLE mytable(f1 int, f2 float, f3 text);
CREATE FUNCTION getf1(mytable) RETURNS int AS 'SELECT $1.f1' 
LANGUAGE SQL;
```

在下面的查询中，由于只有一个 `getf1()` 函数，不存在歧义，因此不需要转换该值：

```sql
SELECT getf1(ROW(1,2.5,'this is a test'));
 getf1
-------
     1
CREATE TYPE myrowtype AS (f1 int, f2 text, f3 numeric);
CREATE FUNCTION getf1(myrowtype) RETURNS int AS 'SELECT 
$1.f1' LANGUAGE SQL;
```

现在需要使用类型转换来指示应调用哪个函数：

```sql
SELECT getf1(ROW(1,2.5,'this is a test'));
ERROR:  function getf1(record) is not unique
```

```sql
SELECT getf1(ROW(1,2.5,'this is a test')::mytable);
 getf1
-------
     1
SELECT getf1(CAST(ROW(11,'this is a test',2.5) AS 
myrowtype));
 getf1
-------
    11
```

可以使用行构造器构造复合值，将其存储在复合类型表列中，或将其传递给接受复合参数的函数。
