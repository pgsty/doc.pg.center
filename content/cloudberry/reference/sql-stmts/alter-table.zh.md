---
title: "ALTER TABLE"
description: "修改表的定义。"
weight: 320
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-table.md"
---

## 概要 {#synopsis}

```sql
ALTER TABLE [IF EXISTS] [ONLY] <name> [ * ]
    <action> [, ... ]

ALTER TABLE [IF EXISTS] [ONLY] <name> [ * ]
    RENAME [COLUMN] <column_name> TO <new_column_name>

ALTER TABLE [IF EXISTS] [ ONLY ] <name> [ * ]
    RENAME CONSTRAINT <constraint_name> TO <new_constraint_name>

ALTER TABLE [IF EXISTS] <name> 
    RENAME TO <new_name>

ALTER TABLE [IF EXISTS] <name> 
    SET SCHEMA <new_schema>

ALTER TABLE ALL IN TABLESPACE <name> [ OWNED BY <role_name> [, ... ] ]
    SET TABLESPACE <new_tablespace> [ NOWAIT ]

ALTER TABLE [ IF EXISTS ] <name>
    ATTACH PARTITION <partition_name> { FOR VALUES <partition_bound_spec> | DEFAULT }

ALTER TABLE [ IF EXISTS ] <name>
    DETACH PARTITION <partition_name>

ALTER TABLE [IF EXISTS] [ONLY] <name> SET
   [ WITH (reorganize={ true | false }) ]
     DISTRIBUTED BY ({<column_name> [<opclass>]} [, ... ] )
   | DISTRIBUTED RANDOMLY
   | DISTRIBUTED REPLICATED

-- where <action> is one of:
                        
  ADD [COLUMN] [IF NOT EXISTS] <column_name> <data_type> [ COLLATE <collation> ] [<column_constraint> [ ... ]]
      [ ENCODING ( <storage_directive> [,...] ) ]
  DROP [COLUMN] [IF EXISTS] <column_name> [RESTRICT | CASCADE]
  ALTER [COLUMN] <column_name> [ SET DATA ] TYPE <data_type> [COLLATE <collation>] [USING <expression>]
  ALTER [COLUMN] <column_name> SET DEFAULT <expression>
  ALTER [COLUMN] <column_name> DROP DEFAULT
  ALTER [COLUMN] <column_name> { SET | DROP } NOT NULL
  ALTER [COLUMN] <column_name> ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( <sequence_options> ) ]
  ALTER [COLUMN] <column_name> { SET GENERATED { ALWAYS | BY DEFAULT } 
       | SET <sequence_option>
       | RESTART [ [ WITH ] <restart> ] } [...]
  ALTER [COLUMN] <column_name> DROP IDENTITY [ IF EXISTS ]
  ALTER [COLUMN] <column_name> SET STATISTICS <integer>
  ALTER [COLUMN] <column_name> SET ( <attribute_option> = <value> [, ... ] )
  ALTER [COLUMN] <column_name> RESET ( <attribute_option> [, ... ] )
  ALTER [COLUMN] <column_name> SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
  ALTER [COLUMN] <column_name> SET ENCODING ( storage_directive> [, ...] )
  ADD <table_constraint> [NOT VALID]
  ADD <table_constraint_using_index>
  ALTER CONSTRAINT <constraint_name> [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]
  VALIDATE CONSTRAINT <constraint_name>
  DROP CONSTRAINT [IF EXISTS] <constraint_name> [RESTRICT | CASCADE]
  DISABLE ROW LEVEL SECURITY
  ENABLE ROW LEVEL SECURITY
  FORCE ROW LEVEL SECURITY
  NO FORCE ROW LEVEL SECURITY
  CLUSTER ON <index_name>
  REPACK BY COLUMNS (<colum_name_1> [ASC|DESC], <column_name_2> [ASC|DESC], ...)
  SET WITHOUT CLUSTER
  SET WITHOUT OIDS
  SET TABLESPACE <new_tablespace>
  SET { LOGGED | UNLOGGED }
  SET ( <storage_parameter> [= <value>] [, ...])
  SET WITH (<set_with_parameter> = <value> [, ...])
  SET ACCESS METHOD <access_method>  [WITH ( <storage_parameter> = <value>, [, ...] )]
  RESET (<storage_parameter> [, ... ])
  INHERIT <parent_table>
  NO INHERIT <parent_table>
  OF <type_name>
  NOT OF
  OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

and <partition_bound_spec> is:

  IN ( <partition_bound_expr> [, ...] ) |
  FROM ( { <partition_bound_expr> | MINVALUE | MAXVALUE } [, ...] )
    TO ( { <partition_bound_expr> | MINVALUE | MAXVALUE } [, ...] ) |
  WITH ( MODULUS <numeric_literal>, REMAINDER <numeric_literal> )

-- and <column_constraint> is:

  [ CONSTRAINT <constraint_name>]
  { NOT NULL
    | NULL
    | CHECK  ( <expression> ) [ NO INHERIT ]
    | DEFAULT <default_expr>
    | GENERATED ALWAYS AS ( <generation_expr> ) STORED
    | GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( <sequence_options> ) ]
    | UNIQUE <index_parameters>
    | PRIMARY KEY <index_parameters>
    | REFERENCES <reftable> [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
        [ ON DELETE <referential_action> ] [ ON UPDATE <referential_action> ] }
  [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

-- and <table_constraint> is:

  [ CONSTRAINT <constraint_name> ]
  { CHECK ( <expression> ) [ NO INHERIT ]
    | UNIQUE ( <column_name> [, ... ] ) <index_parameters>
    | PRIMARY KEY ( <column_name> [, ... ] ) <index_parameters>
    | EXCLUDE [ USING <index_method> ] ( <exclude_element> WITH <operator> [, ... ] )
        <index_parameters> [ WHERE ( <predicate> ) ]
    | FOREIGN KEY ( <column_name> [, ... ] ) REFERENCES <reftable> [ ( <refcolumn> [, ... ] ) ]
        [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE <referential_action> ] [ ON UPDATE <referential_action> ] }
  [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

-- and <table_constraint_using_index> is:

  [ CONSTRAINT <constraint_name> ]
  { UNIQUE | PRIMARY KEY } USING INDEX <index_name>
  [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

-- and <index_parameters> in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

  [ INCLUDE ( <column_name> [, ... ] ) ]
  [ WITH ( <storage_parameter> [=<value>] [, ... ] ) ]
  [ USING INDEX TABLESPACE <tablespace_name> ]

-- and <exclude_element> in an EXCLUDE constraint is:

  { <column_name> | ( <expression> ) } [ <opclass> ] [ ASC | DESC ]
     [ NULLS { FIRST | LAST }

-- and <set_with_parameter> is:

   reorganize={ true | false } |
   orientation={COLUMN|ROW}
   appendoptimized={ true | false } [, <storage_parameter> [, ...]]
```

经典分区语法元素包括：

