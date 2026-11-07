---
title: Keywords
linkTitle: Keywords
description: AgensGraph inherits PostgreSQL's keyword list and adds the words its graph statements need.
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/keywords.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph inherits PostgreSQL's keyword list and adds the words its graph statements need.
A keyword's category decides where the word can still be used as a name. An **unreserved**
word may name anything. A **reserved** word may not, and has to be double-quoted first.

PostgreSQL's [Key Words](https://www.postgresql.org/docs/18/sql-keywords-appendix.html)
appendix lists the inherited SQL words with their categories. This page covers only what
AgensGraph adds and changes. Two categories PostgreSQL uses, *type/function name* and
*column name*, have no AgensGraph entries. Every word below is either unreserved or fully
reserved.

Identifiers are quoted the SQL way, with double quotes. A backtick is a syntax error, so
`` `let` `` does not work as an escape — write `"let"`.

## Words AgensGraph adds {#words-agensgraph-adds}

These twenty-four words are in AgensGraph's keyword list and not in PostgreSQL 18's. The
comment names the clause or statement the word belongs to.

| Word | Category | Comment |
| --- | --- | --- |
| `allshortestpaths` | Unreserved | Path function: every shortest path between two vertices. |
| `assert` | Unreserved | `CREATE CONSTRAINT … ASSERT`. |
| `collect` | Unreserved | The `COLLECT { }` subquery expression. |
| `contains` | Unreserved | The `CONTAINS` string predicate. |
| `count` | Unreserved | The `COUNT { }` subquery expression. |
| `current_graph` | **Reserved** | The working graph, as a bare keyword. |
| `current_property_graph` | **Reserved** | Synonym for `CURRENT_GRAPH`. |
| `dijkstra` | Unreserved | Path function: weighted shortest path. |
| `elabel` | Unreserved | `CREATE ELABEL`, `ALTER ELABEL`, `DROP ELABEL`. |
| `ends` | Unreserved | The `ENDS WITH` string predicate. |
| `finish` | **Reserved** | The `FINISH` clause, which ends a query that projects nothing. |
| `graph` | Unreserved | `CREATE GRAPH`, `DROP GRAPH`, and the `graph_path` setting's statements. |
| `let` | **Reserved** | The `LET` clause. |
| `optional` | Unreserved | `OPTIONAL MATCH` and `OPTIONAL CALL`. |
| `property` | Unreserved | `CREATE PROPERTY INDEX`, `CURRENT_PROPERTY_GRAPH`. |
| `remove` | Unreserved | The `REMOVE` clause. |
| `shortestpath` | Unreserved | Path function: one shortest path. |
| `single` | Unreserved | The `single()` list predicate. |
| `size` | Unreserved | The `size()` function. |
| `starts` | Unreserved | The `STARTS WITH` string predicate. |
| `unwind` | **Reserved** | The `UNWIND` clause. |
| `vlabel` | Unreserved | `CREATE VLABEL`, `ALTER VLABEL`, `DROP VLABEL`. |
| `xor` | **Reserved** | The `XOR` boolean operator. |
| `yield` | Unreserved | `CALL … YIELD`. |

Four words AgensGraph inherits are reserved here and unreserved in PostgreSQL, because each
one leads a Cypher clause: `insert`, `match`, `merge` and `return`.

`CALL` was deliberately left unreserved, so `call` still names a column, table, alias, label,
property key or variable. Exactly two spellings change meaning, because the lexer treats
`CALL` specially when a `(` or a `{` follows it:

- `call(...)` — a function literally named `call`, invoked with arguments. Quote it:
  `"call"(1)`.
- `(call { ... })` — a node pattern whose variable is named `call` and which carries a
  property map but no label. Quote it: `("call" { ... })`.

## Words that became reserved in 2.18 {#words-that-became-reserved-in-218}

