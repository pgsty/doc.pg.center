---
title: Syntax
linkTitle: Syntax
description: 'The lexical layer every statement obeys, whichever language it is written in: the notation this reference
  uses for syntax, and the rules for identifiers, literals, operators, comments and null.'
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/syntax.html
upstream_source: agensgraph
upstream_modified: true
---


The lexical layer every statement obeys, whichever language it is written in: the notation
this reference uses for syntax, and the rules for identifiers, literals, operators, comments
and null.

Cypher, GQL and SQL share one parser, so these rules are the same in all three. Where a rule
differs between them, the difference is called out.

## Syntax conventions {#syntax-conventions}

Every synopsis in this reference is written the same way:

```text
MATCH pattern [, pattern ] ... [ WHERE condition ]
```

Nothing else in a synopsis is notation. A comma, a parenthesis or an arrow is part of the
statement, and you type it as shown.

**bold**
: A keyword. Type it as it appears; case does not matter.

*italic*
: A placeholder you supply. Each one is defined under *Parameters* on the same page.

`[ ]`
: The enclosed part is optional.

`{ ... | ... }`
: Braces around alternatives separated by a vertical bar: choose exactly one.

`...`
: The item before it may be repeated.

`[, ... ]`
: The item before it may be repeated, separated by commas.

Two or more synopsis lines
: Alternative forms of the same statement. Use one of them.

`where` *placeholder* `is one of:`
: Expands a placeholder that is too large to sit inline, on the lines that follow.

Brackets and braces are never literal. Some statements really do contain a bracket: a list
literal, a map, an edge pattern. For those, the synopsis says so in prose, or shows the
bracket in a different position, as in `-[` *variable* `]->`.

## Identifiers {#identifiers}

An identifier names a graph, a label, a variable, a property key, a column, an index or a
constraint.

### Case folding {#case-folding}

An unquoted identifier is folded to **lower case**, exactly as PostgreSQL folds an unquoted
SQL identifier. So `MOVIE`, `Movie` and `movie` all name the same label:

```cypher
MATCH (n:MOVIE {title: 'The Matrix'}) RETURN n.title AS title;
```

```
    title
--------------
 "The Matrix"
```

A double-quoted identifier is taken as written. `"MOVIE"` is a different name from `movie`.
No label is called `MOVIE`, so the pattern matches nothing rather than failing:

```cypher
MATCH (n:"MOVIE" {title: 'The Matrix'}) RETURN n.title AS title;
```

```
 title
-------
(0 rows)
```

Quoting works for variables too, and a quoted variable has to be quoted at every mention:

```cypher
MATCH ("Film":movie {title: 'The Matrix'}) RETURN "Film".title AS title;
```

```
    title
--------------
 "The Matrix"
```

Property keys fold the same way. `{MixedKey: 1}` stores the key `mixedkey`; `{"MixedKey": 1}`
stores `MixedKey`. The two are different keys and a vertex can carry both, so quote a key
consistently or not at all.

Backticks are not a quoting character. `` `movie` `` is a syntax error, not a quoted
identifier:

```cypher
MATCH (n:`movie`) RETURN n.title;
```

```
ERROR:  syntax error at or near "`"
LINE 1: MATCH (n:`movie`) RETURN n.title;
                 ^
```

### Characters {#characters}

An unquoted identifier starts with a letter or an underscore and continues with letters,
digits, underscores and dollar signs. "Letter" includes non-ASCII letters, so `café` is a
valid identifier. It may not start with a digit. `1abc` is read as a number with trailing
junk. A double-quoted identifier may contain any character except a null byte, and a double
quote inside one is written twice (`"say ""hi"""`).

The length limit is PostgreSQL's: 63 bytes, and a longer name is truncated to that. The
limit counts bytes, not characters, so a name of multi-byte letters runs out sooner.

### Reserved words {#reserved-words}

Some keywords are **reserved**: the grammar reads the word as a keyword and not as a name.
`both`, `let`, `finish`, `insert`, `offset` and `xor` are all reserved. Some are inherited
from PostgreSQL, some added for a graph clause. Which positions each one still
works in varies, so [Keywords](/agensgraph/appendix/keywords/) carries the position-by-position
table. A pattern variable is a position none of them survives:

```cypher
MATCH (both:movie {title: 'The Matrix'}) RETURN both.title;
```

```
ERROR:  syntax error at or near "both"
LINE 1: MATCH (both:movie {title: 'The Matrix'}) RETURN both.title;
               ^
