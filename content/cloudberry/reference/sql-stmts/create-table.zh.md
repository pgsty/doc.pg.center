---
title: "CREATE TABLE"
description: "定义新表。"
weight: 830
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-table.md"
---

> **注意** Apache Cloudberry 接受参照完整性语法（外键约束），但不实施这些约束。

## 语法概要 {#synopsis}

```sql
CREATE [ [GLOBAL | LOCAL] {TEMPORARY | TEMP} | UNLOGGED ] TABLE [IF NOT EXISTS] <table_name> ( 
  [ { <column_name> <data_type> [ COLLATE <collation> ] [ ENCODING ( <storage_directive> [, ...] ) ] [<column_constraint> [ ... ] ]
    | <table_constraint>
    | LIKE <source_table> [ <like_option> ... ]
    | COLUMN <column_name> ENCODING ( <storage_directive> [, ...] ) [, ...] }
] )
[ INHERITS ( <parent_table> [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { <column_name> | ( <expression> ) } [ COLLATE <collation> ] [ <opclass> ] [, ... ] ) ]
[ USING ( <access_method> ) ]
[ WITH ( <storage_parameter> [=<value>] [, ... ] ) ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE <tablespace_name> ]
[ DISTRIBUTED BY ( <column> [<opclass>] [, ... ] ) 
    | DISTRIBUTED RANDOMLY
    | DISTRIBUTED REPLICATED ]

CREATE [ [GLOBAL | LOCAL] {TEMPORARY | TEMP} | UNLOGGED ] TABLE [IF NOT EXISTS] <table_name>
  OF <type_name> [ (
  { <column_name> [WITH OPTIONS] [ <column_constraint> [ ... ] ]
    | <table_constraint> }
    [, ... ]
) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { <column_name> | ( <expression> ) } [ COLLATE <collation> ] [ <opclass> ] [, ... ] ) ]
[ USING <access_method> ]
[ WITH ( <storage_parameter> [=<value>] [, ... ] ) ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE <tablespace_name> ]
[ DISTRIBUTED BY ( <column> [<opclass>] [, ... ] ) 
    | DISTRIBUTED RANDOMLY
    | DISTRIBUTED REPLICATED ]

CREATE [ [GLOBAL | LOCAL] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] <table_name>
  PARTITION OF <parent_table> [ (
  { <column_name [ WITH OPTIONS ] [ <column_constraint> [ ... ] ]
    | <table_constraint> }
    [, ... ]
) ] { FOR VALUES <partition_bound_spec> | DEFAULT }
[ PARTITION BY { RANGE | LIST | HASH } ( { <column_name> | ( <expression> ) } [ COLLATE <collation> ] [ <opclass> ] [, ... ] ) ]
[ USING <access_method> ]
[ WITH ( <storage_parameter> [=<value>] [, ... ] ) ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE <tablespace_name> ]

-- where <column_constraint> is:

  [ CONSTRAINT <constraint_name>]
  { NOT NULL 
    | NULL 
    | CHECK  ( <expression> ) [ NO INHERIT ]
    | DEFAULT <default_expr>
    | GENERATED ALWAYS AS ( <generation_expr> ) STORED
    | GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( <sequence_options> ) ]
    | UNIQUE <index_parameters>
    | PRIMARY KEY <index_parameters>
    | REFERENCES <reftable> [ ( refcolumn ) ] 
        [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]  
        [ ON DELETE <referential_action> ] [ ON UPDATE <referential_action> ] }
  [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and <table_constraint> is:

  [ CONSTRAINT <constraint_name> ]
  { CHECK ( <expression> ) [ NO INHERIT ]
    | UNIQUE ( <column_name> [, ... ] ) <index_parameters>
    | PRIMARY KEY ( <column_name> [, ... ] ) <index_parameters>
    | EXCLUDE [ USING <index_method> ] ( <exclude_element> WITH <operator> [, ... ] )
        <index_parameters> [ WHERE ( <predicate> ) ]
    | FOREIGN KEY ( <column_name> [, ... ] ) REFERENCES <reftable> [ ( <refcolumn> [, ... ] ) ]
        [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] 
        [ ON DELETE <referential_action> ] [ ON UPDATE <referential_action> ] }
  [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and <like_option> is:

  { INCLUDING | EXCLUDING }
  { AM | COMMENTS | CONSTRAINTS | DEFAULTS | ENCODING | GENERATED | IDENTITY
       | INDEXES | RELOPT | STATISTICS | STORAGE | ALL }

and <partition_bound_spec> is:

  IN ( <partition_bound_expr> [, ...] ) |
  FROM ( { <partition_bound_expr> | MINVALUE | MAXVALUE } [, ...] )
    TO ( { <partition_bound_expr> | MINVALUE | MAXVALUE } [, ...] ) |
  WITH ( MODULUS <numeric_literal>, REMAINDER <numeric_literal> )

and <index_parameters> in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

  [ INCLUDE ( <column_name> [, ... ] ) ]
  [ WITH ( <storage_parameter> [=<value>] [, ... ] ) ]
  [ USING INDEX TABLESPACE <tablespace_name> ] 

and <exclude_element> in an EXCLUDE constraint is:

  { <column_name> | ( <expression> ) } [ <opclass> ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]
```

经典分区语法的组成部分包括：

```sql
CREATE [ [GLOBAL | LOCAL] {TEMPORARY | TEMP} | UNLOGGED ] TABLE [IF NOT EXISTS] <table_name> (
  [ { <column_name> <data_type> [ COLLATE <collation> ] [ ENCODING ( <storage_directive> [, ...] ) ] [<column_constraint> [ ... ] ]
    | <table_constraint>
    | LIKE <source_table> [ <like_option> ... ]
    | COLUMN <column_name> ENCODING ( <storage_directive> [, ...] ) [, ...] }
] )
[ INHERITS ( <parent_table> [, ... ] ) ]
[ USING ( <access_method> ) ]
[ WITH ( <storage_parameter> [=<value>] [, ... ] ) ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE <tablespace_name> ]
[ DISTRIBUTED BY ( <column> [<opclass>] [, ... ] )
    | DISTRIBUTED RANDOMLY
    | DISTRIBUTED REPLICATED ]

{ --partitioned table using SUBPARTITION TEMPLATE
[ PARTITION BY { RANGE | LIST } (<column>) 
  {  [ SUBPARTITION BY { RANGE | LIST } (<column1>) 
       SUBPARTITION TEMPLATE ( <template_spec> ) ]
          [ SUBPARTITION BY { RANGE | LIST } (<column2>) 
            SUBPARTITION TEMPLATE ( <template_spec> ) ]
              [...]  }
  ( <classic_partition_spec> ) ]
} 

|

{ -- partitioned table without SUBPARTITION TEMPLATE
[ PARTITION BY { RANGE | LIST } (<column>)
   [ SUBPARTITION BY { RANGE | LIST } (<column1>) ]
      [ SUBPARTITION BY { RANGE | LIST } (<column2>) ]
         [...]
  ( <classic_partition_spec>
     [ ( <subpartition_spec_column1>
          [ ( <subpartition_spec_column2>
               [...] ) ] ) ],
  [ <classic_partition_spec>
     [ ( <subpartition_spec_column1>
        [ ( <subpartition_spec_column2>
             [...] ) ] ) ], ]
    [...]
  ) ]
}

-- where <classic_partition_spec> is:

  <partition_element> [, ...]

and <partition_element> is:

   DEFAULT PARTITION <name>
  | [PARTITION <name>] VALUES (<list_value> [,...] )
  | [PARTITION <name>] 
     START ([<datatype>] '<start_value>') [INCLUSIVE | EXCLUSIVE]
     [ END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE] ]
     [ EVERY ([<datatype>] [<number> | INTERVAL] '<interval_value>') ]
  | [PARTITION <name>] 
     END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE]
     [ EVERY ([<datatype>] [<number> | INTERVAL] '<interval_value>') ]
[ WITH ( <storage_parameter> = <value> [ , ... ] ) ]
[ <storage_directive> [ , ... ] ]
[ TABLESPACE <tablespace> ]

and <subpartition_spec> or <template_spec> is:

  <subpartition_element> [, ...]

and <subpartition_element> is:

  DEFAULT SUBPARTITION <name>
  | [SUBPARTITION <name>] VALUES (<list_value> [,...] )
  | [SUBPARTITION <name>] 
     START ([<datatype>] '<start_value>') [INCLUSIVE | EXCLUSIVE]
     [ END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE] ]
     [ EVERY ([<datatype>] [<number> | INTERVAL] '<interval_value>') ]
  | [SUBPARTITION <name>] 
     END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE]
     [ EVERY ([<datatype>] [<number> | INTERVAL] '<interval_value>') ]
[ WITH ( <storage_parameter> = <value> [ , ... ] ) ]
[ <storage_directive> [, ...] ]
[ TABLESPACE <tablespace> ]
```

## 说明 {#description}

