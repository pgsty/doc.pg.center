---
title: 语法
linkTitle: 语法
description: 每条语句都遵循的词法层，无论它用哪种语言书写：本参考使用的语法记法，以及标识符、字面量、运算符、注释和 null 的规则。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/syntax.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


这里是每条语句都遵循的词法层，无论它用哪种语言书写：本参考使用的语法记法，以及标识符、字面量、运算符、注释和 null 的规则。

Cypher、GQL 和 SQL 共用一个解析器，所以这些规则在三者中相同。某条规则在它们之间不同时，文中会明确指出。

## 语法约定 {#syntax-conventions}

本参考中的每个语法摘要都采用相同写法：

```text
MATCH pattern [, pattern ] ... [ WHERE condition ]
```

语法摘要中的其他内容都不是记法。逗号、圆括号或箭号是语句的一部分，按显示原样输入。

**粗体**
: 关键字。按显示原样输入；大小写无关。

*斜体*
: 由你提供的占位符。每个占位符都在同一页的*参数*下定义。

`[ ]`
: 括起的部分可选。

`{ ... | ... }`
: 用花括号包住由竖线分隔的多个选项：必须恰好选择一个。

`...`
: 它前面的项可以重复。

`[, ... ]`
: 它前面的项可以重复，并用逗号分隔。

两行或更多语法摘要行
: 同一语句的备选形式。使用其中一行。

`where` *placeholder* `is one of:`
: 在随后的行中展开一个太大而不便内联的占位符。

方括号和花括号绝不是字面量。有些语句确实包含方括号：列表字面量、映射、边模式。对这类语句，语法摘要会在正文中说明，或者把方括号显示在不同位置，例如 `-[` *variable* `]->`。

## 标识符 {#identifiers}

标识符为图、标签、变量、属性键、列、索引或约束命名。

### 大小写折叠 {#case-folding}

未加引号的标识符会折叠为**小写**，与 PostgreSQL 折叠未加引号的 SQL 标识符的方式完全相同。因此 `MOVIE`、`Movie` 和 `movie` 指同一个标签：

```cypher
MATCH (n:MOVIE {title: 'The Matrix'}) RETURN n.title AS title;
```

```
    title
--------------
 "The Matrix"
```

双引号标识符按书写形式保留。`"MOVIE"` 与 `movie` 是不同名称。没有名为 `MOVIE` 的标签，所以这个模式匹配不到结果，而不是失败：

```cypher
MATCH (n:"MOVIE" {title: 'The Matrix'}) RETURN n.title AS title;
```

```
 title
-------
(0 rows)
```

变量也可以加引号；加引号的变量在每次引用时都必须加引号：

```cypher
MATCH ("Film":movie {title: 'The Matrix'}) RETURN "Film".title AS title;
```

```
    title
--------------
 "The Matrix"
```

属性键的折叠方式相同。`{MixedKey: 1}` 存储键 `mixedkey`；`{"MixedKey": 1}` 存储 `MixedKey`。二者是不同的键，一个顶点可以同时携带它们，所以一个键要么始终加引号，要么始终不加。

反引号不是引号字符。`` `movie` `` 是语法错误，不是加引号的标识符：

```cypher
MATCH (n:`movie`) RETURN n.title;
```

```
ERROR:  syntax error at or near "`"
LINE 1: MATCH (n:`movie`) RETURN n.title;
                 ^
```

### 字符 {#characters}

未加引号的标识符以字母或下划线开头，后续字符可以是字母、数字、下划线和美元符号。“字母”包含非 ASCII 字母，所以 `café` 是有效标识符。标识符不能以数字开头。`1abc` 会被读成后面带杂项字符的数字。双引号标识符可以包含除空字节以外的任何字符，其中的双引号要写两次（`"say ""hi"""`）。

长度限制沿用 PostgreSQL：63 字节，更长的名称会被截断到该长度。限制按字节而不是字符计数，所以由多字节字母组成的名称会更早达到限制。

### 保留字 {#reserved-words}

有些关键字是**保留**的：语法会把这个词读作关键字而不是名称。`both`、`let`、`finish`、`insert`、`offset` 和 `xor` 都保留。有些继承自 PostgreSQL，有些为图子句新增。每个词仍可在哪些位置使用并不相同，因此[关键字](/zh/agensgraph/appendix/keywords/)给出了逐位置表格。模式变量是它们都不能存活的位置：

```cypher
MATCH (both:movie {title: 'The Matrix'}) RETURN both.title;
```

```
ERROR:  syntax error at or near "both"
LINE 1: MATCH (both:movie {title: 'The Matrix'}) RETURN both.title;
               ^
