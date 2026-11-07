---
title: GQL conformance
linkTitle: GQL conformance
description: AgensGraph implements part of ISO/IEC 39075:2024, Information technology — Database languages — GQL.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/gql-conformance.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph implements part of ISO/IEC 39075:2024, *Information technology — Database
languages — GQL*. This appendix is not a full statement of conformance. It covers the main
topics in as much detail as is reasonable and useful.

The tables below are keyed by subclause of the standard, because that is the unit the
standard itself uses to attach a conformance rule to a piece of syntax. Every row was
checked against a running 2.18 server. A row says **Yes** only when the syntax the subclause
defines was accepted and produced the result the subclause requires. It says **Partial** when
some of the subclause's syntax is accepted and the rest raises an error, and **No** when none
of it parses. Where the standard offers several spellings of the same idea, the comment says
which one AgensGraph takes.

Three general points hold across every row and are not repeated in each comment.

GQL is not a separate mode. A GQL statement and a Cypher statement go through the same
parser and may be mixed in one pipeline, so `LET` sits next to `WITH` and `INSERT` next to
`CREATE`. See [Cypher, GQL and SQL](/agensgraph/concepts/languages/).

A graph is a PostgreSQL schema and a label is a table. So the parts of the standard that
describe a catalog of directories, schemas and graph types have a PostgreSQL counterpart
rather than a GQL one. The working graph comes from the `graph_path` setting instead of a
`USE` clause, and privileges are PostgreSQL privileges. See [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/).

Errors carry a five-character SQLSTATE, not a GQLSTATUS. See [Error
codes](/agensgraph/appendix/error-codes/).

## Supported features {#supported-features}

These subclauses are wholly or partly implemented. A **Partial** comment names what is
missing, so that a reader porting standard GQL knows what to look for.

