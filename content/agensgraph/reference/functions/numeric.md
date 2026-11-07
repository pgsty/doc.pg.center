---
title: Numeric functions
linkTitle: Numeric functions
description: Arithmetic, logarithmic and trigonometric functions.
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/numeric.html
upstream_source: agensgraph
upstream_modified: true
---


Arithmetic, logarithmic and trigonometric functions. Most have a `jsonb` overload that takes
a property directly, and a `double precision` overload from PostgreSQL. Either way, a Cypher
`RETURN` prints the result as a `jsonb` number.

Angles are in radians unless the name ends in `d`.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## abs {#abs}

```
abs ( x jsonb ) -> jsonb
abs ( x numeric ) -> numeric
```

Returns the absolute value of a number.

```cypher
MATCH (m:movie {title:'Inception'}) RETURN abs(m.year - 2000) AS gap;
```

```
 gap
-----
 10
```

## acos {#acos}

```
acos ( x jsonb ) -> jsonb
acos ( x double precision ) -> double precision
```

Returns the arc cosine of `x`, in radians. `x` must be between −1 and 1.

## asin {#asin}

```
asin ( x jsonb ) -> jsonb
asin ( x double precision ) -> double precision
```

Returns the arc sine of `x`, in radians. `x` must be between −1 and 1.

## atan {#atan}

```
atan ( x jsonb ) -> jsonb
atan ( x double precision ) -> double precision
```

Returns the arc tangent of `x`, in radians.

## atan2 {#atan2}

```
atan2 ( y jsonb, x jsonb ) -> jsonb
atan2 ( y double precision, x double precision ) -> double precision
```

Returns the arc tangent of `y / x`, in radians, using the signs of both arguments to place
the result in the correct quadrant.

**Considerations**

- Prefer this to `atan(y / x)`, which cannot tell −15/3 from 15/−3 and so loses the quadrant.

```cypher
RETURN cot(1.5) AS cot, asin(1) AS asin, acos(0.5) AS acos, atan(-1) AS atan, atan2(-1.5, 1.3) AS atan2;
```

```
         cot         |        asin        |        acos        |        atan         |        atan2
---------------------+--------------------+--------------------+---------------------+---------------------
 0.07091484430265245 | 1.5707963267948966 | 1.0471975511965979 | -0.7853981633974483 | -0.8567056281827387
```

## ceil {#ceil}

```
ceil ( x jsonb ) -> jsonb
ceil ( x numeric ) -> numeric
```

Returns the smallest integer that is not less than `x`.

```cypher
RETURN ceil(3.1) AS up, floor(3.1) AS down, round(3.6) AS nearest, sign(-19.93) AS sign;
```

```
 up | down | nearest | sign
----+------+---------+------
 4  | 3    | 4       | -1
```

## cos {#cos}

```
cos ( x jsonb ) -> jsonb
cos ( x double precision ) -> double precision
```

Returns the cosine of an angle given in radians.

## cosd {#cosd}

```
cosd ( x double precision ) -> double precision
```

Returns the cosine of an angle given in degrees.

**Considerations**

- Exact at the quarter turns, where converting the angle first is not: `cosd(90)` is 0 while
  `cos(radians(90))` is 0.00000000000000006123233995736766.
- The degree forms have no `jsonb` overload, so a property coerces to `double precision`.

```cypher
RETURN sind(30) AS sind, cosd(60) AS cosd, tand(45) AS tand;
```

```
 sind | cosd | tand
------+------+------
 0.5  | 0.5  | 1
```

## cot {#cot}

```
cot ( x jsonb ) -> jsonb
cot ( x double precision ) -> double precision
```

