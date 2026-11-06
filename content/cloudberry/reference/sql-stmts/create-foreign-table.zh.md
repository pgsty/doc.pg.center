---
title: "CREATE FOREIGN TABLE"
description: "定义新的外表。"
weight: 620
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-foreign-table.md"
---

## 语法概要 {#synopsis}

```sql
CREATE FOREIGN TABLE [ IF NOT EXISTS ] <table_name> ( [
  { <column_name> <data_type> [ OPTIONS ( <option> '<value>' [, ... ] ) ] [ COLLATE <collation> ] [ <column_constraint> [ ... ] ]
    | <table_constraint> }
    [, ... ]
] )
[ INHERITS ( <parent_table> [, ... ] ) ]
  SERVER <server_name>
  [ OPTIONS ( [ mpp_execute { 'coordinator' | 'any' | 'all segments' } [, ] ] <option> '<value>' [, ... ] ) ]

CREATE FOREIGN TABLE [ IF NOT EXISTS ] <table_name>
  PARTITION OF <parent_table> [ (
  { <column_name> [ WITH OPTIONS ] [ <column_constraint> [ ... ] ]
    | <table_constraint> }
    [, ... ]
) ]
{ FOR VALUES <partition_bound_spec> | DEFAULT }
  SERVER <server_name>
  [ OPTIONS ( [ mpp_execute { 'coordinator' | 'any' | 'all segments' } [, ] ] <option> '<value>' [, ... ] ) ]

-- where <column_constraint> is:

[ CONSTRAINT <constraint_name> ]
{ NOT NULL |
  NULL |
  DEFAULT <default_expr> |
  GENERATED ALWAYS AS ( <generation_expr> ) STORED}

-- and <table_constraint> is:

[ CONSTRAINT <constraint_name> ]
CHECK ( <expression> ) [ NO INHERIT ]

-- and <partition_bound_spec> is:

IN ( <partition_bound_expr> [, ...] ) |
FROM ( { <partition_bound_expr> | MINVALUE | MAXVALUE } [, ...] )
  TO ( { <partition_bound_expr> | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS <numeric_literal>, REMAINDER <numeric_literal> )
```

## 说明 {#description}

`CREATE FOREIGN TABLE` 在当前数据库中创建新的外表。创建外表的用户成为其所有者。

如果用模式名限定表名（例如 `CREATE FOREIGN TABLE myschema.mytable ...`），Apache Cloudberry 会在指定模式中创建该表；否则在当前模式中创建外表。外表名称必须与同一模式中任何其他外表、表、序列、索引、视图或物化视图的名称不同。

由于 `CREATE FOREIGN TABLE` 会自动创建表示外表一行对应复合类型的数据类型，外表不能与同一模式中已有数据类型同名。

如果指定 `PARTITION OF` 子句，则会按照指定边界将表创建为 parent_table 的分区。

要创建外表，必须对外部服务器拥有 `USAGE` 权限，并对表中使用的所有列类型拥有 `USAGE` 权限。

## 参数 {#parameters}

**`IF NOT EXISTS`**

如果同名关系已存在，则不抛出错误。Apache Cloudberry 会在这种情况下发出提示。请注意，无法保证现有关系与要创建的关系相似。

**`table_name`**

要创建的外表名称（可以用模式名限定）。

**`column_name`**

要在新外表中创建的列名称。

**`data_type`**

列的数据类型，包括数组说明符。

**`COLLATE collation`**

`COLLATE` 子句为列指定排序规则（列必须是可排序规则的数据类型）。如果未指定，则使用列数据类型的默认排序规则。

**`INHERITS ( parent_table [, ... ] )`**

可选的 `INHERITS` 子句指定一个表列表，新外表自动继承这些表的所有列。父表可以是普通表或外表。更多详情参见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) 的类似形式。

**`PARTITION OF parent_table { FOR VALUES partition_bound_spec | DEFAULT }`**

此形式可用于将外表创建为给定父表的分区，并指定分区边界值。更多详情参见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) 的类似形式。请注意，目前如果父表上存在 `UNIQUE` 索引，则不能将外表创建为该父表的分区。（另请参见 [ALTER TABLE ATTACH PARTITION](/cloudberry/reference/sql-stmts/alter-table/)。）

**`CONSTRAINT constraint_name`**

列约束或表约束的可选名称。如果违反约束，错误消息中会显示约束名称，因此可以使用类似 `col must be positive` 的约束名称向客户端应用传达有用的约束信息。（指定包含空格的约束名称时需要使用双引号。）如果未指定约束名称，系统会生成名称。

**`NOT NULL`**

不允许列包含空值。

**`NULL`**

允许列包含空值。这是默认值。

此子句仅为兼容非标准 SQL 数据库而提供。新应用不建议使用。

**`CHECK ( expression ) [ NO INHERIT ]`**

`CHECK` 子句指定一个产生布尔结果的表达式，外表中的每一行都应满足该表达式；也就是说，对于外表中的所有行，表达式都应产生 TRUE 或 UNKNOWN，不能产生 FALSE。作为列约束指定的检查约束只能引用该列的值，而表约束中的表达式可以引用多个列。

目前，`CHECK` 表达式不能包含子查询，也不能引用当前行列之外的变量。可以引用系统列 `tableoid`，但不能引用其他系统列。

