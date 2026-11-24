---
title: Snowflake Functions
description: You can query the following Snowflake functions at the psql command line to return useful information
  about tables that use Snowflake sequences.
weight: 200
upstream_source: pgedge-snowflake-20261121
upstream_link: https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/snowflake_functions.md
upstream_modified: true
upstream_ref: 9506e1bd5c1f
source_kind: pinned-release-tag
type: docs
---



You can query the following Snowflake functions at the psql command line to return useful information about tables that use Snowflake sequences.

**`snowflake.nextval([sequence regclass])`** 
Generates the next Snowflake in the specified sequence. If no sequence is specified, the internal, database-wide sequence `snowflake.id_seq` is used. For example, the following query returns the next number in the `orders_id_seq` sequence:

```sql
acctg=# SELECT * FROM snowflake.nextval('orders_id_seq'::regclass);
      nextval       
--------------------
 136169504773242881
(1 row)
```

**`snowflake.currval([sequence regclass])`** 
Returns the current value of the specified sequence. This value is undefined until the function `snowflake.nextval()` has been called for the sequence in the current session. For example, the following query returns the current value of the `orders_id_seq` sequence:

```sql
acctg=# SELECT * FROM snowflake.currval('orders_id_seq'::regclass);
      currval       
--------------------
 136169504773242881
(1 row)
```

**`snowflake.get_epoch(snowflake int8)`** Returns the Unix timestamp in seconds as a `NUMERIC` with three decimal places. Snowflake IDs store milliseconds relative to 2023-01-01 UTC. The function adds the offset from the Unix epoch before returning the value. The example returns `1704996539.845`:

```sql
acctg=# SELECT * FROM snowflake.get_epoch(136169504773242881);
   get_epoch    
----------------
 1704996539.845
(1 row)
```

You can use the `to_timestamp(snowflake.get_epoch(<value>))` function to convert the epoch into a timestamp.  For example:

```sql
acctg=# SELECT to_timestamp(snowflake.get_epoch(136169504773242881));
        to_timestamp        
----------------------------
 2024-01-11 13:08:59.845-05
(1 row)
```

> [!NOTE] Node and counter in the upstream transcript
> In v2.6.1, bits 12–21 of `136169504773242881` encode node `0` and the low 12 bits encode count `1`. For this ID, `get_node()` returns `0`, `get_count()` returns `1`, and `format()` reports `"id": 0` and `"count": 1`. The upstream transcripts below show different values. [Pinned bit layout](https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/snowflake.c#L109-L122)

**`snowflake.get_count(snowflake int8)`** Returns the count part of the given Snowflake as `int4` value; count resets to `0` for each new millisecond. For example:

```sql
acctg=# SELECT snowflake.get_count(136169504773242881);
 get_count 
-----------
         3
(1 row)
```

**`snowflake.get_node(snowflake int8)`** Returns the node number encoded in the ID. It reflects the `snowflake.node` setting at allocation time. Decoding does not read the issuing host’s configuration file. The historical upstream transcript follows.

```sql
acctg=# SELECT * FROM snowflake.get_node(136169504773242881);
 get_node 
----------
        1
(1 row)
```

**`snowflake.format(snowflake int8)`** Returns a `jsonb` object of the given Snowflake in the form: `{"id": 1, "ts": "2023-10-16 17:57:26.361+00", "count": 0}`.  For example:

```sql
acctg=# SELECT * FROM snowflake.format(136169504773242881);
                          format                           
-----------------------------------------------------------
 {"id": 1, "ts": "2024-01-11 13:08:59.845-05", "count": 0}
(1 row)
```


---

[Upstream source](https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/snowflake_functions.md) · `9506e1bd5c1f` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
