---
title: 审查表元数据中的序列定义
description: 使用 \\d+ 对比序列转换前后的表 Default 定义。
weight: 200
upstream_source: pgedge-snowflake-20261121
upstream_link: https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/review_seq.md
upstream_modified: true
upstream_ref: 9506e1bd5c1f
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



转换序列之前，在 psql 中用 `\d+ orders` 查看表的元数据，`Default` 列会显示 PostgreSQL 序列定义。

```sh
acctg=# \d+ orders;
                                                             Table "public.orders"
  Column  |       Type        | Collation | Nullable |              Default               | Storage  | Compression | Stats target | Description 
----------+-------------------+-----------+----------+------------------------------------+----------+-------------+--------------+-------------
 customer | character varying |           |          |                                    | extended |             |              | 
 invoice  | character varying |           |          |                                    | extended |             |              | 
 id       | bigint            |           | not null | nextval('orders_id_seq'::regclass) | plain    |             |              | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Access method: heap
```

执行转换后，`\d+ table_name` 命令显示的 `Default` 值为 `snowflake.nextval('orders_id_seq'::regclass)`：

``` sh
acctg=# \d+ orders
                                                                  Table "public.orders"
  Column  |       Type        | Collation | Nullable |                   Default                    | Storage  | Compression | Stats target | Descripti
on 
----------+-------------------+-----------+----------+----------------------------------------------+----------+-------------+--------------+----------
---
 customer | character varying |           |          |                                              | extended |             |              | 
 invoice  | character varying |           |          |                                              | extended |             |              | 
 id       | bigint            |           | not null | snowflake.nextval('orders_id_seq'::regclass) | plain    |             |              | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Access method: heap
```

---

[上游原文](https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/review_seq.md) · `9506e1bd5c1f` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