| Subclause | Name | Support | Comment |
| --- | --- | --- | --- |
| 8.1–8.4 | `<start transaction command>`, `<transaction characteristics>`, `<rollback command>`, `<commit command>` | Yes | PostgreSQL's own transaction statements answer these. `START TRANSACTION READ ONLY`, `COMMIT` and `ROLLBACK` all work. |
| 9.2 | `<procedure body>` | Partial | `NEXT` chains one statement onto the result of the previous one. `NEXT` cannot carry a `YIELD` clause, and the binding-variable definition block that 9.2 also allows does not exist — see 10.1–10.3 below. |
| 11.1 | `<graph expression>` | Partial | `CURRENT_GRAPH` and `CURRENT_PROPERTY_GRAPH` are accepted, in Cypher and in SQL. They are bare keywords: `current_graph()` is a syntax error. No other form of graph expression exists. |
| 12.4 | `<create graph statement>` | Partial | `CREATE GRAPH name` and `CREATE GRAPH IF NOT EXISTS name` work. The graph type the standard requires after the name (`ANY`, `LIKE`, or a graph type reference) is not accepted, nor is `OR REPLACE`, `PROPERTY GRAPH` or `AS COPY OF`. |
| 12.5 | `<drop graph statement>` | Partial | `DROP GRAPH name` and `DROP GRAPH IF EXISTS name` work, plus a non-standard `CASCADE`, which is needed because a new graph already contains `ag_vertex` and `ag_edge`. `DROP PROPERTY GRAPH` is a syntax error. |
| 13.1 | `<linear data-modifying statement>` | Yes | A statement composes read clauses and write clauses in one pipeline, and a write clause's changes are visible to a read clause after it. |
| 13.2 | `<insert statement>` | Yes | `INSERT` takes the same pattern as Cypher `CREATE` and is a synonym for it. |
| 13.3 | `<set statement>` | Partial | Property assignment works, including the non-standard `+=` merge form. The label-set assignment the subclause also defines does not exist: a vertex has exactly one label. |
| 13.4 | `<remove statement>` | Partial | `REMOVE n.prop` removes a property. `REMOVE n:Label` does not exist, for the same reason. |
| 13.5 | `<delete statement>` | Yes | `DELETE` and `DETACH DELETE`. Deleting a vertex that still has edges is refused unless `DETACH` is given. |
| 14.2 | `<composite query expression>` | Partial | `UNION`, `UNION ALL`, `EXCEPT` and `INTERSECT` compose two query statements. `OTHERWISE` is a syntax error. |
| 14.3 | `<linear query statement>` and `<simple query statement>` | Yes | A query is a sequence of the primitive query statements below, ending in a primitive result statement. |
| 14.4 | `<match statement>` | Partial | `MATCH` and `OPTIONAL MATCH` work. The braced form, `OPTIONAL { MATCH … MATCH … }`, is a syntax error. |
| 14.5 | `<call query statement>` | Partial | Both call forms work. See 15.2 and 15.3 for what each one requires. |
| 14.6 | `<filter statement>` | Yes | Both `FILTER expr` and `FILTER WHERE expr`. |
| 14.7 | `<let statement>` | Yes | Additive, row-wise, and able to lead a query. An aggregate in a `LET` expression is refused. |
| 14.8 | `<for statement>` | Partial | Iterating a list works, with `WITH OFFSET AS name` giving a 0-based index. `WITH ORDINALITY` is a syntax error, and `FOR` cannot iterate a binding table. |
| 14.9 | `<order by and page statement>` | Yes | `ORDER BY`, `SKIP`, `OFFSET` and `LIMIT` are statements in their own right and can sit anywhere in a pipeline. Like the standard, AgensGraph does not let one *end* a query — 14.3 requires a primitive result statement last — so a query ending in `ORDER BY` raises `ERROR: Cypher query must end with RETURN, FINISH or update clause`. |
| 14.10 | `<primitive result statement>` | Yes | `RETURN`, `RETURN … ORDER BY …`, and `FINISH`. |
| 14.11 | `<return statement>` | Partial | `RETURN`, `RETURN DISTINCT`, `RETURN ALL`, `RETURN *` and explicit aliases. `RETURN NO BINDINGS` is a syntax error. Grouping is implicit — see 16.15. |
| 15.1 | `<call procedure statement>` and `<procedure call>` | Yes | `CALL` and `OPTIONAL CALL`, over either call form. |
| 15.2 | `<inline procedure call>` | Partial | `CALL (v) { … }`, `CALL () { … }`, `CALL (*) { … }` and `CALL { WITH v … }` all import correctly. A bare `CALL { … }` deviates: Syntax Rule 3 says an absent variable scope clause is rewritten to one naming *every* field of the incoming working record, so under the standard it imports everything, as `CALL (*) { … }` does. AgensGraph imports nothing instead, and raises no error, so the query answers a different question than it appears to — always write an import list. Write clauses in the subquery body are refused, and `IN TRANSACTIONS` does not exist. |
| 15.3 | `<named procedure call>` | Partial | `CALL routine(args) YIELD item [AS alias]` and `YIELD *` work, correlated when an argument references a variable already in scope. `YIELD` is mandatory, where the subclause makes it optional, and the clause can neither lead nor end a query. The name resolves to a PostgreSQL function, not to a procedure of the catalog 17.5 describes: a stock server registers no procedures, and calling one raises `<name>() is a procedure`. |
| 16.3 | `<graph pattern binding table>` | Partial | A graph pattern produces a binding table. The pattern `YIELD` clause the subclause also allows is a syntax error. |
| 16.4 | `<graph pattern>` | Partial | Comma-separated path patterns work. The match modes (`DIFFERENT EDGES`, `REPEATABLE ELEMENTS`) and the `KEEP` clause are syntax errors. |
| 16.5 | `<insert graph pattern>` | Yes | The pattern after `INSERT` or `CREATE` may create vertices, edges, or edges between vertices already bound. |
| 16.7 | `<path pattern expression>` | Partial | Concatenation works. Path multiset alternation and path pattern union — two path patterns separated by `\|` — are syntax errors. |
| 16.8 | `<label expression>` | Partial | A single label name only. Disjunction (`:a\|b`), conjunction (`:a&b`), negation (`:!a`) and the wildcard (`:%`) are all syntax errors. Test a label with the `label()` function in `WHERE` instead. |
| 16.9 | `<path variable reference>` | Yes | `MATCH p = (…)` binds the whole path, and `nodes()`, `relationships()` and `length()` read it. |
| 16.10 | `<element variable reference>` | Yes | A pattern variable is in scope for every clause after it. |
| 16.11 | `<graph pattern quantifier>` | Partial | The edge quantifier `-[r*1..3]->` walks a variable number of hops. The standard's quantifier on a parenthesized path pattern, `(…)->{1,3}`, is a syntax error, and so is `+` in place of `*`. |
| 16.13 | `<where clause>` | Partial | `WHERE` after a `MATCH`, and inside `FILTER`, `WITH` and a list comprehension. `WHERE` inside a node pattern is a syntax error. A search condition must be a boolean; a property read is not coerced. |
| 16.16 | `<order by clause>` | Yes | Multiple sort keys, `ASC`/`DESC`, `NULLS FIRST`/`NULLS LAST`, expressions as sort keys, and a `RETURN` alias as a sort key. |
| 16.17 | `<sort specification list>` | Yes | As 16.16. An integer sort key is a constant, not an output-column number — see [Cypher compatibility](/agensgraph/appendix/cypher-compatibility/). |
| 16.18 | `<limit clause>` | Yes | `LIMIT`, including an expression as the count. |
| 16.19 | `<offset clause>` | Yes | Both spellings the subclause defines, `OFFSET` and `SKIP`. |
| 19.1 | `<search condition>` | Yes | A condition takes a boolean and nothing else, which is what the subclause requires. |
| 19.2 | `<predicate>` | Partial | The four predicates below. The nine others 19.6–19.13 defines are not supported. |
| 19.3 | `<comparison predicate>` | Yes | `=`, `<>`, `<`, `<=`, `>`, `>=`, over scalars, graph elements and lists. |
| 19.4 | `<exists predicate>` | Partial | Four of the five forms the subclause defines: `EXISTS { pattern }` (with an optional `WHERE`), `EXISTS ( pattern )` (without one — a `WHERE` inside the parentheses is a syntax error), `EXISTS { MATCH … }`, and `EXISTS { <read statement> }`. `EXISTS ( MATCH … )` is a syntax error, and a match statement block of more than one `MATCH` needs a `RETURN` to parse, so Feature GQ22 is not met. |
| 19.5 | `<null predicate>` | Yes | `IS NULL` and `IS NOT NULL`. |
| 20.1 | `<value expression>` | Yes | Operators, function calls, `CASE`, subquery expressions and constructors compose freely. |
| 20.2 | `<value expression primary>` | Yes | Literals, variables, property references, parenthesized expressions. |
| 20.3 | `<value specification>` | Partial | `SESSION_USER` and `CURRENT_USER`. A parameter is a PostgreSQL parameter, `$1`, supplied by the driver rather than by a GQL general-parameter declaration. |
| 20.6 | `<value query expression>` | Yes | `VALUE { … }`, which is all this subclause defines: the body's single value, in its own type, and null when the body is empty. Syntax Rule 10 requires the body to carry `LIMIT 1` or an aggregate; AgensGraph accepts any body and raises `more than one row returned by a subquery used as an expression` at run time instead. `EXISTS { }` is 19.4; `COUNT { }`, `COLLECT { }`, `ARRAY { }` and `x IN { }` are extensions — see below. |
| 20.7 | `<case expression>` | Yes | Both the searched and the simple form, plus `NULLIF` and `COALESCE`. |
| 20.8 | `<cast specification>` | Partial | The `::` operator casts, and it accepts a keyword type name (`::int`, `::numeric`, `::interval`). `CAST(x AS t)` is a syntax error in Cypher; it works in SQL. |
| 20.9 | `<aggregate function>` | Partial | `COUNT(*)`, and the general set functions `AVG`, `COUNT`, `MAX`, `MIN`, `SUM`, `STDDEV_SAMP` and `STDDEV_POP`, each accepting `DISTINCT` or `ALL`. `MIN` and `MAX` over a vertex or edge are ambiguous and must be given a cast or an identity. `COLLECT_LIST` is spelled `collect`. The binary set functions `PERCENTILE_CONT` and `PERCENTILE_DISC` are unreachable from Cypher: both need `WITHIN GROUP`, which is a syntax error there. |
| 20.11 | `<property reference>` | Yes | `n.prop`, nested as `n.a.b`, and subscripted as `n.list[0]`. |
| 20.12 | `<binding variable reference>` | Yes | Names bound by a pattern, `WITH`, `LET`, `FOR` or `YIELD`. |
| 20.13 | `<path value expression>` | Partial | A path bound by `MATCH p = (…)` is a first-class value of type `graphpath`. |
| 20.15 | `<list value expression>` | Partial | `[a, b, c]`, subscripting, `IN`, and list comprehensions. `LIST[…]` is a syntax error. |
| 20.17 | `<list value constructor>` | Partial | As 20.15. |
| 20.18 | `<record constructor>` | Partial | `{a: 1, b: 2}` builds a map, and `.a` reads a field back. The `RECORD { … }` spelling is a syntax error. |
| 20.19 | `<field>` | Yes | Field access on a map, `({a: 1}).a`. |
| 20.20 | `<boolean value expression>` | Yes | `AND`, `OR`, `NOT`, `XOR`, and `IS [NOT] UNKNOWN`. |
| 20.21 | `<numeric value expression>` | Yes | `+`, `-`, `*`, `/`, `%`, `^`. |
| 20.22 | `<numeric value function>` | Yes | `abs`, `ceil`, `floor`, `round`, `sign`, `sqrt`, `exp`, `ln`, `log`, `log10`, `power`, `mod`, `pi`, the trigonometric functions, `degrees`, `radians`, `char_length`, `octet_length` and `rand`. |
| 20.23 | `<string value expression>` | Yes | Concatenation with `\|\|`, and with `+`. |
| 20.24 | `<character string function>` | Partial | `upper`, `lower`, `btrim`, `ltrim`, `rtrim`, `trim`, `substring(s, from, count)`, `left`, `right`, `replace`, `reverse`, `split`. `NORMALIZE` and the `SUBSTRING(s FROM a FOR b)` spelling are syntax errors in Cypher. |
| 20.26 | `<datetime value expression>` | Partial | Date and timestamp arithmetic through PostgreSQL's types. |
| 20.27 | `<datetime value function>` | Partial | `CURRENT_DATE`, `CURRENT_TIME`, `CURRENT_TIMESTAMP`, `LOCALTIME`, `LOCALTIMESTAMP`. The underscored spellings the standard uses, such as `LOCAL_TIME`, are not recognized. |
| 21.1 | Names and variables | Partial | An unquoted identifier folds to lower case; a double-quoted identifier keeps its case. The standard's backtick-delimited identifier is a syntax error. |
| 21.2 | `<literal>` | Partial | Integers including hexadecimal, octal, binary and underscore-separated forms; floats; strings; `true`, `false` and `null`; lists; maps. The typed literals — `DATE '…'`, `DURATION '…'`, byte strings — are syntax errors, as is `UNKNOWN` used as a value. |
| 21.3 | `<token>`, `<separator>`, and `<identifier>` | Partial | `--` and `/* */` delimit comments, as the standard requires. This makes the openCypher anonymous arrows `-->` and `--` unusable — see [Cypher compatibility](/agensgraph/appendix/cypher-compatibility/). |

