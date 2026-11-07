---
title: Drivers and client libraries
linkTitle: Drivers and client libraries
description: Connect through PostgreSQL drivers, the Python driver, and AI integration packages.
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/drivers/index.html
upstream_source: agensgraph
upstream_modified: true
cascade:
  type: docs
no_list: true
---


- [AI and LLM integrations](/agensgraph/drivers/ai-integrations/)

AgensGraph speaks the PostgreSQL wire protocol, so **any PostgreSQL driver connects to it and can run Cypher** — a Cypher statement is just a statement as far as the protocol is concerned. You do not need a graph-specific client to use AgensGraph.

What a driver cannot do without help is decode the graph types. A query that returns `m.title` hands back `jsonb`, which every driver understands; a query that returns `m` hands back a `vertex`, and `p` from a path pattern hands back a `graphpath`. A stock driver sees those as text. A driver written for AgensGraph adds the type handling, so a vertex arrives as an object with its label, id and properties.

That gives you two ways to work:

**Use the PostgreSQL driver you already have.** Return properties rather than whole elements, and wrap the Cypher in SQL where you want plain scalars instead of `jsonb` — see [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/). This is the least code and the fewest dependencies, and in any language other than Python it is the route to take.

**Use the Python driver** when you want vertices, edges and paths as native objects, or when you are building on one of the AI integrations.

## The Python driver {#the-python-driver}

[AgensGraph for Python](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/python/) is the driver to build on. It adds the graph type handling on top of psycopg 3, and it is what every one of the [AI integrations](/agensgraph/drivers/ai-integrations/) runs on. Its manual has installation and usage.

LangChain, LlamaIndex, LightRAG, cognee and the MCP servers all sit on that driver. See [AI and LLM integrations](/agensgraph/drivers/ai-integrations/).

## Other languages {#other-languages}

For Java, Node.js and Go, use a stock PostgreSQL driver — pgjdbc, node-postgres or pgx — and read properties rather than whole elements, as above. That is the combination to build on today.

Drivers for those three languages do exist, and each is kept here for the projects already using it rather than as a starting point:

- [Java / JDBC](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/jdbc/) **legacy** — a fork of pgjdbc, published as `net.bitnine:agensgraph-jdbc:1.4.3` in January 2023.
- [Node.js](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/nodejs/) **legacy** — wraps node-postgres, against `pg >= 6.1.2`. Published as `@skaiworldwide/ag-driver` 1.1.0 in September 2025.
- [Go](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/go/) **legacy** — built on `lib/pq`, distributed as a Go module at tag `v0.1.1`.

## Connection and parameters {#connection-and-parameters}

**Set** `graph_path` **on the connection.** It is per-session, so a pooled connection needs it set each time it is handed out — or set it once for the role or the database:

``` sql
ALTER ROLE appuser SET graph_path = moviekb;
```

The Python driver's `ConnectionPool` takes a `graph=` argument and sets it once on each connection it opens, not again on each handout, so a borrower that changes `graph_path` and commits passes the change on to the next borrower.

**Give Cypher parameters a type.** A parameter whose type the driver leaves unspecified is parsed as JSON, so a plain string fails:

```
ERROR:  invalid input syntax for type json
DETAIL:  Token "The" is invalid.
CONTEXT:  JSON data, line 1: The...
```

Either declare the parameter's type through the driver's API, or cast it in the statement:

```
MATCH (m:movie {title: $1::text}) RETURN m.year;
```

The cast is the portable form, and it costs nothing. It matters most where a value could be read either way: without a type, `'123'` arrives as the *number* 123 and stops matching a property holding the *string* `"123"`.

The Python driver declares the type for you. From version 2.0 it sends a Python `str` as `text`, so a string parameter needs no cast there. The cast is still needed where the statement wants another type from a string, such as `%s::date`.
