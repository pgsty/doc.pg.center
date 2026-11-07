---
title: The agens client
linkTitle: The agens client
description: agens is the interactive terminal client.
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/agens.html
upstream_source: agensgraph
upstream_modified: true
---


`agens` is the interactive terminal client. It is PostgreSQL's `psql` under an AgensGraph
name, plus five meta-commands that describe a graph.

Because it is `psql`, [PostgreSQL's `psql` reference](https://www.postgresql.org/docs/18/app-psql.html)
documents every option, every variable and every other meta-command. None of that is
repeated here. This page covers two things: the graph meta-commands, which appear nowhere
else, and the two environment details that are AgensGraph's.

## The same program under two names {#the-same-program-under-two-names}

The build produces two binaries from the same source and installs both. The only difference
is branding: the name each one prints, and the bug-report and home-page lines in its help.

```shell
agens --version
psql --version
```

```
agens (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
psql (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
```

Diffing the two help texts shows the whole of the difference:

```shell
diff <(agens --help) <(psql --help)
```

```
1c1
< agens is the AgensGraph interactive terminal.
---
> psql is the PostgreSQL interactive terminal.
4c4
<   agens [OPTION]... [DBNAME [USERNAME]]
---
>   psql [OPTION]... [DBNAME [USERNAME]]
62,63c62,63
< Report bugs to <inquiry@skaiworldwide.com>.
< AgensGraph home page: <https://skaiworldwide.com/>
---
> Report bugs to <pgsql-bugs@lists.postgresql.org>.
> PostgreSQL home page: <https://www.postgresql.org/>
```

Two consequences follow, and both save work.

**Everything you know about `psql` applies.** The same options, the same `~/.psqlrc`, the same
`PG*` environment variables, the same `\copy`, `\watch`, `\gexec`, `\timing`, `\x`, `\pset`,
tab completion and variable interpolation.

```shell
agens -d docs -c "SHOW agversion;"
```

```
 agversion
------------
 2.18.6.1
```

**The graph meta-commands are in both binaries.** The two are built from the same objects, so
a `psql` from this installation lists graphs exactly as `agens` does. If you already have
`psql` on your path you do not need to switch clients to describe a graph.

The server tools follow the same pattern, with one pair renamed:

| AgensGraph name | PostgreSQL name | Difference |
| --- | --- | --- |
| `agens` | `psql` | Branding only. Both installed. |
| `ag_ctl` | `pg_ctl` | Branding only. Both installed. |

Every other tool keeps its PostgreSQL name and only that name. Those are `initdb`,
`postgres`, `pg_dump`, `pg_dumpall`, `pg_restore`, `pg_basebackup`, `pg_upgrade`,
`pg_controldata`, `pg_checksums`, `pg_rewind`, `pg_waldump`, `createdb`, `dropdb`,
`createuser`, `dropuser`, `vacuumdb`, `reindexdb`, `clusterdb`, `pgbench`, `ecpg` and the
rest. There is no `ag_dump` and no `ag_basebackup`. [Server-side
tools](/agensgraph/operations/tools/) covers what they do with a graph.

## Graph meta-commands {#graph-meta-commands}

Five meta-commands describe a graph. `+` adds columns to each, and a pattern narrows what is
listed.

| Command | Lists |
| --- | --- |
| `\dG[+] [PATTERN]` | Graphs. |
| `\dGl[+] [PATTERN]` | Labels, both kinds. |
| `\dGv[+] [PATTERN]` | Vertex labels, then a description of each. |
| `\dGe[+] [PATTERN]` | Edge labels, then a description of each. |
| `\dGi[+] [PATTERN]` | Property indexes. |

Case matters. `\dG` lists graphs. `\dg` is PostgreSQL's own command and lists roles.

These five are the complete set, and none of them appears in `\?`. The `x` and `S` modifiers
that other `\d` commands take are not accepted directly after `\dG`:

```psql
\dGx moviekb
```

```
invalid command \dGx
```

`x` does work on the four sub-commands, so `\dGvx` prints the list in expanded mode.

Every example below runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### List the graphs in a database {#list-the-graphs-in-a-database}

```psql
\dG moviekb
```

```
 List of graphs
  Name   | Owner
---------+-------
 moviekb | agens
```

`+` adds the graph's access privileges and its comment. A graph is a schema, so the privileges
are schema privileges. They are empty until something is granted, so grant one to see the
column filled in:

```sql
GRANT USAGE ON SCHEMA moviekb TO PUBLIC;
```

```psql
\dG+ moviekb
```

```
                  List of graphs
  Name   | Owner | Access privileges | Description
---------+-------+-------------------+-------------
 moviekb | agens | agens=UC/agens   +|
         |       | =U/agens          |
```

Revoke it again, so the example dataset is left as it was:

```sql
REVOKE USAGE ON SCHEMA moviekb FROM PUBLIC;
```

With no pattern, `\dG` lists every graph in the database.

### List a graph's labels {#list-a-graphs-labels}

`\dGl` lists both kinds together, ordered by graph, then kind, then name:

```psql
\dGl moviekb.*
```

```
            List of labels
  Graph  |    Name    |  Type  | Owner
---------+------------+--------+-------
 moviekb | acted_in   | edge   | agens
 moviekb | ag_edge    | edge   | agens
 moviekb | directed   | edge   | agens
 moviekb | related_to | edge   | agens
 moviekb | ag_vertex  | vertex | agens
 moviekb | movie      | vertex | agens
 moviekb | person     | vertex | agens
```

`ag_vertex` and `ag_edge` are there because every graph has them. See [Label
inheritance](/agensgraph/concepts/label-inheritance/).

`+` adds the label's on-disk size and its comment. The sizes are `pg_table_size` of the
label's table, so they reflect whatever you have loaded:

```psql
\dGl+ moviekb.*
```

```
                                     List of labels
  Graph  |    Name    |  Type  | Owner |    Size    |            Description
---------+------------+--------+-------+------------+------------------------------------
 moviekb | acted_in   | edge   | agens | 16 kB      |
 moviekb | ag_edge    | edge   | agens | 8192 bytes | base edge label of graph moviekb
 moviekb | directed   | edge   | agens | 16 kB      |
 moviekb | related_to | edge   | agens | 16 kB      |
 moviekb | ag_vertex  | vertex | agens | 8192 bytes | base vertex label of graph moviekb
 moviekb | movie      | vertex | agens | 16 kB      |
 moviekb | person     | vertex | agens | 16 kB      |
```

### Describe the vertex labels {#describe-the-vertex-labels}

`\dGv` narrows the list to vertex labels and then prints a block for each one, the way `\d`
prints a table's footers. The block carries the label's property indexes, its constraints, the
labels it inherits from and the labels that inherit from it:

```psql
\dGv moviekb.*
```

```
            List of labels
  Graph  |   Name    |  Type  | Owner
---------+-----------+--------+-------
 moviekb | ag_vertex | vertex | agens
 moviekb | movie     | vertex | agens
 moviekb | person    | vertex | agens

Vertex label "moviekb.ag_vertex"
--
Child labels: moviekb.movie,
              moviekb.person

Vertex label "moviekb.movie"
--
Inherits: moviekb.ag_vertex

Vertex label "moviekb.person"
--
Inherits: moviekb.ag_vertex
```

A label with an index and a constraint shows both:

```cypher
CREATE GRAPH demo;
SET graph_path = demo;
CREATE VLABEL book;
CREATE PROPERTY INDEX ON book (title);
CREATE CONSTRAINT book_isbn_uq ON book ASSERT isbn IS UNIQUE;
```

```psql
\dGv demo.book
```

```
        List of labels
 Graph | Name |  Type  | Owner
-------+------+--------+-------
 demo  | book | vertex | agens

Vertex label "demo.book"
--
Property Indexes:
    "book_title_idx" btree (title)
Constraints:
    "book_isbn_uq" ASSERT (isbn) IS UNIQUE
Inherits: demo.ag_vertex
```

Note what the block does **not** show: the label's columns. To see `id`, `properties` and
any promoted column, use `\d` on the table, since a label is a table:

```psql
\d moviekb.movie
```

```
                                                          Table "moviekb.movie"
   Column   |  Type   | Collation | Nullable |                                          Default
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('moviekb.movie'::cstring), nextval('moviekb.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
Inherits: moviekb.ag_vertex
```

### Describe the edge labels {#describe-the-edge-labels}

`\dGe` is `\dGv` for edges, and its blocks have the same shape:

```psql
\dGe moviekb.acted_in
```

```
          List of labels
  Graph  |   Name   | Type | Owner
---------+----------+------+-------
 moviekb | acted_in | edge | agens

Edge label "moviekb.acted_in"
--
Inherits: moviekb.ag_edge
```

`\dGl` is the one that does not print these blocks. It is the summary of both kinds, and
nothing more.

### List the property indexes {#list-the-property-indexes}

`\dGi` reads `ag_property_indexes` and shows each index's Cypher definition, the one you
would type to recreate it. A graph with no property indexes lists nothing:

```psql
\dGi moviekb.*
```

```
No matching property indexes found.
```

```psql
\dGi demo.*
```

```
                                                List of property indexes
 Graph | LabelName |   IndexName    | Unique | Owner |                             Indexdef
-------+-----------+----------------+--------+-------+------------------------------------------------------------------
 demo  | book      | book_title_idx | f      | agens | CREATE PROPERTY INDEX book_title_idx ON book USING btree (title)
```

`+` adds the index's size and its comment:

```psql
\dGi+ demo.*
```

```
                                                             List of property indexes
 Graph | LabelName |   IndexName    | Unique | Owner |                             Indexdef                             |    Size    | Description
-------+-----------+----------------+--------+-------+------------------------------------------------------------------+------------+-------------
 demo  | book      | book_title_idx | f      | agens | CREATE PROPERTY INDEX book_title_idx ON book USING btree (title) | 8192 bytes |
```

A uniqueness constraint is not a property index and does not appear here. It shows up in the
`\dGv` or `\dGe` block for its label, and as an exclusion constraint in `\d`.

```psql
DROP GRAPH demo CASCADE;
```

```
NOTICE:  drop cascades to 4 other objects
DETAIL:  drop cascades to sequence demo.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
drop cascades to vlabel book
DROP GRAPH
```

### Narrow a listing with a pattern {#narrow-a-listing-with-a-pattern}

The pattern is PostgreSQL's `\d` pattern language, applied to two name parts separated by a
dot. That language has `*` and `?` wildcards, character classes, and double quotes to defeat
case folding.

Which two parts differ by command, and the difference catches people:

| Command | *first*`.`*second* means |
| --- | --- |
| `\dG` | The graph name. There is no second part. |
| `\dGl`, `\dGv`, `\dGe` | Graph, then **label** name. |
| `\dGi` | Graph, then **index** name. |

So `\dGi moviekb.movie` finds nothing, because `movie` is matched against index names:

```psql
\dGi moviekb.movie
```

```
No matching property indexes found.
```

Name the index instead, or use `moviekb.*` and read the `LabelName` column. A pattern that
matches nothing says so, and it is not an error:

```psql
\dGv nosuchgraph.*
```

```
No matching labels found.
```

## AGDATA {#agdata}

`AGDATA` names a data directory, the way `PGDATA` does. Exactly three programs read it:
`initdb`, `pg_ctl` and `ag_ctl`. No other tool does, not `agens`, not `psql`, not `pg_dump`
and not `pg_basebackup`. So `PGDATA` is still the variable to set if you want one that
everything honours.

Export it once and the three of them stop needing `-D`:

```shell
export AGDATA=/tmp/agensdata
ag_ctl status
```

```
ag_ctl: no server running
```

The precedence differs between the two programs that read both, so check it before you set
both:

| Program | Order |
| --- | --- |
| `initdb` | `-D`, then `AGDATA`, then `PGDATA`. |
| `pg_ctl` and `ag_ctl` | `-D`, then `PGDATA`, then `AGDATA`. |

`initdb` also sets `AGDATA` in its own environment once it has decided, and its closing hint
names `ag_ctl`:

```shell
env -u PGDATA AGDATA=/tmp/agensdata initdb -U agens --no-sync
```

```
Success. You can now start the database server using:

    ag_ctl -D /tmp/agensdata -l logfile start
```

With neither variable set and no `-D`, the message names `PGDATA` only. `AGDATA` would have
worked just as well:

```shell
ag_ctl status
```

```
ag_ctl: no database directory specified and environment variable PGDATA unset
Try "ag_ctl --help" for more information.
```

[Deployment](/agensgraph/operations/deployment/) covers where to put a data directory and how to
start a server from an init system.

## See also {#see-also}

- [Server-side tools](/agensgraph/operations/tools/) — `ag_ctl`, `pg_dump`, `pg_upgrade` and a graph
- [The example dataset](/agensgraph/get-started/example-dataset/) — the graph every listing above
  describes
- [System catalogs](/agensgraph/system-catalogs/catalogs/) — `ag_graph`, `ag_label` and
  `ag_property_indexes`, which these commands query
- [Server settings](/agensgraph/reference/guc/) — `graph_path`, which a session needs before it can run Cypher
- [PostgreSQL: psql](https://www.postgresql.org/docs/18/app-psql.html) — every option and
  every other meta-command
- [PostgreSQL: pg_ctl](https://www.postgresql.org/docs/18/app-pg-ctl.html) — what `ag_ctl` is
