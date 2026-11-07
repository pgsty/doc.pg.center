---
title: Snowflake 函数
description: 介绍 Snowflake 的 nextval、currval、epoch、count、node 和 format 函数及查询示例。
weight: 200
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/snowflake_functions.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



你可以在 psql 命令行查询以下 Snowflake 函数，获取使用 Snowflake 序列的表的有用信息。

**`snowflake.nextval([sequence regclass])`** 
在指定序列中生成下一个 Snowflake。如果未指定序列，则使用数据库范围内的内部序列 `snowflake.id_seq`。例如，以下查询返回 `orders_id_seq` 序列中的下一个数字：

```sql
acctg=# SELECT * FROM snowflake.nextval('orders_id_seq'::regclass);
      nextval       
--------------------
 136169504773242881
(1 row)
```

**`snowflake.currval([sequence regclass])`** 
返回指定序列的当前值。在当前会话中调用该序列的 `snowflake.nextval()` 之前，这个值是未定义的。例如，以下查询返回 `orders_id_seq` 序列的当前值：

```sql
acctg=# SELECT * FROM snowflake.currval('orders_id_seq'::regclass);
      currval       
--------------------
 136169504773242881
(1 row)
```

**`snowflake.get_epoch(snowflake int8)`** 以 `EPOCH`（自 2023-01-01 起的秒数）形式返回 Snowflake 的时间戳部分，类型是精度为三位数的 `NUMERIC` 值。例如，以下序列值的时间戳是自 2023 年 1 月 1 日以来的 `1704996539.845` 秒：

```sql
acctg=# SELECT * FROM snowflake.get_epoch(136169504773242881);
   get_epoch    
----------------
 1704996539.845
(1 row)
```

可以使用 `to_timestamp(snowflake.get_epoch(<value>))` 函数把 epoch 转换为时间戳。例如：

```sql
acctg=# SELECT to_timestamp(snowflake.get_epoch(136169504773242881));
        to_timestamp        
----------------------------
 2024-01-11 13:08:59.845-05
(1 row)
```

**`snowflake.get_count(snowflake int8)`** 以 `int4` 值返回给定 Snowflake 的 count 部分；每进入一个新毫秒，count 会重置为 `0`。例如：

```sql
acctg=# SELECT snowflake.get_count(136169504773242881);
 get_count 
-----------
         3
(1 row)
```

**`snowflake.get_node(snowflake int8)`** 返回指定 Snowflake 序列所在主机 `snowflake.node` 在 `postgresql.conf` 中的值。例如，Snowflake 序列号 `136169504773242881` 位于节点 `1`：

```sql
acctg=# SELECT * FROM snowflake.get_node(136169504773242881);
 get_node 
----------
        1
(1 row)
```

**`snowflake.format(snowflake int8)`** 以 `jsonb` 对象形式返回给定 Snowflake，格式为：`{"node": 1, "ts": "2023-10-16 17:57:26.361+00", "count": 0}`。例如：

```sql
acctg=# SELECT * FROM snowflake.format(136169504773242881);
                          format                           
-----------------------------------------------------------
 {"id": 1, "ts": "2024-01-11 13:08:59.845-05", "count": 0}
(1 row)
```

---

[上游原文](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/snowflake_functions.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
