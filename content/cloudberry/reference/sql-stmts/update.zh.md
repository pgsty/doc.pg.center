---
title: "UPDATE"
description: "更新表中的行。"
weight: 1780
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/update.md"
---

## 语法概要 {#synopsis}

```sql
[ WITH [ RECURSIVE ] <with_query> [, ...] ]
UPDATE [ ONLY ] <table_name> [ [ AS ] <alias> ]
   SET { <column_name> = { <expression> | DEFAULT } |
       ( <column_name> [, ...] ) = [ ROW ] ( { <expression> | DEFAULT } [, ...] ) |
       ( <column_name> [, ...] ) = ( <sub-SELECT> )
       } [, ...]
   [ FROM <from_item> [, ...] ]
   [ WHERE <condition> | WHERE CURRENT OF <cursor_name> ]
   [ RETURNING * | <output_expression> [ [AS] <output_name> ] [, ...] ]
```

## 说明 {#description}

`UPDATE` 修改所有满足条件的行中指定列的值。`SET` 子句只需列出要修改的列；未显式修改的列保留原值。

利用数据库中其他表的信息修改某个表有两种方法：使用子查询，或在 `FROM` 子句中指定其他表。采用哪种方法更合适取决于具体情况。

可选的 `RETURNING` 子句使 `UPDATE` 根据每个实际更新的行计算并返回值。Apache Cloudberry 可以使用该表的列和/或 `FROM` 中其他表的列计算任意表达式，使用的是该表各列的新值（更新后的值）。`RETURNING` 列表的语法与 `SELECT` 输出列表的语法相同。

必须对表具有 `UPDATE` 权限，或至少对列出要更新的列具有该权限。对于表达式或条件中读取其值的任何列，还必须具有 `SELECT` 权限。

> **注意** 默认情况下，Apache Cloudberry 对堆表执行 `UPDATE` 操作时会获取表上的 `EXCLUSIVE` 锁。启用全局死锁检测器后，堆表上 `UPDATE` 操作的锁模式为 `ROW EXCLUSIVE`。

## 参数 {#parameters}

**`with_query`**

`WITH` 子句允许指定一个或多个子查询，并在 `UPDATE` 查询中按名称引用它们。详情请参阅 [SELECT](/cloudberry/reference/sql-stmts/select/)。

对于包含 `WITH` 子句的 `UPDATE` 命令，该子句只能包含 `SELECT` 命令，`WITH` 子句不能包含数据修改命令（`INSERT`、`UPDATE` 或 `DELETE`）。

查询（`SELECT` 语句）本身也可以包含 `WITH` 子句。在这种情况下，两组 with_query 都可以在 `UPDATE` 查询中引用，但第二组嵌套得更深，因此优先。

**`table_name`**

要更新的表名（可用模式限定）。如果在表名前指定 `ONLY`，则只更新指定表中匹配的行。如果未指定 `ONLY`，还会更新继承自该表的所有表中匹配的行。也可以在表名后指定 `*`，显式表示包含后代表。

**`alias`**

目标表的替代名称。提供别名后，实际表名会被完全隐藏。例如，使用 `UPDATE foo AS f` 后，`UPDATE` 语句的其余部分必须用 `f` 而不能用 `foo` 引用此表。

**`column_name`**

table_name 所指定表中的列名。必要时可以用子字段名或数组下标限定列名。指定目标列时不要包含表名；例如，`UPDATE table_name SET table_name.col = 1` 是无效的。

**`expression`**

要赋给该列的表达式。表达式可以使用该列及表中其他列的旧值。

**`DEFAULT`**

将列设为其默认值（如果没有为其指定默认表达式，则为 NULL）。

**`sub-SELECT`**

一个 `SELECT` 子查询，其输出列数与前面括号内列列表的列数相同。子查询执行时最多只能产生一行。如果产生一行，就将其列值赋给目标列；如果没有产生行，则将 NULL 值赋给目标列。子查询可以引用被更新表当前行的旧值。

**`from_item`**

