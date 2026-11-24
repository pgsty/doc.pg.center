---
title: Snowflake 函数
description: 介绍 Snowflake 的 nextval、currval、epoch、count、node 和 format 函数及查询示例。
weight: 200
upstream_source: pgedge-snowflake-20261121
upstream_link: https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/snowflake_functions.md
upstream_modified: true
upstream_ref: 9506e1bd5c1f
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



你可以在 psql 命令行查询以下 Snowflake 函数，获取使用 Snowflake 序列的表的有用信息。

**`snowflake.nextval([sequence regclass])`** 
在指定序列中生成下一个 Snowflake ID。如果未指定序列，则使用数据库范围内的内部序列 `snowflake.id_seq`。例如，以下查询返回 `orders_id_seq` 序列中的下一个数字：

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

**`snowflake.get_epoch(snowflake int8)`** 返回 Snowflake ID 中的时间戳，单位为秒，返回类型是保留三位小数的 `NUMERIC`。以下示例的结果为 `1704996539.845`。

> [!NOTE] 译校说明
> ID 内部时间字段从 2023-01-01 UTC 起算。v2.6.1 实现会补回从 1970 到 2023 年的偏移量，因此返回的是 Unix 时间戳，可直接传给 `to_timestamp`。[固定版本实现](https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/snowflake.c#L297-L304)

```sql
acctg=# SELECT * FROM snowflake.get_epoch(136169504773242881);
   get_epoch    
----------------
 1704996539.845
(1 row)
```

可以使用 `to_timestamp(snowflake.get_epoch(<value>))` 将返回的秒数转换为时间戳。例如：

```sql
acctg=# SELECT to_timestamp(snowflake.get_epoch(136169504773242881));
        to_timestamp        
----------------------------
 2024-01-11 13:08:59.845-05
(1 row)
```

> [!NOTE] 示例中的节点号和计数器
> 按 v2.6.1 的位布局，`136169504773242881` 的第 12–21 位为 `0`，低 12 位为 `1`。因此该 ID 的 `get_node()` 应返回 `0`，`get_count()` 应返回 `1`，`format()` 中对应字段为 `"id": 0` 和 `"count": 1`。下方保留的上游输出与该版本不同。[固定版本的位掩码](https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/snowflake.c#L109-L122)

**`snowflake.get_count(snowflake int8)`** 以 `int4` 返回给定 Snowflake ID 中的计数器值。每开始一个新的毫秒，计数器就重置为 `0`。例如：

```sql
acctg=# SELECT snowflake.get_count(136169504773242881);
 get_count 
-----------
         3
(1 row)
```

**`snowflake.get_node(snowflake int8)`** 返回 ID 中编码的节点号。生成 ID 时使用节点的 `snowflake.node` 设置，解码时无需读取该节点的配置文件。下方为上游记录的输出。

```sql
acctg=# SELECT * FROM snowflake.get_node(136169504773242881);
 get_node 
----------
        1
(1 row)
```

**`snowflake.format(snowflake int8)`** 以 `jsonb` 对象形式返回给定 Snowflake，格式为：`{"id": 1, "ts": "2023-10-16 17:57:26.361+00", "count": 0}`。例如：

```sql
acctg=# SELECT * FROM snowflake.format(136169504773242881);
                          format                           
-----------------------------------------------------------
 {"id": 1, "ts": "2024-01-11 13:08:59.845-05", "count": 0}
(1 row)
```

---

[上游原文](https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/snowflake_functions.md) · `9506e1bd5c1f` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