```sql
ALTER TABLE <name>
   [ ALTER PARTITION { <partition_name> | FOR (<value>) } [...] ] <partition_action>

-- where <partition_action> is one of:

  ALTER DEFAULT PARTITION
  DROP DEFAULT PARTITION [IF EXISTS]
  DROP PARTITION [IF EXISTS] { <partition_name> | 
      FOR (<value>) } [CASCADE]
  TRUNCATE DEFAULT PARTITION
  TRUNCATE PARTITION { <partition_name> | FOR (<value>) }
  RENAME DEFAULT PARTITION TO <new_partition_name>
  RENAME PARTITION { <partition_name> | FOR (<value>) } TO <new_partition_name>
  ADD DEFAULT PARTITION <name> [ ( <subpartition_spec> ) ]
  ADD PARTITION [<partition_name>] <partition_element>
     [ ( <subpartition_spec> ) ]
  EXCHANGE PARTITION { <partition_name> | FOR (<value>) } WITH TABLE <table_name>
        [ WITH | WITHOUT VALIDATION ]
  EXCHANGE DEFAULT PARTITION WITH TABLE <table_name>
   [ WITH | WITHOUT VALIDATION ]
  SET SUBPARTITION TEMPLATE (<subpartition_spec>)
  SPLIT DEFAULT PARTITION
    {  AT (<list_value>)
     | START([<datatype>] <range_value>) [INCLUSIVE | EXCLUSIVE] 
        END([<datatype>] <range_value>) [INCLUSIVE | EXCLUSIVE] }
    [ INTO ( PARTITION <new_partition_name>, 
             PARTITION <default_partition_name> ) ]
  SPLIT PARTITION { <partition_name> | FOR (<value>) } AT (<value>) 
    [ INTO (PARTITION <partition_name>, PARTITION <partition_name>)]  

-- and <partition_element> is:

    VALUES (<list_value> [,...] )
  | START ([<datatype>] '<start_value>') [INCLUSIVE | EXCLUSIVE]
     [ END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE] ]
  | END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE]
[ WITH ( <storage_parameter> = value> [ , ... ] ) ]
[ TABLESPACE <tablespace> ]

and <subpartition_spec> is:

<subpartition_element> [, ...]

-- and <subpartition_element> is:

   DEFAULT SUBPARTITION <subpartition_name>
  | [SUBPARTITION <subpartition_name>] VALUES (<list_value> [,...] )
  | [SUBPARTITION <subpartition_name>] 
     START ([<datatype>] '<start_value>') [INCLUSIVE | EXCLUSIVE]
     [ END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE] ]
     [ EVERY ( [<number | datatype>] '<interval_value>') ]
  | [SUBPARTITION <subpartition_name>] 
     END ([<datatype>] '<end_value>') [INCLUSIVE | EXCLUSIVE]
     [ EVERY ( [<number | datatype>] '<interval_value>') ]
[ WITH ( <storage_parameter>=<value> [, ... ] ) ]
[ TABLESPACE <tablespace> ]
```

## 说明 {#description}

`ALTER TABLE` 用于修改现有表的定义。下面描述了几种子形式。请注意，各子形式所需的锁级别可能不同。除非明确注明，否则都会获取 `ACCESS EXCLUSIVE` 锁。提供多个子命令时，Apache Cloudberry 会获取所有子命令所需锁中最严格的那一个。

**`ADD COLUMN [ IF NOT EXISTS ]`**

向表中添加新列，使用与 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) 相同的语法。如果指定了 `IF NOT EXISTS`，并且已经存在同名的列，则不会抛出错误。

**`DROP COLUMN [ IF EXISTS ]`**

从表中删除一列。请注意，如果删除了用作 Apache Cloudberry 分布键的表列，则该表的分布策略将被更改为 `DISTRIBUTED RANDOMLY`。涉及该列的索引和表约束也会被自动删除。如果删除该列会导致某个多元统计信息仅包含单个列的数据，则引用被删除列的多元统计信息也会被移除。如果表之外的任何对象（例如视图）依赖于该列，则需要指定 `CASCADE`。如果指定了 `IF EXISTS` 并且该列不存在，则不会抛出错误；Apache Cloudberry 会改为发出一条提示。

**`SET DATA TYPE`**

此形式修改表中某一列的数据类型。请注意，不能修改用作分布键或分区键的列的数据类型。涉及该列的索引和简单表约束将通过重新解析最初提供的表达式而自动转换为使用新的列类型。可选的 `COLLATE` 子句为新列指定排序规则；如果省略，则排序规则为新列类型的默认排序规则。可选的 `USING` 子句指定如何根据旧值计算新的列值。如果省略，默认转换与从旧数据类型到新数据类型的赋值类型转换相同。如果不存在从旧类型到新类型的隐式或赋值类型转换，则必须提供 `USING` 子句。

> **注意** 只有当查询中的所有列都使用相同的排序规则时，Cloudberry 查询优化器（GPORCA）才支持排序规则。如果查询中的列使用不同的排序规则，则 Apache Cloudberry 会使用 Postgres 规划器。

