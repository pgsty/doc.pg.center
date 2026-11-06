---
title: "START TRANSACTION"
description: "启动事务块。"
weight: 1750
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/start-transaction.md"
---

## 概要 {#synopsis}

```sql
START TRANSACTION [<transaction_mode>] [, ...]

-- where <transaction_mode> is one of:

   ISOLATION LEVEL {SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED}
   READ WRITE | READ ONLY
   [NOT] DEFERRABLE
```

## 描述 {#description}

`START TRANSACTION` 启动新的事务块。如果指定隔离级别、读写模式或可延迟模式，新事务就会具有这些特性，如同执行了 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)。此命令与 [`BEGIN`](/cloudberry/reference/sql-stmts/begin/) 相同。

## 参数 {#parameters}

此语句参数的含义见 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)。

## 兼容性 {#compatibility}

在标准中，启动事务块无需发出 `START TRANSACTION`：任何 SQL 命令都会隐式开始一个事务块。Apache Cloudberry 的行为可以理解为：对于每条不位于 `START TRANSACTION`（或 `BEGIN`）之后的命令，执行后都隐式发出 `COMMIT`，因此通常称为“自动提交”。其他关系数据库系统也可能提供自动提交功能以便使用。

`DEFERRABLE` transaction_mode 是 Apache Cloudberry 的语言扩展。

SQL 标准要求连续的 transaction_modes 之间使用逗号，但出于历史原因，Apache Cloudberry 允许省略逗号。

另见 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) 的兼容性一节。

## 另见 {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/), [`SAVEPOINT`](/cloudberry/reference/sql-stmts/savepoint/), [`SET TRANSACTION`](/cloudberry/reference/sql-stmts/set-transaction/)