Returns the cotangent of an angle given in radians: the reciprocal of the tangent. See
[`atan2`](#atan2) for a worked example.

## degrees {#degrees}

```
degrees ( x jsonb ) -> jsonb
degrees ( x double precision ) -> double precision
```

Converts radians to degrees.

```cypher
RETURN degrees(pi()) AS half_turn, radians(180) AS in_radians;
```

```
 half_turn |    in_radians
-----------+-------------------
 180       | 3.141592653589793
```

## e {#e}

```
e ( ) -> numeric
```

Returns Euler's number as a `numeric`.

**Considerations**

- The result is `numeric`, so it carries more digits than `exp(1)`, which is
  `double precision`: `2.7182818284590452` against `2.718281828459045`.

```cypher
RETURN e() AS e, exp(1) AS exp_one;
```

```
         e          |      exp_one
--------------------+-------------------
 2.7182818284590452 | 2.718281828459045
```

## exp {#exp}

```
exp ( x jsonb ) -> jsonb
exp ( x numeric ) -> numeric
```

Returns *e* raised to the power `x`.

## floor {#floor}

```
floor ( x jsonb ) -> jsonb
floor ( x numeric ) -> numeric
```

Returns the largest integer that is not greater than `x`. See [`ceil`](#ceil) for a worked
example.

## ln {#ln}

```
ln ( x double precision ) -> double precision
ln ( x numeric ) -> numeric
```

Returns the natural logarithm of `x`. This is the function [`log`](#log) resolves to in
Cypher, and it can also be called under this name.

## log {#log}

```
log ( x jsonb ) -> jsonb
```

Returns the **natural** logarithm of `x`.

**Considerations**

- In a Cypher query the parser rewrites `log` to [`ln`](#ln), so the result column is named
  `ln` and there is **no two-argument form**:

```cypher
RETURN log(2, 8);
```

```
ERROR:  function ln(integer, integer) does not exist
LINE 1: RETURN log(2, 8);
               ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

- This is the opposite of PostgreSQL's `log`, which is base 10. For base 10 in Cypher, use
  [`log10`](#log10).

```cypher
RETURN log(27) AS natural, log10(27) AS base_ten;
```

```
      natural      |      base_ten
-------------------+--------------------
 3.295836866004329 | 1.4313637641589874
```

## log10 {#log10}

```
log10 ( x double precision ) -> double precision
log10 ( x numeric ) -> numeric
```

Returns the base-10 logarithm of `x`. Not rewritten, so this name means what it says.

## pi {#pi}

```
pi ( ) -> double precision
```

Returns π. See [`degrees`](#degrees) for a worked example.

## radians {#radians}

```
radians ( x jsonb ) -> jsonb
radians ( x double precision ) -> double precision
```

Converts degrees to radians.

## rand {#rand}

```
rand ( ) -> jsonb
```

Returns a number in the half-open range 0 to 1.

**Considerations**

- `rand()` is marked immutable, so the planner folds it to a single constant. Every row of a
  query, and every execution of a prepared statement, sees the **same** number. Call
  PostgreSQL's `random()` instead, which is volatile and works in Cypher.

```cypher
FOR x IN [1,2,3] RETURN x, rand(), random();
```

```
 x |       rand        |       random
---+-------------------+---------------------
 1 | 0.533950385997692 | 0.33269661597409694
 2 | 0.533950385997692 | 0.10517878758331145
 3 | 0.533950385997692 | 0.3874591104544447
```

## round {#round}

```
round ( x jsonb ) -> jsonb
round ( x numeric [, scale integer ] ) -> numeric
```

Rounds `x` to the nearest integer, halves away from zero.

**Considerations**

- The `jsonb` form rounds to an integer only. To keep decimal places, cast and use the
  `numeric` form: `round(x::numeric, 2)`.

## sign {#sign}

```
sign ( x jsonb ) -> jsonb
sign ( x numeric ) -> numeric
```

Returns −1, 0 or 1 according to the sign of `x`. See [`ceil`](#ceil) for a worked example.

## sin {#sin}

```
sin ( x double precision ) -> double precision
```

Returns the sine of an angle given in radians.

**Considerations**

- Of the trigonometric functions, sine alone has no `jsonb` overload under its own name: the
  `jsonb` sine is catalogued as `jsonb_sin`. Nothing is lost. A property coerces to
  `double precision` and `sin()` resolves to the PostgreSQL function. But the result type
  differs from its neighbours over a `jsonb` argument.

```cypher
RETURN sin(0.5) AS sin, cos(0) AS cos, tan(0) AS tan;
```

```
        sin        | cos | tan
-------------------+-----+-----
 0.479425538604203 | 1   | 0
```

```cypher
MATCH (m:movie {title:'The Matrix'})
RETURN pg_typeof(cos(m.embedding[0])) AS cos_t, pg_typeof(sin(m.embedding[0])) AS sin_t,
       pg_typeof(tan(m.embedding[0])) AS tan_t;
```

```
  cos_t  |       sin_t        |  tan_t
---------+--------------------+---------
 "jsonb" | "double precision" | "jsonb"
```

## sind {#sind}

```
sind ( x double precision ) -> double precision
```

Returns the sine of an angle given in degrees. See [`cosd`](#cosd) for a worked example.

## sqrt {#sqrt}

```
sqrt ( x jsonb ) -> jsonb
sqrt ( x numeric ) -> numeric
```

Returns the square root of `x`.

**Considerations**

- A negative argument is an error rather than null:

```cypher
RETURN sqrt(-16);
```

```
ERROR:  cannot take square root of a negative number
```

```cypher
MATCH (m:movie {title:'The Matrix'}) RETURN sqrt(m.year) AS root;
```

```
        root
--------------------
 44.710177812216314
```

## tan {#tan}

```
tan ( x jsonb ) -> jsonb
tan ( x double precision ) -> double precision
```

Returns the tangent of an angle given in radians. See [`sin`](#sin) for a worked example.

## tand {#tand}

```
tand ( x double precision ) -> double precision
```

Returns the tangent of an angle given in degrees. See [`cosd`](#cosd) for a worked example.

## Arithmetic on properties {#arithmetic-on-properties}

The operators `+`, `-`, `*`, `/`, `%` and `^` work on properties, but on `jsonb` operands
they follow `jsonb`'s own rules, not SQL's: two integers divide as integers.

```cypher
RETURN 7 % 3 AS modulo, 2 ^ 10 AS power, 7 / 2 AS integer_division, 7.0 / 2 AS real_division;
```

```
 modulo | power | integer_division |   real_division
--------+-------+------------------+--------------------
 1      | 1024  | 3                | 3.5000000000000000
```

Each is implemented by a backtick-named operator over `jsonb`; see
[arithmetic operators on jsonb](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb).

## Compatibility {#compatibility}

### openCypher {#opencypher}

`log()` is base *e* here and base 10 in PostgreSQL. openCypher spells the natural logarithm
`log` too, so a Cypher query is portable and a SQL one is not. openCypher's `e()` and
`rand()` exist; `rand()` deviates by being folded to a constant. `haversin()` is not
supported.

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Aggregate functions](/agensgraph/reference/functions/aggregate/) — `avg`, `sum`, `stdev`
- [Type conversion functions](/agensgraph/reference/functions/type-conversion/) — `toInteger`, `toFloat`