`CREATE TABLE` 在当前数据库中创建一个初始为空的新表。执行命令的用户拥有该表。

创建表必须对所有列类型，或相应的 `OF` 子句中的类型，具有 `USAGE` 权限。

如果指定模式名，Apache Cloudberry 会在该模式中创建表，否则在当前模式中创建。临时表位于特殊模式中，因此创建临时表时不能指定模式名。表名必须不同于同一模式中任何其他表、外部表、序列、索引、视图或外表的名称。

`CREATE TABLE` 还会自动创建一个数据类型，表示与表中一行对应的复合类型。因此，表不能与同一模式中的任何已有数据类型同名。

可选的约束子句指定新行或更新后的行必须满足的条件，只有满足这些条件，插入或更新操作才会成功。约束是一种 SQL 对象，以各种方式帮助定义表中有效值的集合。

Apache Cloudberry 接受参照完整性（外键）约束，但不实施这些约束。相关信息保留在系统目录中，除此之外会被忽略。

可以定义两类约束：表约束和列约束。列约束作为列定义的一部分定义；表约束的定义不绑定特定列，可以涉及多个列。每个列约束也可以写成表约束；当约束只影响一列时，列约束只是更便捷的写法。

创建表时，可以通过额外的子句声明 Apache Cloudberry 分布策略。如果未提供 `DISTRIBUTED BY`、`DISTRIBUTED RANDOMLY` 或 `DISTRIBUTED REPLICATED` 子句，Apache Cloudberry 会为表指定哈希分布策略，以 `PRIMARY KEY`（如果表有主键）或表的第一列作为分布键。几何类型或用户定义类型的列不能作为 Apache Cloudberry 分布键列。如果表中没有类型合适的列，则按随机分布方式分布各行。为确保数据在 Apache Cloudberry 系统中均匀分布，应选择每条记录都唯一的分布键；如果无法做到，则选择 `DISTRIBUTED RANDOMLY`。

如果提供 `DISTRIBUTED REPLICATED` 子句，Apache Cloudberry 会将表的所有行分布到系统中的所有 Segment。当用户定义函数必须在 Segment 上运行，而且需要访问表的所有行时，可以使用此选项。复制表还可以避免该表的广播 Motion，从而提高查询性能。`DISTRIBUTED REPLICATED` 子句不能与 `PARTITION` 子句或 `INHERITS` 子句一起使用。复制表也不能被其他表继承。用户查询复制表时，不能引用隐藏系统列（`ctid`、`cmin`、`cmax`、`xmin`、`xmax` 和 `gp_segment_id`），因为它们没有单一、无歧义的值；Apache Cloudberry 会为该查询返回 `column does not exist` 错误。

`PARTITION BY` 和 `PARTITION OF` 子句允许将表划分为多个子表（或部分），它们共同组成父表，并共享其结构。

## 参数 {#parameters}

**`GLOBAL | LOCAL`**

这些关键字用于兼容 SQL 标准，但在 Apache Cloudberry 中没有作用，并且已弃用。

**`TEMPORARY | TEMP`**

指定后，将创建临时表。临时表在会话结束时自动删除，也可以选择在当前事务结束时删除（参阅 `ON COMMIT`）。临时表存在期间，同名的已有永久表对当前会话不可见，除非用模式限定名引用。临时表上创建的任何索引也自动成为临时索引。

务必通过会话中的 SQL 命令，对临时表执行适当的清理和分析操作。例如，如果要在复杂查询中使用临时表，应在填充数据后对其运行 `ANALYZE`。

**`UNLOGGED`**

指定后，将创建不记录日志的表。写入此类表的数据不会写入预写日志（WAL），因此比普通表快得多。不过，不记录日志的表的内容不会复制到镜像 Segment 实例。此外，这种表不能保证崩溃安全：发生崩溃或非正常关闭后，Apache Cloudberry 会自动清空它。此类表上创建的任何索引也自动不记录日志。

**`IF NOT EXISTS`**

如果已存在同名关系，不抛出错误，Apache Cloudberry 会发出通知。注意，并不能保证现有关系与原本要创建的关系有任何相似之处。

**`table_name`**

要创建的表名（可用模式限定）。

**`OF type_name`**

创建一个*类型化表*，其结构取自指定的复合类型（名称可用模式限定）。类型化表与其类型绑定；例如，通过 `DROP TYPE ... CASCADE` 删除该类型时，表也会被删除。

创建类型化表时，列的数据类型由底层复合类型决定，不在 `CREATE TABLE` 命令中指定。但 `CREATE TABLE` 命令可以为表添加默认值和约束，并指定存储参数。

**`column_name`**

要在新表中创建的列名。

**`data_type`**

列的数据类型，可以包含数组说明符。有关 Apache Cloudberry 支持的数据类型的更多信息，请参阅“数据类型”文档。

