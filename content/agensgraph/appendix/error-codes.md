---
title: Error codes
linkTitle: Error codes
description: Every message the AgensGraph server produces carries a five-character SQLSTATE code, exactly as PostgreSQL
  does.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/error-codes.html
upstream_source: agensgraph
upstream_modified: true
---


Every message the AgensGraph server produces carries a five-character SQLSTATE code, exactly
as PostgreSQL does. The first two characters name the error *class*, and the last three the
specific condition within it. So an application that does not recognize a code can still act
on its class.

**AgensGraph defines no error codes of its own.** Its error-code list is byte-identical to
PostgreSQL 18's, and a graph statement that fails raises one of PostgreSQL's existing codes.
The complete list of codes, with the condition name PL/pgSQL uses for each, is PostgreSQL's
[Error Codes](https://www.postgresql.org/docs/18/errcodes-appendix.html) appendix. It is not
reproduced here.

For a client, the practical consequence is that a graph-specific failure cannot be
recognized by its code. `multiple types for relationship not supported` and `Cypher query
must end with RETURN, FINISH or update clause` arrive as `0A000` and `42601`. Those are the
same codes an unsupported SQL feature and a SQL syntax error use. Match on the message text
when you need to tell them apart, and treat the class as the reliable part.

## Reading a code {#reading-a-code}

Run `\set VERBOSITY verbose` in `psql` and every error afterwards carries its SQLSTATE and
the source location that raised it:

```psql
\set VERBOSITY verbose
```

```cypher
MATCH (m:movie {year: 1999}) WHERE m.title RETURN count(m);
```

```
ERROR:  42846: cannot cast "The Matrix" (jsonb type string) to boolean
LOCATION:  ExecEvalCypherTypeCast, execExprInterp.c:5900
```

Setting `VERBOSITY` to `sqlstate` prints the code alone. From a driver, the code is a field
of the error object: `sqlstate` in most PostgreSQL clients.

## Codes a graph statement commonly raises {#codes-a-graph-statement-commonly-raises}

These are the codes to expect from graph work, with a real message for each. The condition
name is the one PL/pgSQL and most drivers use.

| Code | Condition name | Raised by, for example |
| --- | --- | --- |
| `0A000` | `feature_not_supported` | `multiple types for relationship not supported` — a relationship pattern with more than one type. |
| `22023` | `invalid_parameter_value` | `labid out of range: 65536` — a `graphid` outside the range in [Limits](/agensgraph/appendix/limits/). |
| `3F000` | `invalid_schema_name` | `graph_path is NULL` — no working graph is set. A graph is a schema, which is why the class is this one. |
| `42601` | `syntax_error` | `Cypher query must end with RETURN, FINISH or update clause`, and every parse failure. |
| `42703` | `undefined_column` | `variable does not exist` — a name that is not in scope. |
| `42712` | `duplicate_alias` | `WITH passes on "t" more than once`, and the other name-collision refusals. |
| `42846` | `cannot_coerce` | `cannot cast "…" (jsonb type string) to boolean` — a condition given something other than a boolean. |
| `42P07` | `duplicate_table` | `label "movie" already exists` — a label is a table, so a duplicate label is a duplicate table. |
| `54000` | `program_limit_exceeded` | `no more new labels are available` — the label ids of a graph are exhausted. |
| `55000` | `object_not_in_prerequisite_state` | `Vertex with connected edges cannot be removed` — a `DELETE` that would leave a dangling edge. |

Three of those rows show the pattern to expect. A graph is a schema, a label is a table, and
a property is a `jsonb` value. So a graph error is reported in the class of the PostgreSQL
object it is really about.

## See also {#see-also}

- [Cypher compatibility](/agensgraph/appendix/cypher-compatibility/) — the errors a query ported from another
  Cypher hits, with their text
- [Limits](/agensgraph/appendix/limits/) — the two limits that produce `22023` and `54000`
- [Glossary](/agensgraph/appendix/glossary/) — the terms these messages use
