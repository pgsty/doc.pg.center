---
title: String functions
linkTitle: String functions
description: Functions over text.
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/string.html
upstream_source: agensgraph
upstream_modified: true
---


Functions over text. A property arrives as `jsonb`, and several of these functions have both
a `text` and a `jsonb` overload. Which one the parser picks depends on what you pass, so a
literal and a property do not always behave alike. Each entry says so where it matters.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## left {#left}

```
left ( string jsonb, n jsonb ) -> jsonb
left ( string text, n integer ) -> text
```

Returns the first `n` characters of a string.

**Considerations**

- A property with an integer literal is **ambiguous**, because `left(jsonb, jsonb)` and
  `left(text, integer)` match equally well:

```cypher
MATCH (m:movie {title:'Blade Runner 2049'}) RETURN left(m.title, 12);
```

```
ERROR:  function left(jsonb, integer) is not unique
LINE 1: ...ATCH (m:movie {title:'Blade Runner 2049'}) RETURN left(m.tit...
                                                             ^
HINT:  Could not choose a best candidate function. You might need to add explicit type casts.
```

  Cast the string, as `left(m.title::text, 12)`, or use [`substring`](#substring), which has
  no such clash.
- An `n` larger than the string returns the whole string.

```cypher
MATCH (m:movie {title:'Blade Runner 2049'})
RETURN left(m.title::text, 12) AS head, right(m.title::text, 4) AS tail;
```

```
      head      |  tail
----------------+--------
 "Blade Runner" | "2049"
```

## lower {#lower}

```
lower ( string text ) -> text
```

Returns the string in lower case. This is PostgreSQL's own function, reachable from Cypher
because a `jsonb` string coerces to `text`. [`toLower`](#tolower) is the Cypher spelling and
takes `jsonb` directly.

```cypher
RETURN lower('AbCdeFG') AS lower, upper('AbCdeFG') AS upper;
```

```
   lower   |   upper
-----------+-----------
 "abcdefg" | "ABCDEFG"
```

## lTrim {#ltrim}

```
lTrim ( string jsonb ) -> jsonb
```

Removes whitespace from the start of a string.

**Considerations**

- Whitespace only. There is no form that takes a set of characters to strip; use
  PostgreSQL's `ltrim(text, text)` for that.

```cypher
RETURN lTrim('    ABCD    ') AS l, rTrim('    ABCD    ') AS r, trim('    ABCD    ') AS both;
```

```
     l      |     r      |  both
------------+------------+--------
 "ABCD    " | "    ABCD" | "ABCD"
```

## replace {#replace}

```
replace ( string jsonb, old jsonb, new jsonb ) -> jsonb
```

Replaces every occurrence of one substring with another.

| Name | Type | Description |
| --- | --- | --- |
| `string` | `jsonb` | The string to search. |
| `old` | `jsonb` | Substring to find. Every occurrence is replaced, not just the first. |
| `new` | `jsonb` | Replacement. May be longer or shorter than `old`, or empty. |

**Considerations**

- `old` and `new` need not be the same length.
- An `old` that does not occur returns the string unchanged.

```cypher
MATCH (m:movie {title:'Terminator 2: Judgment Day'})
RETURN replace(m.title, 'Judgment', 'Judgement') AS british;
```

```
            british
-------------------------------
 "Terminator 2: Judgement Day"
```

## reverse {#reverse}

```
reverse ( string text ) -> text
reverse ( list jsonb ) -> jsonb
reverse ( list anyarray ) -> anyarray
```

Reverses a string or a list.

**Considerations**

- Which overload you get depends on the argument, and the two disagree about strings. A
  string *literal* resolves to `reverse(text)` and is reversed. A string *property* is
  already `jsonb`, so it resolves to `reverse(jsonb)`, which reverses arrays only:

```cypher
RETURN reverse('Blade Runner 2049'::jsonb);
```

```
ERROR:  reverse(): list is expected but "Blade Runner 2049"
```

  A property reference behaves as that cast does, because it is already `jsonb`. Cast the
  other way to reverse the characters: `reverse(m.title::text)`.
- A list property needs no cast. The `jsonb` overload reverses a list.

```cypher
RETURN reverse('ABCDEFG') AS text, reverse([1,2,3]) AS list;
```

```
   text    |   list
-----------+-----------
 "GFEDCBA" | [3, 2, 1]
```

```cypher
MATCH (m:movie {title:'Blade Runner 2049'}) RETURN reverse(m.title::text) AS backwards;
```

```
      backwards
---------------------
 "9402 rennuR edalB"
```

## right {#right}

```
right ( string jsonb, n jsonb ) -> jsonb
right ( string text, n integer ) -> text
```

Returns the last `n` characters of a string. It shares [`left`](#left)'s ambiguity over a
property with an integer literal, and the same two ways of resolving it.

## rTrim {#rtrim}

```
rTrim ( string jsonb ) -> jsonb
```

Removes whitespace from the end of a string. See [`lTrim`](#ltrim) for a worked example.

## split {#split}

```
split ( string text, delimiter text ) -> anyarray
```

Cuts a string into a list at every occurrence of a delimiter.

**Considerations**

- The value is an array of strings. The catalog declares the return type as `anyarray`, so
  `pg_typeof` reports `anyarray` in SQL. A Cypher `RETURN` boxes it to a `jsonb` list.
- A delimiter that does not occur returns a one-element list holding the whole string.
- The delimiter is a literal string, not a pattern. Use PostgreSQL's `regexp_split_to_array`
  for a regular expression.

```cypher
RETURN split('Action/Sci-Fi/Drama', '/') AS genres;
```

```
            genres
-------------------------------
 ["Action", "Sci-Fi", "Drama"]
```

## str_size {#str_size}

```
str_size ( string text ) -> integer
```

Returns the number of characters in a string, as an `integer`.

**Considerations**

- [`size`](/agensgraph/reference/functions/scalar/#size) and [`length`](/agensgraph/reference/functions/scalar/#length) are the Cypher spellings and
  return `jsonb`. This function exists so that a caller wanting a native `integer` does not
  have to unbox one. A driver, or SQL around a Cypher query, is such a caller.

```cypher
RETURN str_size('hello') AS n;
```

```
 n
---
 5
```

## substring {#substring}

```
substring ( string jsonb, start jsonb ) -> jsonb
substring ( string jsonb, start jsonb, count jsonb ) -> jsonb
```

Returns part of a string, starting at `start` and running to the end or for `count`
characters.

| Name | Type | Description |
| --- | --- | --- |
| `string` | `jsonb` | The string to cut. |
| `start` | `jsonb` | 0-based offset of the first character. |
| `count` | `jsonb` | How many characters to take. Omitted, the rest of the string. A `count` past the end simply stops at the end. |

**Considerations**

- `start` is 0-based, unlike SQL's `substring`, which is 1-based. The parser adds the 1 for
  you, so write the offset you mean.
- Unlike [`left`](#left) and [`right`](#right), this is unambiguous over a property, so it is
  the safer way to take a prefix of one.

```cypher
RETURN substring('ABCDEFG', 2) AS from_two, substring('ABCDEFG', 2, 3) AS three_from_two,
       substring('ABCDEFG', 4, 10) AS past_end;
```

```
 from_two | three_from_two | past_end
----------+----------------+----------
 "CDEFG"  | "CDE"          | "EFG"
```

## toLower {#tolower}

```
toLower ( string jsonb ) -> jsonb
```

Returns the string in lower case.

**Considerations**

- Takes `jsonb`, so it works on a property with no cast, unlike [`reverse`](#reverse).
- [`lower`](#lower) is PostgreSQL's equivalent and also works. They differ only in the type
  they take and return.

```cypher
MATCH (m:movie {title:'The Fifth Element'}) RETURN toLower(m.title) AS lower, toUpper(m.title) AS upper;
```

```
        lower        |        upper
---------------------+---------------------
 "the fifth element" | "THE FIFTH ELEMENT"
```

## toUpper {#toupper}

```
toUpper ( string jsonb ) -> jsonb
```

Returns the string in upper case. See [`toLower`](#tolower) for a worked example.

## trim {#trim}

```
trim ( string jsonb ) -> jsonb
```

Removes whitespace from both ends of a string.

**Considerations**

- `trim` is a grammar form as well as a function name, so it takes exactly one argument
  here. SQL's `trim(BOTH 'x' FROM str)` spelling is not available in Cypher:

```cypher
RETURN trim(BOTH 'x' FROM 'xxaxx');
```

```
ERROR:  syntax error at or near "BOTH"
LINE 1: RETURN trim(BOTH 'x' FROM 'xxaxx');
                    ^
```

## upper {#upper}

```
upper ( string text ) -> text
```

Returns the string in upper case. PostgreSQL's own function; see [`lower`](#lower).

## Matching without a function {#matching-without-a-function}

Four string tests are operators rather than functions, and each has an entry in the catalog
under a name you do not type:

| Operator | Implemented by | Returns true when |
| --- | --- | --- |
| `STARTS WITH` | `string_starts_with` | The left string begins with the right one |
| `ENDS WITH` | `string_ends_with` | The left string ends with the right one |
| `CONTAINS` | `string_contains` | The right string occurs anywhere in the left |
| `=~` | `string_regex` | The left string matches the right as a regular expression |

```cypher
MATCH (m:movie) WHERE m.title STARTS WITH 'The Matrix' RETURN count(*) AS n;
```

```
 n
---
 4
```

None of the four can use a property index. Each is a function call over the property rather
than a comparison against it, so a query that filters on one scans the label.

## Compatibility {#compatibility}

### openCypher {#opencypher}

openCypher spells the case functions `toLower` and `toUpper` and the trims `lTrim`, `rTrim`
and `trim`; all five work. openCypher's `substring` is 0-based, as it is here. `left` and
`right` are PostgreSQL functions that openCypher also defines. The ambiguity over a property
with an integer literal is a deviation, and `substring` is the portable form.

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Type conversion functions](/agensgraph/reference/functions/type-conversion/) — `toString`, `toStringList`
- [List functions](/agensgraph/reference/functions/list/) — what `split` returns