## Features not supported {#features-not-supported}

None of the syntax these subclauses define is accepted. The comment gives the AgensGraph
route to the same result where there is one.

| Subclause | Name | Support | Comment |
| --- | --- | --- | --- |
| 7.1 | `<session set command>` | No | `SESSION SET` is a syntax error. Set the working graph with `SET graph_path = name`, which is a PostgreSQL setting and follows PostgreSQL's session and transaction scoping. |
| 7.2 | `<session reset command>` | No | Use `RESET graph_path` or `RESET ALL`. |
| 7.3 | `<session close command>` | No | Close the connection. |
| 7.4 | `<session parameter specification>` | No | None. |
| 10.1 | `<graph variable definition>` | No | None. A query addresses one graph, named by `graph_path`. |
| 10.2 | `<binding table variable definition>` | No | A `WITH` or `LET` binding, or a SQL common table expression around the Cypher, carries an intermediate result forward. |
| 10.3 | `<value variable definition>` | No | Use `LET`, which is 14.7 and is supported. |
| 11.2 | `<binding table expression>` | No | None. |
| 11.3 | `<object expression primary>` | No | None. |
| 12.1 | `<linear catalog-modifying statement>` | No | Catalog changes are PostgreSQL DDL statements and are not composable into a query pipeline. |
| 12.2 | `<create schema statement>` | No | A graph *is* a schema; `CREATE GRAPH` creates it. SQL `CREATE SCHEMA` also exists but does not make a graph. |
| 12.3 | `<drop schema statement>` | No | `DROP GRAPH`. |
| 12.6 | `<create graph type statement>` | No | None. A label is untyped, except for a property promoted to a column, which acquires that column's type. See [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/). |
| 12.7 | `<drop graph type statement>` | No | None. |
| 12.8 | `<call catalog-modifying procedure statement>` | No | None. |
| 13.6 | `<call data-modifying procedure statement>` | No | A write clause inside a `CALL` body is refused. |
| 14.1 | `<composite query statement>` | No | The optional `USE` prefix a composite query statement carries has no counterpart; the composite query expression itself, 14.2, is supported. |
| 14.12 | `<select statement>` | No | `SELECT … FROM MATCH (…)` is a syntax error. SQL `SELECT` over a Cypher subquery does the same job: see [SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/). |
| 16.1 | `<at schema clause>` | No | A statement runs in the database it is connected to. |
| 16.2 | `<use graph clause>` | No | `SET graph_path = name`. |
| 16.6 | `<path pattern prefix>` | No | Neither the path modes (`WALK`, `TRAIL`, `SIMPLE`, `ACYCLIC`) nor the path search prefixes (`ALL`, `ANY`, `ANY SHORTEST`, `ALL SHORTEST`, `SHORTEST k`, `SHORTEST k GROUPS`) parse. `shortestpath()`, `allshortestpaths()` and `dijkstra()` cover shortest-path search. |
| 16.12 | `<simplified path pattern expression>` | No | The `-/ … /->` form is a syntax error. |
| 16.15 | `<group by clause>` | No | An explicit `GROUP BY` is a syntax error in Cypher. Grouping is implicit: the non-aggregated items of a `RETURN` or `WITH` are the grouping keys. SQL `GROUP BY` is available in SQL. |
| 17.1–17.8 | `<schema reference>` and the other object references | No | An object is named by a PostgreSQL schema-qualified name. The standard's directory paths, `/dir/schema/graph`, do not parse. |
| 18.1–18.10 | `<nested graph type specification>` and the other type elements | No | None. |
| 19.6 | `<value type predicate>` | No | `IS TYPED` and `IS ::` are syntax errors. Cast and compare, or use `pg_typeof`. |
| 19.7 | `<normalized predicate>` | No | None. |
| 19.8 | `<directed predicate>` | No | Every edge is directed. |
| 19.9 | `<labeled predicate>` | No | `IS LABELED` is a syntax error, and so is `n:Label` in an expression. Write `label(n) = 'person'`. |
| 19.10 | `<source/destination predicate>` | No | `IS SOURCE OF` and `IS DESTINATION OF` are syntax errors. Compare identities: `id(a) = id(startNode(r))`. |
| 19.11 | `<all_different predicate>` | No | Compare identities pairwise. |
| 19.12 | `<same predicate>` | No | `id(a) = id(b)`. |
| 19.13 | `<property_exists predicate>` | No | `PROPERTY_EXISTS(n, key)` is a syntax error. Write `exists(n.key)`. |
| 20.4 | `<dynamic parameter specification>` | No | The driver's parameter placeholder, `$1`, takes its place. |
| 20.5 | `<let value expression>` | No | `LET … IN` inside an expression is a syntax error. The `LET` statement, 14.7, is supported. |
| 20.10 | `<element_id function>` | No | `element_id()` does not exist. `id()` returns the identity, as a `graphid`. |
| 20.14 | `<path value constructor>` | No | A path comes from a pattern, not from a constructor. |
| 20.16 | `<list value function>` | No | `trim(list, n)` and `elements()` do not exist. `head`, `last`, `tail`, `size` and `cardinality` do. |
| 20.25 | `<byte string function>` | No | PostgreSQL's `bytea` functions are reachable from SQL. |
| 20.28 | `<duration value expression>` | No | PostgreSQL's `interval` type covers durations, but only from SQL: `INTERVAL '1 day'` is a syntax error in Cypher. |
| 20.29 | `<duration value function>` | No | `duration()` does not exist. |
| 21.4 | `<GQL terminal character>` | No | The lexer is PostgreSQL's, extended for Cypher; it does not implement the standard's character set rules. |
| 22.1–22.20 | Additional common rules | No | These subclauses define the standard's evaluation machinery rather than syntax. AgensGraph evaluates a query through the PostgreSQL planner and executor, so they are not implemented as written. |
| 23.1 | GQLSTATUS | No | An error carries a SQLSTATE. See [Error codes](/agensgraph/appendix/error-codes/). |
| 23.2 | Diagnostic records | No | Diagnostics come from PostgreSQL's error report fields. |

