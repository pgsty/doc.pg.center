---
title: "COMMIT"
description: "提交当前事务。"
weight: 500
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/commit.md"
---

## 概要 {#synopsis}

```sql
COMMIT [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## 描述 {#description}

`COMMIT` 提交当前事务。该事务所做的全部更改会对其他会话可见，并且保证在发生崩溃时仍然持久。

## 参数 {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

可选关键字，没有任何作用。

**`AND CHAIN`**

如果指定了 `AND CHAIN`，则会立即启动一个新事务，其事务特性（参见 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)）与刚刚结束的事务相同。否则，不会启动新事务。

## 注意事项 {#notes}

使用 [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) 可提前结束一个事务。

在不处于事务中时发出 `COMMIT` 不会造成危害，但会引发一条警告消息。不处于事务中时执行 `COMMIT AND CHAIN` 则是错误。

## 示例 {#examples}

要提交当前事务并使其全部更改永久生效：

```sql
COMMIT;
```

## 兼容性 {#compatibility}

命令 `COMMIT` 符合 SQL 标准。`COMMIT TRANSACTION` 形式是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[BEGIN](/cloudberry/reference/sql-stmts/begin/)、[END](/cloudberry/reference/sql-stmts/end/)、[ROLLBACK](/cloudberry/reference/sql-stmts/rollback/)、[START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/)