```

加引号可以解除限制，因为加引号的标识符永远不会被读作关键字：

```cypher
MATCH ("both":movie {title: 'The Matrix'}) RETURN "both".title AS title;
```

```
    title
--------------
 "The Matrix"
```

保留字仍可用作 `RETURN` 别名和属性键，因为这两个位置都不会与关键字混淆：

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS both;
```

```
     both
--------------
 "The Matrix"
```

## 字面量 {#literals}

### 字符串 {#strings}

字符串字面量用**单**引号括起。双引号构成标识符而不是字符串，所以 `"plain"` 是变量引用，且作用域中没有这个变量时会失败。

字面量内的单引号写两次。反斜杠转义遵循 JSON 规则，因为 Cypher 字符串会变成 `jsonb` 字符串：

| 转义 | 含义 |
| --- | --- |
| `''` | 单引号。 |
| `\"` | 双引号。 |
| `\\` | 反斜杠。 |
| `\/` | 正斜杠。 |
| `\b` `\f` `\n` `\r` `\t` | 退格、换页、换行、回车、制表符。 |
| `\u` 加四个十六进制数字 | 具有该码点的字符。 |

任何其他反斜杠序列都会被拒绝：`'a\qb'` 抛出 `Escape sequence "\q" is invalid`。

```cypher
RETURN 'plain', 'it''s', 'a\tb', 'a\\tb', 'say \" hi';
```

```
 ?column? | ?column? | ?column? | ?column? |  ?column?
----------+----------+----------+----------+-------------
 "plain"  | "it's"   | "a\tb"   | "a\\tb"  | "say \" hi"
```

输出是每个值的 `jsonb` 渲染形式，会对打印内容重新转义：第三列包含三个字符，`a`、一个制表符和 `b`。

### 数字 {#numbers}

数字字面量的写法与 SQL 相同，并且接受 PostgreSQL 的非十进制和分隔形式：十六进制 `0x`、八进制 `0o`、二进制 `0b`，以及用作数字分隔符的下划线。

```cypher
RETURN 1, -1, 1.5, 1e3, 1E-3, 0x1F, 0o17, 0b101, 1_000;
```

```
 ?column? | ?column? | ?column? | ?column? | ?column? | ?column? | ?column? | ?column? | ?column?
----------+----------+----------+----------+----------+----------+----------+----------+----------
 1        | -1       | 1.5      | 1000     | 0.001    | 31       | 15       | 5        | 1000
```

不带小数点的数字是 JSON 整数，两个这样的数相除会截断：`7 / 2` 是 `3`。要得到 `3.5`，写 `7.0 / 2`。

### 布尔值、null、列表和映射 {#booleans-null-lists-and-maps}

`true`、`false` 和 `null` 是关键字，大小写均可。列表写在方括号中，映射写在花括号中。二者都可嵌套，也都可混合值类型，因为它们都会变成 `jsonb`。

```cypher
RETURN true, false, null, [1, 'two', true, null], {a: 1, b: [2], c: {d: 3}};
```

```
 ?column? | ?column? | ?column? |        ?column?        |             ?column?
----------+----------+----------+------------------------+-----------------------------------
 t        | f        |          | [1, "two", true, null] | {"a": 1, "b": [2], "c": {"d": 3}}
```

映射键是标识符，并按标识符折叠。`[]` 和 `{}` 分别是空列表和空映射。字面量与存储的 `jsonb` 值之间的关系见[数据类型](/zh/agensgraph/reference/types/)。

## 运算符 {#operators}

### 优先级 {#precedence}

运算符按下表顺序结合，最松的在前。同一行的两个运算符优先级相同，并按该行标明的方向结合。

