---
title: "ROLLBACK"
description: "停止当前事务。"
weight: 1650
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/rollback.md"
---

## 概要 {#synopsis}

```sql
ROLLBACK [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## 描述 {#description}

`ROLLBACK` 回滚当前事务，并丢弃该事务所做的所有更新。

## 参数 {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

可选关键字，没有效果。

**`AND CHAIN`**

如果指定 `AND CHAIN`，会立即启动一个新事务，其事务特性（见 [`SET TRANSACTION`](/cloudberry/reference/sql-stmts/set-transaction/)）与刚结束的事务相同。否则，不启动新事务。

## 注意事项 {#notes}

使用 [`COMMIT`](/cloudberry/reference/sql-stmts/commit/) 成功结束当前事务。

在事务块之外发出 `ROLLBACK` 会产生一条警告，除此之外没有效果。在事务块之外发出 `ROLLBACK AND CHAIN` 则会报错。

## 示例 {#examples}

丢弃当前事务所做的所有更改：

```sql
ROLLBACK;
```

## 兼容性 {#compatibility}

`ROLLBACK` 命令符合 SQL 标准。`ROLLBACK TRANSACTION` 形式是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`ROLLBACK TO SAVEPOINT`](/cloudberry/reference/sql-stmts/rollback-to-savepoint/), [`SAVEPOINT`](/cloudberry/reference/sql-stmts/savepoint/)
