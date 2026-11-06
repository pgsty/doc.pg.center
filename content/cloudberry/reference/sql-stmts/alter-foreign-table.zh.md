---
title: "ALTER FOREIGN TABLE"
description: "更改一个外表的定义。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-foreign-table.md"
---

## 概要 {#synopsis}

```sql
ALTER FOREIGN TABLE [ IF EXISTS ] [ONLY] <name> [ * ]
    <action> [, ... ]
ALTER FOREIGN TABLE [ IF EXISTS ] [ONLY] <name> [ * ]
    RENAME [ COLUMN ] <column_name> TO <new_column_name>
ALTER FOREIGN TABLE [ IF EXISTS ] <name>
    RENAME TO <new_name>
ALTER FOREIGN TABLE [ IF EXISTS ] <name>
    SET SCHEMA <new_schema>

-- where <action> is one of:

    ADD [ COLUMN ] <column_name> <data_type> [ COLLATE <collation> ] [ <column_constraint> [ ... ] ]
    DROP [ COLUMN ] [ IF EXISTS ] <column_name> [ RESTRICT | CASCADE ]
    ALTER [ COLUMN ] <column_name> [ SET DATA ] TYPE <data_type> [ COLLATE <collation> ]
    ALTER [ COLUMN ] <column_name> SET DEFAULT <expression>
    ALTER [ COLUMN ] <column_name> DROP DEFAULT
    ALTER [ COLUMN ] <column_name> { SET | DROP } NOT NULL
    ALTER [ COLUMN ] <column_name> SET STATISTICS <integer>
    ALTER [ COLUMN ] <column_name> SET ( <attribute_option> = <value> [, ... ] )
    ALTER [ COLUMN ] <column_name> RESET ( <attribute_option> [, ... ] )
    ALTER [ COLUMN ] <column_name> SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
    ALTER [ COLUMN ] <column_name> OPTIONS ( [ ADD | SET | DROP ] <option> ['<value>'] [, ... ])
    ADD <table_constraint> [ NOT VALID ]
    VALIDATE CONSTRAINT <constraint_name>
    DROP CONSTRAINT [ IF EXISTS ]  <constraint_name> [ RESTRICT | CASCADE ]
    DISABLE TRIGGER [ <trigger_name> | ALL | USER ]
    ENABLE TRIGGER [ <trigger_name> | ALL | USER ]
    ENABLE REPLICA TRIGGER <trigger_name>
    ENABLE ALWAYS TRIGGER <trigger_name>
    SET WITHOUT OIDS
    INHERIT <parent_table>
    NO INHERIT <parent_table>
    OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
    OPTIONS ( [ ADD | SET | DROP ] <option> ['<value>'] [, ... ] )
```

## 描述 {#description}

`ALTER FOREIGN TABLE` 更改一个现有外表的定义。该命令有若干子形式：

**`ADD COLUMN`**

此形式使用与 [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) 相同的语法向外表添加一个新列。与向常规表添加列的情形不同，底层存储不会发生任何变化：此操作只是声明现在可以通过该外表访问某个新列。

**`DROP COLUMN [ IF EXISTS ]`**

此形式从外表中删除一列。如果表外有任何对象依赖于该列（例如视图），则必须指定 `CASCADE`。如果指定了 `IF EXISTS` 且该列不存在，则不会抛出错误，而是由 Apache Cloudberry 发出一个提示。

**`IF EXISTS`**

如果指定了 `IF EXISTS` 且该外表不存在，则不会抛出错误，而是由 Apache Cloudberry 发出一个提示。

**`SET DATA TYPE`**

此形式更改外表某一列的类型。同样，这对任何底层存储都没有影响：此操作只是更改 Apache Cloudberry 所认为的该列的类型。

**`SET/DROP DEFAULT`**

这些形式设置或移除列的默认值。默认值只应用于此后的 `INSERT` 或 `UPDATE` 命令；它们不会导致表中已有的行发生变化。

**`SET/DROP NOT NULL`**

将列标记为允许或不允许空值。

**`SET STATISTICS`**

此形式为此后的 `ANALYZE` 操作设置每列的统计信息收集目标。更多详情参见 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 的类似形式。

**`SET ( attribute_option = value [, ...] ] )`**<br />
**`RESET ( attribute_option [, ... ] )`**

此形式设置或重置每个属性的选项。更多详情参见 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 的类似形式。

**`SET STORAGE`**

此形式设置列的存储模式。更多详情参见 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 的类似形式。请注意，除非该表的外部数据包装器选择关注存储模式，否则存储模式不起任何作用。

**`ADD table_constraint [ NOT VALID ]`**

此形式使用与 [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) 相同的语法向外表添加一个新约束。目前只支持 `CHECK` 约束。

与向常规表添加约束的情形不同，不会做任何事情来验证该约束是否正确；此操作只是声明应当假定某个新条件对外表中的所有行都成立。（参见 [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) 中的讨论。）如果该约束被标记为 `NOT VALID`，则不会假定它成立，而只是将其记录下来以备将来可能使用。

**`VALIDATE CONSTRAINT`**