对于包含文本数据的表列，应指定 `VARCHAR` 或 `TEXT` 数据类型，不建议指定 `CHAR`。在 Apache Cloudberry 中，`VARCHAR` 或 `TEXT` 会将添加到数据中的填充字符（最后一个非空格字符后添加的空格）视为有意义的字符，而 `CHAR` 不会。请参阅[注意事项](#notes)。

**`COLLATE` collation**

`COLLATE` 子句为列指定排序规则（列的数据类型必须支持排序规则）。未指定时，使用该列数据类型的默认排序规则。

> **注意**：Cloudberry 查询优化器（GPORCA）仅在查询中所有列都使用相同排序规则时支持排序规则。如果查询中的列使用不同的排序规则，Apache Cloudberry 会使用 Postgres 规划器。

**`ENCODING ( storage_directive [, ...] )`**

对于列，可选的 `ENCODING` 子句指定列数据的压缩类型和块大小。有效的列 storage_directives 为 `compresstype`、`compresslevel` 和 `blocksize`。

此子句只适用于 AO 列存表。

列压缩设置从表级继承到分区级，再到子分区级。最底层的设置优先。

**`blocksize`**

设置表中每个块的大小，单位为字节。`blocksize` 必须在 8192 到 2097152 字节之间，且是 8192 的倍数。默认值为 32768。

**`compresslevel`**

对于 AO 表的 Zstd 压缩，可设为 1（压缩最快）到 19（压缩比最高）之间的整数。对于 zlib 压缩，有效范围为 1 到 9。对于 `RLE_TYPE`，压缩级别可以是 1（压缩最快）到 4（压缩比最高）之间的整数。

**`compresstype`**

设为 `ZLIB`（默认值）、`ZSTD` 或 `RLE_TYPE`，以指定压缩类型。值 `NONE` 禁用压缩。Zstd 可以兼顾速度或较高压缩比，通过 `compresslevel` 选项调节。zlib 用于向后兼容。在常见工作负载上，Zstd 优于这些压缩类型。

值 `RLE_TYPE` 仅受 AO 列存表支持，用于启用游程编码（RLE）压缩算法。如果许多连续行具有相同的数据值，RLE 的压缩效果优于 Zstd 或 zlib。

对于 `BIGINT`、`INTEGER`、`DATE`、`TIME` 或 `TIMESTAMP` 类型的列，如果 `compresstype` 选项设为 `RLE_TYPE`，还会应用差分压缩。差分压缩算法基于连续行列值之间的差值，旨在数据按排序顺序加载，或对已排序的列数据进行压缩时改善压缩效果。

**`INHERITS ( parent_table [, …])`**

可选的 `INHERITS` 子句指定新表自动继承其全部列的表列表。父表可以是普通表或外表。

使用 `INHERITS` 会在新子表与其父表之间建立持久关系。父表的结构修改通常也会传播到子表，默认情况下，扫描父表时会包含子表的数据。

如果多个父表存在同名列，除非这些列在各父表中的数据类型一致，否则会报错。如果没有冲突，重复列会合并成新表中的一列。如果新表的列名列表包含一个继承而来的同名列，其数据类型也必须与继承列一致，列定义将合并为一个。如果新表显式为该列指定默认值，此值会覆盖继承声明中的所有默认值。否则，所有为该列指定默认值的父表必须指定相同的默认值，否则 Apache Cloudberry 会报错。

`CHECK` 约束的合并方式与列基本相同：如果多个父表或新表定义中包含同名 `CHECK` 约束，这些约束必须具有相同的检查表达式，否则会报错。名称和表达式相同的约束会合并为一份。父表中标记为 `NO INHERIT` 的约束不参与合并。注意，新表中的未命名 `CHECK` 约束永远不会合并，因为系统始终会为它选择唯一名称。

列的 `STORAGE` 设置也会从父表复制。

如果父表中的列是标识列，该属性不会被继承。需要时可以将子表中的列声明为标识列。

**`PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ opclass ] [, ...] )`**

*现代分区语法*中可选的 `PARTITION BY` 子句指定表的分区策略。由此创建的表称为分区表。括号中的列或表达式列表构成表的分区键。使用范围分区或哈希分区时，分区键可以包含多个列或表达式（最多 32 个）；使用列表分区时，分区键必须只包含一个列或表达式。

范围分区和列表分区需要 btree 操作符类，哈希分区需要 hash 操作符类。如果未显式指定操作符类，将使用相应类型的默认操作符类；如果没有默认操作符类，Apache Cloudberry 会报错。使用哈希分区时，所用操作符类必须实现支持函数 2（详情请参阅 PostgreSQL 文档中的[索引方法支持例程](https://www.postgresql.org/docs/12/xindex.html#XINDEX-SUPPORT)）。

> **注意** 只有现代分区语法支持哈希分区。

分区表被划分为子表（称为分区），通常通过单独的 `CREATE TABLE` 命令创建。分区表本身为空。插入表的数据行会根据分区键中列或表达式的值路由到某个分区。如果没有现有分区与新行中的值匹配，Apache Cloudberry 会报错。

分区表不支持 `EXCLUDE` 约束，但可以在各个分区上定义这些约束。

有关表分区的进一步讨论，请参阅“对大表分区”。

**`PARTITION OF parent_table { FOR VALUES partition_bound_spec | DEFAULT }`**

*现代分区语法*的 `PARTITION OF` 子句将表创建为指定父表的一个*分区*。可以使用 `FOR VALUES` 创建针对特定值的分区，也可以使用 `DEFAULT` 创建默认分区。父表中已有的所有索引和约束都会克隆到新分区中。

partition_bound_spec 必须与父表的分区方法和分区键相对应，且不能与该父表的任何现有分区重叠。带 `IN` 的形式用于列表分区，带 `FROM` 和 `TO` 的形式用于范围分区，带 `WITH` 的形式用于哈希分区。

`partition_bound_expr` 可以是不含变量的任意表达式（不允许子查询、窗口函数、聚合函数和返回集合的函数）。其数据类型必须与对应分区键列的数据类型匹配。表达式在创建表时求值一次，因此甚至可以包含 `CURRENT_TIMESTAMP` 等易变表达式。

创建列表分区时，可以指定 `NULL`，表示该分区允许分区键列为空。但给定父表最多只能有一个这样的列表分区。范围分区不能指定 `NULL`。

创建范围分区时，`FROM` 指定的下界包含在范围内，`TO` 指定的上界不包含在范围内。即 `FROM` 列表中的值是此分区对应分区键列的有效值，而 `TO` 列表中的值不是。注意，必须按照逐行比较的规则理解此说法（更多信息请参阅 PostgreSQL 文档中的[行构造器比较](https://www.postgresql.org/docs/12/functions-comparisons.html#ROW-WISE-COMPARISON)）。例如，对于 `PARTITION BY RANGE (x, y)`，分区边界 `FROM (1, 2) TO (3, 4)` 允许 `x=1` 且任意 `y>=2`，或 `x=2` 且 `y` 为任意非空值，或 `x=3` 且任意 `y<4`。

创建范围分区时，可以用特殊值 `MINVALUE` 和 `MAXVALUE` 表示列值没有下界或上界。例如，使用 `FROM (MINVALUE) TO (10)` 定义的分区允许任何小于 10 的值，而使用 `FROM (10) TO (MAXVALUE)` 定义的分区允许任何大于或等于 10 的值。

创建涉及多列的范围分区时，将 `MAXVALUE` 用作下界的一部分，将 `MINVALUE` 用作上界的一部分，也可能有意义。例如，使用 `FROM (0, MAXVALUE) TO (10, MAXVALUE)` 定义的分区允许第一个分区键列大于 0 且小于或等于 10 的任何行。类似地，使用 `FROM ('a', MINVALUE) TO ('b', MINVALUE)` 定义的分区允许第一个分区键列以“a”开头的任何行。

注意，如果分区边界的某一列使用了 `MINVALUE` 或 `MAXVALUE`，后续所有列都必须使用相同值。例如，`(10, MINVALUE, 0)` 不是有效边界；必须指定 `(10, MINVALUE, MINVALUE)`。

还应注意，timestamp 等某些元素类型具有“infinity”概念，它只是可以存储的另一个值。这不同于 `MINVALUE` 和 `MAXVALUE`：后两者不是可存储的实际值，而是表示值无界的方式。可以将 `MAXVALUE` 理解为大于包括“infinity”在内的任何其他值，将 `MINVALUE` 理解为小于包括“minus infinity”在内的任何其他值。因此，范围 `FROM ('infinity') TO (MAXVALUE)` 不是空范围，它恰好允许存储一个值：“infinity”。

如果指定 `DEFAULT`，该表将被创建为父表的默认分区。此选项不适用于哈希分区表。Apache Cloudberry 会将不适合该父表任何其他分区的分区键值路由到默认分区。

如果表已有 `DEFAULT` 分区，向其添加新分区时必须扫描默认分区，确认其中没有本应属于新分区的行。如果默认分区包含大量行，此操作可能较慢。如果默认分区是外表，或者存在能证明其中不可能包含应放入新分区的行的约束，Apache Cloudberry 会跳过扫描。

创建哈希分区时，必须指定模数和余数。模数必须是正整数，余数必须是小于模数的非负整数。通常，初始设置哈希分区表时，应选择与分区数相等的模数，为每个表指定相同模数和不同余数（见下文示例）。不过，并不要求每个分区的模数都相同，只要求哈希分区表各分区中出现的每个模数都是下一个更大模数的因子。这样就可以逐步增加分区数，而无须一次移动全部数据。例如，假设一个哈希分区表有 8 个分区，每个分区的模数均为 8，但现在需要将分区数增至 16。可以分离一个模数为 8 的分区，创建两个覆盖同一键空间的新分区，模数均为 16（一个的余数与分离分区相同，另一个的余数为该值加 8），然后重新填入数据。随后可以对每个模数为 8 的分区重复此过程，也可以留到以后进行，直到全部替换。虽然每一步仍可能涉及大量数据移动，但仍优于创建一张全新表并一次性移动全部数据。

分区必须与所属分区表具有相同的列名和类型。分区表列名或类型的修改会自动传播到所有分区。每个分区都会自动继承 `CHECK` 约束，但单独的分区可以指定额外的 `CHECK` 约束；如果额外约束的名称和条件与父表相同，就会与父约束合并。可以为每个分区单独指定默认值，但通过分区表插入元组时，不会应用分区的默认值。

Apache Cloudberry 会将插入分区表的行自动路由到正确分区。如果没有合适的分区，就会报错。

通常会影响表及其所有继承子表的操作（例如 `TRUNCATE`）会级联到所有分区，但也可以针对单个分区执行。注意，使用 `DROP TABLE` 删除分区需要在父表上获取 `ACCESS EXCLUSIVE` 锁。

**`LIKE source_table [like_option `...`]`**

`LIKE` 子句指定一个源表，新表会自动复制其所有列名、数据类型、非空约束和分布策略。

> **注意** 存储属性和分区结构*不会*复制到新表。

与 `INHERITS` 不同，创建完成后，新表与原表完全独立。原表的变更不会应用到新表，扫描原表时也无法包含新表的数据。

同样与 `INHERITS` 不同，通过 `LIKE` 复制的列和约束不会与同名列和约束合并。如果显式指定了相同名称，或在另一个 `LIKE` 子句中出现相同名称，Apache Cloudberry 会报错。

可选的 like_option 子句指定还要复制原表的哪些属性。指定 `INCLUDING` 会复制该属性，指定 `EXCLUDING` 则不复制。默认为 `EXCLUDING`。如果对同一种对象指定多次，以最后一次为准。可用选项如下：

**`INCLUDING AM`**

复制原表的访问方法。

包含 `AM` 时，不能再通过 `WITH` 或 `USING` 子句显式指定新表的访问方法。

**`INCLUDING COMMENTS`**

复制所复制列、约束和索引的注释。默认不复制注释，因此新表中复制得到的列和约束没有注释。

**`INCLUDING CONSTRAINTS`**

复制 `CHECK` 约束，不区分列约束和表约束。非空约束始终复制到新表。

**`INCLUDING DEFAULTS`**

复制所复制列定义中的默认表达式。否则不复制默认表达式，新表中复制得到的列默认值为空。注意，复制调用 `nextval` 等数据库修改函数的默认表达式，可能在原表与新表之间建立功能上的关联。

**`INCLUDING ENCODING`**

对于 AO 列存源表，复制各列的编码。

**`INCLUDING GENERATED`**

复制所复制列定义中的所有生成表达式。默认情况下，新列是普通基础列。

**`INCLUDING IDENTITY`**

复制所复制列定义中的所有标识列说明。会为新表的每个标识列创建一个新序列，与旧表关联的序列相互独立。

**`INCLUDING INDEXES`**

在新表上创建原表的索引以及 `PRIMARY KEY`、`UNIQUE` 和 `EXCLUDE` 约束。新索引和约束的名称按默认规则选择，不受原名称影响。（此行为可避免新索引发生重名错误。）

**`INCLUDING RELOPT`**

复制原表的关系存储选项。对于 AO 表和 AO 列存表，复制 `blocksize`、`compresslevel` 和 `compresstype.` 对于堆表，复制 `fillfactor`。也可以指定关系[存储参数](#storage-parameters)。

包含 `RELOPT` 选项时，不能再通过 `WITH` 子句显式指定新表的关系存储选项。

**`INCLUDING STATISTICS`**

将扩展统计信息复制到新表。

**`INCLUDING STORAGE`**

复制所复制列定义的 `STORAGE` 设置。默认不复制 `STORAGE` 设置，新表中复制得到的列会使用该类型的默认设置。

**`INCLUDING ALL`**

`INCLUDING ALL` 是所有可用选项的简写形式。（可以在 `INCLUDING ALL` 后指定单独的 `EXCLUDING` 子句，以选择除某些特定选项之外的所有选项。）

还可以使用 `LIKE` 子句从视图、外表或复合类型复制列定义。Apache Cloudberry 会忽略不适用的选项（例如从视图复制时使用 `INCLUDING INDEXES`）。

**`CONSTRAINT constraint_name`**

列约束或表约束的可选名称。如果违反约束，错误消息中会显示约束名，因此可以使用 `column must be positive` 之类的名称向客户端应用传达有用的约束信息。（包含空格的约束名请使用双引号指定。）如果未指定约束名，系统会自动生成名称。

> **注意** 指定的 constraint_name 用于约束，但索引名会使用系统生成的唯一名称。某些早期版本中，提供的名称同时用于约束名和索引名。

**`NOT NULL`**

该列不允许包含空值。

**`NULL`**

该列允许包含空值。这是默认行为。

此子句仅用于兼容非标准 SQL 数据库。新应用不建议使用。

**`CHECK (expression) [ NO INHERIT ]`**

`CHECK` 子句指定一个返回布尔结果的表达式，新行或更新后的行必须满足该表达式，插入或更新操作才能成功。求值为 `TRUE` 或 `UNKNOWN` 的表达式表示成功。如果插入或更新操作中的任何行求值为 `FALSE`，Apache Cloudberry 会抛出错误异常，插入或更新不会改变数据库。作为列约束指定的检查约束应只引用该列的值，而表约束中的表达式可以引用多个列。

目前，`CHECK` 表达式不能包含子查询，也不能引用当前行列以外的变量。可以引用系统列 `tableoid`，但不能引用其他系统列。

标记为 `NO INHERIT` 的约束不会传播到子表。

表有多个 `CHECK` 约束时，先检查 `NOT NULL` 约束，然后按名称的字母顺序逐行检查这些约束。（以前的 Apache Cloudberry 版本不保证 `CHECK` 约束按特定顺序触发。）

**`DEFAULT default_expr`**

`DEFAULT` 子句为包含该列定义的列分配默认数据值。该值可以是任意不含变量的表达式（尤其不允许交叉引用当前表中的其他列），也不允许子查询。默认表达式的数据类型必须与列的数据类型匹配。任何未为该列指定值的插入操作都会使用默认表达式。如果列没有默认值，则默认值为空值。

**`GENERATED ALWAYS AS ( generation_expr ) STORED`**

此子句将列创建为*生成列*。不能写入该列；读取时会返回指定表达式的结果。

必须使用关键字 `STORED`，表示该列在写入时计算，并存储在磁盘上。

生成表达式可以引用表中的其他列，但不能引用其他生成列。使用的所有函数和操作符都必须是不可变的。不允许引用其他表。

**`GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]`**

此子句将列创建为标识列。Apache Cloudberry 为其附加一个隐式序列，并在新行中自动将序列值分配给该列。这种列隐式具有 `NOT NULL` 属性。

`ALWAYS` 和 `BY DEFAULT` 子句决定 `INSERT` 语句中序列值与用户指定值的优先级。如果指定 `ALWAYS`，只有 `INSERT` 语句指定 `OVERRIDING SYSTEM VALUE` 时才接受用户指定值。如果指定 `BY DEFAULT`，用户指定值优先。详情请参阅 [INSERT](/cloudberry/reference/sql-stmts/insert/)。（在 `COPY` 命令中，无论此设置如何，都始终使用用户指定值。）

可以使用可选的 sequence_options 子句覆盖序列选项。详情请参阅 [CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/)。

**`UNIQUE ( column_constraint )`**

**`UNIQUE ( column_name [, ... ] ) [ INCLUDE ( column_name [, ...]) ] ( table_constraint )`**

`UNIQUE` 约束指定表中的一个或多个列只能包含唯一值。表级唯一约束的行为与列级唯一约束相同，但还可以跨越多个列。因此，该约束要求任意两行至少有一列不同。

对于唯一约束，空值不视为相等。唯一列必须包含 Apache Cloudberry 分布键的所有列。此外，分区表的 `<key>` 还必须包含分区键中的所有列。注意，分区表中的 `<key>` 约束不同于普通 `UNIQUE INDEX`。

每个唯一约束都应指定一组列，且这组列不同于该表定义的任何其他唯一约束或主键约束所指定的列集。（否则，Apache Cloudberry 会丢弃冗余的唯一约束。）

为多级分区层次结构建立唯一约束时，目标分区表以及其所有后代分区表的分区键中的所有列，都必须包含在约束定义中。

添加唯一约束会自动在约束使用的列或列组上创建唯一 btree 索引。

可选的 `INCLUDE` 子句向该索引添加一个或多个列，这些列只是“负载”：不对它们实施唯一性，也不能根据这些列搜索索引。不过，仅索引扫描可以取回它们。注意，虽然约束不对包含列实施唯一性，但仍依赖这些列。因此，对这些列执行某些操作（例如 `DROP COLUMN`）可能导致级联删除约束和索引。

**`PRIMARY KEY ( column constraint )`**<br />
**`PRIMARY KEY ( column_name [, ... ] ) [ INCLUDE ( column_name [, ...]) ] ( table constraint )`**

`PRIMARY KEY` 约束指定表中的一个或多个列只能包含唯一（不重复）、非空值。无论作为列约束还是表约束，一个表只能指定一个主键。

主键约束应指定一组不同于同一表中任何唯一约束所指定列集的列。（否则，唯一约束是冗余的，会被丢弃。）

`PRIMARY KEY` 实施的约束等同于 `UNIQUE` 与 `NOT NULL` 的组合，但将一组列标识为主键还提供了有关模式设计的元数据，因为主键意味着其他表可以依赖这组列作为行的唯一标识符。

在分区表上使用时，`PRIMARY KEY` 约束受前文所述 `UNIQUE` 约束的限制。

添加 `PRIMARY KEY` 约束会自动在约束使用的列或列组上创建唯一 btree 索引。

可选的 `INCLUDE` 子句向该索引添加一个或多个列，这些列只是“负载”：不对它们实施唯一性，也不能根据这些列搜索索引。不过，仅索引扫描可以取回它们。注意，虽然约束不对包含列实施唯一性，但仍依赖这些列。因此，对这些列执行某些操作（例如 `DROP COLUMN`）可能导致级联删除约束和索引。

**`EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ]`**

`EXCLUDE` 子句定义排他约束，保证任意两行在指定列或表达式上使用指定操作符进行比较时，不会使所有比较结果都为 `TRUE`。如果所有指定操作符都测试相等，这等同于 `UNIQUE` 约束，但普通唯一约束会更快。不过，排他约束可以指定比简单相等更一般的约束。例如，可以使用 `&&` 操作符指定表中任意两个行都不能包含重叠圆。

Apache Cloudberry 不支持在随机分布表上指定排他约束。

排他约束通过索引实现，因此每个指定操作符都必须与索引访问方法 index_method 的适当操作符类关联。操作符必须满足交换律。每个 exclude_element 都可以选择指定操作符类和/或排序选项；详见 [CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/)。

访问方法必须支持 `amgettuple`；目前这意味着不能使用 GIN。虽然允许这样做，但在排他约束中使用 B-树 或 hash 索引意义不大，因为普通唯一约束能更好地完成相同工作。因此，实践中访问方法始终会是 GiST 或 SP-GiST。

谓词允许对表的子集指定排他约束；内部会创建部分索引。注意，谓词周围必须有括号。

**`REFERENCES reftable [ ( refcolumn ) ]`**<br />
**`[ MATCH matchtype ] [ON DELETE key_action] [ON UPDATE key_action] (column constraint)`**<br />
**`FOREIGN KEY (column_name [, ...]) REFERENCES reftable [ ( refcolumn [, ... ] ) ]`**<br />
**`[ MATCH matchtype ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] (table constraint)`**

`REFERENCES` 和 `FOREIGN KEY` 子句指定参照完整性约束（外键约束）。Apache Cloudberry 接受参照完整性约束，但不实施它们。

**`DEFERRABLE`**<br />
**`NOT DEFERRABLE`**

`[NOT] DEFERRABLE` 子句控制约束是否可以延迟。不可延迟的约束会在每条命令后立即检查；可延迟约束的检查可以推迟到事务结束（使用 [`SET CONSTRAINTS`](/cloudberry/reference/sql-stmts/set-constraints/) 命令）。`NOT DEFERRABLE` 是默认值。目前只有 `UNIQUE`、`PRIMARY KEY` 和 `EXCLUDE` 约束接受此子句。`NOT NULL` 和 `CHECK` 约束不可延迟。`REFERENCES`（外键）约束接受此子句，但不会实施。注意，带延迟的约束不能作为包含 `ON CONFLICT DO UPDATE` 子句的 `INSERT` 语句中的冲突仲裁条件。

注意，带延迟的约束不能作为包含 `ON CONFLICT DO UPDATE` 子句的 `INSERT` 语句中的冲突仲裁条件。

**`INITIALLY IMMEDIATE`**<br />
**`INITIALLY DEFERRED`**

如果约束可延迟，此子句指定检查约束的默认时机。如果约束为 `INITIALLY IMMEDIATE`，则在每条语句后检查，这是默认行为。如果约束为 `INITIALLY DEFERRED`，则只在事务结束时检查。可以使用 [SET CONSTRAINTS](/cloudberry/reference/sql-stmts/set-constraints/) 命令更改约束检查时机。

**`USING access_method`**

可选的 `USING` 子句指定存储新表内容时使用的表访问方法；该方法必须是类型为 `TABLE` 的访问方法。设为 `heap` 可将表作为堆存储表访问，设为 `ao_row` 可将表作为行存储的 AO 表访问，设为 `ao_column` 可将表作为列存储的 AO/CO 表访问。默认访问方法由服务器配置参数 `default_table_access_method` 的值决定。

> **注意：**
>
> 尽管可以使用 `WITH (appendoptimized=true|false, orientation=row|column)` 指定表的访问方法，但建议改用 `USING <access_method>`。

**`WITH ( storage_parameter=value )`**

`WITH` 子句指定表或索引的可选存储参数；详情请参阅下文的[存储参数](#storage-parameters)。为向后兼容，表的 `WITH` 子句还可以包含 `OIDS=FALSE`，指定新表的行不应包含 OID（对象标识符）；`OIDS=TRUE` 已不再支持。

**`ON COMMIT`**

可以使用 `ON COMMIT` 控制事务块结束时临时表的行为。三个选项如下：

**PRESERVE ROWS** — 对临时表，事务结束时不执行特殊操作。这是默认行为。

**DELETE ROWS** — 每个事务块结束时删除临时表中的所有行。本质上，Apache Cloudberry 会在每次提交时自动执行 [TRUNCATE](/cloudberry/reference/sql-stmts/truncate/)。用于分区表时，此操作不会级联到其分区。

**DROP** — 当前事务块结束时删除临时表。用于分区表时，此操作会删除其分区；用于带继承子表的表时，会删除依赖子表。

**`TABLESPACE` tablespace**

要创建新表所在的表空间名称。未指定时，使用数据库的 `default_tablespace`；如果表是临时表，则使用 temp_tablespaces。对于分区表，由于表本身不需要存储空间，所指定的表空间会覆盖 `default_tablespace`，成为未显式指定其他表空间时新建分区使用的默认表空间。

**`USING INDEX TABLESPACE` tablespace**

此子句允许选择为 `UNIQUE`、`PRIMARY KEY` 或 `EXCLUDE` 约束关联的索引创建的表空间。如果未指定，则使用数据库的 `default_tablespace`；如果表是临时表，则使用 temp_tablespaces。

**`DISTRIBUTED BY ( column [opclass] [, ... ] )`**<br />
**`DISTRIBUTED RANDOMLY`**<br />
**`DISTRIBUTED REPLICATED`**

用于声明表的 Apache Cloudberry 分布策略。`DISTRIBUTED BY` 使用哈希分布，将一个或多个列声明为分布键。为获得最均匀的数据分布，分布键应为表的主键或唯一列（或列集）。如果无法做到，则可以选择 `DISTRIBUTED RANDOMLY`，将数据随机发送到 Segment 实例。此外，还可以指定操作符类 `opclass`，使用非默认哈希函数。

服务器配置参数 `gp_create_table_random_default_distribution` 控制创建表时未指定 DISTRIBUTED BY 子句的默认表分布策略。未指定分布策略时，Apache Cloudberry 按以下规则创建表。

如果该参数的值为 `off`（默认值），Apache Cloudberry 根据命令选择表分布键：

- 如果指定了 `LIKE` 或 `INHERITS` 子句，Apache Cloudberry 会从源表或父表复制分布键。
- 如果指定了 `PRIMARY KEY`、`UNIQUE` 或 `EXCLUDE` 约束，Apache Cloudberry 会从全部键列中选择最大的子集作为分布键。
- 如果没有约束，也没有 `LIKE` 或 `INHERITS` 子句，Apache Cloudberry 会选择第一个合适的列作为分布键。（几何类型或用户定义类型的列不符合 Apache Cloudberry 分布键列的要求。）

如果该参数设为 `on`，Apache Cloudberry 遵循以下规则：

- 如果未指定 `PRIMARY KEY`、`UNIQUE` 或 `EXCLUDE` 列，表将采用随机分布（`DISTRIBUTED RANDOMLY`）。即使建表命令包含 `LIKE` 或 `INHERITS` 子句，表分布仍是随机的。
- 如果指定了 `PRIMARY KEY`、`UNIQUE` 或 `EXCLUDE` 列，则还必须指定 `DISTRIBUTED BY` 子句。如果建表命令中未指定 `DISTRIBUTED BY` 子句，命令会失败。

`DISTRIBUTED REPLICATED` 子句将整张表复制到所有 Apache Cloudberry Segment 实例。当必须在 Segment 上运行需要访问表中所有行的用户定义函数时，或希望通过避免广播 Motion 提高查询性能时，可以使用此子句。

### 经典分区语法参数 {#classic-partitioning-syntax-parameters}

下面介绍*经典分区语法*特有的其他参数。

> **注意**：建议使用现代分区语法。

**`CREATE TABLE table_name ... PARTITION BY`**

使用*经典语法*创建分区表时，Apache Cloudberry 会使用指定的表名创建根分区表。Apache Cloudberry 还会根据指定的分区选项创建一个表层次结构，即作为子分区的子表。pg_partitioned_table 系统目录包含有关子分区表的信息。

**`classic_partition_spec`**

声明要创建的各个分区。可以单独定义每个分区；对于范围分区，也可以使用 `EVERY` 子句（带 `START` 和可选的 `END` 子句）定义用于创建各个分区的递增模式。

**`DEFAULT PARTITION name`**

声明默认分区。当数据与现有分区的边界不匹配时，Apache Cloudberry 会将其插入默认分区。不指定默认分区的分区设计会拒绝不匹配任何现有分区的输入行。

**`PARTITION name`**

声明分区使用的名称。分区按以下命名约定创建：`<table_name>_<level#>_prt_<given_name>`。

**`VALUES`**

对于列表分区，定义分区包含的值。

**`START`**

对于范围分区，定义分区的起始范围值。默认情况下，起始值为 `INCLUSIVE`。例如，如果声明起始日期为 '`2016-01-01`'，则分区会包含大于或等于 '`2016-01-01`' 的所有日期。`START` 表达式的数据类型必须支持合适的 `+` 操作符；如果使用 `EXCLUSIVE` 关键字，例如应为 `timestamp` 或 `integer`，不能为 `float` 或 `text`。通常，`START` 表达式的数据类型与分区键列相同；如果不同，则必须显式转换为目标数据类型。

**`END`**

对于范围分区，定义分区的结束范围值。默认情况下，结束值为 `EXCLUSIVE`。例如，如果声明结束日期为 '`2016-02-01`'，则分区会包含小于但不等于 '`2016-02-01`' 的所有日期。`END` 表达式的数据类型必须支持合适的 `+` 操作符；如果使用 `INCLUSIVE` 关键字，例如应为 `timestamp` 或 `integer`，不能为 `float` 或 `text`。通常，`END` 表达式的数据类型与分区键列相同；如果不同，则必须显式转换为目标数据类型。

**`EVERY`**

对于范围分区，定义从 `START` 到 `END` 创建各个分区时如何递增值。`EVERY` 表达式的数据类型通常与分区键列相同；如果不同，则必须显式转换为目标数据类型。

**`WITH`**

设置分区的表存储选项。例如，可以让较旧分区使用 AO 表，而较新分区使用普通堆表。请参阅下文的[存储参数](#storage-parameters)。

**`TABLESPACE`**

创建分区所在的表空间名称。

**`SUBPARTITION BY`**

声明对表的一级分区进行二次分区所依据的一个或多个列。对于 `LIST` 分区，分区键必须只包含一个列或表达式。子分区说明的格式与上文的分区说明类似。

**`SUBPARTITION TEMPLATE`**

无需为每个分区分别声明每个子分区定义，可以选择声明一个子分区模板，用于创建子分区（较低层级的子表）。此子分区说明随后会应用于所有父分区。

### 存储参数 {#storage-parameters}

`WITH` 子句可以为表，以及与 `UNIQUE`、`PRIMARY KEY` 或 `EXCLUDE` 约束关联的索引指定存储参数。索引的存储参数记录在 [CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/) 参考页中。当前可用于表的存储参数如下。如下所示，其中许多参数还有一个同名但带 `toast.` 前缀的参数，用于控制表的辅助 TOAST 表（如果有）的行为。如果设置了表参数值而没有设置对应的 `toast.` 参数，TOAST 表会使用表参数值。分区表不支持指定这些参数，但可以为单个叶子分区指定。

注意，也可以在*经典语法*分区说明中声明 `WITH` 子句，为特定分区或子分区设置存储参数。最低层分区的设置优先。

可以使用服务器配置参数 `gp_default_storage_options` 为部分表存储选项设置默认值。有关设置默认存储选项的信息，请参阅[注意事项](#notes)。

> **注意** 由于 Apache Cloudberry 不允许对用户表执行 autovacuum，因此会接受但不应用下文所述的某些表级参数设置。

可用的表存储参数如下：

**`analyze_hll_non_part_table`**

即使表不属于分区表，也可以将此存储参数设为 `true`，强制收集 HLL 统计信息。如果表将被交换或添加到分区表中，这很有用，因为不需要重新分析该表。默认值为 `false`。

**`appendoptimized`**

设为 `TRUE` 可将表创建为 AO 表。设为 `FALSE` 或不声明时，会将表创建为普通堆存储表。

**`blocksize`**

设置表中每个块的大小，单位为字节。`blocksize` 必须在 8192 到 2097152 字节之间，且为 8192 的倍数。默认值为 32768。只有 AO 表才支持 `blocksize` 选项。

**`checksum`**

此选项仅适用于 AO 表。默认值为 `TRUE`，启用 AO 表的 CRC 校验。创建块时计算校验和并存储在磁盘上；读取块时执行校验。如果读取时计算的校验和与已存储的校验和不匹配，事务会被取消。如果将值设为 `FALSE` 以禁用校验，就不会检查表数据是否存在磁盘损坏。

**`compresslevel`**

对于 AO 表的 Zstd 压缩，可设为 1（压缩最快）到 19（压缩比最高）之间的整数。对于 zlib 压缩，有效范围为 1 到 9。如果未声明，默认值为 1。对于 `RLE_TYPE`，压缩级别可设为 1（压缩最快）到 4（压缩比最高）之间的整数。

`compresslevel` 选项只有在表为 AO 表时才有效。

**`compresstype`**

设为 `ZLIB`（默认值）、`ZSTD` 或 `RLE_TYPE`，以指定压缩类型。值 `NONE` 禁用压缩。Zstd 可以兼顾速度和较高压缩比，通过 `compresslevel` 选项调节。zlib 用于向后兼容。在常见工作负载上，Zstd 优于这些压缩类型。只有 AO 表才支持 `compresstype` 选项。

值 `RLE_TYPE` 仅受 AO 列存表支持，用于启用游程编码（RLE）压缩算法。如果许多连续行具有相同的数据值，RLE 的压缩效果优于 Zstd 或 zlib。

对于 `BIGINT`、`INTEGER`、`DATE`、`TIME` 或 `TIMESTAMP` 类型的列，如果 `compresstype` 选项设为 `RLE_TYPE`，还会应用差分压缩。差分压缩算法基于连续行列值之间的差值，旨在数据按排序顺序加载，或对已排序的列数据进行压缩时改善压缩效果。

**`fillfactor`**

表的 fillfactor 是 10 到 100 之间的百分比。100（完全填充）是默认值。指定较小的 fillfactor 时，`INSERT` 操作只将表页面填充到指定比例；每个页面的剩余空间保留用于更新该页面上的行。这使 `UPDATE` 有机会将行的更新副本放在与原始行相同的页面上，比放到其他页面更高效。对于从不更新的表，完全填充是最佳选择；对于频繁更新的表，应使用较小的 fillfactor。TOAST 表不能设置此参数。

**`orientation`**

设为 `column` 使用列存储，设为 `row`（默认值）使用行存储。此选项仅适用于 AO 表。堆存储表只能使用行存储。

*以下参数仅支持堆表：*

**`toast_tuple_target (integer)`**

`toast_tuple_target` 指定 Apache Cloudberry 在尝试压缩和/或将较长列值移入 TOAST 表之前所需的最小元组长度，同时也是开始 TOAST 后 Apache Cloudberry 尝试将长度降低到的目标值。它影响标记为 External（用于移出）、Main（用于压缩）或 Extended（两者兼有）的列，且只适用于新元组。对已有行没有作用。默认情况下，该参数设置为每个块至少容纳 4 个元组；使用默认块大小时为 8184 字节。有效值介于 128 字节和（blocksize - header）之间，默认值为 8160 字节。对于非常短或非常长的行，修改此值可能没有用。注意，默认设置通常接近最优，设置此参数在某些情况下可能产生负面影响。不能为 TOAST 表设置此参数。

**`parallel_workers (integer)`**

设置用于辅助并行扫描此表的进程数。如果未设置，Apache Cloudberry 会根据关系大小确定数值。优化器或使用并行扫描的工具语句实际选择的进程数可能更少，例如受 `max_worker_processes` 设置影响。

**`autovacuum_enabled, toast.autovacuum_enabled (boolean)`**

启用或禁用特定表的 autovacuum 守护进程。如果为 `true`，autovacuum 守护进程将按照 PostgreSQL 文档中[autovacuum 守护进程](https://www.postgresql.org/docs/12/routine-vacuuming.html#AUTOVACUUM)所述规则，对该表自动执行 `VACUUM` 和/或 `ANALYZE` 操作。如果为 `false`，Apache Cloudberry 不会对表执行 autovacuum，但防止事务 ID 回卷除外。注意，如果 `autovacuum` 参数为 `false`，autovacuum 守护进程根本不会运行（防止事务 ID 回卷除外）；设置单个表的存储参数不会覆盖这一点。因此，显式将此存储参数设为 `true` 很少有意义，通常只会设为 `false`。

**`vacuum_index_cleanup, toast.vacuum_index_cleanup (boolean)`**

启用或禁用对该表执行 `VACUUM` 时的索引清理。默认值为 `true`。禁用索引清理可以显著加快 `VACUUM`，但如果表经常修改，也可能导致索引严重膨胀。`VACUUM` 的 `INDEX_CLEANUP` 参数（如果指定）会覆盖此选项的值。

当需要尽可能快地运行 `VACUUM` 时，例如为了避免即将发生的事务 ID 回卷，将其设为 `false` 可能有用。但如果不定期清理索引，性能可能下降，因为随着表被修改，索引会积累死亡元组，表本身也会积累死亡行指针，只有索引清理完成后才能移除。

**`vacuum_truncate, toast.vacuum_truncate (boolean)`**

启用或禁用清理时尝试截断表末尾的空页面。默认值为 `true`。为 `true` 时，`VACUUM` 和 autovacuum 会截断空页面，并将截断页面占用的磁盘空间返还给操作系统。注意，截断需要在表上获取 `ACCESS EXCLUSIVE` 锁。`VACUUM` 的 `TRUNCATE` 参数（如果指定）会覆盖此选项的值。

**`autovacuum_vacuum_threshold, toast.autovacuum_vacuum_threshold (integer)`**

服务器配置参数 `autovacuum_vacuum_threshold` 的表级值。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_vacuum_scale_factor, toast.autovacuum_vacuum_scale_factor (floating point)`**

服务器配置参数 `autovacuum_vacuum_scale_factor` 的表级值。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_analyze_threshold (integer)`**

服务器配置参数 `autovacuum_analyze_threshold` 的表级值。

**`autovacuum_analyze_scale_factor (floating point)`**

服务器配置参数 `autovacuum_analyze_scale_factor` 的表级值。

**`autovacuum_vacuum_cost_delay, toast.autovacuum_vacuum_cost_delay (floating point)`**

服务器配置参数 `autovacuum_vacuum_cost_delay` 的表级值。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_vacuum_cost_limit, toast.autovacuum_vacuum_cost_limit (integer)`**

服务器配置参数 `autovacuum_vacuum_cost_limit` 的表级值。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_freeze_min_age, toast.autovacuum_freeze_min_age (integer)`**

服务器配置参数 `vacuum_freeze_min_age` 的表级值。注意，autovacuum 会忽略大于系统范围 `autovacuum_freeze_max_age` 设置一半的表级 `autovacuum_freeze_min_age` 参数。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_freeze_max_age, toast.autovacuum_freeze_max_age (integer)`**

服务器配置参数 `autovacuum_freeze_max_age` 的表级值。注意，autovacuum 会忽略大于系统范围设置的表级 `autovacuum_freeze_max_age` 参数（只能将其设置得更小）。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_freeze_table_age, toast.autovacuum_freeze_table_age (integer)`**

服务器配置参数 `vacuum_freeze_table_age` 的表级值。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_multixact_freeze_min_age, toast.autovacuum_multixact_freeze_min_age (integer)`**

服务器配置参数 `vacuum_multixact_freeze_min_age` 的表级值。注意，autovacuum 会忽略大于系统范围 `autovacuum_multixact_freeze_max_age` 设置一半的表级 `autovacuum_multixact_freeze_min_age` 参数。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_multixact_freeze_max_age, toast.autovacuum_multixact_freeze_max_age (integer)`**

服务器配置参数 `autovacuum_multixact_freeze_max_age` 的表级值。注意，autovacuum 会忽略大于系统范围设置的表级 `autovacuum_multixact_freeze_max_age` 参数（只能将其设置得更小）。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`autovacuum_multixact_freeze_table_age, toast.autovacuum_multixact_freeze_table_age (integer)`**

服务器配置参数 `vacuum_multixact_freeze_table_age` 的表级值。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

**`log_autovacuum_min_duration, toast.log_autovacuum_min_duration (integer)`**

服务器配置参数 `log_autovacuum_min_duration` 的表级值。

> **注意** Apache Cloudberry 接受但不应用这些存储参数的值。

## 注意事项 {#notes}

Apache Cloudberry 会为每个唯一约束和主键约束自动创建索引来实施唯一性，因此无需专门为主键列创建索引。（更多信息请参阅 [CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/)。）

唯一约束和主键不会被继承。

不能定义包含超过 1600 列的表。（实际上，由于元组长度限制，有效上限通常更低。）

Apache Cloudberry 数据类型 `VARCHAR` 或 `TEXT` 会将添加到文本数据中的填充字符（最后一个非空格字符后添加的空格）视为有意义的字符；数据类型 `CHAR` 则不会。

在 Apache Cloudberry 中，`CHAR(<n>)` 类型的值会用尾随空格填充到指定宽度 `<n>`。这些值在存储和显示时都带有空格。不过，填充空格在语义上没有意义。分布数据时会忽略尾随空格。比较两个 `CHAR` 类型值时，尾随空格同样在语义上没有意义；将字符值转换为其他字符串类型时，会移除尾随空格。

对于 Apache Cloudberry 表中作为*分布键*的列，Apache Cloudberry 对主键和唯一约束有特殊要求。要在 Apache Cloudberry 中实施唯一约束，表必须使用哈希分布（不能使用 `DISTRIBUTED RANDOMLY`），并且约束列必须与表的分布键列相同，或是其超集。

复制表（`DISTRIBUTED REPLICATED`）可以同时具有 `PRIMARY KEY` 和 `UNIQUE` 列约束。

主键约束就是唯一约束和非空约束的组合。

Apache Cloudberry 不支持外键约束。

当前实现中，继承表不会继承唯一约束、主键约束、索引和表权限。

对于 AO 表，在可重复读或可串行化事务中不允许执行 `UPDATE` 和 `DELETE`，否则会导致事务提前结束。

AO 表不支持 `DECLARE...FOR UPDATE` 和触发器。

AO 表上的 `CLUSTER` 只支持 B-树 索引。

Apache Cloudberry 查询优化器不支持使用多列（复合）分区键的列表分区。

## 示例 {#examples}

在名为 `baby` 的模式中创建名为 `rank` 的表，并使用 `rank` 和 `year` 列分布数据：

```sql
CREATE TABLE baby.rank (id int, rank int, year smallint, count int )
DISTRIBUTED BY (rank, year);
```

创建名为 `films` 和 `distributors` 的表（默认使用主键作为 Apache Cloudberry 分布键）：

```sql
CREATE TABLE films (
    code        char(5) CONSTRAINT firstkey PRIMARY KEY,
    title       varchar(40) NOT NULL,
    did         integer NOT NULL,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute
);

CREATE TABLE distributors (
    did    integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name   varchar(40) NOT NULL CHECK (name <> '')
);
```

创建 gzip 压缩的 AO 表：

```sql
CREATE TABLE sales (txn_id int, qty int, date date) 
WITH (appendoptimized=true, compresslevel=5) 
DISTRIBUTED BY (txn_id);
```

创建带二维数组的表：

```sql
CREATE TABLE array_int (
    vector  int[][]
);
```

为表 `films` 定义唯一表约束。唯一表约束可以定义在表的一个或多个列上：

```sql
CREATE TABLE films (
    code        char(5),
    title       varchar(40),
    did         integer,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute,
    CONSTRAINT production UNIQUE(date_prod)
);
```

定义列级检查约束：

```sql
CREATE TABLE distributors (
    did     integer CHECK (did > 100),
    name    varchar(40)
);
```

定义表级检查约束：

```sql
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    CONSTRAINT con1 CHECK (did > 100 AND name <> '')
);
```

为表 `films` 定义表级主键约束：

```sql
CREATE TABLE films (
    code        char(5),
    title       varchar(40),
    did         integer,
    date_prod   date,
    kind        varchar(10),
    len         interval hour to minute,
    CONSTRAINT code_title PRIMARY KEY(code,title)
);
```

为表 `distributors` 定义主键约束。以下两个示例等价，第一个使用表约束语法，第二个使用列约束语法：

```sql
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    PRIMARY KEY(did)
);

CREATE TABLE distributors (
    did     integer PRIMARY KEY,
    name    varchar(40)
);
```

为 name 列指定字面量常量默认值；通过选择序列对象的下一个值生成列 `did` 的默认值；并将 `modtime` 的默认值设为插入行的时间：

```sql
CREATE TABLE distributors (
    name      varchar(40) DEFAULT 'Luso Films',
    did       integer DEFAULT nextval('distributors_serial'),
    modtime   timestamp DEFAULT current_timestamp
);
```

为表 `distributors` 定义两个 `NOT NULL` 列约束，其中一个显式指定名称：

```sql
CREATE TABLE distributors (
    did     integer CONSTRAINT no_null NOT NULL,
    name    varchar(40) NOT NULL
);
```

为 `name` 列定义唯一约束：

```sql
CREATE TABLE distributors (
    did     integer,
    name    varchar(40) UNIQUE
);
```

使用表约束写出相同定义：

```sql
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    UNIQUE(name)
);
```

创建同一张表，并为表及其唯一索引指定 70% 的填充因子：

```sql
CREATE TABLE distributors (
    did     integer,
    name    varchar(40),
    UNIQUE(name) WITH (fillfactor=70)
)
WITH (fillfactor=70);
```

在表空间 `diskvol1` 中创建表 `cinemas`：

```sql
CREATE TABLE cinemas (
        id serial,
        name text,
        location text
) TABLESPACE diskvol1;
```

创建复合类型和类型化表：

```sql
CREATE TYPE employee_type AS (name text, salary numeric);

CREATE TABLE employees OF employee_type (
    PRIMARY KEY (name),
    salary WITH OPTIONS DEFAULT 1000
);
```

### 现代分区语法示例 {#modern-partitioning-syntax-examples}

创建范围分区表：

```sql
CREATE TABLE measurement (
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (logdate);
```

创建分区键包含多个列的范围分区表：

```sql
CREATE TABLE measurement_year_month (
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (EXTRACT(YEAR FROM logdate), EXTRACT(MONTH FROM logdate));
```

创建列表分区表：

```sql
CREATE TABLE cities (
    city_id      bigserial not null,
    name         text not null,
    population   bigint
) PARTITION BY LIST (left(lower(name), 1));
```

创建哈希分区表：

```sql
CREATE TABLE orders (
    order_id     bigint not null,
    cust_id      bigint not null,
    status       text
) PARTITION BY HASH (order_id);
```

创建范围分区表的分区：

```sql
CREATE TABLE measurement_y2016m07
    PARTITION OF measurement (
    unitsales DEFAULT 0
) FOR VALUES FROM ('2016-07-01') TO ('2016-08-01');
```

创建分区键包含多个列的范围分区表的几个分区：

```sql
CREATE TABLE measurement_ym_older
    PARTITION OF measurement_year_month
    FOR VALUES FROM (MINVALUE, MINVALUE) TO (2016, 11);

CREATE TABLE measurement_ym_y2016m11
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 11) TO (2016, 12);

CREATE TABLE measurement_ym_y2016m12
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2016, 12) TO (2017, 01);

CREATE TABLE measurement_ym_y2017m01
    PARTITION OF measurement_year_month
    FOR VALUES FROM (2017, 01) TO (2017, 02);
```

创建列表分区表的分区：

```sql
CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b');
```

创建一个本身进一步分区的列表分区表的分区，然后向其中添加一个分区：

```sql
CREATE TABLE cities_ab
    PARTITION OF cities (
    CONSTRAINT city_id_nonzero CHECK (city_id != 0)
) FOR VALUES IN ('a', 'b') PARTITION BY RANGE (population);

CREATE TABLE cities_ab_10000_to_100000
    PARTITION OF cities_ab FOR VALUES FROM (10000) TO (100000);
```

创建哈希分区表的分区：

```sql
CREATE TABLE orders_p1 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE orders_p2 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE orders_p3 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE orders_p4 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

创建默认分区：

```sql
CREATE TABLE cities_partdef
    PARTITION OF cities DEFAULT;
```

### 经典分区语法示例 {#classic-partitioning-syntax-examples}

创建简单的单层分区表：

```sql
CREATE TABLE sales (id int, year int, qtr int, c_rank int, code char(1), region text)
DISTRIBUTED BY (id)
PARTITION BY LIST (code)
( PARTITION sales VALUES ('S'),
  PARTITION returns VALUES ('R')
);
```

创建定义子分区的三层分区表，不使用 `SUBPARTITION TEMPLATE` 子句：

```sql
CREATE TABLE sales (id int, year int, qtr int, c_rank int, code char(1), region text)
DISTRIBUTED BY (id)
PARTITION BY LIST (code)
  SUBPARTITION BY RANGE (c_rank)
    SUBPARTITION by LIST (region)

( PARTITION sales VALUES ('S')
   ( SUBPARTITION cr1 START (1) END (2)
      ( SUBPARTITION ca VALUES ('CA') ), 
      SUBPARTITION cr2 START (3) END (4)
        ( SUBPARTITION ca VALUES ('CA') ) ),

 PARTITION returns VALUES ('R')
   ( SUBPARTITION cr1 START (1) END (2)
      ( SUBPARTITION ca VALUES ('CA') ), 
     SUBPARTITION cr2 START (3) END (4)
        ( SUBPARTITION ca VALUES ('CA') ) )
);
```

使用 `SUBPARTITION TEMPLATE` 子句创建与上一个示例相同的分区表：

```sql
CREATE TABLE sales1 (id int, year int, qtr int, c_rank int, code char(1), region text)
DISTRIBUTED BY (id)
PARTITION BY LIST (code)

   SUBPARTITION BY RANGE (c_rank)
     SUBPARTITION TEMPLATE (
     SUBPARTITION cr1 START (1) END (2),
     SUBPARTITION cr2 START (3) END (4) )

     SUBPARTITION BY LIST (region)
       SUBPARTITION TEMPLATE (
       SUBPARTITION ca VALUES ('CA') )

( PARTITION sales VALUES ('S'),
  PARTITION  returns VALUES ('R')
);
```

使用各层级的子分区模板和默认分区创建三层分区表：

```sql
CREATE TABLE sales (id int, year int, qtr int, c_rank int, code char(1), region text)
DISTRIBUTED BY (id)
PARTITION BY RANGE (year)

  SUBPARTITION BY RANGE (qtr)
    SUBPARTITION TEMPLATE (
    START (1) END (5) EVERY (1), 
    DEFAULT SUBPARTITION bad_qtr )

    SUBPARTITION BY LIST (region)
      SUBPARTITION TEMPLATE (
      SUBPARTITION usa VALUES ('usa'),
      SUBPARTITION europe VALUES ('europe'),
      SUBPARTITION asia VALUES ('asia'),
      DEFAULT SUBPARTITION other_regions)

( START (2009) END (2011) EVERY (1),
  DEFAULT PARTITION outlying_years);
```

## 兼容性 {#compatibility}

`CREATE TABLE` 命令符合 SQL 标准，但有以下例外：

### 临时表 {#temporary-tables}

在 SQL 标准中，只定义一次临时表，并且每个需要它的会话都会自动拥有该表（初始内容为空）。而 Apache Cloudberry 要求每个会话分别为每个要使用的临时表执行自己的 `CREATE TEMPORARY TABLE` 命令。这样，不同会话可以将同一个临时表名用于不同目的；标准的方法则要求给定临时表名的所有实例具有相同的表结构。

SQL 标准区分全局和本地临时表，但 Apache Cloudberry 没有这一概念。Apache Cloudberry 会接受临时表声明中的 `GLOBAL` 和 `LOCAL` 关键字，但它们没有作用且已弃用。

如果省略 `ON COMMIT` 子句，SQL 标准规定默认行为为 `ON COMMIT DELETE ROWS`。而 Apache Cloudberry 的默认行为是 `ON COMMIT PRESERVE ROWS`。SQL 标准不存在 `ON COMMIT DROP` 选项。

### 不延迟的唯一性约束 {#non-deferred-uniqueness-constraints}

如果 `UNIQUE` 或 `PRIMARY KEY` 约束不可延迟，Greeplum Database 会在插入或修改行时立即检查唯一性。SQL 标准规定只能在语句末尾实施唯一性；例如，一条命令更新多个键值时，两者就有区别。要获得符合标准的行为，应将约束声明为 `DEFERRABLE` 但不延迟（例如 `INITIALLY IMMEDIATE`）。注意，这可能比立即检查唯一性慢得多。

### 列检查约束 {#column-check-constraints}

**列检查约束** — SQL 标准规定，`CHECK` 列约束只能引用其应用的列；只有 `CHECK` 表约束可以引用多个列。Apache Cloudberry 不实施此限制，而是将列约束和表约束同等处理。

**排他约束** — `EXCLUDE` 约束类型是 Apache Cloudberry 的扩展。

**NULL 约束** — `NULL` 约束是 Apache Cloudberry 对 SQL 标准的扩展，为兼容某些其他数据库系统（并与 `NOT NULL` 约束保持对称）而加入。由于它是任意列的默认设置，因此不需要显式出现。

### 约束命名 {#constraint-naming}

SQL 标准规定，表约束和域约束的名称在包含该表或域的模式中必须唯一。Apache Cloudberry 的要求更宽松：只需保证约束名在附加到某个特定表或域的约束中唯一。不过，对于基于索引的约束（`UNIQUE`、`PRIMARY KEY` 和 `EXCLUDE` 约束），不存在这种额外自由，因为关联索引与约束同名，而索引名在同一模式的所有关系中必须唯一。

Apache Cloudberry 当前完全不记录 `NOT NULL` 约束的名称，因此它们不受唯一性限制。

### 继承 {#inheritance}

通过 `INHERITS` 子句实现多重继承是 Apache Cloudberry 的语言扩展。SQL:1999 及更高版本使用不同语法和语义定义单继承。Apache Cloudberry 尚不支持 SQL:1999 风格的继承。

### 不含列的表 {#zero-column-tables}

Apache Cloudberry 允许创建没有列的表（例如 `CREATE TABLE foo();`）。这是 SQL 标准的扩展，标准不允许零列表。由于零列表本身用处不大，禁止它会给 `ALTER TABLE DROP COLUMN` 创建特殊情况，因此 Apache Cloudberry 忽略此标准限制。

### 多个标识列 {#multiple-identity-columns}

Apache Cloudberry 允许一张表有多个标识列。标准规定一张表最多只能有一个标识列。Apache Cloudberry 放宽这一限制，为模式变更或迁移提供更大灵活性。注意，`INSERT` 命令只支持一个应用于整个语句的覆盖子句，因此对行为不同的多个标识列支持并不完善。

### 生成列 {#generated-columns}

`STORED` 选项不是标准内容，但其他 SQL 实现也使用它。SQL 标准未规定生成列的存储方式。

### LIKE 子句 {#like-clause}

虽然 SQL 标准中存在 `LIKE` 子句，但 Apache Cloudberry 接受的许多选项并不属于标准，而且标准中的一些选项也未由 Apache Cloudberry 实现。

### WITH 子句 {#with-clause}

`WITH` 子句是 Apache Cloudberry 的扩展；存储参数属于标准内容。

### 表空间 {#tablespaces}

表空间是 Apache Cloudberry 的概念，不属于 SQL 标准。`TABLESPACE` 和 `USING INDEX TABLESPACE` 子句是扩展。

### 类型化表 {#typed-tables}

类型化表实现了 SQL 标准的一个子集。根据标准，类型化表除了具有与底层复合类型对应的列外，还应有一个“自引用列”。Apache Cloudberry 不显式支持自引用列。

### PARTITION BY 子句 {#partition-by-clause}

通过 `PARTITION BY` 子句进行表分区是 Apache Cloudberry 的扩展。

### PARTITION OF 子句 {#partition-of-clause}

通过 `PARTITION OF` 子句进行表分区是 Apache Cloudberry 的扩展。

### 数据分布 {#data-distribution}

并行或分布式数据库是 Apache Cloudberry 的概念，不属于 SQL 标准。`DISTRIBUTED` 子句是扩展。

## 另请参阅 {#see-also}

[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/), [DROP TABLE](/cloudberry/reference/sql-stmts/drop-table/), [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/), [CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/), [CREATE TABLESPACE](/cloudberry/reference/sql-stmts/create-tablespace/), [CREATE TYPE](/cloudberry/reference/sql-stmts/create-type/)
