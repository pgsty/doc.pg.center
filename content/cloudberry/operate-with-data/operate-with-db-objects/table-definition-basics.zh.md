---
title: "定义表的基础知识"
description: "关系数据库中的表与纸面上的表格非常相似：由行和列组成。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/table-definition-basics.md"
---

列的数量和顺序是固定的，每一列都有名称。行数是可变的——它反映某个时刻存储的数据量。SQL 不保证表中行的顺序。读取表时，除非明确请求排序，否则行将以未指定的顺序出现。此外，SQL 不会为行分配唯一标识符，因此表中可能有多行完全相同的记录。

每一列都有数据类型。数据类型限定了可以赋给列的可能值集合，并为列中存储的数据赋予语义，使其可以用于计算。例如，声明为数值类型的列不会接受任意文本字符串，该列中存储的数据可以用于数学计算。相反，声明为字符字符串类型的列几乎可以接受任何类型的数据，但不适合数学计算，不过仍可执行字符串拼接等其他操作。

Apache Cloudberry 内置了大量适用于各种应用的数据类型。用户也可以定义自己的数据类型。大多数内置数据类型的名称和语义都很直观。常用数据类型包括用于整数的 `integer`、用于可能带小数的数字的 `numeric`、用于字符字符串的 `text`、用于日期的 `date`、用于一天中时间的 `time`，以及同时包含日期和时间的 `timestamp`。

要创建表，请使用名副其实的 [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/) 命令。在此命令中，至少要指定新表的名称、列的名称以及每列的数据类型。例如：

```sql
CREATE TABLE my_first_table (
    first_column text,
    second_column integer
);
```

此命令创建了一个名为 `my_first_table` 的表，其中包含两列。第一列名为 `first_column`，数据类型为 `text`；第二列名为 `second_column`，类型为 `integer`。表名和列名遵循 PostgreSQL 文档中[标识符和关键字](https://www.postgresql.org/docs/14/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)所述的标识符语法。类型名称通常也是标识符，但有一些例外。列列表以逗号分隔，并用圆括号括起。

通常，应为表和列指定能够表达其所存储数据类型的名称，例如：

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);
```

（`numeric` 类型可以存储小数部分，货币金额通常就是如此。）

> [!TIP]
> 创建许多相互关联的表时，最好为表和列选择一致的命名规则。例如，可以选择使用单数名词或复数名词作为表名。

Apache Cloudberry 限制表可以包含的列数。根据列类型的不同，上限介于 250 和 1600 之间。定义一个列数接近上限的表非常少见，通常也不是合理的设计。

如果不再需要某个表，可以使用 [`DROP TABLE`](/cloudberry/reference/sql-stmts/drop-table/) 命令将其删除。例如：

```sql
DROP TABLE my_first_table;
DROP TABLE products;
```

尝试删除不存在的表会产生错误。在 SQL 脚本文件中，通常会在创建每个表之前无条件地尝试删除它，并忽略错误消息，这样无论表是否存在，脚本都能运行。可以使用 `DROP TABLE IF EXISTS` 变体来避免错误消息，但这不是标准 SQL。

## 默认列值 {#default-column-values}

可以为列指定默认值。创建新行时，如果没有为某些列指定值，Apache Cloudberry 会为这些列赋予各自的默认值。数据操作命令也可以明确请求将某列设置为其默认值，而无需知道该值是什么。

如果没有为列明确声明默认值，则默认值为 null 值，可以将其视为未知数据。

在表定义中，将默认值写在列数据类型之后。例如：

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric DEFAULT 9.99
);
```

默认值可以是表达式，Apache Cloudberry 会在插入默认值时（而不是创建表时）计算该表达式。常见例子是为时间戳列指定 `CURRENT_TIMESTAMP` 默认值，使其被设置为行插入时的时间。另一个常见例子是为每一行生成“序列号”。在 Apache Cloudberry 中，可以这样做：

```sql
CREATE TABLE products (
    product_no integer DEFAULT nextval('products_product_no_seq'),
    ...
);
```

其中，`nextval()` 函数从序列对象中提供连续值。这种情况非常常见，因此有一种专用简写形式：

```sql
CREATE TABLE products (
    product_no SERIAL,
    ...
);
```

## 生成列 {#generated-columns}

生成列是一种特殊列，它始终根据其他列计算得出；对于列来说，它相当于表的视图。生成列有两种：存储生成列和虚拟生成列。存储生成列在写入（插入或更新）时计算，并像普通列一样占用存储空间。虚拟生成列不占用存储空间，而是在读取时计算。

虚拟生成列类似于视图，存储生成列类似于物化视图（但它总是自动更新）。Apache Cloudberry 目前只实现了存储生成列。

要创建生成列，请在 `CREATE TABLE` 中使用 `GENERATED ALWAYS AS` 子句，例如：

```sql
CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
);
```

必须指定关键字 `STORED` 来选择存储类型的生成列。更多信息请参见 [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/)。

不能直接写入生成列。在 `INSERT` 或 `UPDATE` 命令中，可以不为生成列指定值，但可以指定关键字 `DEFAULT`。

请注意，列默认值与生成列存在以下差异：

- 如果没有提供其他值，列默认值会在行首次插入时计算一次；生成列会在行发生变化时更新，且不能被覆盖。
- 列默认值不能引用表中的其他列；生成表达式通常会引用其他列。
- 列默认值可以使用易变函数，例如 `random()` 或引用当前时间的函数；Apache Cloudberry 不允许生成列使用这类函数。

生成列的定义以及涉及生成列的表有以下限制：

- 生成表达式只能使用不可变函数，不能使用子查询，也不能以任何方式引用当前行以外的内容。
- 生成表达式不能引用另一个生成列。
- 生成表达式不能引用系统列，但 `tableoid` 除外。
- 生成列不能有列默认值或标识定义。
- 生成列不能用作分布键。
- 生成列不能成为分区键的一部分。
- 可以在根分区表中指定生成列，但不能在子表中指定。

- 对于继承：

    - 如果父列是生成列，子列也必须是使用相同表达式的生成列。省略子列定义中的 `GENERATED` 子句；该子句会从父列复制。
    - 对于多重继承，如果一个父列是生成列，则所有父列都必须是生成列，并且使用相同的表达式。
    - 如果父列不是生成列，则可以将子列定义为生成列，也可以不定义为生成列。

使用生成列时还需考虑以下事项：

- 外表可以有生成列。详情请参见 [`CREATE FOREIGN TABLE`](/cloudberry/reference/sql-stmts/create-foreign-table/)。
- 生成列与其底层基列分别维护访问权限。因此，可以授予某个角色读取生成列的权限，而不授予其读取底层基列的权限。
- 从概念上说，生成列会在 `BEFORE` 触发器运行后更新。在 `BEFORE` 触发器中对基列所作的更改会反映到生成列中。但反过来，Apache Cloudberry 不允许 `BEFORE` 触发器访问生成列。