| 优先级 | 运算符 | 结合方向 |
| --- | --- | --- |
| 1（最松） | `UNION` `EXCEPT` | 左 |
| 2 | `INTERSECT` | 左 |
| 3 | `OR` `XOR` | 左 |
| 4 | `AND` | 左 |
| 5 | `NOT` | 右 |
| 6 | `IS NULL` `IS NOT NULL` `IS [NOT] UNKNOWN` | 无 |
| 7 | `<` `<=` `>` `>=` `=` `<>` `!=` | 无 |
| 8 | `IN` `BETWEEN` | 无 |
| 9 | 其他任何运算符，包括 `\|\|` 和 `jsonb` 运算符 | 左 |
| 10 | `+` `-`（二元） | 左 |
| 11 | `*` `/` `%` | 左 |
| 12 | `^` | 左 |
| 13 | `-`（一元） | 右 |
| 14 | `STARTS WITH` `ENDS WITH` `CONTAINS` `=~` | 无 |
| 15 | `[` `]`（下标）、`(` `)`（调用） | 左 |
| 16 | `::` | 左 |
| 17（最紧） | `.` | 左 |

上表列出 Cypher 表达式可以包含的运算符。SQL 另有一些处于自身级别的运算符：`AT TIME ZONE`、`COLLATE`、`LIKE`、`ILIKE` 和 `SIMILAR TO`。Cypher 的表达式语法都不接受。

表中有三点不同于常见预期。

`^` 是**左**结合，且比一元负号更松；这是 PostgreSQL 的规则而不是算术规则。因此 `2 ^ 3 ^ 2` 是 `(2 ^ 3) ^ 2`，而 `-2 ^ 2` 是 `(-2) ^ 2`：

```cypher
RETURN 2 ^ 3 ^ 2 AS pow, -2 ^ 2 AS neg;
```

```
 pow | neg
-----+-----
 64  | 4
```

字符串匹配运算符结合得比除下标、调用、类型转换和属性读取以外的所有运算符都**更紧**。它们比拼接和算术都紧。因此下面 `||` 的右操作数是整个 `STARTS WITH` 测试，而不只是 `'c'`：

```cypher
RETURN 'ab' || 'c' STARTS WITH 'a';
```

```
 ?column?
-----------
 "abfalse"
```

如果你要的是另一种读法，请加圆括号。`('ab' || 'c') STARTS WITH 'a'` 是 `true`。

比较不能链式使用。`1 < 2 < 3` 是语法错误，不是两个比较。

### 逻辑运算符 {#logical-operators}

