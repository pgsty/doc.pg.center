---
title: "SAVEPOINT"
description: "在当前事务中定义新的保存点。"
weight: 1660
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/savepoint.md"
---

## 概要 {#synopsis}

```sql
SAVEPOINT <savepoint_name>
```

## 描述 {#description}

`SAVEPOINT` 在当前事务中建立新的保存点。

保存点是事务中的一种特殊标记，可以回滚建立该标记后执行的所有命令，将事务状态恢复到保存点建立时的状态。

## 参数 {#parameters}

**`savepoint_name`**

新保存点的名称。如果已经存在同名保存点，在释放较新的同名保存点之前，旧保存点不可访问。

## 注意事项 {#notes}

使用 [`ROLLBACK TO SAVEPOINT`](/cloudberry/reference/sql-stmts/rollback-to-savepoint/) 回滚到保存点。使用 [`RELEASE SAVEPOINT`](/cloudberry/reference/sql-stmts/release-savepoint/) 销毁保存点，同时保留建立保存点后执行的命令的效果。

只能在事务块中建立保存点。一个事务中可以定义多个保存点。

## 示例 {#examples}

建立保存点，并在之后撤销建立该保存点后执行的所有命令的效果：

```sql
BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    ROLLBACK TO SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);
COMMIT;
```

上述事务插入值 1 和 3，不插入 2。

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

使用同一个保存点名称：

``` sql
BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);

    -- rollback to the second savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows rows 1 and 2

    -- release the second savepoint
    RELEASE SAVEPOINT my_savepoint;

    -- rollback to the first savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows only row 1
COMMIT;
```

上述事务先回滚第 3 行，再回滚第 2 行。

## 兼容性 {#compatibility}

SQL 要求在建立另一个同名保存点时自动销毁旧保存点。Apache Cloudberry 会保留旧保存点，但回滚或释放时只使用较新的保存点。（释放新保存点后，旧保存点就可以再次用于 [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/) 和 [RELEASE SAVEPOINT](/cloudberry/reference/sql-stmts/release-savepoint/)。）除此之外，`SAVEPOINT` 完全符合 SQL 标准。

## 另见 {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`RELEASE SAVEPOINT`](/cloudberry/reference/sql-stmts/release-savepoint/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/), [`ROLLBACK TO SAVEPOINT`](/cloudberry/reference/sql-stmts/rollback-to-savepoint/)
