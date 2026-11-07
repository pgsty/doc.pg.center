---
title: 数值函数
linkTitle: 数值函数
description: 算术、对数和三角函数。
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/numeric.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


算术、对数和三角函数。多数函数既有直接接收属性的 `jsonb` 重载，也有来自 PostgreSQL 的 `double precision` 重载。无论哪种，Cypher 的 `RETURN` 都会把结果打印为 `jsonb` 数字。

除名称以 `d` 结尾的函数外，角度均以弧度表示。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## abs {#abs}

```
abs ( x jsonb ) -> jsonb
abs ( x numeric ) -> numeric
```

返回数字的绝对值。

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

返回 `x` 的反余弦，单位为弧度。`x` 必须在 −1 到 1 之间。

## asin {#asin}

```
asin ( x jsonb ) -> jsonb
asin ( x double precision ) -> double precision
```

返回 `x` 的反正弦，单位为弧度。`x` 必须在 −1 到 1 之间。

## atan {#atan}

```
atan ( x jsonb ) -> jsonb
atan ( x double precision ) -> double precision
```

返回 `x` 的反正切，单位为弧度。

## atan2 {#atan2}

```
atan2 ( y jsonb, x jsonb ) -> jsonb
atan2 ( y double precision, x double precision ) -> double precision
```

返回 `y / x` 的反正切，单位为弧度；它使用两个参数的符号把结果放入正确的象限。

**注意事项**

- 应优先使用该函数，而不是 `atan(y / x)`：后者无法区分 −15/3 与 15/−3，因此会丢失象限信息。

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

返回不小于 `x` 的最小整数。

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

返回以弧度表示的角度的余弦。

## cosd {#cosd}

```
cosd ( x double precision ) -> double precision
```

返回以度数表示的角度的余弦。

**注意事项**

- 在四分之一圈处结果精确；先转换角度则不精确：`cosd(90)` 是 0，而 `cos(radians(90))` 是 0.00000000000000006123233995736766。
- 度数形式没有 `jsonb` 重载，因此属性会转换为 `double precision`。

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

返回以弧度表示的角度的余切，即正切的倒数。示例见 [`atan2`](#atan2)。

## degrees {#degrees}

```
degrees ( x jsonb ) -> jsonb
degrees ( x double precision ) -> double precision
```

把弧度转换为度数。

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

以 `numeric` 返回欧拉数。

**注意事项**

- 结果是 `numeric`，因此比 `double precision` 的 `exp(1)` 带更多位数：前者为 `2.7182818284590452`，后者为 `2.718281828459045`。

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

返回 *e* 的 `x` 次幂。

## floor {#floor}

```
floor ( x jsonb ) -> jsonb
floor ( x numeric ) -> numeric
```

返回不大于 `x` 的最大整数。示例见 [`ceil`](#ceil)。

## ln {#ln}

```
ln ( x double precision ) -> double precision
ln ( x numeric ) -> numeric
```

返回 `x` 的自然对数。这也是 Cypher 中 [`log`](#log) 解析到的函数，并且可以直接用这个名称调用。

## log {#log}

```
log ( x jsonb ) -> jsonb
```

返回 `x` 的**自然**对数。

**注意事项**

- 在 Cypher 查询中，解析器会把 `log` 改写为 [`ln`](#ln)，因此结果列名为 `ln`，并且**没有双参数形式**：

```cypher
RETURN log(2, 8);
```

```
ERROR:  function ln(integer, integer) does not exist
LINE 1: RETURN log(2, 8);
               ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

- 这与 PostgreSQL 的 `log` 相反；后者的底是 10。在 Cypher 中要用底 10，请使用 [`log10`](#log10)。

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

返回 `x` 的以 10 为底的对数。该名称不会被改写，因此含义与字面相同。

## pi {#pi}

```
pi ( ) -> double precision
```

返回 π。示例见 [`degrees`](#degrees)。

## radians {#radians}

```
radians ( x jsonb ) -> jsonb
radians ( x double precision ) -> double precision
```

把度数转换为弧度。

## rand {#rand}

```
rand ( ) -> jsonb
```

返回位于左闭右开区间 0 到 1 中的数字。

**注意事项**

- `rand()` 被标记为 immutable，因此规划器会把它折叠成单个常量。查询的每一行，以及预编译语句的每次执行，看到的都是**同一个**数字。请改调 PostgreSQL 的 `random()`；它是 volatile 的，并且可在 Cypher 中使用。

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

把 `x` 舍入到最接近的整数；恰为一半时远离零。

**注意事项**

- `jsonb` 形式只会舍入为整数。要保留小数位，请转换类型并使用 `numeric` 形式：`round(x::numeric, 2)`。

## sign {#sign}

```
sign ( x jsonb ) -> jsonb
sign ( x numeric ) -> numeric
```

根据 `x` 的符号返回 −1、0 或 1。示例见 [`ceil`](#ceil)。

## sin {#sin}

```
sin ( x double precision ) -> double precision
```

返回以弧度表示的角度的正弦。

**注意事项**

- 在三角函数中，只有 sine 自身名称下没有 `jsonb` 重载：`jsonb` 正弦在目录中登记为 `jsonb_sin`。这并不损失能力。属性会转换为 `double precision`，`sin()` 解析到 PostgreSQL 函数。但对 `jsonb` 参数而言，其结果类型与相邻函数不同。

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

返回以度数表示的角度的正弦。示例见 [`cosd`](#cosd)。

## sqrt {#sqrt}

```
sqrt ( x jsonb ) -> jsonb
sqrt ( x numeric ) -> numeric
```

返回 `x` 的平方根。

**注意事项**

- 负参数是错误，而不是返回 null：

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

返回以弧度表示的角度的正切。示例见 [`sin`](#sin)。

## tand {#tand}

```
tand ( x double precision ) -> double precision
```

返回以度数表示的角度的正切。示例见 [`cosd`](#cosd)。

## 属性上的算术 {#arithmetic-on-properties}

操作符 `+`、`-`、`*`、`/`、`%` 和 `^` 可作用于属性；但对 `jsonb` 操作数，它们遵循 `jsonb` 自身的规则，而不是 SQL 的规则：两个整数相除会得到整数。

```cypher
RETURN 7 % 3 AS modulo, 2 ^ 10 AS power, 7 / 2 AS integer_division, 7.0 / 2 AS real_division;
```

```
 modulo | power | integer_division |   real_division
--------+-------+------------------+--------------------
 1      | 1024  | 3                | 3.5000000000000000
```

每个操作符都由作用于 `jsonb` 的反引号命名操作符实现；参见 [jsonb 算术操作符](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb)。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

这里的 `log()` 以 *e* 为底，而 PostgreSQL 中以 10 为底。openCypher 也把自然对数拼作 `log`，因此 Cypher 查询可移植，SQL 查询不可。openCypher 的 `e()` 和 `rand()` 存在；`rand()` 因为被折叠为常量而存在偏差。不支持 `haversin()`。

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [聚合函数](/zh/agensgraph/reference/functions/aggregate/) — `avg`、`sum`、`stdev`
- [类型转换函数](/zh/agensgraph/reference/functions/type-conversion/) — `toInteger`、`toFloat`