```

Quoting lifts the restriction, because a quoted identifier is never read as a keyword:

```cypher
MATCH ("both":movie {title: 'The Matrix'}) RETURN "both".title AS title;
```

```
    title
--------------
 "The Matrix"
```

A reserved word is still allowed as a `RETURN` alias and as a property key, since neither
position can be confused with a keyword:

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS both;
```

```
     both
--------------
 "The Matrix"
```

## Literals {#literals}

### Strings {#strings}

A string literal is enclosed in **single** quotes. Double quotes make an identifier, not a
string, so `"plain"` is a variable reference and fails if no such variable is in scope.

A single quote inside a literal is written twice. Backslash escapes follow JSON's rules,
because a Cypher string becomes a `jsonb` string:

| Escape | Meaning |
| --- | --- |
| `''` | A single quote. |
| `\"` | A double quote. |
| `\\` | A backslash. |
| `\/` | A forward slash. |
| `\b` `\f` `\n` `\r` `\t` | Backspace, form feed, line feed, carriage return, tab. |
| `\u` followed by four hex digits | The character with that code point. |

Any other backslash sequence is rejected: `'a\qb'` raises `Escape sequence "\q" is invalid`.

```cypher
RETURN 'plain', 'it''s', 'a\tb', 'a\\tb', 'say \" hi';
```

```
 ?column? | ?column? | ?column? | ?column? |  ?column?
----------+----------+----------+----------+-------------
 "plain"  | "it's"   | "a\tb"   | "a\\tb"  | "say \" hi"
```

The output is the `jsonb` rendering of each value, which re-escapes what it prints: the third
column holds three characters, `a`, a tab and `b`.

### Numbers {#numbers}

A number literal is written as in SQL, and PostgreSQL's non-decimal and separated forms are
accepted: hexadecimal `0x`, octal `0o`, binary `0b`, and underscores as digit separators.

```cypher
RETURN 1, -1, 1.5, 1e3, 1E-3, 0x1F, 0o17, 0b101, 1_000;
```

```
 ?column? | ?column? | ?column? | ?column? | ?column? | ?column? | ?column? | ?column? | ?column?
----------+----------+----------+----------+----------+----------+----------+----------+----------
 1        | -1       | 1.5      | 1000     | 0.001    | 31       | 15       | 5        | 1000
```

A number written without a decimal point is a JSON integer, and dividing two of them
truncates: `7 / 2` is `3`. Write `7.0 / 2` for `3.5`.

### Booleans, null, lists and maps {#booleans-null-lists-and-maps}

`true`, `false` and `null` are keywords, in any case. A list is written in square brackets
and a map in braces. Both nest, and both may mix value types, because both become `jsonb`.

```cypher
RETURN true, false, null, [1, 'two', true, null], {a: 1, b: [2], c: {d: 3}};
```

```
 ?column? | ?column? | ?column? |        ?column?        |             ?column?
----------+----------+----------+------------------------+-----------------------------------
 t        | f        |          | [1, "two", true, null] | {"a": 1, "b": [2], "c": {"d": 3}}
```

A map key is an identifier and folds like one. `[]` and `{}` are the empty list and the empty
map. See [Data types](/agensgraph/reference/types/) for how a literal relates to the stored `jsonb` value.

## Operators {#operators}

### Precedence {#precedence}

