---
title: 字符串函数
linkTitle: 字符串函数
description: 作用于文本的函数。
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/string.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


作用于文本的函数。属性以 `jsonb` 形式到达，其中若干函数同时具有 `text` 和 `jsonb` 重载。解析器选择哪一个取决于传入内容，因此字面量和属性的行为不一定相同。凡是有影响的地方，条目中都会说明。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## left {#left}

```
left ( string jsonb, n jsonb ) -> jsonb
left ( string text, n integer ) -> text
```

返回字符串的前 `n` 个字符。

**注意事项**

- 带整数字面量的属性是**有歧义的**，因为 `left(jsonb, jsonb)` 和 `left(text, integer)` 的匹配程度相同：

```cypher
MATCH (m:movie {title:'Blade Runner 2049'}) RETURN left(m.title, 12);
```

```
ERROR:  function left(jsonb, integer) is not unique
LINE 1: ...ATCH (m:movie {title:'Blade Runner 2049'}) RETURN left(m.tit...
                                                             ^
HINT:  Could not choose a best candidate function. You might need to add explicit type casts.
```

  转换字符串类型，例如 `left(m.title::text, 12)`，或使用没有这种冲突的 [`substring`](#substring)。
- `n` 大于字符串长度时返回整个字符串。

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

返回小写字符串。这是 PostgreSQL 自身的函数；因为 `jsonb` 字符串可转换为 `text`，所以能从 Cypher 调用。[`toLower`](#tolower) 是 Cypher 拼写，直接接收 `jsonb`。

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

移除字符串开头的空白字符。

**注意事项**

- 仅移除空白字符。没有接收要移除字符集合的形式；请改用 PostgreSQL 的 `ltrim(text, text)`。

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

用一个子串替换另一个子串的每次出现。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `string` | `jsonb` | 要搜索的字符串。 |
| `old` | `jsonb` | 要查找的子串。每次出现都会替换，而不只是第一次。 |
| `new` | `jsonb` | 替换内容。可以比 `old` 更长或更短，也可以为空。 |

**注意事项**

- `old` 和 `new` 的长度不必相同。
- `old` 未出现时，字符串原样返回。

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

反转字符串或列表。

**注意事项**

- 得到哪个重载取决于参数，而两个重载对字符串的处理不一致。字符串*字面量*解析为 `reverse(text)`，会被反转。字符串*属性*已经是 `jsonb`，因此解析为 `reverse(jsonb)`；该重载只反转数组：

```cypher
RETURN reverse('Blade Runner 2049'::jsonb);
```

```
ERROR:  reverse(): list is expected but "Blade Runner 2049"
```

  属性引用的行为与这个转换相同，因为它已经是 `jsonb`。要反转字符，请向另一方向转换：`reverse(m.title::text)`。
- 列表属性不需要转换。`jsonb` 重载会反转列表。

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

返回字符串的最后 `n` 个字符。对于带整数字面量的属性，它与 [`left`](#left) 有同样的歧义，也有同样的两种解决方法。

## rTrim {#rtrim}

```
rTrim ( string jsonb ) -> jsonb
```

移除字符串末尾的空白字符。示例见 [`lTrim`](#ltrim)。

## split {#split}

```
split ( string text, delimiter text ) -> anyarray
```

在每个分隔符出现的位置把字符串切分成列表。

**注意事项**

- 值是字符串数组。目录把返回类型声明为 `anyarray`，因此 SQL 中的 `pg_typeof` 报告 `anyarray`。Cypher 的 `RETURN` 会把它装箱为 `jsonb` 列表。
- 分隔符未出现时，返回包含整个字符串的单元素列表。
- 分隔符是字面字符串，不是模式。要使用正则表达式，请用 PostgreSQL 的 `regexp_split_to_array`。

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

以 `integer` 返回字符串的字符数。

**注意事项**

- [`size`](/zh/agensgraph/reference/functions/scalar/#size) 和 [`length`](/zh/agensgraph/reference/functions/scalar/#length) 是 Cypher 拼写，返回 `jsonb`。此函数为需要原生 `integer` 的调用者而存在，使其不必解包结果。驱动程序，或包在 Cypher 查询外的 SQL，就是这样的调用者。

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

返回字符串的一部分，从 `start` 开始，直到字符串末尾或持续 `count` 个字符。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `string` | `jsonb` | 要切分的字符串。 |
| `start` | `jsonb` | 第一个字符的 0 起始偏移量。 |
| `count` | `jsonb` | 要取多少字符。省略时取字符串剩余部分。`count` 超出末尾时就在末尾停止。 |

**注意事项**

- `start` 从 0 开始，而 SQL 的 `substring` 从 1 开始。解析器会为你加上 1，因此请直接写想要的偏移量。
- 与 [`left`](#left) 和 [`right`](#right) 不同，它对属性没有歧义，因此是取属性前缀的更安全方法。

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

返回小写字符串。

**注意事项**

- 接收 `jsonb`，因此与 [`reverse`](#reverse) 不同，属性不需要转换。
- [`lower`](#lower) 是 PostgreSQL 的等价函数，也可使用。两者只在接收和返回的类型上不同。

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

返回大写字符串。示例见 [`toLower`](#tolower)。

## trim {#trim}

```
trim ( string jsonb ) -> jsonb
```

移除字符串两端的空白字符。

**注意事项**

- `trim` 既是语法形式，也是函数名，因此这里只接收一个参数。SQL 的 `trim(BOTH 'x' FROM str)` 拼写在 Cypher 中不可用：

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

返回大写字符串。这是 PostgreSQL 自身的函数；参见 [`lower`](#lower)。

## 不通过函数进行匹配 {#matching-without-a-function}

四个字符串测试是操作符而不是函数；每个操作符在目录中都有一个你不会输入的名称：

| 操作符 | 实现者 | 返回 true 的条件 |
| --- | --- | --- |
| `STARTS WITH` | `string_starts_with` | 左字符串以右字符串开头 |
| `ENDS WITH` | `string_ends_with` | 左字符串以右字符串结尾 |
| `CONTAINS` | `string_contains` | 右字符串出现在左字符串的任意位置 |
| `=~` | `string_regex` | 左字符串匹配作为正则表达式的右字符串 |

```cypher
MATCH (m:movie) WHERE m.title STARTS WITH 'The Matrix' RETURN count(*) AS n;
```

```
 n
---
 4
```

这四个操作符都不能使用属性索引。每个操作符都是对属性执行的函数调用，而不是与属性的比较；因此用其中之一过滤的查询会扫描该标签。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

openCypher 把大小写函数拼作 `toLower` 和 `toUpper`，把修剪函数拼作 `lTrim`、`rTrim` 和 `trim`；这五个都可用。openCypher 的 `substring` 从 0 开始，这里相同。`left` 和 `right` 是 PostgreSQL 函数，openCypher 也有定义。属性带整数字面量时的歧义是偏差；`substring` 是可移植形式。

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [类型转换函数](/zh/agensgraph/reference/functions/type-conversion/) — `toString`、`toStringList`
- [列表函数](/zh/agensgraph/reference/functions/list/) — `split` 返回的内容
