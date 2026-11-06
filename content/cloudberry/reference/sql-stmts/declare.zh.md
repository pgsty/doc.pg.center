---
title: "DECLARE"
description: "定义游标。"
weight: 960
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/declare.md"
---

## 语法概要 {#synopsis}

```sql
DECLARE <name> [BINARY] [INSENSITIVE] [NO SCROLL] [PARALLEL RETRIEVE] CURSOR 
     [{WITH | WITHOUT} HOLD] 
     FOR <query>
```

## 说明 {#description}

`DECLARE` 允许用户创建游标，用于从较大的查询结果中每次检索少量行。游标可以通过 [FETCH](/cloudberry/reference/sql-stmts/fetch/) 返回数据。

> **注意** 本页说明 SQL 命令层面游标的用法。如果要在 PL/pgSQL 函数中使用游标，规则有所不同，参见 PL/pgSQL。

普通游标以文本格式返回数据，与 `SELECT` 产生的数据相同。由于数据原本以二进制格式存储，系统必须进行转换才能生成文本格式。信息以文本形式返回后，客户端应用可能又需要将其转换为二进制格式才能操作。此外，文本格式的数据通常比二进制格式更大。二进制游标以二进制表示返回数据，可能更便于操作。不过，如果最终仍要以文本显示数据，直接以文本形式检索会减少客户端的工作。

例如，查询从整数列返回值一时，默认游标会返回字符串 1，而二进制游标则返回一个包含该值内部表示的 4 字节字段（采用大端字节序）。

应谨慎使用二进制游标。包括 `psql` 在内的许多应用无法处理二进制游标，并预期数据以文本格式返回。

> **注意** 当客户端应用使用“扩展查询”协议发出 `FETCH` 命令时，Bind 协议消息指定以文本格式还是二进制格式检索数据。此选择会覆盖游标定义的方式。因此，使用扩展查询协议时，二进制游标这一概念已经过时；任何游标都可以按文本或二进制方式处理。

可以在 [UPDATE](/cloudberry/reference/sql-stmts/update/) 或 [DELETE](/cloudberry/reference/sql-stmts/delete/) 语句的 `WHERE CURRENT OF` 子句中指定游标，以更新或删除表数据。`UPDATE` 或 `DELETE` 语句只能在服务器上运行，例如在交互式 `psql` 会话或脚本中。

**并行检索游标**

Apache Cloudberry 支持一种特殊游标，即*并行检索游标*。可以使用并行检索游标直接从 Apache Cloudberry Segment 并行检索查询结果，绕过 Apache Cloudberry Coordinator。

并行检索游标不支持 `WITH HOLD` 子句。声明并行检索游标时，Apache Cloudberry 会忽略 `BINARY` 子句。

需要为每个并行检索游标端点打开专用检索会话，并使用 [RETRIEVE](/cloudberry/reference/sql-stmts/retrieve/) 命令从并行检索游标获取查询结果。

## 参数 {#parameters}

**`name`**

要创建的游标名称。

**`BINARY`**

使游标以二进制格式而非文本格式返回数据。

> **注意** 声明 `PARALLEL RETRIEVE` 游标时，Apache Cloudberry 会忽略 `BINARY` 子句。

**`INSENSITIVE`**

表示游标创建后对其底层表的更新不应影响游标检索的数据。Apache Cloudberry 中所有游标都是不敏感的。此关键字目前没有效果，仅为兼容 SQL 标准而保留。

**`NO SCROLL`**

不能使用该游标以非顺序方式检索行。这是 Apache Cloudberry 的默认行为；不支持可滚动游标（`SCROLL`）。

**`PARALLEL RETRIEVE`**

声明并行检索游标。这是一种特殊游标，可用于直接从 Apache Cloudberry Segment 并行检索结果。

**`WITH HOLD`**<br />
**`WITHOUT HOLD`**

`WITH HOLD` 指定在创建游标的事务成功提交后仍可继续使用游标。`WITHOUT HOLD` 指定游标不能在创建它的事务之外使用。默认为 `WITHOUT HOLD`。

