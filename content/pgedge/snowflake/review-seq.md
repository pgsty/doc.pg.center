---
title: Reviewing Sequence Definitions in your Table Meta-data
description: 'If you query the table meta-data before performing a sequence conversion with the \d+ orders command,
  the PostgreSQL sequence is defined in the Default column:'
weight: 200
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/review_seq.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
type: docs
---



If you query the table meta-data before performing a sequence conversion with the `\d+ orders` command, the PostgreSQL sequence is defined in the `Default` column:

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

After performing a conversion, the `\d+ table_name` command shows a `Default` value of `snowflake.nextval('orders_id_seq'::regclass)`:

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

[Upstream source](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/review_seq.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
