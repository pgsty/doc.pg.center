---
title: Limits
linkTitle: Limits
description: Two of AgensGraph's limits come from the identity it gives every vertex and edge.
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/limits.html
upstream_source: agensgraph
upstream_modified: true
---


Two of AgensGraph's limits come from the identity it gives every vertex and edge. The rest
are PostgreSQL's, because a graph is a schema and a label is a table.

## Graph limits {#graph-limits}

Every vertex and edge carries an identity of type `graphid`, and its layout sets the two
limits a graph can reach. A `graphid` is a 64-bit unsigned integer split in two. The top 16
bits are the **label id**, and the low 48 bits are the **local id**, the row's serial number
within its label. An identity therefore prints as two numbers. `movie[3.7]` is label 3,
row 7.

| Limit | Value | Comes from |
| --- | --- | --- |
| Labels per graph | 65,535 | The 16-bit label id. Zero is reserved as the invalid label id, so the usable range is 1 to 65,535. |
| Rows per label | 281,474,976,710,655 | The 48-bit local id: 2<sup>48</sup> − 1. |
| Label name length | 63 bytes | PostgreSQL's identifier length. |

A graph itself has no separate limit: a graph is a schema, and PostgreSQL sets no limit on
schemas per database. A large number of graphs consumes relations, since every graph creates
a sequence and two root labels of its own.

Both halves of a `graphid` are range-checked. The constructor refuses either one out of
range:

```sql
SELECT graphid(65536, 1);
```

```
ERROR:  labid out of range: 65536
```

```sql
SELECT graphid(1, 281474976710656);
```

```
ERROR:  locid out of range: 281474976710656
```

The same two messages, without the offending value, come back when a `graphid` literal is
parsed: `SELECT '65536.1'::graphid` raises `labid out of range`.

The counters that hand out these numbers are ordinary sequences, so you can inspect them.
Each graph has one `ag_label_seq` for label ids and each label an `<label>_id_seq` for local
ids:

```sql
SELECT sequencename, max_value FROM pg_sequences
WHERE schemaname = 'moviekb' AND sequencename IN ('ag_label_seq', 'movie_id_seq');
```

```
 sequencename |    max_value    
--------------+-----------------
 ag_label_seq |           65535
 movie_id_seq | 281474976710655
```

`ag_label_seq` cycles, and label creation skips a number already in use, so dropping a label
frees its id for reuse. When no free id is left, creating a label fails:

```
ERROR:  no more new labels are available
```

Two labels arrive in every new graph: `ag_vertex` with label id 1 and `ag_edge` with label
id 2. They are the two roots every vertex and edge label inherits from. So 65,533 ids are
available to your own labels.

## A label name over 63 bytes is truncated {#a-label-name-over-63-bytes-is-truncated}

An identifier is 63 bytes. A longer label name is cut to 63 bytes with a notice. So **two
label names that share their first 63 bytes are one label**. The second `CREATE VLABEL`
sees the first:

```cypher
CREATE VLABEL a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_aaa;
CREATE VLABEL a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_bbb;
```

```
NOTICE:  identifier "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_aaa" will be truncated to "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes"
CREATE VLABEL
NOTICE:  identifier "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_bbb" will be truncated to "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes"
ERROR:  label "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes" already exists
```

This bites in a pattern, because a pattern creates a label it does not find and nothing
fails. Writing to the two names above puts both rows in the same label:

```cypher
CREATE (:a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_aaa {via:'aaa'});
CREATE (:a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_bbb {via:'bbb'});
MATCH (n) RETURN label(n) AS lab, n.via ORDER BY n.via;
```

```
                                lab                                |  via  
-------------------------------------------------------------------+-------
 "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes" | "aaa"
 "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes" | "bbb"
```

Keep a label name inside 63 bytes, and make the first 63 bytes distinct. The limit is in
bytes, not characters, so a name in a multi-byte script reaches it sooner.

## PostgreSQL limits a graph runs into {#postgresql-limits-a-graph-runs-into}

A label is a table, so a graph is subject to the same limits as the rest of the database.
These are the ones graph work reaches. PostgreSQL's
[Limits](https://www.postgresql.org/docs/18/limits.html) appendix has the full list.

| Limit | Value | What it means for a graph |
| --- | --- | --- |
| Relation size | 32 TB | One label's storage, at the default 8 kB block size. A label past this needs partitioning, or splitting into child labels. |
| Field size | 1 GB | The whole property map of one vertex or edge, since the properties are one `jsonb` field. Long values are compressed and moved out of line first. |
| Columns per relation | 1600 | Reached only by promoting properties to columns. A vertex label starts with two columns and an edge label with four. |
| Identifier length | 63 bytes | Label names, graph names, property-index names, and variable names. Property *keys* are not identifiers and are not limited by this. |
| Rows per table | Bounded by relation size | The 48-bit local id is far larger, so the storage limit is what you hit first. |
| Indexes per table | Unlimited | Property indexes on one label. |

> [!NOTE]
> Nothing limits how many properties one element may hold, or how deeply a property may nest,
> short of the 1 GB field size. Reading a property does have a cost that grows with the size of
> the map, because the whole map is fetched to reach one key. Promoting the key to a column,
> with [`ALTER VLABEL`](/agensgraph/reference/ddl/alter-label/), is the way out of that.

## See also {#see-also}

- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) — the storage
  layout these limits describe
- [Label inheritance](/agensgraph/concepts/label-inheritance/) — splitting one large label into several
- [Data definition](/agensgraph/reference/ddl/) — the statements that create labels and indexes