Operators bind in this order, loosest first. Two operators on the same row have equal
precedence and associate as the row says.

| Precedence | Operators | Associativity |
| --- | --- | --- |
| 1 (loosest) | `UNION` `EXCEPT` | left |
| 2 | `INTERSECT` | left |
| 3 | `OR` `XOR` | left |
| 4 | `AND` | left |
| 5 | `NOT` | right |
| 6 | `IS NULL` `IS NOT NULL` `IS [NOT] UNKNOWN` | none |
| 7 | `<` `<=` `>` `>=` `=` `<>` `!=` | none |
| 8 | `IN` `BETWEEN` | none |
| 9 | any other operator, including `\|\|` and the `jsonb` operators | left |
| 10 | `+` `-` (binary) | left |
| 11 | `*` `/` `%` | left |
| 12 | `^` | left |
| 13 | `-` (unary) | right |
| 14 | `STARTS WITH` `ENDS WITH` `CONTAINS` `=~` | none |
| 15 | `[` `]` (subscript), `(` `)` (call) | left |
| 16 | `::` | left |
| 17 (tightest) | `.` | left |

The table lists the operators a Cypher expression can contain. SQL adds a few more at levels
of its own: `AT TIME ZONE`, `COLLATE`, `LIKE`, `ILIKE` and `SIMILAR TO`. Cypher's expression
grammar accepts none of them.

Three things in the table differ from a common expectation.

`^` is **left**-associative and binds looser than unary minus, which is PostgreSQL's rule
rather than arithmetic's. So `2 ^ 3 ^ 2` is `(2 ^ 3) ^ 2` and `-2 ^ 2` is `(-2) ^ 2`:

```cypher
RETURN 2 ^ 3 ^ 2 AS pow, -2 ^ 2 AS neg;
```

```
 pow | neg
-----+-----
 64  | 4
```

The string-matching operators bind **tighter** than everything except a subscript, a call, a
cast and a property read. They bind tighter than concatenation and tighter than arithmetic.
So the right-hand operand of `||` below is the whole `STARTS WITH` test, not just `'c'`:

```cypher
RETURN 'ab' || 'c' STARTS WITH 'a';
```

```
 ?column?
-----------
 "abfalse"
```

Parenthesise when you mean the other reading. `('ab' || 'c') STARTS WITH 'a'` is `true`.

Comparisons do not chain. `1 < 2 < 3` is a syntax error rather than two comparisons.

### Logical operators {#logical-operators}