> **注意** Apache Cloudberry 不支持使用 `WITH HOLD` 子句声明 `PARALLEL RETRIEVE` 游标。当 `query` 包含 `FOR UPDATE` 或 `FOR SHARE` 子句时，也不能指定 `WITH HOLD`。

**`query`**

为游标提供返回行的 [SELECT](/cloudberry/reference/sql-stmts/select/) 或 [VALUES](/cloudberry/reference/sql-stmts/values/) 命令。

如果在 [UPDATE](/cloudberry/reference/sql-stmts/update/) 或 [DELETE](/cloudberry/reference/sql-stmts/delete/) 命令的 `WHERE CURRENT OF` 子句中使用游标，`SELECT` 命令必须满足以下条件：

- 不能引用视图或外部表。
- 只引用一个表。

    该表必须是堆表，且不能采用复制分布（不能是视图、外部表或 AO 列存表）。

- 不能包含以下任何内容：
    - 分组子句
    - `UNION ALL` 或 `UNION DISTINCT` 等集合操作
    - 排序子句
    - 窗口子句
    - 连接或自连接

    在 `SELECT` 命令中指定 `FOR UPDATE` 子句，可防止其他会话在行被获取后、更新前修改这些行。不使用 `FOR UPDATE` 子句时，如果游标创建后该行发生变化，随后执行带有 `WHERE CURRENT OF` 子句的 `UPDATE` 或 `DELETE` 命令将不会产生效果。

    > **注意** 在 `SELECT` 命令中指定 `FOR UPDATE` 子句会锁定整个表，而不只是选中的行。

关键字 `BINARY`、`INSENSITIVE` 和 `NO SCROLL` 可以按任意顺序出现。

## 注意事项 {#notes}

除非指定 `WITH HOLD`，否则此命令创建的游标只能在当前事务内使用。因此，不带 `WITH HOLD` 的 `DECLARE` 在事务块外没有用处：游标只能存活到语句完成。所以，在事务块外使用此命令时 Apache Cloudberry 会报错。使用 `BEGIN` 和 `COMMIT`（或 `ROLLBACK`）定义事务块。

如果指定了 `WITH HOLD`，并且创建游标的事务成功提交，则同一会话中的后续事务可以继续访问该游标。（但如果创建事务提前中止，游标就会被移除。）使用 `WITH HOLD` 创建的游标会在对其显式执行 `CLOSE` 命令或会话结束时关闭。在当前实现中，保留游标所表示的行会被复制到临时文件或内存区域，以供后续事务继续访问。

如果在事务中用 `DECLARE` 命令创建游标，则在用 `CLOSE` 命令关闭游标之前，不能在该事务中使用 `SET` 命令。

Apache Cloudberry 目前不支持可滚动游标。只能使用 `FETCH` 或 `RETRIEVE` 向前移动游标位置，不能后退。

AO 表不支持 `DECLARE...FOR UPDATE`。

可以通过查询 `pg_cursors` 系统视图查看所有可用游标。

## 示例 {#examples}

声明游标：

```sql
DECLARE mycursor CURSOR FOR SELECT * FROM mytable;
```

为同一查询声明并行检索游标：

```sql
DECLARE myprcursor PARALLEL RETRIEVE CURSOR FOR SELECT * FROM mytable;
```

## 兼容性 {#compatibility}

SQL 标准只允许在嵌入式 SQL 和模块中使用游标。Apache Cloudberry 允许交互式使用游标。

Apache Cloudberry 没有为游标实现 `OPEN` 语句。游标声明时即被视为打开。

SQL 标准允许游标前进和后退。Apache Cloudberry 的所有游标只能向前移动（不可滚动）。

二进制游标是 Apache Cloudberry 的扩展。

SQL 标准未规定并行检索游标。

## 另请参阅 {#see-also}

[CLOSE](/cloudberry/reference/sql-stmts/close/), [DELETE](/cloudberry/reference/sql-stmts/delete/), [FETCH](/cloudberry/reference/sql-stmts/fetch/), [MOVE](/cloudberry/reference/sql-stmts/move/), [RETRIEVE](/cloudberry/reference/sql-stmts/retrieve/), [SELECT](/cloudberry/reference/sql-stmts/select/), [UPDATE](/cloudberry/reference/sql-stmts/update/)
