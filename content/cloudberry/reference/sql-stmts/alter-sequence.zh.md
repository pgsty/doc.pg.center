---
title: "ALTER SEQUENCE"
description: "修改序列生成器的定义。"
weight: 290
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-sequence.md"
---

## 概要 {#synopsis}

```sql
ALTER SEQUENCE [ IF EXISTS ] <name>
     [ AS <data_type> ]
     [INCREMENT [ BY ] <increment>] 
     [MINVALUE <minvalue> | NO MINVALUE] 
     [MAXVALUE <maxvalue> | NO MAXVALUE] 
     [START [ WITH ] <start> ]
     [RESTART [ [ WITH ] <restart>] ]
     [CACHE <cache>] [[ NO ] CYCLE] 
     [OWNED BY {<table_name.column_name> | NONE}]

ALTER SEQUENCE [ IF EXISTS ] <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER SEQUENCE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER SEQUENCE [ IF EXISTS ] <name> SET SCHEMA <new_schema>
```

## 说明 {#description}

`ALTER SEQUENCE` 用于修改现有序列生成器的参数。`ALTER SEQUENCE` 命令中未明确设置的任何参数都保持其先前的设置。

你必须是序列的所有者才能使用 `ALTER SEQUENCE`。要修改序列的模式，你还必须拥有新模式上的 `CREATE` 权限。请注意，超级用户自动拥有所有这些权限。

要修改所有者，你必须是新所属角色的直接或间接成员，并且该角色必须拥有序列所在模式上的 `CREATE` 权限。（这些限制确保修改所有者不会做出你通过删除并重新创建序列所做不到的事情。不过，超级用户无论如何都可以修改任何序列的所有权。）

## 参数 {#parameters}

**`name`**

要修改的序列的名称（可以带模式限定）。

**`IF EXISTS`**

如果序列不存在，不要抛出错误。在这种情况下，Apache Cloudberry 会发出一条提示。

**`data_type`**

可选子句 `AS data_type` 用于修改序列的数据类型。有效类型为 `smallint`、`integer` 和 `bigint`。

当且仅当先前的最小值和最大值是旧数据类型的最小值或最大值时（换言之，如果序列是隐式或显式地使用 `NO MINVALUE` 或 `NO MAXVALUE` 创建的），修改数据类型会自动修改序列的最小值和最大值。否则，最小值和最大值保持不变，除非在同一命令中给出了新值。如果最小值和最大值不适合新的数据类型，Apache Cloudberry 会产生错误。

**`increment`**

子句 `INCREMENT BY increment` 是可选的。正值会产生升序序列，负值会产生降序序列。如果未指定，则保持旧的增量值。

**`minvalue`**<br />
**`NO MINVALUE`**

可选子句 `MINVALUE minvalue` 决定序列可以生成的最小值。如果指定 `NO MINVALUE`，则对升序和降序序列分别使用默认值 `1` 和该数据类型的最小值。如果两个选项都未指定，则保持当前的最小值。

**`maxvalue`**<br />
**`NO MAXVALUE`**

可选子句 `MAXVALUE maxvalue` 决定序列的最大值。如果指定 `NO MAXVALUE`，则对升序和降序序列分别使用默认值：该数据类型的最大值和 `-1`。如果两个选项都未指定，则保持当前的最大值。

**`start`**

可选子句 `START WITH start` 用于修改序列所记录的起始值。这对序列的*当前*值没有影响；它只是设置了今后的 `ALTER SEQUENCE RESTART` 命令将使用的值。

**`restart`**

可选子句 `RESTART [ WITH restart ]` 用于修改序列的当前值。这等效于以 `is_called = false` 调用 `setval(sequence, start_val, is_called)` 函数。指定的值将由*下一次*调用 `nextval(sequence)` 函数时返回。写出不带重启值的 `RESTART`，等效于提供由 `CREATE SEQUENCE` 记录的、或最后由 `ALTER SEQUENCE START WITH` 设置的起始值。

与 `setval()` 调用不同，对序列的 `RESTART` 操作是事务性的，并且会阻止并发事务从同一序列获取编号。如果这不是期望的操作模式，则应使用 `setval()`。

**`cache`**

子句 `CACHE cache` 使序列编号能够被预分配并存储在内存中，以便更快地访问。最小值为 1（一次只能生成一个值，即没有缓存）。如果未指定，则保持旧的缓存值。

> **注意** 使用序列编号缓存（`cache > 1`）时，Apache Cloudberry 可能会丢弃一些已缓存的序列值。如果需要连续的值，则必须在创建或修改序列时显式设置 `CACHE 1`。

**`CYCLE`**

可选的 `CYCLE` 关键字可用于使序列在升序或降序序列达到 `maxvalue` 或 `minvalue` 时回绕。如果达到限值，下一个生成的编号将分别是 `minvalue` 或 `maxvalue`。

**`NO CYCLE`**

如果指定了可选的 `NO CYCLE` 关键字，则在序列达到其最大值之后，对 `nextval()` 的任何调用都将返回错误。如果 `CYCLE` 和 `NO CYCLE` 都未指定，则保持旧的循环行为。

**`OWNED BY table_name.column_name`**<br />
**`OWNED BY NONE`**

`OWNED BY` 选项使序列与特定的表列相关联，这样，如果该列（或其所在的整个表）被删除，序列也会被自动删除。如果指定了该选项，此关联会替换先前为该序列指定的任何关联。指定的表必须与序列具有相同的所有者，并且位于同一个模式中。指定 `OWNED BY NONE` 会移除任何现有的表列关联。

**`new_owner`**

序列新所有者的用户名。

**`new_name`**

序列的新名称。

**`new_schema`**

序列的新模式。

## 注解 {#notes}

`ALTER SEQUENCE` 不会立即影响当前后端以外的、已预分配（缓存）序列值的后端中的 `nextval()` 结果。这些后端会先用完所有缓存的值，然后才会注意到序列生成参数已更改。当前后端会立即受到影响。

`ALTER SEQUENCE` 会阻塞并发的 `nextval()` 和 `setval()` 调用。

由于历史原因，`ALTER TABLE` 也可以用于序列；但是，`ALTER TABLE` 允许用于序列的变体仅限于与上面所示形式等效的那些。

## 示例 {#examples}

将名为 `serial` 的序列重新启动，从 `105` 开始：

```sql
ALTER SEQUENCE serial RESTART WITH 105;
```

## 兼容性 {#compatibility}

`ALTER SEQUENCE` 符合 SQL 标准，但 `AS`、`START WITH`、`OWNED BY`、`OWNER TO`、`RENAME TO` 和 `SET SCHEMA` 子句除外，它们是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/)、[DROP SEQUENCE](/cloudberry/reference/sql-stmts/drop-sequence/)、[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)
