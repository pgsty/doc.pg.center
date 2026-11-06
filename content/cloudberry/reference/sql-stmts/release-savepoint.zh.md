---
title: "RELEASE SAVEPOINT"
description: "销毁先前定义的保存点。"
weight: 1600
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/release-savepoint.md"
---

## 概要 {#synopsis}

```sql
RELEASE [SAVEPOINT] <savepoint_name>
```

## 描述 {#description}

`RELEASE SAVEPOINT` 销毁当前事务中先前定义的保存点。

销毁保存点后，就不能再回滚到该保存点，但没有其他用户可见的行为。它不会撤销建立保存点后执行的命令的效果。（要进行撤销，见 [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/)。）在不再需要保存点时将其销毁，可能使系统在事务结束前就回收部分资源。

`RELEASE SAVEPOINT` 还会销毁在指定保存点*之后*建立的所有保存点。

## 参数 {#parameters}

**`savepoint_name`**

要销毁的保存点名称。

## 注意事项 {#notes}

指定先前未定义的保存点名称会报错。

事务处于中止状态时，不能释放保存点。

如果多个保存点同名，Apache Cloudberry 只释放最近定义且尚未释放的保存点。重复执行此命令，会逐步释放更早的保存点。

## 示例 {#examples}

建立保存点并在之后将其销毁：

```sql
BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

上述事务同时插入 3 和 4。

## 兼容性 {#compatibility}

此命令符合 SQL 标准。标准要求必须写出 `SAVEPOINT` 关键字，但 Apache Cloudberry 允许省略。

## 另见 {#see-also}

[BEGIN](/cloudberry/reference/sql-stmts/begin/), [COMMIT](/cloudberry/reference/sql-stmts/commit/), [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/), [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/), [SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/)