修改列的数据类型可能需要也可能不需要重写表。有关 `ALTER TABLE` 所执行的表重写的信息，请参阅[注解](#notes)。

**`SET DEFAULT`**<br />
**`DROP DEFAULT`**

设置或移除列的默认值。默认值仅适用于后续的 `INSERT` 或 `UPDATE` 命令；它们不会导致表中已有的行发生变化。

**`SET NOT NULL`**<br />
**`DROP NOT NULL`**

修改列是被标记为允许空值还是拒绝空值。

只有当表中没有任何记录在该列上包含 `NULL` 值时，才能对该列应用 `SET NOT NULL`。这通常在 `ALTER TABLE` 期间通过扫描整个表来检查；但是，如果发现一个有效的 `CHECK` 约束可以证明不可能存在 `NULL`，则 Apache Cloudberry 会跳过表扫描。

如果此表是一个分区，则当某列在父表中被标记为 `NOT NULL` 时，不能对该列执行 `DROP NOT NULL`。要从所有分区中删除 `NOT NULL` 约束，请在父表上执行 `DROP NOT NULL`。即使父表上没有 `NOT NULL` 约束，也仍然可以根据需要向各个分区添加这样的约束；也就是说，即使父表允许空值，子表也可以不允许空值，但反过来则不行。

**`ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY`**<br />
**`SET GENERATED { ALWAYS | BY DEFAULT }`**<br />
**`DROP IDENTITY [ IF EXISTS ]`**

这些形式修改列是否为标识列，或者修改现有标识列的生成属性。详情请参阅 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

如果指定了 `DROP IDENTITY IF EXISTS` 并且该列不是标识列，则不会抛出错误。在这种情况下，Apache Cloudberry 会改为发出一条提示。

**`SET sequence_option`**<br />
**`RESTART`**

这些形式修改现有标识列底层的序列。sequence_option 是 [ALTER SEQUENCE](/cloudberry/reference/sql-stmts/alter-sequence/) 所支持的选项，例如 `INCREMENT BY`。

**`SET STATISTICS`**

为后续的 [ANALYZE](/cloudberry/reference/sql-stmts/analyze/) 操作设置每列的统计信息收集目标。目标可以设置在 0 到 10000 的范围内，或者设置为 -1 以恢复使用系统默认的统计目标（`default_statistics_target`）。设置为 0 时，不收集统计信息。

`SET STATISTICS` 会获取 `SHARE UPDATE EXCLUSIVE` 锁。

**`SET ( attribute_option = value [, ... ] )`**<br />
**`RESET ( attribute_option [, ...] )`**

设置或重置每个属性的选项。目前，唯一定义的每属性选项是 `n_distinct` 和 `n_distinct_inherited`，它们会覆盖后续 [ANALYZE](/cloudberry/reference/sql-stmts/analyze/) 操作所做的不同值数量估计。`n_distinct` 影响表自身的统计信息，而 `n_distinct_inherited` 影响为该表及其继承子表所收集的统计信息。设置为正值时，`ANALYZE` 假定该列恰好包含指定数量的不同非空值。设置为负值（必须大于或等于 -1）时，`ANALYZE` 假定该列中不同非空值的数量与表的大小呈线性关系；确切的数量将通过把估计的表大小乘以给定数字的绝对值来计算。例如，值 -1 表示该列中的所有值都互不相同，而值 -0.5 表示每个值平均出现两次。当表的大小随时间变化时，这会很有用，因为乘以表中行数的操作要到查询规划时才会执行。指定值 0 可恢复为正常估计不同值的数量。

修改每个属性的选项会获取 `SHARE UPDATE EXCLUSIVE` 锁。

不要使用此形式的 `SET` 来设置追加优化列存表的属性编码选项。请改用 `ALTER COLUMN ... SET ENCODING ...`。

**`SET STORAGE`**

此形式设置列的存储模式。它控制该列是内联保存还是保存在辅助的 TOAST 表中，以及数据是否应被压缩。`PLAIN` 必须用于整数等定长值，为内联、不压缩。`MAIN` 用于内联、可压缩的数据。`EXTERNAL` 用于外部、不压缩的数据，`EXTENDED` 用于外部、压缩的数据。对于大多数支持非 `PLAIN` 存储的数据类型，`EXTENDED` 是默认值。使用 `EXTERNAL` 会使对非常大的 text 和 bytea 值的子串操作运行得更快，代价是增加存储空间。请注意，`SET STORAGE` 本身不会更改表中的任何内容，它只是设置在今后更新表时要采用的策略。

**`SET ENCODING ( storage_directive> [, ...] )`**

此形式为追加优化列存表设置列编码选项。

**`ADD table_constraint [ NOT VALID ]`**

使用与 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) 相同的语法向表中添加新约束。`NOT VALID` 选项目前仅允许用于外键约束和 `CHECK` 约束。

