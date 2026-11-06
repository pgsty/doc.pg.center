---
title: "BEGIN"
description: "开始一个事务块。"
weight: 440
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/begin.md"
---

## 概要 {#synopsis}

```sql
BEGIN [WORK | TRANSACTION] [<transaction_mode>]

-- where <transaction_mode> is:

   ISOLATION LEVEL {READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ | SERIALIZABLE}
   READ WRITE | READ ONLY
   [NOT] DEFERRABLE
```

## 描述 {#description}

`BEGIN` 启动一个事务块，也就是说，`BEGIN` 命令之后的所有语句都将在同一个事务中运行，直到显式给出 [COMMIT](/cloudberry/reference/sql-stmts/commit/) 或 [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) 为止。默认情况下（不使用 `BEGIN`），Apache Cloudberry 以“自动提交”模式运行事务，也就是说，每条语句都在各自的事务中运行，并在语句结束时隐式提交（若执行成功；否则执行回滚）。

在事务块中运行语句会更快，因为事务的启动和提交需要大量的 CPU 和磁盘活动。在进行多项相关更改时，在一个事务内执行多条语句也有助于保证一致性：其他会话将无法看到相关更新尚未全部完成时的中间状态。

如果指定了隔离级别、读写模式或可延迟模式，新事务就具有这些特性，就像运行了 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) 一样。

## 参数 {#parameters}

WORK
**`TRANSACTION`**

可选关键字，没有任何作用。

关于该语句其他参数含义的信息，请参阅 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)。

## 注意事项 {#notes}

[START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/) 与 `BEGIN` 具有相同的功能。

使用 [COMMIT](/cloudberry/reference/sql-stmts/commit/) 或 [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) 来结束一个事务块。

在已处于事务块中时发出 `BEGIN` 会引发一条警告消息，事务的状态不受影响。若要在事务块内嵌套事务，请使用保存点（参见 [SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/)）。

出于向后兼容的原因，相邻的 transaction_modes 之间的逗号可以省略。

## 示例 {#examples}

开始一个事务块：

```sql
BEGIN;
```

## 兼容性 {#compatibility}

`BEGIN` 是 Apache Cloudberry 的语言扩展。它等价于 SQL 标准命令 [START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/)，后者的参考页包含更多兼容性信息。

`DEFERRABLE` transaction_mode 是 Apache Cloudberry 的语言扩展。

另外，关键字 `BEGIN` 在嵌入式 SQL 中用于不同的目的。在移植数据库应用程序时，请注意事务语义。

## 另见 {#see-also}

[COMMIT](/cloudberry/reference/sql-stmts/commit/)、[ROLLBACK](/cloudberry/reference/sql-stmts/rollback/)、[SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/)、[START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/)
