---
title: "ROLLBACK TO SAVEPOINT"
description: "将当前事务回滚到保存点。"
weight: 1640
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/rollback-to-savepoint.md"
---

## 概要 {#synopsis}

```sql
ROLLBACK [ WORK | TRANSACTION ] TO [ SAVEPOINT ] <savepoint_name>
```

## 描述 {#description}

此命令回滚建立保存点后执行的所有命令。该保存点仍然有效，之后如有需要，还可以再次回滚到它。

`ROLLBACK TO SAVEPOINT` 隐式销毁在指定保存点之后建立的所有保存点。

## 参数 {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

可选关键字，没有效果。

**`savepoint_name`**

要回滚到的保存点名称。

## 注意事项 {#notes}

使用 [RELEASE SAVEPOINT](/cloudberry/reference/sql-stmts/release-savepoint/) 可以销毁保存点，同时保留建立保存点后所执行命令的效果。

指定尚未建立的保存点名称会报错。

对于保存点，游标具有一些非事务性行为。在保存点范围内打开的游标，会在回滚到该保存点时关闭。如果先前打开的游标受到保存点范围内某条 `FETCH` 命令的影响，而该保存点随后回滚，游标仍停留在 `FETCH` 使其指向的位置（即由 `FETCH` 引起的游标移动不会回滚）。关闭游标的操作也不会因回滚而撤销。不过，如果游标查询引起的其他副作用（例如查询调用的易变函数的副作用）发生在随后回滚的保存点范围内，这些副作用*会*回滚。如果游标的执行导致事务提前结束，该游标会进入不可执行状态；因此，虽然可以使用 `ROLLBACK TO SAVEPOINT` 恢复事务，却不能再使用此游标。

## 示例 {#examples}

撤销建立 `my_savepoint` 后执行的命令的效果：

```sql
ROLLBACK TO SAVEPOINT my_savepoint;
```

保存点回滚不会影响游标位置：

```sql
BEGIN;
DECLARE foo CURSOR FOR SELECT 1 UNION SELECT 2;
SAVEPOINT foo;
FETCH 1 FROM foo;
column 
----------
        1

ROLLBACK TO SAVEPOINT foo;
FETCH 1 FROM foo;
column 
----------
        2

COMMIT;
```

## 兼容性 {#compatibility}

SQL 标准要求必须写出 `SAVEPOINT` 关键字，但 Apache Cloudberry（以及 Oracle）允许省略。SQL 只允许在 `ROLLBACK` 后使用噪声词 `WORK`，不允许使用 `TRANSACTION`。另外，SQL 有一个可选子句 `AND [NO] CHAIN`，Apache Cloudberry 目前不支持。除此之外，此命令符合 SQL 标准。

## 另见 {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`RELEASE SAVEPOINT`](/cloudberry/reference/sql-stmts/release-savepoint/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/), [`SAVEPOINT`](/cloudberry/reference/sql-stmts/savepoint/)