通常，此形式会导致扫描表，以验证表中所有现有行都满足新约束。如果约束被标记为 `NOT VALID`，Apache Cloudberry 会跳过这个可能耗时很长的初始检查，即不验证表中所有行是否满足该约束。该约束仍将对后续的插入或更新强制执行（也就是说，对于外键，除非被引用表中存在匹配的行，否则它们会失败；并且除非新行匹配指定的检查约束，否则它们会失败）。但是，在使用 `VALIDATE CONSTRAINT` 选项对其进行验证之前，数据库不会假定该约束对表中的所有行都成立。有关使用 `NOT VALID` 选项的更多信息，请参阅[注解](#notes)。

大多数形式的 `ADD <table_constraint>` 都需要 `ACCESS EXCLUSIVE` 锁。

向分区表添加唯一约束或主键约束时，适用额外的限制；请参阅 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`ADD table_constraint_using_index`**

此形式基于现有的唯一索引向表中添加新的 `PRIMARY KEY` 或 `UNIQUE` 约束。该索引的所有列都将包含在约束中。

该索引不能包含表达式列，也不能是部分索引。此外，它必须是采用默认排序顺序的 B-树索引。这些限制确保该索引等同于由常规 `ADD PRIMARY KEY` 或 `ADD UNIQUE` 命令所构建的索引。

如果指定了 `PRIMARY KEY`，并且该索引的列尚未被标记为 `NOT NULL`，则此命令会尝试对每个这样的列执行 `ALTER COLUMN SET NOT NULL`。这需要全表扫描来验证这些列不包含空值。在所有其他情况下，这是一个快速操作。

如果提供了约束名称，则 Apache Cloudberry 会重命名该索引以匹配约束名称。否则，约束将与索引同名。

执行此命令后，该索引由该约束“拥有”，就像该索引是由常规 `ADD PRIMARY KEY` 或 `ADD UNIQUE` 命令构建的一样。特别是，删除该约束也会使该索引消失。

此形式目前不支持分区表。

**`ALTER CONSTRAINT`**

此形式修改先前创建的约束的属性。目前只能修改外键约束，Apache Cloudberry 会接受但不会强制执行。

**`VALIDATE CONSTRAINT`**

此形式验证先前以 `NOT VALID` 创建的外键约束，方法是扫描表以确保不存在不满足该约束的行。如果约束已被标记为有效，则不会发生任何事情。将验证与约束的初始创建分开的好处是，验证对表所需的锁比创建约束所需的锁更低。

此命令会获取 `SHARE UPDATE EXCLUSIVE` 锁。

**`DROP CONSTRAINT [IF EXISTS]`**

删除表上的指定约束，以及该约束底层的任何索引。如果指定了 `IF EXISTS` 并且该约束不存在，则不会抛出错误。在这种情况下，Apache Cloudberry 会改为发出一条提示。

**`DISABLE ROW LEVEL SECURITY`**<br />
**`ENABLE ROW LEVEL SECURITY`**

这些形式控制是否应用属于该表的行安全策略。如果启用且该表不存在任何策略，则 Apache Cloudberry 会应用默认拒绝策略。请注意，即使禁用了行级安全性，表也可以存在策略——在这种情况下，策略将不会被应用，并且会被忽略。另请参阅 [CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/)。

**`NO FORCE ROW LEVEL SECURITY`**<br />
**`FORCE ROW LEVEL SECURITY`**

这些形式控制当用户是表所有者时，是否应用属于该表的行安全策略。如果启用，则当用户是表所有者时将应用行级安全策略。如果禁用（默认值），则当用户是表所有者时不会应用行级安全性。另请参阅 [CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/)。

**`CLUSTER ON`**

选择今后 [CLUSTER](/cloudberry/reference/sql-stmts/cluster/) 操作的默认索引。它实际上并不会对表重新聚簇。

修改聚簇选项会获取 `SHARE UPDATE EXCLUSIVE` 锁。

**`REPACK BY COLUMNS`**

基于一个或多个列对表进行物理重排，以改善物理相关性。你需要指定一个或多个列，以及可选的列顺序。如果未指定，默认为 `ASC`。该命令等同于 [CLUSTER](/cloudberry/reference/sql-stmts/cluster/) 命令，但它使用所提供的列列表而不是索引来确定排序顺序。

该命令对于以小批量加载的表特别有用。你可以将 `REPACK BY COLUMNS` 与大多数不需要重写表的其他 `ALTER TABLE` 命令组合使用。你可以使用 `REPACK BY COLUMNS` 在对表进行物理重排的同时添加压缩或更改表现有的压缩设置，从而获得更好的压缩效果和存储效果。更多详情请参阅[示例](#examples)。

**`SET WITHOUT CLUSTER`**

从表中移除最近使用的 [CLUSTER](/cloudberry/reference/sql-stmts/cluster/) 索引规范。这会影响今后未指定索引的聚簇操作。

修改聚簇选项会获取 `SHARE UPDATE EXCLUSIVE` 锁。

**`SET TABLESPACE`**

将表的表空间更改为指定的表空间，并将与该表关联的数据文件移动到新的表空间。表上的索引（如果有）不会被移动；但可以用额外的 `SET TABLESPACE` 命令分别移动它们。应用于分区表时，不会移动任何内容，但此后使用 `CREATE TABLE ... PARTITION OF` 创建的任何分区都将使用该表空间，除非使用 `TABLESPACE` 子句覆盖它。

使用 `ALL IN TABLESPACE` 形式可以移动当前数据库中某个表空间内的所有表，该形式会先锁定所有要移动的表，然后逐个移动。此形式还支持 `OWNED BY`，它只会移动由指定角色拥有的表。如果指定了 `NOWAIT` 选项，则当命令无法立即获取所需的全部锁时将会失败。请注意，此命令不会移动系统目录，如有需要，请改用 `ALTER DATABASE` 或显式的 `ALTER TABLE` 调用。`information_schema` 关系不被视为系统目录的一部分，因此会被移动。另请参阅 [CREATE TABLESPACE](/cloudberry/reference/sql-stmts/create-tablespace/)。

如果更改分区表的表空间，则所有子表也将被移动到新的表空间。

**`SET { LOGGED | UNLOGGED }`**

此形式将表从非日志表改为日志表，或反之。它不能应用于临时表。

**`SET ( storage_\parameter [= value] [, ... ] )`**

此形式修改一个或多个表级选项。有关可用参数的详情，请参阅 `CREATE TABLE` 参考页中的[存储参数](/cloudberry/reference/sql-stmts/create-table/#storage-parameters)。请注意，对于堆表，此命令不会立即修改表的内容；根据参数的不同，你可能需要重写表才能获得所需的效果。这可以通过 [VACUUM FULL](/cloudberry/reference/sql-stmts/vacuum/)、[CLUSTER](/cloudberry/reference/sql-stmts/cluster/) 或强制重写表的某种 `ALTER TABLE` 形式来完成，请参阅[注解](#notes)。对于追加优化列存表，修改存储参数总会导致表重写。对于与规划器相关的参数，更改从下一次锁定该表时开始生效，因此当前正在执行的查询不受影响。

设置 `fillfactor`、toast 和 autovacuum 存储参数以及规划器参数 `parallel_workers` 时，Apache Cloudberry 会获取 `SHARE UPDATE EXCLUSIVE` 锁。

**`RESET ( storage_parameter [, ... ] )`**

此形式将一个或多个表级选项重置为其默认值。与 `SET` 一样，可能需要重写表才能完全更新该表。

**`SET WITH (<set_with_parameter> = <value> [, ...])`**

你可以使用此形式的命令重组表，或者设置表访问方法，并可选地设置存储参数。

> **注意：**
>
> 尽管你可以使用 `appendoptimized` 和 `orientation` 存储参数来指定表的访问方法，但我们建议你改用 `SET ACCESS METHOD <access_method>`。

**`INHERIT parent_table`**

将目标表添加为指定父表的新子表。针对父表的查询将包含目标表的记录。要被添加为子表，目标表必须已经包含与父表相同的所有列（也可以有额外的列）。这些列必须具有匹配的数据类型，并且如果它们在父表中具有 `NOT NULL` 约束，则在子表中也必须具有 `NOT NULL` 约束。

对于父表的所有 `CHECK` 约束，还必须存在匹配的子表约束，但父表中标记为不可继承的约束（即使用 `ALTER TABLE ... ADD CONSTRAINT ... NO INHERIT` 创建的约束）除外，这些约束会被忽略；所有被匹配的子表约束都不得被标记为不可继承。目前不考虑 `UNIQUE`、`PRIMARY KEY` 和 `FOREIGN KEY` 约束。

**`NO INHERIT parent_table`**

此形式将目标表从指定父表的子表列表中移除。针对父表的查询将不再包含取自目标表的记录。

**`OF type_name`**

此形式将表链接到一个复合类型，就如同它是由 `CREATE TABLE OF` 形成的一样。表的列名和类型列表必须与该复合类型的列表精确匹配。该表不得继承自任何其他表。这些限制确保 `CREATE TABLE OF` 会允许等价的表定义。

**`NOT OF`**

此形式解除类型化表与其类型的关联。

**`OWNER TO`**

将表、序列、视图、物化视图或外表的所有者更改为指定的用户。

**`RENAME`**

更改表（或索引、序列、视图、物化视图或外表）的名称、表中单个列的名称，或表的某个约束的名称。重命名具有底层索引的约束时，该索引也会被重命名。这对存储的数据没有影响。

**`SET SCHEMA`**

将表移动到另一个模式。关联的索引、约束以及由表列所拥有的序列也会一并移动。

**`SET DISTRIBUTED`**

更改表的分布策略。更改哈希分布策略，或者在复制策略与其他策略之间切换，会导致表数据在磁盘上被物理重分布，这可能会消耗大量资源。如果声明相同的哈希分布策略，或者从哈希分布改为随机分布，则除非声明 `SET WITH (reorganize=true)`，否则不会重分布数据。

虽然 Apache Cloudberry 允许更改可写外部表的分布策略，但该操作绝不会导致外部数据的物理重分布。

**`ATTACH PARTITION partition_name { FOR VALUES partition_bound_spec | DEFAULT }`**

这是*现代分区语法*的一种形式，它将现有的表（该表本身也可以是分区表）作为目标表的一个分区附加上去。可以使用 `FOR VALUES` 将表附加为特定值的分区，也可以使用 `DEFAULT` 将其附加为默认分区。对于目标表中的每个索引，将在被附加的表中创建一个对应的索引；或者，如果已经存在等价的索引，则它将被附加到目标表的索引上，就像你运行了 `ALTER INDEX ATTACH PARTITION` 一样。请注意，如果现有表是外表，并且目标表上存在 `UNIQUE` 索引，则 Cloudberry 不允许将该表附加为目标表的分区。（另请参阅 [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/)。）

使用 `FOR VALUES` 的分区对 partition_bound_spec> 使用与 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) 相同的语法。分区边界规范必须与目标表的分区策略和分区键相对应。要附加的表必须具有与目标表完全相同的所有列，不能多也不能少；此外，列的类型也必须匹配。同时，它必须具有目标表的所有 `NOT NULL` 和 `CHECK` 约束。目前不考虑 `FOREIGN KEY` 约束。如果父表中的 `UNIQUE` 和 `PRIMARY KEY` 约束在分区中尚不存在，则将在分区中创建它们。如果被附加表的任何 `CHECK` 约束被标记为 `NO INHERIT`，则命令将失败；此类约束必须在不带 `NO INHERIT` 子句的情况下重新创建。

如果新分区是常规表，则 Apache Cloudberry 会执行全表扫描，以检查表中现有的行没有违反分区约束。可以通过在运行此命令之前向表添加一个有效的 `CHECK` 约束来避免这次扫描，该约束仅允许满足所需分区约束的行。该 `CHECK` 约束将用于判定无需扫描该表来验证分区约束。但是，如果任何分区键是表达式，并且该分区不接受 `NULL` 值，则这种做法不起作用。如果附加的是不接受 `NULL` 值的列表分区，则还应向分区键列添加 `NOT NULL` 约束，除非它是表达式。

如果新分区是外表，则不会做任何事情来验证外表中的所有行是否遵守分区约束。（请参阅 [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) 中关于外表上约束的讨论。）

当表具有默认分区时，定义新分区会更改默认分区的分区约束。默认分区不能包含任何需要移动到新分区的行，并且将被扫描以验证不存在此类行。与对新分区的扫描一样，如果存在适当的 `CHECK` 约束，则可以避免这次扫描。同样与对新分区的扫描一样，当默认分区是外表时，总是会跳过该扫描。

附加分区时，除了对被附加的表和默认分区（如果有）获取 `ACCESS EXCLUSIVE` 锁之外，还会对父表获取 `SHARE UPDATE EXCLUSIVE` 锁。

如果被附加的表本身是分区表，则必须对其所有子分区额外持有锁。如果默认分区本身是分区表，情况同样如此。可以通过添加 `CHECK` 约束来避免对子分区加锁，具体见对大型表分区的相关说明。

**`DETACH PARTITION partition_name`**

这是*现代分区语法*的一种形式，它分离目标表的指定分区。被分离的分区继续作为独立的表存在，但与其被分离出来的表不再有任何关联。附加到目标表索引上的任何索引都会被分离。

**`ALTER PARTITION | DROP PARTITION | RENAME PARTITION | TRUNCATE PARTITION | ADD PARTITION | SPLIT PARTITION | EXCHANGE PARTITION | SET SUBPARTITION TEMPLATE`**

这些是*经典分区语法*的形式，用于更改分区表的结构。你必须通过父表来修改它的某个子表。

> **注意** 如果向具有子分区编码的表添加分区，则新分区会继承子分区的存储指令。

你可以把所有作用于单个表的 `ALTER TABLE` 形式组合成一个由多个修改组成的列表一并应用，但 `RENAME`、`SET SCHEMA`、`ATTACH PARTITION` 和 `DETACH PARTITION` 除外。例如，可以在单个命令中添加多个列和/或修改多个列的类型。这对于大型表特别有用，因为只需对表遍历一遍。

你必须是表的所有者才能使用 `ALTER TABLE`。要更改表的模式或表空间，你还必须拥有新模式或表空间上的 `CREATE` 权限。要将表添加为某个父表的新子表，你还必须拥有该父表。同样，要将表附加为该表的新分区，你必须拥有被附加的表。要修改所有者，你还必须是新所属角色的直接或间接成员，并且该角色必须拥有该表所在模式上的 `CREATE` 权限。要添加列、修改列类型或使用 `OF` 子句，你还必须拥有该数据类型上的 `USAGE` 权限。超级用户自动拥有这些权限。

> **注意** 当表具有许多分区、表使用了压缩，或者表的块大小较大时，内存使用量会显著增加。如果与该表关联的关系数量很大，这种情况会迫使对该表的操作使用更多内存。例如，如果该表是追加优化列存表并且有大量的列，则每一列都是一个关系。访问表中所有列的操作会分配相应的缓冲区。如果该表有 40 列和 100 个分区，列已压缩且块大小为 2 MB（系统因子为 3），则系统会尝试分配 24 GB，即 (40 ×100) × (2 ×3) MB 或 24 GB。

## 参数 {#parameters}

**`IF EXISTS`**

如果表不存在，不要抛出错误。在这种情况下，Apache Cloudberry 会发出一条提示。

**`name`**

要修改的现有表的名称（可以带模式限定）。如果指定了 `ONLY`，则仅修改该表。如果未指定 `ONLY`，则该表及其所有后代表（如果有）都会被更新。你可以选择在表名后指定 `*`，以明确表示包含后代表。

> **注意** 不允许仅在父表或后代表中添加或删除列，或更改列的类型。父表及其后代表必须始终具有相同的列和类型。

**`column_name`**

新列或现有列的名称。请注意，Apache Cloudberry 分布键列必须特别小心地对待。修改或删除这些列可能会更改表的分布策略。

**`new_column_name`**

现有列的新名称。

**`new_name`**

表的新名称。

**`type`**

新列的数据类型，或现有列的新数据类型。如果要更改 Cloudberry 分布键列的数据类型，则只允许将其更改为兼容的类型（例如，`text` 改为 `varchar` 可以，但 `text` 改为 `int` 不行）。

**`table_constraint`**

表的新表约束。请注意，Apache Cloudberry 目前不支持外键约束。此外，一个表只允许有一个唯一约束，并且唯一性必须包含在 Apache Cloudberry 分布键之内。

**`constraint_name`**

要删除的现有约束的名称。

**`ENCODING ( <storage_directive> [,...] )`**

`ENCODING` 子句仅对追加优化列存表有效。

向追加优化列存表添加列时，Apache Cloudberry 会按照以下优先顺序，根据下列设置来设定该列的每个数据压缩参数（`compresstype`、`compresslevel` 和 `blocksize`）。

1. `ALTER TABLE` 命令的 `ENCODING` 子句中指定的压缩参数设置。
2. 创建表时在 `WITH` 子句中指定的表的数据压缩设置。
3. 服务器配置参数 gp_default_storage_option 中指定的压缩参数设置。
4. 默认的压缩参数值。

有关所支持的 `ENCODING` 存储指令的更多信息，请参阅 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`CASCADE`**

自动删除依赖于被删除的列或约束的对象（例如引用该列的视图），以及依次依赖于这些对象的所有对象。

**`RESTRICT`**

如果存在任何依赖对象，则拒绝删除该列或约束。这是默认行为。

**`index_name`**

现有索引的名称。

**`storage_parameter`**

表存储参数的名称。有关参数列表，请参阅 `CREATE TABLE` 参考页上的[存储参数](/cloudberry/reference/sql-stmts/create-table/#storage-parameters)一节。

**`value`**

表存储参数的新值。根据参数的不同，这可能是数字或单词。

**`parent_table`**

要与此表关联或解除关联的父表。

**`new_owner`**

表的新所有者的角色名称。

**`new_tablespace`**

表将被移动到的表空间的名称。

**`new_schema`**

表将被移动到的模式的名称。

**`partition_name`**

要作为新分区附加或要从此表分离的表的名称。

**`partition_bound_spec`**

新分区的分区边界规范。有关其语法的更多详情，请参阅 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`access_method`**

用于访问表的方法。有关 Apache Cloudberry 中可用的表存储模型和访问方法的更多信息，请参阅选择存储模型。设置为 `heap` 可将表作为堆存储表来访问，设置为 `ao_row` 可将表作为行存储的追加优化表（AO）来访问，设置为 `ao_column` 可将表作为列存储的追加优化表（AO/CO）来访问。

> **注意：**
>
> 尽管你可以使用 `SET <storage_parameter>` 来指定表的访问方法，但我们建议你改用 `SET ACCESS METHOD <access_method>`。

**`SET WITH (reorganize=true|false)`**

当哈希分布策略没有变化，或者你已从哈希分布改为随机分布，并且仍希望重分布数据时，请使用 `reorganize=true`。

如果要设置分布策略，则必须在 `DISTRIBUTED ...` 子句之前指定 `WITH (reorganize=<value>)` 子句。

任何重组外部表的尝试都会因错误而失败。

### 经典分区语法参数 {#classic-partitioning-syntax-parameters}

下面描述特定于*经典分区语法*的其他参数。

**`ALTER [DEFAULT] PARTITION`**

如果要修改比第一级分区更深层的分区，请使用 `ALTER PARTITION` 子句来指定要修改层次结构中的哪个子分区。对于表层次结构中位于目标分区之上的每一个分区级别，请在 `ALTER PARTITION` 子句中指定与目标分区相关的分区。

**`DROP [DEFAULT] PARTITION`**

删除指定的分区。如果该分区有子分区，则这些子分区也会被自动删除。

**`TRUNCATE [DEFAULT] PARTITION`**

截断指定的分区。如果该分区有子分区，则这些子分区也会被自动截断。

**`RENAME [DEFAULT] PARTITION`**

更改分区的分区名称（而不是关系名称）。分区表使用以下命名约定创建：`<`parentname`>_<`level`>_prt_<`partition_name`>`。

**`ADD DEFAULT PARTITION`**

向现有的分区设计添加默认分区。当数据与现有分区都不匹配时，将被插入默认分区。没有默认分区的分区设计会拒绝与现有分区都不匹配的传入行。默认分区必须指定名称。

**`ADD PARTITION`**

partition_element - 使用表现有的分区类型（范围或列表），定义你要添加的新分区的边界。

name - 此新分区的名称。

**VALUES** - 对于列表分区，定义该分区将包含的值。

**START** - 对于范围分区，定义该分区的起始范围值。默认情况下，起始值为 `INCLUSIVE`。例如，如果你声明起始日期为 '`2016-01-01`'，则该分区将包含大于或等于 '`2016-01-01`' 的所有日期。如果 `START` 表达式使用 `EXCLUSIVE` 关键字定义，则其数据类型必须支持合适的 `+` 操作符，例如 `timestamp` 或 `integer`（而不是 `float` 或 `text`）。通常，`START` 表达式的数据类型与分区键列的类型相同。如果不是这种情况，则必须显式转换为预期的数据类型。

**END** - 对于范围分区，定义该分区的结束范围值。默认情况下，结束值为 `EXCLUSIVE`。例如，如果你声明结束日期为 '`2016-02-01`'，则该分区将包含小于但不等于 '`2016-02-01`' 的所有日期。如果 `END` 表达式使用 `INCLUSIVE` 关键字定义，则其数据类型必须支持合适的 `+` 操作符，例如 `timestamp` 或 `integer`（而不是 `float` 或 `text`）。通常，`END` 表达式的数据类型与分区键列的类型相同。如果不是这种情况，则必须显式转换为预期的数据类型。

**WITH** - 设置分区的表存储选项。例如，你可能希望较旧的分区是追加优化表，而较新的分区是常规堆表。有关存储选项的说明，请参阅 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**TABLESPACE** - 要在其中创建该分区的表空间的名称。

subpartition_spec - 仅允许用于创建时没有使用子分区模板的分区设计。为你要添加的新分区声明子分区规范。如果分区表最初是使用子分区模板定义的，则将使用该模板自动生成子分区。

**`EXCHANGE [DEFAULT] PARTITION`**

将另一个表交换到分区层次结构中，替换现有的某个分区。在多级分区设计中，只能交换最低级别的分区（即包含数据的分区）。

**WITH TABLE** table_name - 要交换到分区设计中的表的名称。你可以交换数据存储在数据库中的表。例如，使用 `CREATE TABLE` 命令创建的表。该表必须与父表具有相同的列数、列顺序、列名、列类型和分布策略。

使用 `EXCHANGE PARTITION` 子句，你还可以将可读外部表（使用 `CREATE EXTERNAL TABLE` 命令创建）交换到分区层次结构中，替换现有的某个叶子分区。

如果分区表包含带有检查约束或 `NOT NULL` 约束的列，则不支持用外部表交换叶子分区。

不能用复制表交换分区。不支持用分区表或分区表的子分区来交换分区。

**WITH** | **WITHOUT VALIDATION** - 空操作（始终根据分区约束验证数据）。

**`SET SUBPARTITION TEMPLATE`**

修改现有分区的子分区模板。设置新的子分区模板之后，所有新添加的分区都将采用新的子分区设计（现有分区不会被修改）。

**`SPLIT DEFAULT PARTITION`**

拆分默认分区。在多级分区中，只能拆分范围分区，而不能拆分列表分区，并且只能拆分最低级别的默认分区（即包含数据的分区）。拆分默认分区会创建一个包含指定值的新分区，并使默认分区保留所有与现有分区都不匹配的值。

**AT** - 对于列表分区表，指定用作拆分条件的单个列表值。

**START** - 对于范围分区表，指定新分区的起始值。

**END** - 对于范围分区表，指定新分区的结束值。

**INTO** - 允许你为新分区指定名称。使用 `INTO` 子句拆分默认分区时，指定的第二个分区名称应始终是现有默认分区的名称。如果你不知道默认分区的名称，可以使用 pg_partitions 视图查找。

**`SPLIT PARTITION`**

将现有分区拆分为两个分区。在多级分区中，只能拆分范围分区，而不能拆分列表分区，并且只能拆分最低级别的分区（即包含数据的分区）。

**AT** - 指定用作拆分条件的单个值。该分区将被划分为两个新分区，所指定的拆分值将作为后一个分区的起始范围。

**INTO** - 允许你为拆分所创建的两个新分区指定名称。

**`partition_name`**

分区的给定名称。你可以使用 `pg_partition_tree() 函数获取分区表的叶子分区的表名。

**`FOR ('value')`**

通过声明一个落在分区边界规范内的值来指定分区。如果用 `FOR` 声明的值同时匹配某个分区及其某个子分区（例如，值是日期，且表先按月再按日分区），则 `FOR` 将在找到匹配的第一级上操作（例如，按月分区）。如果你打算操作某个子分区，则必须按如下方式声明：`ALTER TABLE name ALTER PARTITION FOR ('2016-10-01') DROP PARTITION FOR ('2016-10-01');`

## 注解 {#notes}

关键字 `COLUMN` 是噪声词，可以省略。

使用 `ADD COLUMN` 添加列时，表中所有现有的行都会用该列的默认值初始化；如果未指定 `DEFAULT` 子句，则初始化为 `NULL`。添加带有非空默认值的列，或更改现有列的类型，将需要重写整个表和索引。作为例外，如果 `USING` 子句不更改列内容，并且旧类型可以二进制强制转换为新类型，或者是新类型之上的无约束域，则不需要重写表，但受影响列上的任何索引仍必须重建。对于大型表，重建表和/或索引可能需要大量时间；并且会临时需要多达两倍的磁盘空间。

添加 `CHECK` 或 `NOT NULL` 约束需要扫描表，以验证现有行满足该约束，但不需要重写表。

同样，附加新分区时，可能会对其进行扫描，以验证现有行满足分区约束。

Apache Cloudberry 提供了在单个 `ALTER TABLE` 中指定多项更改的选项，这样可以将多次表扫描或重写合并为对表的一次遍历。

扫描大型表以验证新的检查约束可能需要很长时间，并且在 `ALTER TABLE ADD CONSTRAINT` 命令提交之前，对该表的其他更新都会被锁定。`NOT VALID` 约束选项的主要目的是减少添加约束对并发更新的影响。使用 `NOT VALID` 时，`ADD CONSTRAINT` 命令不会扫描表，可以立即提交。此后，可以发出 `VALIDATE CONSTRAINT` 命令来验证现有行满足该约束。验证步骤不需要锁定并发更新，因为它知道其他事务将对它们插入或更新的行强制执行该约束；只需要检查已有的行。因此，验证只对被修改的表获取 `SHARE UPDATE EXCLUSIVE` 锁。除了提高并发性之外，在已知表中存在已有违规数据的情况下，使用 `NOT VALID` 和 `VALIDATE CONSTRAINT` 也会很有用。一旦约束就位，就不能再插入新的违规数据，并且你可以修正现有的问题，直到 `VALIDATE CONSTRAINT` 最终成功。

`DROP COLUMN` 形式并不会物理移除该列，只是使其对 SQL 操作不可见。表中随后的插入和更新操作将为该列存储空值。因此，删除列的速度很快，但不会立即减小表的磁盘大小，因为被删除列所占用的空间并未回收。随着现有行的更新，空间将逐渐被回收。但是，如果删除系统 `oid` 列，则会立即重写表。

要强制立即回收被删除列所占用的空间，可以运行某种会重写整个表的 `ALTER TABLE` 形式。这会重建每一行，并将被删除的列替换为空值。

下表列出了对采用指定表存储类型定义的表执行时需要重写表的 `ALTER TABLE` 操作。

|操作（见注意）|追加优化列存|追加优化|堆|
|----------------------|---------------------------------|----------------|----|
|`ALTER COLUMN TYPE`|否|是|是|
|`ADD COLUMN`|否|否|否|
| `ALTER COLUMN SET ENCODING`|否|不适用|不适用|

> **重要** 执行表重写的 `ALTER TABLE` 形式不是 MVCC 安全的。表重写之后，如果并发事务使用的是重写发生之前获取的快照，则该表对它们而言将显示为空。更多详情请参阅 [MVCC 注意事项](https://www.postgresql.org/docs/12/mvcc-caveats.html)。

修改或删除属于 Apache Cloudberry 分布键的列时要格外小心，因为这可能会更改表的分布策略。

`SET DATA TYPE` 的 `USING` 选项实际上可以指定任何涉及该行旧值的表达式；也就是说，它可以引用被转换的列以外的其他列。这使得可以用 `SET DATA TYPE` 语法完成非常通用的转换。由于这种灵活性，`USING` 表达式不会应用于该列的默认值（如果有）；其结果可能不是默认值所要求的常量表达式。这意味着，当不存在从旧类型到新类型的隐式或赋值类型转换时，即使提供了 `USING` 子句，`SET DATA TYPE` 也可能无法转换默认值。在这种情况下，请使用 `DROP DEFAULT` 删除默认值，执行 `ALTER TYPE`，然后使用 `SET DEFAULT` 添加合适的新默认值。涉及该列的索引和约束也有类似的考虑。

如果表有任何后代表，则不允许在不对后代表做同样操作的情况下，在父表中添加、重命名列或更改列的类型。这确保后代表中的列始终与父表匹配。同样，不能在父表中重命名 `CHECK` 约束而不同时在所有后代表中重命名它，这样父表与其后代表之间的 `CHECK` 约束也是匹配的。（但是，该限制不适用于基于索引的约束。）此外，由于从父表中选择也会从其后代表中选择，因此除非父表上的约束对这些后代表也被标记为有效，否则它不能被标记为有效。在所有这些情况下，`ALTER TABLE ONLY` 都将被拒绝。

递归的 `DROP COLUMN` 操作只有在后代表不从任何其他父表继承该列，并且从未对该列有过独立定义时，才会移除后代表的该列。非递归的 `DROP COLUMN`（`ALTER TABLE ONLY ... DROP COLUMN`）从不移除任何后代表的列，而是将它们标记为独立定义而非继承。非递归的 `DROP COLUMN` 命令对分区表会失败，因为表的所有分区必须与分区根具有相同的列。

针对标识列的操作（`ADD GENERATED`、`SET` 等、`DROP IDENTITY`），以及操作 `CLUSTER`、`OWNER` 和 `TABLESPACE`，从不递归到后代表；也就是说，它们的行为始终如同指定了 `ONLY`。添加约束只对未标记为 `NO INHERIT` 的 `CHECK` 约束递归。

Apache Cloudberry 目前不支持外键约束。要在 Apache Cloudberry 中强制执行唯一约束，表必须是哈希分布的（而不是 `DISTRIBUTED RANDOMLY`），并且所有分布键列必须与唯一约束列的起始列相同。

Apache Cloudberry 不允许更改系统目录表的任何部分。

有关有效参数的进一步说明，请参阅 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

使用*经典语法*修改分区表时，请注意以下几点：

- 在 `ALTER TABLE` 命令中指定的表名必须是分区的实际表名，而不是经典语法中指定的分区别名。
- 使用 `pg_partition_tree()` 函数查看分区表的结构。该函数返回分区层次结构，可以帮助你确定可能想要修改的特定分区。
- 如果没有更改包含已交换为使用外部表的叶子分区的分区表上的数据，则支持以下 `ALTER PARTITION` 操作。否则，将返回错误。

    -  添加或删除列。
    -  更改列的数据类型。

- 对于包含已交换为使用外部表的叶子分区的分区表，不支持以下 `ALTER PARTITION` 操作：

    -  设置子分区模板。
    -  修改分区属性。
    -  创建默认分区。
    -  设置分布策略。
    -  设置或删除列的 `NOT NULL` 约束。
    -  添加或删除约束。
    -  拆分外部分区。

## 示例 {#examples}

向表中添加 `varchar` 类型的列：

```sql
ALTER TABLE distributors ADD COLUMN address varchar(30);
```

从表中删除一列：

```sql
ALTER TABLE distributors DROP COLUMN address RESTRICT;
```

在一次操作中更改两个现有列的类型：

```sql
ALTER TABLE distributors
    ALTER COLUMN address TYPE varchar(80),
    ALTER COLUMN name TYPE varchar(100);
```

通过 `USING` 子句，将包含 Unix 时间戳的整数列更改为 `timestamp with time zone`：

```sql
ALTER TABLE foo
    ALTER COLUMN foo_timestamp SET DATA TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second';
```

同样的操作，但该列具有不会自动转换为新数据类型的默认表达式：

```sql
ALTER TABLE foo
    ALTER COLUMN foo_timestamp DROP DEFAULT,
    ALTER COLUMN foo_timestamp TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second',
    ALTER COLUMN foo_timestamp SET DEFAULT now();
```

重命名现有列：

```sql
ALTER TABLE distributors RENAME COLUMN address TO city;
```

重命名现有表：

```sql
ALTER TABLE distributors RENAME TO suppliers;
```

重命名现有约束：

```sql
ALTER TABLE distributors RENAME CONSTRAINT zipchk TO zip_check;
```

向列添加非空约束：

```sql
ALTER TABLE distributors ALTER COLUMN street SET NOT NULL;
```

重命名现有约束：

```sql
ALTER TABLE distributors RENAME CONSTRAINT zipchk TO zip_check;
```

从列中移除非空约束：

```sql
ALTER TABLE distributors ALTER COLUMN street DROP NOT NULL;
```

向表及其所有子表添加检查约束：

```sql
ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK 
  (char_length(zipcode) = 5);
```

仅向表添加检查约束，而不向其子表添加：

```sql
ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5)
  NO INHERIT;
```

（该检查约束也不会被将来的子表继承。）

从表及其所有子表中移除检查约束：

```sql
ALTER TABLE distributors DROP CONSTRAINT zipchk;
```

仅从一个表中移除检查约束：

```sql
ALTER TABLE ONLY distributors DROP CONSTRAINT zipchk;
```

（对于继承 `distributors` 的任何子表，该检查约束仍然保留。）

向表添加（多列）唯一约束：

```sql
ALTER TABLE distributors ADD CONSTRAINT dist_id_zipcode_key UNIQUE (dist_id, zipcode);
```

向表添加自动命名的主键约束，请注意一个表只能有一个主键：

```sql
ALTER TABLE distributors ADD PRIMARY KEY (dist_id);
```

将表移动到不同的表空间：

```sql
ALTER TABLE distributors SET TABLESPACE fasttablespace;
```

将表移动到不同的模式：

```sql
ALTER TABLE myschema.distributors SET SCHEMA yourschema;
```

将表的访问方法更改为 `ao_row`：

```sql
ALTER TABLE distributors SET ACCESS METHOD ao_row;
```

将表的 `blocksize` 更改为 `32768`：

```sql
ALTER TABLE distributors SET (blocksize = 32768);
```

将表的访问方法更改为 `ao_row`，压缩类型更改为 `zstd`，压缩级别更改为 `4`：

```sql
ALTER TABLE sales SET ACCESS METHOD ao_row with (compresstype=zstd,compresslevel=4);
```

或者，你也可以使用 `SET WITH` 执行相同的操作：

```sql
ALTER TABLE sales SET WITH (appendoptimized=true, compresstype=zstd, compresslevel=4);
```

更改表的所有现有分区的访问方法：

```sql
ALTER TABLE sales SET ACCESS METHOD ao_row;
```

将表的所有未来分区更改为使用 `heap` 访问方法，而保持当前分区的访问方法不变：

```sql
ALTER TABLE ONLY sales SET ACCESS METHOD heap;
```

添加列并更改表的访问方法：

```sql
ALTER TABLE distributors SET ACCESS METHOD ao_row, ADD column j int;
```

添加列并更改表的存储参数：

```sql
ALTER TABLE distributors SET (compresslevel=7), ADD COLUMN k int;
```

将表的分布策略更改为复制：

```sql
ALTER TABLE myschema.distributors SET DISTRIBUTED REPLICATED;
```

将表的分布策略更改为随机，并强制重写表：

```sql
ALTER TABLE distributors SET WITH (REORGANIZE=true) SET DISTRIBUTED RANDOMLY;
```

为表设置压缩，并按列 `i` 对表进行物理重排：

```sql
ALTER TABLE distributors 
    REPACK BY COLUMNS (i),
    SET (compresstype=zstd, compresslevel=3);
```

### 现代语法分区示例 {#modern-syntax-partioning-examples}

将分区附加到范围分区表：

```sql
ALTER TABLE measurement
    ATTACH PARTITION measurement_y2016m07 FOR VALUES FROM ('2016-07-01') TO ('2016-08-01');
```

将分区附加到列表分区表：

```sql
ALTER TABLE cities
    ATTACH PARTITION cities_ab FOR VALUES IN ('a', 'b');
```

将分区附加到哈希分区表：

```sql
ALTER TABLE orders
    ATTACH PARTITION orders_p4 FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

将默认分区附加到分区表：

```sql
ALTER TABLE cities
    ATTACH PARTITION cities_partdef DEFAULT;
```

从分区表中分离分区：

```sql
ALTER TABLE measurement
    DETACH PARTITION measurement_y2015m12;
```

### 经典语法分区示例 {#classic-syntax-partioning-examples}

向分区表添加新分区：

```sql
ALTER TABLE sales ADD PARTITION 
            START (date '2017-02-01') INCLUSIVE 
            END (date '2017-03-01') EXCLUSIVE;
```

向现有的分区设计添加默认分区：

```sql
ALTER TABLE sales ADD DEFAULT PARTITION other;
```

重命名分区：

```sql
ALTER TABLE sales RENAME PARTITION FOR ('2016-01-01') TO 
jan08;
```

将表交换到你的分区设计中：

```sql
ALTER TABLE sales EXCHANGE PARTITION FOR ('2016-01-01') WITH 
TABLE jan08;
```

拆分默认分区（现有默认分区的名称为 `other`），以添加 2017 年 1 月的新月度分区：

```sql
ALTER TABLE sales SPLIT DEFAULT PARTITION 
  START ('2017-01-01') INCLUSIVE 
  END ('2017-02-01') EXCLUSIVE 
INTO (PARTITION jan09, PARTITION other);
```

将一个月度分区拆分为两个，第一个分区包含 1 月 1 日至 15 日的日期，第二个分区包含 1 月 16 日至 31 日的日期：

```sql
ALTER TABLE sales SPLIT PARTITION FOR ('2016-01-01')
AT ('2016-01-16')
INTO (PARTITION jan081to15, PARTITION jan0816to31);
```

对于由年、季度和区域三个级别组成的多级分区表，将叶子分区 `region` 与表 `region_new` 交换。

```sql
ALTER TABLE sales ALTER PARTITION year_1 ALTER PARTITION quarter_4 EXCHANGE PARTITION region WITH TABLE region_new ;
```

在上一条命令中，两个 `ALTER PARTITION` 子句标识要交换哪个 `region` 分区。要标识要交换的特定分区，这两个子句都是必需的。

## 兼容性 {#compatibility}

形式 `ADD`（不带 `USING INDEX`）、`DROP [COLUMN]`、`DROP IDENTITY`、`RESTART`、`SET DEFAULT`、`SET DATA TYPE`（不带 `USING`）、`SET GENERATED` 和 `SET <sequence_option>` 符合 SQL 标准。其他形式是 Apache Cloudberry 对 SQL 标准的扩展。此外，在单个 `ALTER TABLE` 命令中指定多个操作的能力也是一种扩展。

`ALTER TABLE DROP COLUMN` 可用于删除表的唯一一列，从而留下一个零列的表。这是对 SQL 的扩展，SQL 不允许零列表。

## 另请参阅 {#see-also}

[CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)、[DROP TABLE](/cloudberry/reference/sql-stmts/drop-table/)
