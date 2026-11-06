---
title: "CLOSE"
description: "关闭一个游标。"
weight: 470
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/close.md"
---

## 概要 {#synopsis}

```sql
CLOSE { <cursor_name> | ALL }
```

## 描述 {#description}

`CLOSE` 释放与一个已打开游标相关联的资源。游标关闭后，不允许再对其执行任何后续操作。不再需要某个游标时，应当将其关闭。

当事务通过 `COMMIT` 或 `ROLLBACK` 终止时，每个已打开的不可保持游标都会被隐式关闭。如果创建可保持游标的事务通过 `ROLLBACK` 提前结束，该可保持游标会被隐式关闭。如果创建它的事务成功提交，则该可保持游标会一直保持打开状态，直到显式运行 `CLOSE` 或者客户端断开连接为止。

## 参数 {#parameters}

**`cursor_name`**

要关闭的已打开游标的名称。

**`ALL`**

关闭所有已打开的游标。

## 注解 {#notes}

Apache Cloudberry 没有显式的 `OPEN` 游标语句。游标在声明时即被视为已打开。请使用 [DECLARE](/cloudberry/reference/sql-stmts/declare/) 语句声明（并打开）游标。

通过查询 `pg_cursors` 系统视图，可以查看所有可用的游标。

如果游标在某个保存点之后被关闭，而该保存点后来又被回滚，则 `CLOSE` 不会被回滚；也就是说，该游标仍保持关闭状态。

## 示例 {#examples}

关闭游标 `portala`：

```sql
CLOSE portala;
```

## 兼容性 {#compatibility}

`CLOSE` 完全符合 SQL 标准。`CLOSE ALL` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[DECLARE](/cloudberry/reference/sql-stmts/declare/)、[FETCH](/cloudberry/reference/sql-stmts/fetch/)、[MOVE](/cloudberry/reference/sql-stmts/move/)、[RETRIEVE](/cloudberry/reference/sql-stmts/retrieve/)