一个表表达式，允许其他表中的列出现在 `WHERE` 条件和更新表达式中。其语法与 [SELECT](/cloudberry/reference/sql-stmts/select/) 语句的 `FROM` 子句相同；例如，可以为表名指定别名。除非要进行自连接，否则不要在 from_item 中重复列出目标表；进行自连接时，目标表必须在 from_item 中使用别名。

**`condition`**

返回 `boolean` 类型值的表达式。只有该表达式返回 `true` 的行才会被更新。

**`cursor_name`**

用于 `WHERE CURRENT OF` 条件的游标名称。要更新的是最近一次从该游标取回的行。该游标必须是在 `UPDATE` 目标表上执行的非分组查询。注意，`WHERE CURRENT OF` 不能与布尔条件一起指定。有关将游标与 `WHERE CURRENT OF` 配合使用的更多信息，请参阅 [DECLARE](/cloudberry/reference/sql-stmts/declare/)。

`UPDATE...WHERE CURRENT OF` 语句只能在服务器上运行，例如在交互式 psql 会话或脚本中运行。PL/pgSQL 等语言扩展不支持可更新游标。

**`output_expression`**

`UPDATE` 命令在更新每一行后要计算并返回的表达式。表达式可以使用 table_name 所指定表或 `FROM` 所列各表中的任何列名。使用 `*` 可返回所有列。

**`output_name`**

返回列所使用的名称。

## 输出 {#outputs}

成功完成后，`UPDATE` 命令返回以下形式的命令标签：

```sql
UPDATE <count>
```

count 是更新的行数，包括匹配但值未发生变化的行。如果 count 为 0，表示查询没有更新任何行（这不视为错误）。

如果 `UPDATE` 命令包含 `RETURNING` 子句，其结果类似于 `SELECT` 语句的结果，包含 `RETURNING` 列表定义的列和值，并对命令更新的各行进行计算。

## 注意事项 {#notes}

存在 `FROM` 子句时，目标表会与 from_item 列表中提到的表连接，连接的每个输出行代表对目标表的一次更新操作。使用 `FROM` 时，必须确保连接对于每个待修改行最多产生一个输出行。换言之，目标行不应与其他表中的多行连接。否则，只有其中一个连接行会用于更新目标行，但很难预测会使用哪一个。

由于存在这种不确定性，只在子查询中引用其他表更安全，不过通常比连接更难阅读，速度也更慢。

对于分区表，未启用全局死锁检测器时（默认情况），`UPDATE` 操作会锁定所有子表。启用全局死锁检测器后，只会锁定部分叶子子表。

对于分区表，更新行可能使它不再满足所在分区的分区约束。在这种情况下，如果分区树中存在另一个分区，且该行满足其分区约束，则会将该行移到那个分区。如果不存在这样的分区，则会报错。底层实际上通过 `DELETE` 和 `INSERT` 操作实现行移动。

对于分区表，未启用全局死锁检测器时（默认情况），`UPDATE` 操作会锁定所有子表。启用全局死锁检测器后，只会锁定部分叶子分区。

对正在移动的行并发执行 `UPDATE` 或 `DELETE` 可能产生串行化失败错误。假设会话 1 正在对分区键执行 `UPDATE`，与此同时，能看到该行的并发会话 2 对此行执行 `UPDATE` 或 `DELETE` 操作。此时，会话 2 的 `UPDATE` 或 `DELETE` 会检测到行移动，并抛出串行化失败错误（始终返回 SQLSTATE 代码 '40001'）。发生这种情况时，应用可以重试事务。在表未分区或未发生行移动的通常情况下，会话 2 会识别出新更新的行，并对这个新行版本执行 `UPDATE/DELETE`。

注意，行可以从本地分区移到外表分区（前提是外部数据包装器支持元组路由），但不能从外表分区移到其他分区。

## 示例 {#examples}

将 `films` 表的 `kind` 列中的单词 `Drama` 改为 `Dramatic`：

```sql
UPDATE films SET kind = 'Dramatic' WHERE kind = 'Drama';
```

调整 `weather` 表中某一行的温度记录，并将降水量重置为默认值：

