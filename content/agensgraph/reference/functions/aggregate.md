---
title: Aggregate functions
linkTitle: Aggregate functions
description: Functions that reduce a group of rows to one value.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/aggregate.html
upstream_source: agensgraph
upstream_modified: true
---


Functions that reduce a group of rows to one value. Cypher forms a group the same way SQL
does: every non-aggregated expression in the `RETURN` or `WITH` list is a grouping key. With
no key at all, the whole result is one group.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## avg {#avg}

```
avg ( expression numeric ) -> numeric
```

Returns the arithmetic mean of the non-null values in the group.

**Considerations**

- A property arrives as `jsonb` and is coerced to `numeric`, so the result is `numeric` and
  keeps full precision rather than rounding to `double precision`.
- Rows whose value is null are skipped. A group with no non-null value returns null.

```cypher
MATCH (m:movie) RETURN avg(m.year) AS mean_year;
```

```
       mean_year
-----------------------
 2002.0555555555555556
```

## collect {#collect}

```
collect ( expression anyelement ) -> jsonb
collect ( v vertex ) -> vertex[]
collect ( e edge ) -> edge[]
collect ( p graphpath ) -> graphpath[]
```

Gathers the values in the group into a list, in the group's row order.

**Considerations**

- A `vertex`, `edge` or `graphpath` argument produces a native array rather than a `jsonb`
  array: `vertex[]`, `edge[]` or `graphpath[]`. Everything else produces `jsonb`.
  **Added in 2.18**
- A native array is indexed from 0 by Cypher's subscript, like a `jsonb` list.
- Null values are collected. `collect(DISTINCT expr)` removes duplicates.
- `length()` counts the elements of any of the four result types.

```cypher
MATCH (p:person)-[:directed]->(m:movie)
WITH p, collect(m.title) AS films
RETURN p.name AS director, films ORDER BY p.name LIMIT 2;
```

```
      director       |             films
---------------------+-------------------------------
 "Andrew Niccol"     | ["Gattaca"]
 "Christopher Nolan" | ["Inception", "Interstellar"]
```

Collecting the graph elements themselves gives an array of them:

```cypher
MATCH (:movie {title:'The Matrix'})-[e:related_to]->()
WITH collect(e) AS edges
RETURN length(edges) AS n, pg_typeof(edges) AS type;
```

```
 n |   type
---+----------
 3 | "edge[]"
```

## count {#count}

```
count ( * ) -> bigint
count ( expression ) -> bigint
```

Counts rows in the group. `count(*)` counts every row; `count(expression)` counts the rows
whose expression is not null.

**Considerations**

- `count(v)` over a whole vertex or edge counts the element's identity: the parser replaces
  the argument with its `graphid`, so the property bag is never read.
- `count(DISTINCT expression)` counts distinct non-null values.
- A group with no rows returns 0, not null.

```cypher
MATCH (m:movie)
RETURN count(*) AS films, count(m.genre) AS with_genre, count(DISTINCT m.genre) AS genres;
```

```
 films | with_genre | genres
-------+------------+--------
 18    | 18         | 3
```

## max {#max}

```
max ( expression jsonb ) -> jsonb
max ( expression numeric ) -> numeric
```

Returns the largest value in the group.

**Considerations**

- A `jsonb` argument is ordered by `jsonb`'s own type ordering, in which every number sorts
  below every string. A numeric or text property read from a typed column is compared in
  that column's type.
- Nulls are skipped; a group with no non-null value returns null.

```cypher
MATCH (m:movie) RETURN min(m.year) AS earliest, max(m.year) AS latest;
```

```
 earliest | latest
----------+--------
 1982     | 2021
```

## min {#min}

```
min ( expression jsonb ) -> jsonb
min ( expression numeric ) -> numeric
```

Returns the smallest value in the group. The considerations for [`max`](#max) apply
unchanged.

## percentileCont {#percentilecont}

```
percentileCont ( list jsonb, percentile numeric ) -> double precision
```

Returns the percentile of a list of numbers, interpolating between the two values that
straddle the requested position.

**Considerations**

- This is a plain function over a list, not an aggregate. To take a percentile of a group,
  build the list first: `percentileCont(collect(m.year), 0.5)`.
- The argument must be a list. A scalar is refused, and the message names the wrong
  function:

```cypher
RETURN percentileCont(2010, 0.5);
```

```
ERROR:  reverse(): list is expected but 2010
```
- Returns null when the list holds fewer than two elements, or when the percentile is
  outside the range 0 to 1.
- Non-numeric elements are ignored rather than rejected.

```cypher
MATCH (m:movie) RETURN percentileCont(collect(m.year), 0.5) AS median;
```

```
 median
--------
 2002.5
```

## percentileDisc {#percentiledisc}

```
percentileDisc ( list jsonb, percentile numeric ) -> double precision
```

Returns the percentile of a list of numbers, rounded down to an element that is actually in
the list. Its considerations are those of [`percentileCont`](#percentilecont).

```cypher
MATCH (m:movie) RETURN percentileDisc(collect(m.year), 0.5) AS median;
```

```
 median
--------
 2002
```

## stdev {#stdev}

```
stdev ( expression numeric ) -> numeric
```

Returns the sample standard deviation of the values in the group: the estimate that
divides by *n* − 1.

**Considerations**

- The parser rewrites the name to `stddev_samp`, so that is the name the result column
  carries and the name an error message uses.
- Unquoted identifiers fold to lower case, so `stDev` and `STDEV` are the same call.
- `stdDev` is a *different* function: it folds to `stddev`, PostgreSQL's own alias for
  `stddev_samp`. It computes the same number.
- A group of one row returns null.

```cypher
MATCH (m:movie) RETURN stdev(m.year) AS sample_sd, stdevp(m.year) AS population_sd;
```

```
      sample_sd      |    population_sd
---------------------+---------------------
 11.3628508344062724 | 11.0427061006209596
```

## stdevp {#stdevp}

```
stdevp ( expression numeric ) -> numeric
```

Returns the population standard deviation of the values in the group: the estimate that
divides by *n*. The parser rewrites the name to `stddev_pop`, and `stDevP` is the same
call.

## sum {#sum}

```
sum ( expression numeric ) -> numeric
```

Returns the total of the non-null values in the group.

**Considerations**

- Nulls are skipped. A group with no non-null value returns null, not 0.
- Nothing deduplicates the input: a value that a pattern matches twice is added twice.
  Use `sum(DISTINCT expr)` if that is not what you want.

```cypher
MATCH (p:person)-[:acted_in]->(:movie) RETURN sum(p.born) AS born_total;
```

```
 born_total
------------
 49017
```

## Compatibility {#compatibility}

### openCypher {#opencypher}

`stDev` and `stDevP` are openCypher's names for the sample and population standard
deviation; both spellings work here. openCypher's `percentileCont` and `percentileDisc` are
aggregates that take a value per row. These take a finished list, so a query written for
openCypher needs `collect()` around the first argument.

### ISO/IEC 39075 {#isoiec-39075}

`avg`, `count`, `max`, `min`, `stddev_pop`, `stddev_samp` and `sum` are the GQL aggregate
functions and are spelled as the standard spells them. `collect` corresponds to the GQL
`COLLECT` value expression, which is documented with the
[subquery expressions](/agensgraph/reference/clauses/subquery-expressions/).

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Predicate functions](/agensgraph/reference/functions/predicate/) — `all`, `any`, `none`, `single`
- [List functions](/agensgraph/reference/functions/list/) — working with the list `collect` produces
