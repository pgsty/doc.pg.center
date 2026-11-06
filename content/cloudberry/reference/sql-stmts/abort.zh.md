---
title: "ABORT"
description: "终止当前事务。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/abort.md"
---

## 概要 {#synopsis}

```sql
ABORT [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## 描述 {#description}

`ABORT` 回滚当前事务，并丢弃该事务所做的全部更新。该命令在行为上与标准 SQL 命令 [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/) 完全相同，仅出于历史原因而保留。

## 参数 {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

可选关键字，没有任何作用。

**`AND CHAIN`**

如果指定了 `AND CHAIN`，则会立即启动一个新事务，其事务特性（参见 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)）与刚刚结束的事务相同。否则，不会启动新事务。

## 注意事项 {#notes}

使用 [`COMMIT`](/cloudberry/reference/sql-stmts/commit/) 可成功地终止一个事务。

在事务块之外发出 `ABORT` 会产生一条警告，除此之外没有任何效果。

## 示例 {#examples}

要终止所有更改：

```sql
ABORT;
```

## 兼容性 {#compatibility}

该命令是 Apache Cloudberry 的扩展，仅出于历史原因而保留。`ROLLBACK` 是与之等效的标准 SQL 命令。

## 另见 {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/)、[`COMMIT`](/cloudberry/reference/sql-stmts/commit/)、[`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/)
