---
title: "DELETE"
description: "从表中删除行。"
weight: 970
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/delete.md"
---

## 语法概要 {#synopsis}

```sql
[ WITH [ RECURSIVE ] <with_query> [, ...] ]
DELETE FROM [ONLY] <table_name> [[AS] <alias>]
      [USING <from_item> [, ...] ]
      [WHERE <condition> | WHERE CURRENT OF <cursor_name>]
      [RETURNING * | <output_expression> [[AS] <output_name>] [, …]]
```

## 说明 {#description}

`DELETE` 从指定表中删除满足 `WHERE` 子句的行。如果没有 `WHERE` 子句，则删除表中的所有行。结果是一个有效的空表。

**提示：** [TRUNCATE](/cloudberry/reference/sql-stmts/truncate/) 提供了更快的机制，可移除表中的所有行。

利用数据库中其他表的信息删除表中行有两种方法：使用子查询，或在 `USING` 子句中指定其他表。哪种技术更合适取决于具体情况。

可选的 `RETURNING` 子句使 `DELETE` 根据实际删除的每一行计算并返回值。可以计算使用该表的列和/或 `USING` 中其他表的列的任意表达式。`RETURNING` 列表的语法与 `SELECT` 的输出列表相同。

要从表中删除行，必须具有该表的 `DELETE` 权限，并对 `USING` 子句中的任何表或在条件中读取其值的表具有 `SELECT` 权限。

> **注意** 从 AO 表中删除行时不支持 `RETURNING` 子句。

> **注意** 默认情况下，对堆表执行 `DELETE` 操作时，Apache Cloudberry 会对表获取 `EXCLUSIVE` 锁。启用全局死锁检测器后，堆表上 `DELETE` 操作的锁模式为 `ROW EXCLUSIVE`。

## 参数 {#parameters}

**`with_query`**

`WITH` 子句允许指定一个或多个子查询，并在 `DELETE` 查询中按名称引用它们。

对于包含 `WITH` 子句的 `DELETE` 命令，该子句只能包含 `SELECT` 语句；`WITH` 子句不能包含数据修改命令（`INSERT`、`UPDATE` 或 `DELETE`）。

详情请参见 [SELECT](/cloudberry/reference/sql-stmts/select/)。

**`table_name`**

要从中删除行的表的名称（可以用模式名限定）。如果在表名前指定 `ONLY`，Apache Cloudberry 只从指定表中删除匹配行。如果未指定 `ONLY`，也会从继承该表的所有表中删除匹配行。还可以在表名后指定 `*`，明确表示包含后代表。

**`alias`**

目标表的替代名称。提供别名后，它会完全隐藏表的实际名称。例如，给定 `DELETE FROM foo AS f`，`DELETE` 语句的其余部分必须使用 `f` 而不是 `foo` 引用该表。

**`from_item`**

允许其他表的列出现在 `WHERE` 条件中的表表达式。其语法与 [SELECT](/cloudberry/reference/sql-stmts/select/) 语句的 `FROM` 子句相同；例如可以为表名指定别名。不要在 from_item 中重复目标表，除非希望建立自连接（此时它必须在 from_item 中以别名出现）。

**`condition`**

返回 `boolean` 类型值的表达式。Apache Cloudberry 只删除该表达式返回 `true` 的行。

**`cursor_name`**

在 `WHERE CURRENT OF` 条件中使用的游标名称。要删除的行是最近从该游标获取的行。游标必须是针对 `DELETE` 目标表的非分组查询。请注意，不能同时指定 `WHERE CURRENT OF` 和布尔条件。有关配合 `WHERE CURRENT OF` 使用游标的更多信息，参见 [DECLARE](/cloudberry/reference/sql-stmts/declare/)。

`DELETE...WHERE CURRENT OF` 游标语句只能在服务器上运行，例如在交互式 psql 会话或脚本中。PL/pgSQL 等语言扩展不支持可更新游标。

**`output_expression`**

每行删除后由 `DELETE` 命令计算并返回的表达式。该表达式可以使用 table_name 所指定表或 `USING` 中列出表的任意列名。写成 `*` 可返回所有列。

**`output_name`**

返回列使用的名称。

## 输出 {#outputs}

成功完成时，`DELETE` 命令返回以下形式的命令标签：

```sql
DELETE <count>
```

count 是删除的行数。如果 count 为 0，则查询未删除任何行（这不视为错误）。

如果 `DELETE` 命令包含 `RETURNING` 子句，则结果类似于 `SELECT` 语句，包含 `RETURNING` 列表中定义的列和值，这些值基于命令删除的行计算。

## 注意事项 {#notes}

从 AO 表中删除行时不支持 `RETURNING` 子句。

复制表不支持 `WHERE CURRENT OF` 子句。

Apache Cloudberry 允许通过在 `USING` 子句中指定其他表，在 `WHERE` 条件中引用这些表的列。例如，要删除某个制片人制作的所有电影，可以执行：

```sql
DELETE FROM films USING producers
  WHERE producer_id = producers.id AND producers.name = 'foo';
```
这里实际上在 `films` 和 `producers` 之间执行连接，并将所有成功连接的 `films` 行标记为待删除。此语法不属于标准。更符合标准的写法是：

```sql
DELETE FROM films
  WHERE producer_id IN (SELECT id FROM producers WHERE name = 'foo');
```

对于分区表，当未启用全局死锁检测器时（默认情况），`DELETE` 操作期间会锁定所有子表。启用全局死锁检测器后，只锁定部分叶子子表。

## 示例 {#examples}

删除除音乐剧之外的所有电影：

```sql
DELETE FROM films WHERE kind <> 'Musical';
```

清空表 films：

```sql
DELETE FROM films;
```

删除已完成的任务，返回已删除行的完整信息：

```sql
DELETE FROM tasks WHERE status = 'DONE' RETURNING *;
```

删除 tasks 中游标 `c_tasks` 当前所在的行：

```sql
DELETE FROM tasks WHERE CURRENT OF c_tasks;
```

使用连接进行删除：

```sql
DELETE FROM rank USING names WHERE names.id = rank.id AND 
name = 'Hannah';
```

## 兼容性 {#compatibility}

此命令符合 SQL 标准，但 `USING` 和 `RETURNING` 子句以及在 `DELETE` 中使用 `WITH` 的能力是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[TRUNCATE](/cloudberry/reference/sql-stmts/truncate/)
