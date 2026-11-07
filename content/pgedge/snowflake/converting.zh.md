---
title: 将 PostgreSQL 序列转换为 Snowflake 序列
description: 说明如何识别既有序列、调用 snowflake.convert_sequence_to_snowflake()，并理解转换后新旧值的差异。
weight: 200
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/converting.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



不能直接创建 snowflake 序列；必须先在 PostgreSQL 中创建序列，再进行转换。序列可以通过 `CREATE SEQUENCE` 命令显式创建，也会由 `GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY` 表列，或 `SERIAL` 与 `BIGSERIAL` 列隐式创建。`GENERATED AS IDENTITY` 是推荐的 ANSI SQL 方法。

可以使用 `snowflake.convert_sequence_to_snowflake()` 函数将单个序列转换为 snowflake 序列。注意，该操作转换的是序列定义；序列列中的既有值不会改变。SQL 命令语法为：

    `SELECT snowflake.convert_sequence_to_snowflake('sequence_name');`

**其中**

`sequence_name` 是序列的名称。

有多种方法可以返回序列列表。其中一种方法是使用 PostgreSQL [`psql client`](https://www.postgresql.org/docs/current/app-psql.html) 执行以下命令：

```
    \ds
```

另一种方法是在 `psql` 或其他 SQL 编辑器中直接查询元数据 catalog 信息。

```
    SELECT * FROM information_schema.sequences;
```

第二条命令会包含数据类型信息，这有助于了解哪些序列会被转换为 BIGINT 数据类型（64 位）。


## 示例：转换既有序列 {#example-converting-an-existing-sequence}

下面的示例演示在 psql 命令行中转换序列；示例使用名为 `orders` 的表，该表有三列，最后一列是由序列生成的 `id` 列：

```
acctg=# CREATE TABLE orders (customer VARCHAR, invoice VARCHAR, id bigserial PRIMARY KEY);
CREATE TABLE
```

创建表后，向 `orders` 表插入数据。这里只需提供前两列的内容，因为序列定义会跟踪第三列的值，并按需添加它：

```
acctg=# INSERT INTO orders VALUES ('Chesterfield Schools', 'art_9338');
INSERT 0 1
acctg=# INSERT INTO orders VALUES ('Chesterfield Schools', 'math_9663');
INSERT 0 1
acctg=# INSERT INTO orders VALUES ('Albemarle Schools', 'sci_2009');
INSERT 0 1
acctg=# INSERT INTO orders VALUES ('King William Schools', 'sci_7399');
INSERT 0 1
acctg=# INSERT INTO orders VALUES ('King William Schools', 'art_9484');
INSERT 0 1
acctg=# INSERT INTO orders VALUES ('Hanover Schools', 'music_1849');
INSERT 0 1
acctg=# INSERT INTO orders VALUES ('Washington Schools', 'hist_2983');
INSERT 0 1
```
查询表中的行时，可以在 `id` 列看到序列号：

```
acctg=# SELECT * FROM orders;
       customer       |  invoice   | id 
----------------------+------------+----
 Chesterfield Schools | art_9338   |  1
 Chesterfield Schools | math_9663  |  2
 Albemarle Schools    | sci_2009   |  3
 King William Schools | sci_7399   |  4
 King William Schools | art_9484   |  5
 Hanover Schools      | music_1849 |  6
 Washington Schools   | hist_2983  |  7
(7 rows)
```

要把 `orders` 表的序列定义转换为使用 Snowflake 序列，请在 `psql` 或其他 SQL 编辑器中调用以下命令：

```
SELECT snowflake.convert_sequence_to_snowflake('orders_id_seq'::regclass);
```

转换过程会修改序列定义，使其使用 Snowflake 序列，但不会更新既有行。如果用 psql 重新连接并向表添加新行，新行的 `id` 就是 Snowflake 序列：

```
acctg=# INSERT INTO orders VALUES ('Prince William Schools', 'math_8330');
INSERT 0 1
acctg=# INSERT INTO orders VALUES ('Fluvanna Schools', 'art_9447');
INSERT 0 1
```

在随后的查询结果中，`id` 列显示未格式化的序列值，`format` 列显示同一信息，并由 `snowflake.format(id)` 函数格式化。转换为 Snowflake 序列之前添加的行显示固定时间戳 `2022-12-31 19:00:00-05`，而 Snowflake 序列拥有唯一的 `id` 和时间戳。

表中的原始条目显示 PostgreSQL 序列，转换之后创建的条目显示 Snowflake 序列：

```
acctg=# SELECT id, snowflake.format(id), customer, invoice FROM orders;
         id         |                          format                           |        customer        |  invoice   
--------------------+-----------------------------------------------------------+------------------------+------------
                  1 | {"id": 1, "ts": "2022-12-31 19:00:00-05", "count": 0}     | Chesterfield Schools   | art_9338
                  2 | {"id": 2, "ts": "2022-12-31 19:00:00-05", "count": 0}     | Chesterfield Schools   | math_9663
                  3 | {"id": 3, "ts": "2022-12-31 19:00:00-05", "count": 0}     | Albemarle Schools      | sci_2009
                  4 | {"id": 4, "ts": "2022-12-31 19:00:00-05", "count": 0}     | King William Schools   | sci_7399
                  5 | {"id": 5, "ts": "2022-12-31 19:00:00-05", "count": 0}     | King William Schools   | art_9484
                  6 | {"id": 6, "ts": "2022-12-31 19:00:00-05", "count": 0}     | Hanover Schools        | music_1849
                  7 | {"id": 7, "ts": "2022-12-31 19:00:00-05", "count": 0}     | Washington Schools     | hist_2983
 135824181823537153 | {"id": 1, "ts": "2024-01-10 14:16:48.438-05", "count": 0} | Prince William Schools | math_8330
 135824609030176769 | {"id": 1, "ts": "2024-01-10 14:18:30.292-05", "count": 0} | Fluvanna Schools       | art_9447
(9 rows)
```

**INCREMENT 与缓存**

在同一毫秒内，snowflake 最多允许 4096 个值。Hibernate 等 ORM 框架可能被配置为尝试获取一个序列值，并使用序列的 `INCREMENT` 值缓存和分配一段范围。Snowflake 序列会遵循增量值，但不应使用大于 4096 的值。如果要修改增量值，请使用 `ALTER SEQUENCE <seq_name> INCREMENT <increment_value> NO MAXVALUE`。

---

[上游原文](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/converting.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