## Extensions beyond the standard {#extensions-beyond-the-standard}

AgensGraph accepts a good deal that ISO/IEC 39075 does not define. Some of it is openCypher,
which the product supported first. Some of it exists because a graph here is stored in
PostgreSQL and both halves are addressable.

| Extension | What it adds |
| --- | --- |
| A SQL statement over a Cypher subquery, and Cypher over a label table | A Cypher query is a table expression and a label is a table, so one statement can join graph and relational data. See [SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/). |
| `LOAD FROM table AS r CREATE (…)` | Creates graph elements from the rows of a relation, including a foreign table. See [Loading data](/agensgraph/guides/loading-data/). |
| Label inheritance | `CREATE VLABEL child INHERITS (parent)` makes a hierarchy of labels, and a match on the parent also returns the children. `MATCH (n:parent ONLY)` restricts the match to the parent. See [Label inheritance](/agensgraph/concepts/label-inheritance/). |
| `SET n += map` | Merges a map into the properties instead of replacing them. |
| `dijkstra()`, `shortestpath()`, `allshortestpaths()` | Weighted and unweighted shortest-path search, in place of the standard's path search prefixes. |
| Promoted properties | `ALTER VLABEL movie ADD COLUMN year int GENERATED` gives a property a typed, indexable column, and a property read resolves to it. See [`ALTER VLABEL`](/agensgraph/reference/ddl/alter-label/). |
| Graph DDL | `CREATE VLABEL`, `CREATE ELABEL`, `CREATE PROPERTY INDEX`, `CREATE CONSTRAINT`, `REINDEX VLABEL` and `ALTER VLABEL`. See [Data definition](/agensgraph/reference/ddl/). |
| openCypher clauses | `UNWIND`, `MERGE` with `ON CREATE` and `ON MATCH`, and `WITH`. |
| `COUNT { }`, `COLLECT { }`, `ARRAY { }`, `x IN { }` | Four subquery value expressions the standard has no form for — 20.9 defines only `COUNT(*)`, `COUNT(expr)` and the `COLLECT_LIST` aggregate over rows. `COUNT { }` and `COLLECT { }` come from openCypher, `ARRAY { }` from SQL's `ARRAY(subquery)`, and `x IN { }` from SQL's `IN (subquery)`. See [Subquery value expressions](/agensgraph/reference/clauses/subquery-expressions/). |
| openCypher operators and functions | `STARTS WITH`, `ENDS WITH`, `CONTAINS`, `=~`, list comprehensions, `all`/`any`/`none`/`single`, `keys`, `properties`, `id`, `label`, `labels`, `type`, `startNode`, `endNode`, `nodes`, `relationships`, `length`, `range`, `head`, `last`, `tail`, `toString`, `toInteger`, `toFloat`. |
| PostgreSQL's whole surface | Every SQL type, function, index method, extension and setting is available to a graph query, which is how vector and full-text search work. See [vector search](/agensgraph/guides/search/vector/). |

## See also {#see-also}

- [Cypher, GQL and SQL](/agensgraph/concepts/languages/) — how the three languages relate in one
  statement
- [Cypher compatibility](/agensgraph/appendix/cypher-compatibility/) — where AgensGraph differs from other
  Cypher implementations
- [Keywords](/agensgraph/appendix/keywords/) — the words the standard's new statements reserved
- [AgensGraph 2.18.6.1 release notes](/agensgraph/release-notes/2.18/) — the GQL statements this
  release added