**`DEFAULT default_expr`**

`DEFAULT` 子句为包含该定义的列指定默认值。该值可以是任意不含变量的表达式；Apache Cloudberry 不允许子查询，也不允许引用当前表中的其他列。默认表达式的数据类型必须与列的数据类型匹配。

对于未指定列值的插入操作，Apache Cloudberry 使用默认表达式。如果列没有默认值，则默认值为 null。

**`GENERATED ALWAYS AS ( generation_expr ) STORED`**

此子句将列创建为生成列。不能写入该列；读取时会返回指定表达式的结果。

必须使用关键字 `STORED` 表示该列在写入时计算。（计算结果会提供给外部数据包装器进行存储，并且读取时必须由其返回。）

生成表达式可以引用表中的其他列，但不能引用其他生成列。使用的所有函数和操作符都必须是不可变的。不允许引用其他表。

**`server_name`**

要用于外表的现有服务器名称。有关定义服务器的详情，请参见 [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/)。

**`OPTIONS ( option 'value' [, ... ] )`**

新外表或其某一列的选项。选项名称必须唯一，但表选项和列选项可以使用同名。选项名称和值由外部数据包装器决定。Apache Cloudberry 使用外部数据包装器的 validator_function 验证这些选项和值。

**`mpp_execute { 'coordinator' | 'any' | 'all segments' }`**

Apache Cloudberry 专用选项，用于标识外部数据包装器读取或写入数据的主机：

- `coordinator`（默认值）— 从 Coordinator 主机读取或向其写入数据。
- `any`— 根据哪条路径代价更低，从 Coordinator 主机或任意一个 Segment 读取数据。
- `all segments`— 从所有 Segment 读取或向其写入数据。要支持此选项值，外部数据包装器必须具有将 Segment 与数据匹配的策略。

> **注意** 只有设置 `mpp_execute 'all segments'` 时，Apache Cloudberry 才支持并行写入外表。

对外表 `mpp_execute` 选项及其具体模式的支持由外部数据包装器决定。

可以在多个命令中指定 `mpp_execute` 选项：`CREATE FOREIGN TABLE`、`CREATE SERVER` 和 `CREATE FOREIGN DATA WRAPPER`。外表设置优先于外部服务器设置，外部服务器设置又优先于外部数据包装器设置。

## 注意事项 {#notes}

Apache Cloudberry 不会强制执行外表上的约束（例如 `CHECK` 或 `NOT NULL` 子句），大多数外部数据包装器也不会尝试执行；也就是说，系统简单地假定约束成立。强制执行意义不大，因为它只适用于通过外表插入或更新的行，不适用于通过其他方式（例如直接在远程服务器上）修改的行。因此，附加到外表的约束应表示远程服务器正在执行的约束。

某些特殊用途的外部数据包装器可能是其所访问数据的唯一访问机制；这种情况下，由外部数据包装器自身执行约束可能合适。但除非其文档明确说明，否则不能假定包装器会执行约束。

虽然 Apache Cloudberry 不尝试强制执行外表上的约束，但会在查询优化时假定约束正确。如果外表中可见的行不满足声明的约束，查询可能产生错误或不正确的结果。用户有责任确保约束定义符合实际情况。

<div class="note">当外表用作分区表的一个分区时，会隐含要求其内容满足分区规则。同样，用户有责任确保这一点；最佳做法是在远程服务器上安装匹配的约束。</div>

在包含外表分区的分区表中，如果 `UPDATE` 更改分区键值，并且外部数据包装器支持元组路由，行可能会从本地分区移动到外表分区。不过，目前不能将行从一个外表分区移动到另一个分区。如果执行此类移动，`UPDATE` 会因分区约束而失败，前提是远程服务器正确执行了该约束。

生成列也有类似情况。存储的生成列在本地 Apache Cloudberry 服务器上插入或更新时计算，然后交给外部数据包装器写入外部数据存储；但系统不会强制查询外表返回的存储生成列值与生成表达式一致。同样，这可能导致查询结果不正确。

## 示例 {#examples}

创建名为 `films`、使用名为 `film_server` 的服务器的外表：

```sql
CREATE FOREIGN TABLE films (
    code        char(5) NOT NULL,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
)
SERVER film_server;
```

创建外表 `measurement_y2016m07`。该表将通过服务器 `server_07` 访问，并作为范围分区表 measurement 的一个分区：

```sql
CREATE FOREIGN TABLE measurement_y2016m07
    PARTITION OF measurement FOR VALUES FROM ('2016-07-01') TO ('2016-08-01')
    SERVER server_07;
```

## 兼容性 {#compatibility}

`CREATE FOREIGN TABLE` 基本符合 SQL 标准；不过，与 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) 类似，Apache Cloudberry 允许 `NULL` 约束和零列外表。指定列默认值的能力是 Apache Cloudberry 的扩展，`mpp_execute` 选项也是如此。按 Apache Cloudberry 定义的形式实现的表继承不属于标准。

## 另请参阅 {#see-also}

[ALTER FOREIGN TABLE](/cloudberry/reference/sql-stmts/alter-foreign-table/)、[DROP FOREIGN TABLE](/cloudberry/reference/sql-stmts/drop-foreign-table/)、[CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/)
