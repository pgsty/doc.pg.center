---
title: "CREATE RULE"
description: "定义新的重写规则。"
weight: 770
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-rule.md"
---

## 语法概要 {#synopsis}

```sql
CREATE [OR REPLACE] RULE <name> AS ON <event>
  TO <table_name> [WHERE <condition>] 
  DO [ALSO | INSTEAD] { NOTHING | <command> | (<command>; <command> 
  ...) }

-- where <event> can be one of:

  SELECT | INSERT | UPDATE | DELETE
```

## 说明 {#description}

`CREATE RULE` 为指定的表或视图定义新规则。`CREATE OR REPLACE RULE` 可以创建新规则，也可以替换同一表中同名的现有规则。

Apache Cloudberry 规则系统允许为数据库表中的插入、更新或删除定义要执行的替代动作。规则会在对给定表执行给定命令时运行额外命令或替代命令。`INSTEAD` 规则可以用另一个命令替换给定命令，或使该命令完全不运行。规则也可用于实现 SQL 视图。必须认识到，规则实际上是一种命令转换机制，或命令宏。转换发生在命令开始执行之前；它不会像触发器一样对每个物理行独立运行。

`ON SELECT` 规则必须是无条件的 `INSTEAD` 规则，并且动作只能由一条 `SELECT` 命令组成。因此，`ON SELECT` 规则实际上会将表变成视图：其可见内容是规则的 `SELECT` 命令返回的行，而不是表中存储的内容（如果有）。通常，编写 `CREATE VIEW` 命令比创建真实表再为其定义 `ON SELECT` 规则更好。

可以通过定义 `ON INSERT`、`ON UPDATE` 和 `ON DELETE` 规则（或足以满足用途的其中一部分），制造可更新视图的假象，将视图上的更新动作替换为对其他表的适当更新。如果希望支持 `INSERT RETURNING` 等功能，请确保在每条规则中加入合适的 `RETURNING` 子句。

如果尝试对复杂的视图更新使用条件规则，会有一个问题：对于希望允许的每项操作，必须存在无条件的 `INSTEAD` 规则。如果规则有条件，或不是 `INSTEAD`，系统仍会拒绝执行更新，因为它认为在某些情况下可能会尝试对视图的虚拟表执行该操作。如果希望通过条件规则处理所有有用情况，请添加无条件的 `DO INSTEAD NOTHING` 规则，让系统知道它永远不会被要求更新虚拟表；然后让条件规则不使用 `INSTEAD`。在适用条件的情况下，这些规则会补充默认的 `INSTEAD NOTHING` 动作。（不过，这种方法目前不支持 `RETURNING` 查询。）

> **注意** 足够简单、可以自动更新的视图（参见 [CREATE VIEW](/cloudberry/reference/sql-stmts/create-view/)）不需要用户创建规则即可更新。虽然仍然可以显式创建规则，但自动更新转换通常比显式规则性能更好。

## 参数 {#parameters}

**`name`**

要创建的规则名称。该名称必须与同一表中其他规则的名称不同。同一表和同一事件类型上的多个规则会按名称的字母顺序应用。

**`event`**

事件可以是 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE`。请注意，带有 `ON CONFLICT` 子句的 `INSERT` 不能用于同时具有 `INSERT` 或 `UPDATE` 规则的表。此时可以考虑使用可更新视图。

**`table_name`**

规则适用的表或视图名称（可以用模式名限定）。

**`condition`**

任意 SQL 条件表达式（返回 `boolean`）。条件表达式不能引用 `NEW` 和 `OLD` 之外的表，也不能包含聚合函数。

**`INSTEAD`**

`INSTEAD` 表示应运行这些命令来*替代*原始命令。

**`ALSO`**

`ALSO` 表示应运行这些命令，作为原始命令的*附加*操作。如果未指定 `ALSO` 或 `INSTEAD`，默认使用 `ALSO`。

**`command`**

构成规则动作的一个或多个命令。有效命令为 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 或 `NOTIFY`。

在条件和命令中，可以使用特殊表名 `NEW` 和 `OLD` 引用被引用表中的值。`NEW` 可用于 `ON INSERT` 和 `ON UPDATE` 规则，表示正在插入或更新的新行。`OLD` 可用于 `ON UPDATE` 和 `ON DELETE` 规则，表示正在更新或删除的现有行。

## 注意事项 {#notes}

必须是表的所有者才能为其创建或更改规则。

对于视图上的 `INSERT`、`UPDATE` 或 `DELETE` 规则，可以添加返回视图列的 `RETURNING` 子句。如果规则由 `INSERT RETURNING`、`UPDATE RETURNING` 或 `DELETE RETURNING` 命令触发，将使用该子句计算输出。如果触发规则的命令不带 `RETURNING`，则忽略规则的 `RETURNING` 子句。当前实现只允许无条件的 `INSTEAD` 规则包含 `RETURNING`；此外，同一事件的所有规则中最多只能有一个 `RETURNING` 子句。（这样可以确保只有一个候选 `RETURNING` 子句用于计算结果。）如果任何可用规则中都没有 `RETURNING` 子句，则视图上的 `RETURNING` 查询会被拒绝。

必须特别注意避免循环规则。例如，虽然 Apache Cloudberry 接受下面两个规则定义，但执行 `SELECT` 命令时会因规则递归展开而报告错误：

```sql
CREATE RULE "_RETURN" AS
    ON SELECT TO t1
    DO INSTEAD
        SELECT * FROM t2;

CREATE RULE "_RETURN" AS
    ON SELECT TO t2
    DO INSTEAD
        SELECT * FROM t1;

SELECT * FROM t1;
```

如果规则动作包含 `NOTIFY` 命令，则 `NOTIFY` 命令会无条件执行，也就是说，即使没有任何行符合规则，仍会发出 `NOTIFY`。例如，在下面的示例中：

```sql
CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable;

UPDATE mytable SET name = 'foo' WHERE id = 42;
```

在 `UPDATE` 执行期间会发送一个 `NOTIFY` 事件，无论是否有行满足条件 id = 42。

## 兼容性 {#compatibility}

`CREATE RULE` 是 Apache Cloudberry 的扩展，整个查询重写系统也是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[ALTER RULE](/cloudberry/reference/sql-stmts/alter-rule/), [DROP RULE](/cloudberry/reference/sql-stmts/drop-rule/)
