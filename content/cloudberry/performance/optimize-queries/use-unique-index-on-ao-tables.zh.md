---
title: "在 AO 表上创建唯一索引"
description: "在 Apache Cloudberry 中，可以为 AO 表或 AOCS 列存表创建唯一索引。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/use-unique-index-on-ao-tables.md"
---

有了唯一索引，Apache Cloudberry 会在向 AO 表插入数据时检查唯一约束，确保数据的唯一性。同时，数据库会通过优化器优化特定查询，提高查询性能。不过，维护唯一索引也会带来一定开销，尤其是在插入数据时。

## 工作原理 {#how-it-works}

当 AO 表上存在唯一索引时，向 AO 表插入元组会使 Apache Cloudberry 在该表的辅助索引结构 BlockDirectory 中插入占位项，阻止插入相同的键，从而实现唯一索引。

## 如何为 AO 表添加唯一索引 {#how-to-add-a-unique-index-on-an-ao-table}

可以通过两种方式为 AO 表添加唯一索引，请根据需要选择。

- 创建表时指定唯一键或约束。

    ```sql
    CREATE TABLE foo(i int UNIQUE) USING ao_row;
    CREATE TABLE bar(i int UNIQUE) USING ao_column;
    CREATE TABLE foo2(i int, CONSTRAINT iuniq UNIQUE(i));
    ```

- 创建表后单独添加唯一索引或约束。

    ```sql
    CREATE TABLE baz(i int) with (appendonly=true);
    CREATE UNIQUE INDEX on baz(i);

    CREATE TABLE foobar(i int) USING ao_row;
    ALTER TABLE foobar ADD CONSTRAINT unique_i UNIQUE (i);
    ```

## 使用示例 {#usage-examples}

1. 创建带唯一约束的 AO 表。

    ```sql
    postgres=# CREATE TABLE foo(i int UNIQUE) USING ao_row;
    CREATE TABLE

    postgres=# \d foo
                    Table "public.foo"
    Column |  Type   | Collation | Nullable | Default 
    --------+---------+-----------+----------+---------
    i      | integer |           |          | 
    Compression Type: None
    Compression Level: 0
    Block Size: 32768
    Checksum: t
    Indexes:
        "foo_i_key" UNIQUE CONSTRAINT, btree (i)
    Distributed by: (i)
    ```

2. 向表中插入相同的键值会返回 `duplicate key` 错误。

    ```sql
    postgres=# INSERT INTO foo VALUES(1);
    INSERT 0 1

    postgres=# INSERT INTO foo VALUES(1);
    ERROR:  duplicate key value violates unique constraint "foo_i_key"  (seg1 127.0.1.1:8003 pid=557)
    DETAIL:  Key (i)=(1) already exists.
    ```

并发插入数据示例：在 READ COMMITTED 事务隔离级别下，两个事务并发向同一张 AO 表插入相同的值，其中一个成功，另一个被阻塞。

1. 如果一个事务成功，另一个插入操作会失败。

    ```sql
    -- Session 1
    postgres=# BEGIN;
    BEGIN

    postgres=*# INSERT INTO foo VALUES(1);
    INSERT 0 1  -- Insertion successful

    postgres=*# COMMIT;
    COMMIT
    ```

    ```sql
    -- Session 2
    postgres=# BEGIN;
    BEGIN

    postgres=*# INSERT INTO foo VALUES(1);
    ERROR:  duplicate key value violates unique constraint "foo_i_key"  (seg1 127.0.1.1:8003 pid=2726)
    DETAIL:  Key (i)=(1) already exists.  -- Insertion fails

    postgres=!# END;
    ROLLBACK
    ```

2. 如果一个事务插入失败，另一个事务就会成功。

    ```sql
    postgres=# BEGIN;
    BEGIN
    postgres=*# INSERT INTO foo VALUES(1);
    INSERT 0 1
    postgres=*# ROLLBACK;
    ROLLBACK
    ```

    ```sql
    postgres=# BEGIN;
    BEGIN
    postgres=*# INSERT INTO foo VALUES(1);
    INSERT 0 1
    postgres=*# COMMIT;
    COMMIT
    ```