`AND`, `OR`, `NOT` and `XOR` take booleans and return a boolean, over three values. See
[Null and three-valued logic](#null-and-three-valued-logic) for the truth tables. `XOR` is
AgensGraph's addition to SQL's set, and it sits at `OR`'s precedence.

### Comparison and predicates {#comparison-and-predicates}

`=`, `<>` (or `!=`), `<`, `<=`, `>` and `>=` compare two values. Comparing values of
different `jsonb` types does not fail. It orders them by `jsonb`'s own type order.

`IN` tests membership of a list. `IS NULL` and `IS NOT NULL` test any value for null without
comparing it. `IS UNKNOWN` and `IS NOT UNKNOWN` are the standard's spelling of that test on a
boolean, and are accepted here:

```cypher
RETURN 2 IN [1, 2, 3] AS present, null IS NULL AS nul, null IS UNKNOWN AS unk;
```

```
 present | nul | unk
---------+-----+-----
 t       | t   | t
```

### String matching {#string-matching}

Four operators match strings. `LIKE`, `ILIKE` and `SIMILAR TO` are **SQL only**. They are
not part of Cypher's expression grammar, and they are a syntax error there. PostgreSQL's
regular expression operators (`~`, `~*`, `!~`, `!~*`) do work in Cypher.

| Operator | Test |
| --- | --- |
| *string* `STARTS WITH` *prefix* | The string begins with the prefix. |
| *string* `ENDS WITH` *suffix* | The string ends with the suffix. |
| *string* `CONTAINS` *substring* | The substring occurs anywhere in the string. |
| *string* `=~` *pattern* | The whole string matches the POSIX regular expression. |

```cypher
RETURN 'Matrix' STARTS WITH 'Mat' AS sw, 'Matrix' ENDS WITH 'rix' AS ew,
       'Matrix' CONTAINS 'atr' AS c, 'Matrix' =~ '^M.*x$' AS re;
```

```
 sw | ew | c | re
----+----+---+----
 t  | t  | t | t
```

None of the four can be answered from an index. A predicate that has to be sargable needs
`=` or a range. [Data types](/agensgraph/reference/types/) covers the index-visible forms of a property.

### Arithmetic {#arithmetic}

`+`, `-`, `*`, `/`, `%` and `^` work on numbers, and unary `+` and `-` negate. On a property
they run against `jsonb` rather than a SQL numeric type, which gives `+` two extra jobs: it
concatenates two strings, and it appends to a list.

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born + 1 AS plus, p.born % 7 AS mod, -p.born AS neg,
       p.name + '!' AS concat, [1, 2] + 3 AS appended;
```

```
 plus | mod |  neg  |     concat      | appended
------+-----+-------+-----------------+-----------
 1965 | 4   | -1964 | "Keanu Reeves!" | [1, 2, 3]
```

`+` on two maps is refused, with `invalid expression: {"a": 1} + {"b": 2}`. Merge maps with
the `jsonb` concatenation operator instead:

```cypher
RETURN {a: 1} || {b: 2} AS merged;
```

```
      merged
------------------
 {"a": 1, "b": 2}
```

To merge into an element rather than into a value, use `SET n += ` *map*.

### jsonb operators {#jsonb-operators}

A property is `jsonb`, so PostgreSQL's `jsonb` operators apply to one directly. These are the
ones worth knowing:

| Operator | Result |
| --- | --- |
| *json* `->` *key* / *index* | The member as `jsonb`. |
| *json* `->>` *key* / *index* | The member as `text`. |
| *json* `#>` *path* | The value at a text-array path, as `jsonb`. |
| *json* `#>>` *path* | The value at a text-array path, as `text`. |
| *json* `?` *key* | Whether the key is present. |
| *json* `@>` *json* | Whether the left value contains the right. |
| *json* `<@` *json* | Whether the left value is contained in the right. |
| *json* `\|\|` *json* | Concatenation: two objects merge, other combinations make an array. |

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN properties(m) -> 'title' AS as_json, properties(m) ->> 'title' AS as_text,
       properties(m) ? 'genre' AS has_genre, properties(m) @> '{"genre": "Action"}' AS is_action;
```

```
   as_json    |   as_text    | has_genre | is_action
--------------+--------------+-----------+-----------
 "The Matrix" | "The Matrix" | t         | t
```

`->>` returned `text`, but a Cypher `RETURN` boxes a scalar column back to `jsonb`, so the
quotes are still there. To get a plain string out, wrap the query in SQL. See
[Data types](/agensgraph/reference/types/#what-a-return-hands-back).

Two rules govern the rest of PostgreSQL's `jsonb` operator set inside Cypher, and both follow
from Cypher owning the arithmetic spellings.

`-` between two `jsonb` values is subtraction, so `jsonb`'s key-deletion operator is not
reachable from Cypher: `properties(m) - 'plot'` raises `invalid expression`. Delete a key with
a SQL wrapper, or with `REMOVE`.

A bare string literal beside a native `jsonb` operator is parsed as a whole JSON document
rather than as a JSON string. So `m.title || '!'` fails on `Token "!" is invalid`. Give the
operator a typed operand, as in `m.title || to_jsonb('!'::text)`. Or use `+`, which takes the
Cypher reading.

## Comments {#comments}

A comment runs from `--` to the end of the line, or from `/*` to a matching `*/`. Block
comments nest, so a commented-out region containing a comment stays balanced. `//` is not a
comment and is a syntax error.

```cypher
MATCH (m:movie {title: 'The Matrix'})   -- one film
/* a block comment
   over two lines */
RETURN m.title AS title;
```

```
    title
--------------
 "The Matrix"
```

## Null and three-valued logic {#null-and-three-valued-logic}

`null` means *unknown*. It is not a value you can compare with, and it is not a property
value. Assigning null to a property removes it, unless
[`allow_null_properties`](/agensgraph/reference/guc/#allow_null_properties) is on.

### Truth tables {#truth-tables}

`AND`, `OR` and `XOR` extend to three values as follows. The table is the output of running
every combination:

```psql
SELECT a #>> '{}' AS a, b #>> '{}' AS b,
       andv::text AS "a AND b", orv::text AS "a OR b", xorv::text AS "a XOR b"
FROM (UNWIND [true, false, null] AS a
      UNWIND [true, false, null] AS b
      RETURN a, b, a AND b AS andv, a OR b AS orv, a XOR b AS xorv) q;
```

```
   a   |   b   | a AND b | a OR b | a XOR b
-------+-------+---------+--------+---------
 true  | true  | true    | true   | false
 true  | false | false   | true   | true
 true  | null  | null    | true   | null
 false | true  | false   | true   | true
 false | false | false   | false  | false
 false | null  | false   | null   | null
 null  | true  | null    | true   | null
 null  | false | false   | null   | null
 null  | null  | null    | null   | null
```

`NOT` maps true to false, false to true, and null to null:

```psql
SELECT a #>> '{}' AS a, notv::text AS "NOT a"
FROM (UNWIND [true, false, null] AS a RETURN a, NOT a AS notv) q;
```

```
   a   | NOT a
-------+-------
 true  | false
 false | true
 null  | null
```

So `AND` is false as soon as one side is false, and `OR` is true as soon as one side is true,
whatever the other side is. Everything else involving null is null.

`IN` follows from the same rule: a value not found in a list that contains null might still
have been there, so the answer is unknown rather than false.

```psql
SELECT expr, res::text AS result FROM (
  RETURN '2 IN [1, 2, 3]' AS expr, 2 IN [1,2,3] AS res
  UNION ALL RETURN '2 IN [1, null, 3]', 2 IN [1,null,3]
  UNION ALL RETURN '2 IN [1, 2, null]', 2 IN [1,2,null]
  UNION ALL RETURN '2 IN [1]', 2 IN [1]
  UNION ALL RETURN '2 IN []', 2 IN []
  UNION ALL RETURN 'null IN [1, 2, 3]', null IN [1,2,3]
  UNION ALL RETURN 'null IN [1, null, 3]', null IN [1,null,3]
  UNION ALL RETURN 'null IN []', null IN []
) q;
```

```
          expr          | result
------------------------+--------
 "2 IN [1, 2, 3]"       | true
 "2 IN [1, null, 3]"    | null
 "2 IN [1, 2, null]"    | true
 "2 IN [1]"             | false
 "2 IN []"              | false
 "null IN [1, 2, 3]"    | null
 "null IN [1, null, 3]" | null
 "null IN []"           | false
```

An empty list is the exception: nothing is in it, so the answer is false even for null.

### Expressions that yield null {#expressions-that-yield-null}

These are the expressions that produce null rather than an error or a value:

| Expression | Why |
| --- | --- |
| `n.no_such_property` | The element has no such property. |
| `[][0]`, `head([])` | The list has no such element. |
| `1 + null` | Arithmetic with an unknown operand. |
| `1 < null`, `null = null` | Comparison with an unknown value. |
| `sin(null)`, `toUpper(null)` | A function called with null. |

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN m.no_such_property AS missing_property, [][0] AS missing_element,
       head([]) AS head_of_empty, 1 + null AS arithmetic, 1 < null AS comparison,
       sin(null) AS function, null = null AS equality;
```

```
 missing_property | missing_element | head_of_empty | arithmetic | comparison | function | equality
------------------+-----------------+---------------+------------+------------+----------+----------
 null             | null            | null          | null       | null       | null     | null
```

`IS NULL` exists because `null = null` is null. It is the only way to test for null.

### A condition takes only a boolean {#a-condition-takes-only-a-boolean}

`WHERE`, `FILTER`, `CASE WHEN` and every other condition accept a boolean and nothing else. A
condition that evaluates to a `jsonb` string, number, list or map is an error:

```cypher
CREATE GRAPH demo;
SET graph_path = demo;
CREATE VLABEL t;
CREATE (:t {name: 'Jack'});
MATCH (n:t) WHERE n.name RETURN n.name;
```

```
ERROR:  cannot cast "Jack" (jsonb type string) to boolean
```

That error comes from evaluating the condition, so the value it names is whichever row the
executor reached first. A condition that is not `jsonb` at all is rejected earlier, when the
statement is parsed:

```cypher
MATCH (n:t) WHERE 1 RETURN n.name;
```

```
ERROR:  argument of WHERE must be type boolean, not type integer
LINE 1: MATCH (n:t) WHERE 1 RETURN n.name;
                          ^
```

Write the test you mean. `WHERE n.name IS NOT NULL` asks whether the property is there:

```cypher
MATCH (n:t) WHERE n.name IS NOT NULL RETURN n.name AS name;
```

```
  name
--------
 "Jack"
```

`WHERE n.name <> ''` asks whether it is non-empty, and `WHERE n.active` works when the
property really holds a boolean, because a `jsonb` boolean casts to one.

Null is still accepted, and behaves as it does in SQL: a row whose condition is null is not
returned, and nothing is raised. So `WHERE n.no_such_property` returns no rows.

> [!NOTE]
> This is a deliberate compatibility break with earlier releases, which accepted a non-empty
> value as a condition. A query written that way fails rather than filtering on something it
> did not mean.
> [Cypher compatibility](/agensgraph/appendix/cypher-compatibility/#a-condition-takes-only-a-boolean)
> lists what to change.

## Compatibility {#compatibility}

### openCypher {#opencypher}

Three lexical differences will catch a reader who knows Cypher from elsewhere.

* **Identifiers fold to lower case, and backticks are not a quoting character.** Use double
  quotes. `` `My Label` `` is a syntax error.
* **A string literal takes single quotes only.** Double quotes make an identifier.
* **`//` is not a comment.** Use `--` or `/* */`.

`XOR`, `STARTS WITH`, `ENDS WITH`, `CONTAINS` and `=~` are all present and mean what they mean
in openCypher.

### ISO/IEC 39075 {#isoiec-39075}

The notation in this reference follows the same conventions as the standard's syntax
productions, but is not the standard's BNF.

`IS [NOT] UNKNOWN` is the standard's spelling of the null test on a boolean and is accepted
alongside `IS [NOT] NULL`. So is `XOR`. Both fall under the standard's
`<boolean value expression>` (ISO/IEC 39075:2024 §20.20). `UNKNOWN` used as a *value* is a
syntax error. See [GQL conformance](/agensgraph/appendix/gql-conformance/) for the rest.

## See also {#see-also}

- [Data types](/agensgraph/reference/types/) — `graphid`, `vertex`, `edge`, `graphpath` and `jsonb` properties
- [Server settings](/agensgraph/reference/guc/) — including `graph_path`, which every session needs
- [Keywords](/agensgraph/appendix/keywords/) — the full keyword list and each word's category
- [Cypher, GQL and SQL](/agensgraph/concepts/languages/) — which language to reach for
- [PostgreSQL: SQL syntax](https://www.postgresql.org/docs/18/sql-syntax.html) — the SQL half
  of the same lexer