此形式把先前标记为 `NOT VALID` 的约束标记为有效。不会采取任何动作来验证该约束，但此后的查询将假定它成立。

**`DROP CONSTRAINT [ IF EXISTS ]`**

此形式删除外表上指定的约束。如果指定了 `IF EXISTS` 且该约束不存在，则不会抛出错误，而是发出一个提示。

**`DISABLE/ENABLE [ REPLICA | ALWAYS ] TRIGGER`**

这些形式配置属于该外表的触发器的触发方式。更多详情参见 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 的类似形式。

**`SET WITHOUT OIDS`**

用于移除 oid 系统列的向后兼容语法。由于已不能再添加 oid 系统列，因此它永远不会产生任何效果。

**`INHERIT parent_table`**

此形式将目标外表添加为指定父表的新子表。更多详情参见 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 的类似形式。

**`NO INHERIT parent_table`**

此形式将目标外表从指定父表的子表列表中移除。

**`OWNER`**

此形式把外表的所有者更改为指定的用户。

**`RENAME`**

`RENAME` 形式更改外表的名称或外表中某一列的名称。

**`SET SCHEMA`**

此形式把外表移入另一个模式。

**`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`**

更改外表的选项。`ADD`、`SET` 和 `DROP` 指定要执行的操作。如果没有显式指定操作，则默认操作为 `ADD`。选项名称必须唯一（不过表选项和列选项可以同名）。Apache Cloudberry 还会使用服务器的外部数据包装器来验证名称和值。

除 `RENAME` 和 `SET SCHEMA` 之外的所有操作都可以合并成一个由多项更改组成的列表，由 Apache Cloudberry 并行应用。例如，可以在单个命令中添加多个列和/或更改多个列的类型。

如果命令写成 `ALTER FOREIGN TABLE IF EXISTS ...` 且该外表不存在，则不会抛出错误，此时会发出一个提示。

要使用 `ALTER FOREIGN TABLE`，你必须拥有该表。要更改外表的模式，你还必须在新模式上具有 `CREATE` 权限。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该表所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该表无法做到的事情。不过，超级用户无论如何都可以更改任何表的所有权。）要添加列或更改列的类型，你还必须对该数据类型具有 `USAGE` 权限。

## 参数 {#parameters}

**`name`**

要更改的现有外表的名称（可以是模式限定的）。如果在表名前指定了 `ONLY`，则只更改该表。如果未指定 `ONLY`，则会更改该表及其所有后代表（如果有）。可以选择在表名后指定 `*`，以显式表明包含后代表。

**`column_name`**

新列或现有列的名称。

**`new_column_name`**

现有列的新名称。

**`new_name`**

外表的新名称。

**`data_type`**

新列的数据类型，或现有列的新数据类型。

**`table_constraint`**

外表的新表约束。

**`constraint_name`**

要验证或删除的现有约束的名称。

**`CASCADE`**

自动删除依赖于被删除列或约束的对象（例如引用该列的视图），进而删除依赖于这些对象的所有对象。

**`RESTRICT`**

如果存在任何依赖对象，则拒绝删除该列或约束。这是默认行为。

**`trigger_name`**

要停用或启用的单个触发器的名称。

**`ALL`**

停用或启用属于该外表的所有触发器。（如果其中任何触发器是内部生成的触发器，则需要超级用户权限。核心系统不会向外表添加此类触发器，但附加代码可能会这样做。）

**`USER`**

停用或启用属于该外表的所有触发器，但内部生成的触发器除外。

**`parent_table`**

要与该外表建立关联或解除关联的父表。

**`new_owner`**

外表的新所有者的用户名。

**`new_schema`**

外表将被移入的模式的名称。

## 注解 {#notes}

关键字 `COLUMN` 是噪声词，可以省略。

使用 `ADD COLUMN` 或 `DROP COLUMN` 添加或删除列、添加 `NOT NULL` 或 `CHECK` 约束，或使用 `SET DATA TYPE` 更改列类型时，不会检查与外部服务器的一致性。确保表定义与远端相符是你的责任。

有关有效参数的进一步说明，请参阅 [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/)。

## 示例 {#examples}

将一列标记为非空：

```sql
ALTER FOREIGN TABLE distributors ALTER COLUMN street SET NOT NULL;
```

更改外表的选项：

```sql
ALTER FOREIGN TABLE myschema.distributors 
    OPTIONS (ADD opt1 'value', SET opt2 'value2', DROP opt3 'value3');
```

## 兼容性 {#compatibility}

`ADD`、`DROP` 和 `SET DATA TYPE` 形式符合 SQL 标准。其他形式是 SQL 标准的 Apache Cloudberry 扩展。在单个 `ALTER FOREIGN TABLE` 命令中指定多个操作的能力同样是 Apache Cloudberry 的扩展。

你可以使用 `ALTER FOREIGN TABLE ... DROP COLUMN` 删除外表的唯一一列，得到一个零列的表。这是对 SQL 的扩展，SQL 不允许零列的外表。

## 另见 {#see-also}

[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)、[CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/)、[DROP FOREIGN TABLE](/cloudberry/reference/sql-stmts/drop-foreign-table/)
