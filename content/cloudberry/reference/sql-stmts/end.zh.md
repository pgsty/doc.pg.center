---
title: "END"
description: "提交当前事务。"
weight: 1440
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/end.md"
---

## 概要 {#synopsis}

```sql
END [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## 描述 {#description}

`END` 提交当前事务。该事务所做的所有更改对其他用户变为可见，并保证在发生崩溃时仍然持久保存。此命令是 Apache Cloudberry 的扩展，等效于 [`COMMIT`](/cloudberry/reference/sql-stmts/commit/)。

## 参数 {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

可选关键字，没有效果。

**`AND CHAIN`**

如果指定 `AND CHAIN`，会立即启动一个新事务，其事务特性（见 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)）与刚结束的事务相同。否则，不启动新事务。

## 注意事项 {#notes}

使用 [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/) 终止事务。

不在事务内时发出 `END` 不会造成损害，但会产生一条警告消息。

## 示例 {#examples}

提交当前事务并使所有更改永久生效：

```sql
END;
```

## 兼容性 {#compatibility}

`END` 是 Apache Cloudberry 的扩展，提供与 SQL 标准规定的 [`COMMIT`](/cloudberry/reference/sql-stmts/commit/) 相同的功能。

## 另见 {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/)