```sql
UPDATE weather SET temp_lo = temp_lo+1, temp_hi = 
temp_lo+15, prcp = DEFAULT
WHERE city = 'San Francisco' AND date = '2016-07-03';
```

执行相同操作并返回更新后的记录：

```sql
UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT
  WHERE city = 'San Francisco' AND date = '2003-07-03'
  RETURNING temp_lo, temp_hi, prcp;
```

使用另一种列列表语法执行相同的更新：

```sql
UPDATE weather SET (temp_lo, temp_hi, prcp) = (temp_lo+1, 
temp_lo+15, DEFAULT)
WHERE city = 'San Francisco' AND date = '2016-07-03';
```

使用 `FROM` 子句语法增加负责 Acme Corporation 账户的销售人员的销售计数（假定参与连接的两个表在 Apache Cloudberry 中均按 `id` 列分布）：

```sql
UPDATE employees SET sales_count = sales_count + 1 FROM 
accounts
WHERE accounts.name = 'Acme Corporation'
AND employees.id = accounts.id;
```

在 `WHERE` 子句中使用子查询执行相同操作：

```sql
UPDATE employees SET sales_count = sales_count + 1 WHERE id =
  (SELECT id FROM accounts WHERE name = 'Acme Corporation');
```

更新 `accounts` 表中的联系人姓名，使之与当前指定的销售人员一致：

```sql
UPDATE accounts SET (contact_first_name, contact_last_name) =
    (SELECT first_name, last_name FROM salesmen
     WHERE salesmen.id = accounts.sales_id);
```

也可以通过连接获得类似结果：

```sql
UPDATE accounts SET contact_first_name = first_name,
                    contact_last_name = last_name
  FROM salesmen WHERE salesmen.id = accounts.sales_id;
```

不过，如果 `salesmen.id` 不是唯一键，第二个查询可能产生意外结果，而第一个查询在存在多个 `id` 匹配项时一定会报错。另外，如果某个 `accounts.sales_id` 记录没有匹配项，第一个查询会将相应姓名字段设为 NULL，而第二个查询完全不会更新该行。

更新 `summary` 表中的统计数据，使之与当前数据一致：

```sql
UPDATE summary s SET (sum_x, sum_y, avg_x, avg_y) =
    (SELECT sum(x), sum(y), avg(x), avg(y) FROM data d
     WHERE d.group_id = s.group_id);
```

尝试插入一个新的库存项目及其库存数量。如果该项目已存在，则更新现有项目的库存数量。使用保存点可以避免因此导致整个事务失败。

```sql
BEGIN;
-- other operations
SAVEPOINT sp1;
INSERT INTO wines VALUES('Chateau Lafite 2003', '24');
-- Assume the above fails because of a unique key violation,
-- so now we issue these commands:
ROLLBACK TO sp1;
UPDATE wines SET stock = stock + 24 WHERE winename = 'Chateau 
Lafite 2003';
-- continue with other operations, and eventually
COMMIT;
```

## 兼容性 {#compatibility}

此命令符合 SQL 标准，但 `FROM` 和 `RETURNING` 子句是 Apache Cloudberry 的扩展，在 `UPDATE` 中使用 `WITH` 的能力也是扩展。

一些其他数据库系统提供的 `FROM` 选项要求在 `FROM` 中再次列出目标表。Apache Cloudberry 对 `FROM` 的解释并非如此。移植使用此扩展的应用时请注意。

根据标准，括号中目标列名子列表的源值可以是任何产生正确列数的行值表达式。Apache Cloudberry 只允许源值为[行构造器](https://www.postgresql.org/docs/12/sql-expressions.html#SQL-SYNTAX-ROW-CONSTRUCTORS)或子 `SELECT`。使用行构造器时，可以将单个列的更新值指定为 `DEFAULT`，但在子 `SELECT` 中不能这样做。

## 另请参阅 {#see-also}

[DECLARE](/cloudberry/reference/sql-stmts/declare/), [DELETE](/cloudberry/reference/sql-stmts/delete/), [SELECT](/cloudberry/reference/sql-stmts/select/), [INSERT](/cloudberry/reference/sql-stmts/insert/)