`AND`、`OR`、`NOT` 和 `XOR` 接受布尔值并返回布尔值，按三值逻辑运行。真值表见 [null 与三值逻辑](#null-and-three-valued-logic)。`XOR` 是 AgensGraph 对 SQL 运算符集合的补充，优先级与 `OR` 相同。

### 比较与谓词 {#comparison-and-predicates}

`=`、`<>`（或 `!=`）、`<`、`<=`、`>` 和 `>=` 比较两个值。比较不同 `jsonb` 类型的值不会失败，而是按 `jsonb` 自身的类型顺序排序。

`IN` 测试是否属于列表。`IS NULL` 和 `IS NOT NULL` 对任何值做 null 测试而不进行比较。`IS UNKNOWN` 和 `IS NOT UNKNOWN` 是标准对该测试在布尔值上的拼法，这里也接受：

```cypher
RETURN 2 IN [1, 2, 3] AS present, null IS NULL AS nul, null IS UNKNOWN AS unk;
```

```
 present | nul | unk
---------+-----+-----
 t       | t   | t
```

### 字符串匹配 {#string-matching}

四个运算符匹配字符串。`LIKE`、`ILIKE` 和 `SIMILAR TO` **仅限 SQL**。它们不属于 Cypher 的表达式语法，在 Cypher 中是语法错误。PostgreSQL 的正则表达式运算符（`~`、`~*`、`!~`、`!~*`）可以在 Cypher 中使用。

| 运算符 | 测试 |
| --- | --- |
| *string* `STARTS WITH` *prefix* | 字符串以前缀开头。 |
| *string* `ENDS WITH` *suffix* | 字符串以后缀结尾。 |
| *string* `CONTAINS` *substring* | 子串出现在字符串任意位置。 |
| *string* `=~` *pattern* | 整个字符串匹配 POSIX 正则表达式。 |

```cypher
RETURN 'Matrix' STARTS WITH 'Mat' AS sw, 'Matrix' ENDS WITH 'rix' AS ew,
       'Matrix' CONTAINS 'atr' AS c, 'Matrix' =~ '^M.*x$' AS re;
```

```
 sw | ew | c | re
----+----+---+----
 t  | t  | t | t
```

这四个都不能由索引回答。必须可下推到索引（sargable）的谓词需要 `=` 或范围。[数据类型](/zh/agensgraph/reference/types/)介绍属性对索引可见的形式。

### 算术 {#arithmetic}

`+`、`-`、`*`、`/`、`%` 和 `^` 作用于数字，一元 `+` 和 `-` 表示取负。作用于属性时，它们运行在 `jsonb` 上而不是 SQL 数值类型上，这给 `+` 增加了两个额外职责：拼接两个字符串，以及向列表追加。

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

两个映射相加会被拒绝，错误为 `invalid expression: {"a": 1} + {"b": 2}`。请改用 `jsonb` 拼接运算符合并映射：

```cypher
RETURN {a: 1} || {b: 2} AS merged;
```

```
      merged
------------------
 {"a": 1, "b": 2}
```

要合并到元素而不是值中，使用 `SET n += ` *map*。

### jsonb 运算符 {#jsonb-operators}

属性是 `jsonb`，所以 PostgreSQL 的 `jsonb` 运算符可以直接作用于它。以下是值得了解的运算符：

| 运算符 | 结果 |
| --- | --- |
| *json* `->` *key* / *index* | 成员，类型为 `jsonb`。 |
| *json* `->>` *key* / *index* | 成员，类型为 `text`。 |
| *json* `#>` *path* | 文本数组路径上的值，类型为 `jsonb`。 |
| *json* `#>>` *path* | 文本数组路径上的值，类型为 `text`。 |
| *json* `?` *key* | 键是否存在。 |
| *json* `@>` *json* | 左值是否包含右值。 |
| *json* `<@` *json* | 左值是否被右值包含。 |
| *json* `\|\|` *json* | 拼接：两个对象合并，其他组合生成数组。 |

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

`->>` 返回 `text`，但 Cypher 的 `RETURN` 会把标量列重新装箱为 `jsonb`，所以引号仍在。要得到普通字符串，请用 SQL 包裹查询。见[数据类型](/zh/agensgraph/reference/types/#what-a-return-hands-back)。

两条规则约束 PostgreSQL 其余 `jsonb` 运算符在 Cypher 中的行为，二者都源于 Cypher 拥有算术拼法。

两个 `jsonb` 值之间的 `-` 是减法，所以无法从 Cypher 调用 `jsonb` 的键删除运算符：`properties(m) - 'plot'` 抛出 `invalid expression`。用 SQL 包装或 `REMOVE` 删除键。

原生 `jsonb` 运算符旁边的裸字符串字面量会解析为整个 JSON 文档而不是 JSON 字符串。因此 `m.title || '!'` 以 `Token "!" is invalid` 失败。给运算符一个带类型的操作数，例如 `m.title || to_jsonb('!'::text)`；或者使用采用 Cypher 语义的 `+`。

## 注释 {#comments}

注释从 `--` 到行尾，或从 `/*` 到匹配的 `*/`。块注释可嵌套，因此被注释掉且本身包含注释的区域仍保持配对。`//` 不是注释，而是语法错误。

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

## null 与三值逻辑 {#null-and-three-valued-logic}

`null` 表示*未知*。它不是可以拿来比较的值，也不是属性值。给属性赋 null 会删除它，除非 [`allow_null_properties`](/zh/agensgraph/reference/guc/#allow_null_properties) 开启。

### 真值表 {#truth-tables}

`AND`、`OR` 和 `XOR` 按如下方式扩展到三个值。下表是运行每种组合后的输出：

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

`NOT` 把 true 映射为 false，false 映射为 true，null 映射为 null：

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

因此，只要一侧为 false，`AND` 就是 false；只要一侧为 true，`OR` 就是 true，无论另一侧是什么。其他所有涉及 null 的情况都是 null。

`IN` 遵循同一规则：值没有在包含 null 的列表中找到时，它仍可能在那里，所以结果是 unknown 而不是 false。

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

空列表是例外：没有任何东西在其中，所以即使对 null，结果也是 false。

### 产生 null 的表达式 {#expressions-that-yield-null}

以下表达式产生 null，而不是错误或值：

| 表达式 | 原因 |
| --- | --- |
| `n.no_such_property` | 元素没有这个属性。 |
| `[][0]`、`head([])` | 列表没有这个元素。 |
| `1 + null` | 算术操作数未知。 |
| `1 < null`、`null = null` | 与未知值比较。 |
| `sin(null)`、`toUpper(null)` | 用 null 调用函数。 |

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

`IS NULL` 之所以存在，是因为 `null = null` 是 null。它是测试 null 的唯一方式。

### 条件只接受布尔值 {#a-condition-takes-only-a-boolean}

`WHERE`、`FILTER`、`CASE WHEN` 和其他所有条件都只接受布尔值。求值为 `jsonb` 字符串、数字、列表或映射的条件是错误：

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

这个错误来自条件求值，因此它命名的值是执行器先到达的那一行。完全不是 `jsonb` 的条件会更早被拒绝，即在语句解析时：

```cypher
MATCH (n:t) WHERE 1 RETURN n.name;
```

```
ERROR:  argument of WHERE must be type boolean, not type integer
LINE 1: MATCH (n:t) WHERE 1 RETURN n.name;
                          ^
```

写出你真正要做的测试。`WHERE n.name IS NOT NULL` 询问属性是否存在：

```cypher
MATCH (n:t) WHERE n.name IS NOT NULL RETURN n.name AS name;
```

```
  name
--------
 "Jack"
```

`WHERE n.name <> ''` 询问它是否非空；`WHERE n.active` 只有当属性确实持有布尔值时才可用，因为 `jsonb` 布尔值可以转换为布尔值。

null 仍被接受，并按 SQL 中的方式工作：条件为 null 的行不返回，也不抛出任何错误。因此 `WHERE n.no_such_property` 不返回行。

> [!NOTE]
> 这是对早期版本的有意兼容性中断；早期版本接受非空值作为条件。以那种方式写的查询会失败，而不会按并非本意的条件过滤。
> [Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/#a-condition-takes-only-a-boolean)
> 列出了需要修改的内容。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

三处词法差异会困扰从其他实现了解 Cypher 的读者。

* **标识符折叠为小写，反引号不是引号字符。**请使用双引号。`` `My Label` `` 是语法错误。
* **字符串字面量只能用单引号。**双引号构成标识符。
* **`//` 不是注释。**请使用 `--` 或 `/* */`。

`XOR`、`STARTS WITH`、`ENDS WITH`、`CONTAINS` 和 `=~` 都存在，含义与 openCypher 中相同。

### ISO/IEC 39075 {#isoiec-39075}

本参考使用的记法遵循与标准语法产生式相同的约定，但不是标准的 BNF。

`IS [NOT] UNKNOWN` 是标准中布尔值 null 测试的拼法，与 `IS [NOT] NULL` 一起接受。`XOR` 也是如此。二者都属于标准的 `<boolean value expression>`（ISO/IEC 39075:2024 §20.20）。把 `UNKNOWN` 用作*值*是语法错误。其余内容见[GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)。

## 另见 {#see-also}

- [数据类型](/zh/agensgraph/reference/types/)——`graphid`、`vertex`、`edge`、`graphpath` 和 `jsonb` 属性
- [服务端设置](/zh/agensgraph/reference/guc/)——包括每个会话都需要的 `graph_path`
- [关键字](/zh/agensgraph/appendix/keywords/)——完整关键字表及每个词的类别
- [Cypher、GQL 和 SQL](/zh/agensgraph/concepts/languages/)——应选择哪种语言
- [PostgreSQL: SQL syntax](https://www.postgresql.org/docs/18/sql-syntax.html)——同一词法分析器的 SQL 一侧