Six words are reserved in 2.18 and were not in 2.17: `insert`, `finish`, `let`, `xor`,
`current_graph` and `current_property_graph`. Reserving a word can break an application that
used it as a name, so each was made as narrow as the grammar allowed. The result is not
uniform. Some positions still work, and the table below is the measured outcome rather than
the general rule.

Each cell is the result of running the position against a 2.18 server. **Works** means the
unquoted word was accepted.

| Word | Label in a pattern | `CREATE VLABEL` | Variable | `RETURN … AS` alias | Alias as a sort key | Property key |
| --- | --- | --- | --- | --- | --- | --- |
| `insert` | Works | Fails | Works | Works | Works | Works |
| `finish` | Works | Fails | Fails | Works | Fails | Works |
| `let` | Fails | Fails | Fails | Works | Fails | Works |
| `xor` | Fails | Fails | Fails | Works | Fails | Works |
| `current_graph` | Fails | Fails | Fails | Works | Works | Works |
| `current_property_graph` | Fails | Fails | Fails | Works | Works | Works |

Two columns in that table read oddly, and both need stating in words.

For `insert` and `finish`, a label works in a pattern but not in the label DDL.
`CREATE (:insert)` and `MATCH (n:insert)` are accepted. `CREATE VLABEL insert` is not:

```cypher
CREATE VLABEL insert;
```

```
ERROR:  syntax error at or near "insert"
```

Create the label with a quoted name, `CREATE VLABEL "insert"`. The unquoted pattern
spelling still finds it afterwards, because an unquoted identifier folds to lower case.

An alias always works, but sorting by that alias does not always. `RETURN n.k AS let` is
accepted and the `ORDER BY let` after it is not:

```cypher
MATCH (n:t) RETURN n.k AS let ORDER BY let;
```

```
ERROR:  syntax error at or near "let"
```

`current_graph` and `current_property_graph` are the exception. An alias of either name
sorts.

Double-quoting the name fixes every failing cell, at both its definition and every use:

```cypher
MATCH (n:t) RETURN n.k AS "let" ORDER BY "let";
```

A property key never needs quoting. A key is a string inside a `jsonb` document, not an
identifier, so `CREATE (:t {let: 1})` and `RETURN n.let` are unaffected by any of this.

On the SQL side the same six words need quoting as column names. `CREATE TABLE t (xor int)`
is a syntax error. `CREATE TABLE t ("xor" int)` works.

## The reserved set is wider than the graph words {#the-reserved-set-is-wider-than-the-graph-words}

Reserving a word for a graph clause is only part of the picture. AgensGraph inherits
PostgreSQL's reserved words too. A Cypher label or variable is an identifier in the same
grammar, so any of them is refused unquoted. `both` is a good example: a PostgreSQL reserved
word with nothing to do with graphs:

```cypher
CREATE VLABEL both;
```

```
ERROR:  syntax error at or near "both"
```

The same is true of `all`, `and`, `any`, `array`, `as`, `case`, `cast`, `end`, `from`, `in`,
`not`, `null`, `or`, `select`, `table`, `to`, `union`, `when`, `where` and the rest of
PostgreSQL's reserved list. Before choosing a label, variable or property-index name, check
it against PostgreSQL's [Key
Words](https://www.postgresql.org/docs/18/sql-keywords-appendix.html) appendix, which gives
the category of every SQL word AgensGraph carries.

> [!NOTE]
> The keyword list is a single file in the AgensGraph source, one line
> per word with its category. Consult it when a name is refused and this page does not say why.

## See also {#see-also}

- [Syntax](/agensgraph/reference/syntax/) — the lexical rules, including identifier folding
- [Cypher compatibility](/agensgraph/appendix/cypher-compatibility/) — the other differences a ported query hits
- [Upgrading to 2.18](/agensgraph/release-notes/upgrade-to-2.18/) — the full pre-upgrade checklist
- [AgensGraph 2.18.6.1 release notes](/agensgraph/release-notes/2.18/) — the clauses these words serve
