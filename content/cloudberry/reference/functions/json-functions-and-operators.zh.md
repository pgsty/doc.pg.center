---
title: "Apache Cloudberry JSON 函数和操作符"
linkTitle: "JSON 函数和操作符"
description: "使用 Apache Cloudberry 的函数、操作符和 SQL/JSON 路径语言创建与处理 JSON 数据。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/functions/json-functions-and-operators.md"
---

本文介绍：

- 用于处理和创建 JSON 数据的函数和操作符
- SQL/JSON 路径语言

## 处理和创建 JSON 数据 {#process-and-creating-json-data}

Apache Cloudberry 内置了用于创建和操作 JSON 数据的函数和操作符：

- [JSON 操作符](#json-operators)
- [JSON 创建函数](#json-creation-functions)
- [JSON 聚合函数](#json-aggregate-functions)
- [JSON 处理函数](#sqljson-path-language)

### JSON 操作符 {#json-operators}

下表介绍可用于 `json` 和 `jsonb` 数据类型的操作符。

|操作符|右操作数类型|返回类型|描述|示例|示例结果|
|--------|------------------|-----------|-----------|-------|--------------|
|`->`|`int`| `json` 或 `jsonb` | 获取 JSON 数组元素（下标从 0 开始，负整数从末尾计数）。|`'[{"a":"foo"},{"b":"bar"},{"c":"baz"}]'::json->2`|`{"c":"baz"}`|
|`->`|`text`| `json` 或 `jsonb` | 根据键获取 JSON 对象字段。|`'{"a": {"b":"foo"}}'::json->'a'`|`{"b":"foo"}`|
|`->>`|`int`| `text` | 将 JSON 数组元素作为 `text` 获取。|`'[1,2,3]'::json->>2`|`3`|
|`->>`|`text`| `text` | 将 JSON 对象字段作为 `text` 获取。|`'{"a":1,"b":2}'::json->>'b'`|`2`|
|`#>`|`text[]`| `json` 或 `jsonb` | 获取指定路径上的 JSON 对象。|`'{"a": {"b":{"c": "foo"}}}'::json#>'{a,b}`'|`{"c": "foo"}`|
|`#>>`|`text[]`| `text` | 将指定路径上的 JSON 对象作为 `text` 获取。|`'{"a":[1,2,3],"b":[4,5,6]}'::json#>>'{a,2}'`|`3`|

> **注意** 这些操作符针对 `json` 和 `jsonb` 两种数据类型都有对应的变体。字段、元素和路径提取操作符返回的数据类型与左侧输入相同（`json` 或 `jsonb`），但指定返回 `text` 的操作符会将值强制转换为 `text`。如果 JSON 输入的结构无法匹配请求，例如所需元素不存在，字段、元素和路径提取操作符会返回 `NULL`，而不会报错。所有接受整数 JSON 数组下标的字段、元素和路径提取操作符，都支持使用负数下标从数组末尾计数。

以下标准比较操作符可用于 `jsonb`，但不可用于 `json.`。它们遵循 jsonb 索引部分所述的 B-树操作排序规则。

|操作符|描述|
|--------|-----------|
|`<`|小于|
|`>`|大于|
|`<=`|小于或等于|
|`>=`|大于或等于|
|`=`|相等|
|`<>` 或 `!=`|不相等|

> **注意** 解析器会在解析阶段将 `!=` 操作符转换为 `<>`。因此，无法实现功能不同的 `!=` 和 `<>` 操作符。

下表介绍要求左操作数为 `jsonb` 数据类型的操作符。其中许多操作符可以通过 `jsonb` 操作符类使用索引。

|操作符|右操作数类型|描述|示例|
|--------|------------------|-----------|-------|
|`@>`|`jsonb`|左侧 JSON 值是否在顶层包含右侧 JSON 路径/值条目？|`'{"a":1, "b":2}'::jsonb @> '{"b":2}'::jsonb`|
|`<@`|`jsonb`|左侧 JSON 路径/值条目是否包含在右侧 JSON 值的顶层中？|`'{"b":2}'::jsonb <@ '{"a":1, "b":2}'::jsonb`|
|`?`|`text`|该*字符串*是否作为顶层键存在于 JSON 值中？|`'{"a":1, "b":2}'::jsonb ? 'b'`|
|`?\|` |`text[]`|这些数组*字符串*中是否有任意一个作为顶层键存在？|`'{"a":1, "b":2, "c":3}'::jsonb ?\| array['b', 'c']`|
|`?&`|`text[]`|这些数组*字符串*是否全部作为顶层键存在？|`'["a", "b"]'::jsonb ?& array['a', 'b']`|
| `\|\|` | `jsonb` | 将两个 `jsonb` 值连接为一个新的 `jsonb` 值。 | `'["a", "b"]'::jsonb \|\| '["c", "d"]'::jsonb` |
| `-` | `text` | 从左操作数中删除键值对或*字符串*元素。键值对根据其键的值进行匹配。| `'{"a": "b"}'::jsonb - 'a'` |
| `-` | `text[]` | 从左操作数中删除多个键值对或*字符串*元素。键值对根据其键的值进行匹配。| `'{"a": "b", "c": "d"}'::jsonb - '{a,c}'::text[]` |
| `-` | `integer` | 删除指定下标的数组元素（负整数从末尾计数）。如果顶层容器不是数组，则抛出错误。| `'["a", "b"]'::jsonb - 1` |
| `#-` | `text[]` | 删除指定路径上的字段或元素（对于 JSON 数组，负整数从末尾计数）。 | `'["a", {"b":1}]'::jsonb #- '{1,b}'` |
| `@?` | `jsonpath` | 对于指定的 JSON 值，JSON 路径是否返回任意项？| `'{"a":[1,2,3,4,5]}'::jsonb @? '$.a[*] ? (@ > 2)'` |
| `@@` | `jsonpath` | 返回对指定 JSON 值执行 JSON 路径谓词检查的结果。只考虑结果中的第一项。如果结果不是布尔值，则返回 `null`。| `'{"a":[1,2,3,4,5]}'::jsonb @@ '$.a[*] > 2'` |

> **注意** `||` 操作符连接两个 JSON 对象时，会生成一个包含两者键并集的对象；遇到重复键时，采用第二个对象的值。其他情况都生成 JSON 数组：先将所有非数组输入转换为单元素数组，再连接两个数组。该操作不会递归进行，只合并顶层数组或对象结构。

> **注意** `@?` 和 `@@` 操作符会抑制以下错误：缺少对象字段或数组元素、JSON 项类型不符合预期，以及数值错误。在搜索结构各异的 JSON 文档集合时，这种行为可能很有帮助。

### JSON 创建函数 {#json-creation-functions}

下表介绍用于创建 `json` 和 `jsonb` 数据类型值的函数。（对于 `jsonb`，没有与 `row_to_json()` 和 `array_to_json()` 对应的函数。不过，`to_jsonb()` 函数提供了基本相同的功能。）

|函数|描述|示例|示例结果|
|--------|-----------|-------|--------------|
|`to_json(anyelement)` <br /> `to_jsonb(anyelement)`|将值作为 `json` 或 `jsonb` 对象返回。数组和复合类型分别递归转换为数组和对象；否则，如果输入类型提供了到 `json` 的类型转换，就使用该类型转换函数完成转换；再否则，生成一个标量值。对于数字、布尔值和空值以外的标量类型，使用其文本表示，并使其成为有效的 `json` 或 `jsonb` 值。|`to_json('Fred said "Hi."'::text)` |`"Fred said "Hi.""`|
|`array_to_json(anyarray [, pretty_bool])`|将数组作为 JSON 数组返回。多维数组变为由数组组成的 JSON 数组。如果 `pretty_bool` 为 true，则在第一维的元素之间添加换行符。|`array_to_json('{{1,5},{99,100}}'::int[])`|`[[1,5],[99,100]]`|
|`row_to_json(record [, pretty_bool])`|将行作为 JSON 对象返回。如果 `pretty_bool` 为 true，则在第一层元素之间添加换行符。|`row_to_json(row(1,'foo'))`|`{"f1":1,"f2":"foo"}`|
|`json_build_array(VARIADIC "any")` <br /> `jsonb_build_array(VARIADIC "any")`|根据 `VARIADIC` 参数列表构建 JSON 数组，其中各元素的类型可以不同。|`json_build_array(1,2,'3',4,5)`|`[1, 2, "3", 4, 5]`|
|`json_build_object(VARIADIC "any")` <br /> `jsonb_build_object(VARIADIC "any")`|根据 `VARIADIC` 参数列表构建 JSON 对象。按顺序取出参数列表中的参数，并转换为一组键值对。|`json_build_object('foo',1,'bar',2)`|`{"foo": 1, "bar": 2}`|
|`json_object(text[])`<br />`jsonb_object(text[])`| 根据文本数组构建 JSON 对象。该数组必须是一维且成员数量为偶数，此时交替将成员用作键和值；或者是二维且每个内层数组恰好包含两个元素，将这两个元素用作一个键值对。 |`json_object('{a, 1, b, "def", c, 3.5}')` <br/><br/> `json_object('{{a, 1},{b, "def"},{c, 3.5}}')`|`{"a": "1", "b": "def", "c": "3.5"}`|
|`json_object(keys text[], values text[])` <br/> `jsonb_object(keys text[], values text[])`|根据文本数组构建 JSON 对象。这种形式的 `json_object` 从两个独立数组中成对获取键和值，其他方面与单参数形式完全相同。|`json_object('{a, b}', '{1,2}')`|`{"a": "1", "b": "2"}`|

> **注意** 除了提供美化输出选项外，`array_to_json()` 和 `row_to_json()` 的行为与 `to_json()` 相同。对 `to_json()` 的行为说明，同样适用于其他 JSON 创建函数所转换的每个值。

> **注意** hstore 扩展提供了从 `hstore` 到 `json` 的类型转换，因此通过 JSON 创建函数转换的 `hstore` 值会表示为 JSON 对象，而不是基本字符串值。

### JSON 聚合函数 {#json-aggregate-functions}

下表列出将记录聚合为 JSON 对象数组，以及将成对的值聚合为 JSON 对象的函数。

|函数|参数类型|返回类型|描述|
|--------|--------------|-----------|-----------|
|`json_agg(record)` <br /> `jsonb_agg(record)`|`record`|`json`|将记录聚合为由对象组成的 JSON 数组。|
|`json_object_agg(name, value)` <br /> `jsonb_object_agg(name, value)`|`("any", "any")`|`json`|将名称/值对聚合为 JSON 对象。|

### SQL/JSON 路径语言 {#sqljson-path-language}

SQL/JSON 路径表达式指定要从 JSON 数据中检索的项，类似于 SQL 访问 XML 时使用的 XPath 表达式。在 Apache Cloudberry 中，路径表达式通过 `jsonpath` 数据类型实现。

JSON 查询函数和操作符会将给定的路径表达式交给*路径引擎*求值。如果表达式匹配所查询的 JSON 数据，就返回相应的 SQL/JSON 项。路径表达式使用 SQL/JSON 路径语言编写，也可以包含算术表达式和函数。查询函数将给定表达式视为文本字符串，因此必须用单引号将其括起。

路径表达式由 `jsonpath` 数据类型允许的一系列元素组成。路径表达式从左向右求值，但可以使用括号改变运算顺序。如果求值成功，就会产生一系列 SQL/JSON 项（*SQL/JSON 序列*），并将求值结果返回给 JSON 查询函数，由其完成指定的计算。

要在路径表达式中引用待查询的 JSON 数据（*上下文项*），可使用 `$` 符号。其后可以跟一个或多个访问操作符，逐层深入 JSON 结构，获取上下文项的内容。后续每个操作符都处理前一步求值的结果。

例如，假设要解析以下来自 GPS 跟踪器的 JSON 数据：

```shell
{
  "track": {
    "segments": [
      {
        "location":   [ 47.763, 13.4034 ],
        "start time": "2018-10-14 10:05:14",
        "HR": 73
      },
      {
        "location":   [ 47.706, 13.2635 ],
        "start time": "2018-10-14 10:39:21",
        "HR": 135
      }
    ]
  }
}
```

要检索已有的轨迹段，需要对前面的每个 JSON 对象使用 `.<key>` 访问操作符：

```shell
'$.track.segments'
```

如果要检索的项是数组元素，必须使用 `[*]` 操作符展开该数组。例如，以下路径返回所有已有轨迹段的位置坐标：

```shell
'$.track.segments[*].location'
```

如果只想返回第一个轨迹段的坐标，可以在 `[]` 访问操作符中指定相应下标。注意，SQL/JSON 数组的下标从 0 开始：

```shell
'$.track.segments[0].location'
```

路径求值每一步的结果，都可以由下文 [SQL/JSON 路径操作符和方法](#sqljson-path-operators-and-methods)中列出的一个或多个 `jsonpath` 操作符和方法处理。每个方法名前都必须加一个点。例如，可以获取数组大小：

```shell
'$.track.segments.size()'
```

关于在路径表达式中使用 `jsonpath` 操作符和方法的更多示例，请参阅下文的 [SQL/JSON 路径操作符和方法](#sqljson-path-operators-and-methods)。

定义路径时，还可以使用一个或多个*过滤表达式*，其作用类似于 SQL 的 `WHERE` 子句。过滤表达式以问号开头，并在括号中给出条件：

```shell
? (condition)
```

过滤表达式必须紧跟在其作用的路径求值步骤之后。该步骤的结果将被过滤，只保留满足给定条件的项。SQL/JSON 定义了三值逻辑，因此条件可以为 `true`、`false` 或 `unknown`。`unknown` 值的作用与 SQL `NULL` 相同，可以用 is `unknown` 谓词进行检测。后续路径求值步骤只使用过滤表达式返回 `true` 的项。

过滤表达式可用的函数和操作符列于 [jsonpath 过滤表达式元素](#sqljson-filter-expression-elements)。待过滤的路径求值结果用 `@` 变量表示。要引用位于更深嵌套层级的 JSON 元素，可在 `@` 后添加一个或多个访问操作符。

假设要检索所有高于 130 的心率值，可以使用以下表达式：

```shell
'$.track.segments[*].HR ? (@ > 130)'
```

如果要获取具有这些心率值的轨迹段的开始时间，就需要先滤除不相关的轨迹段，再返回开始时间。因此，过滤表达式要作用于前一步，条件中使用的路径也有所不同：

```shell
'$.track.segments[*] ? (@.HR > 130)."start time"'
```

如有需要，可以在同一嵌套层级使用多个过滤表达式。例如，以下表达式选择位置坐标符合条件且心率较高的所有轨迹段：

```shell
'$.track.segments[*] ? (@.location[1] < 13.4) ? (@.HR > 130)."start time"'
```

也可以在不同嵌套层级使用过滤表达式。以下示例先按位置过滤所有轨迹段，再返回这些轨迹段中较高的心率值（如果存在）：

```shell
'$.track.segments[*] ? (@.location[1] < 13.4).HR ? (@ > 130)'
```

过滤表达式还可以相互嵌套：

```shell
'$.track ? (exists(@.segments[*] ? (@.HR > 130))).segments.size()'
```
如果轨迹包含任何心率较高的轨迹段，该表达式返回轨迹的大小；否则返回空序列。

### 与标准的差异 {#deviations-from-standard}

Apache Cloudberry 的 SQL/JSON 路径语言实现与 SQL/JSON 标准存在以下差异：

- 尚未实现 `.datetime()` 项方法，主要原因是不可变的 `jsonpath` 函数和操作符无法引用会话时区，而某些日期时间操作需要使用会话时区。Apache Cloudberry 的未来版本将为 `jsonpath` 增加日期时间支持。
- 路径表达式可以是布尔谓词，尽管 SQL/JSON 标准只允许在过滤器中使用谓词。这是实现 `@@` 操作符所必需的。例如，以下 `jsonpath` 表达式在 Apache Cloudberry 中有效：

    ```shell
    '$.track.segments[*].HR < 70'
    ```
- 对 `like_regex` 过滤器中使用的正则表达式模式的解释略有不同，详见[正则表达式](#regular-expressions)。

### 严格模式和宽松模式 {#strict-and-lax-modes}

查询 JSON 数据时，路径表达式可能与实际 JSON 数据结构不匹配。尝试访问不存在的对象成员或数组元素会产生结构错误。SQL/JSON 路径表达式有两种处理结构错误的模式：

- lax（宽松，默认）——路径引擎隐式调整所查询的数据，使其适应指定路径。剩余的结构错误都会被抑制，并转换为空的 SQL/JSON 序列。

- strict（严格）——出现结构错误时抛出错误。

当 JSON 数据不符合预期模式时，宽松模式便于 JSON 文档结构与路径表达式相互匹配。如果某个操作数不满足特定操作的要求，可以在执行该操作前，将其自动包装为 SQL/JSON 数组，或者将其元素转换为 SQL/JSON 序列以进行展开。此外，比较操作符在宽松模式下会自动展开操作数，因此可以直接比较 SQL/JSON 数组。大小为 1 的数组被视为与其唯一元素相等。仅在以下情况下不进行自动展开：

- 路径表达式包含 `type()` 或 `size()` 方法，它们分别返回类型和数组中的元素个数。

- 查询的 JSON 数据包含嵌套数组。此时只展开最外层数组，所有内层数组保持不变。因此，每一步路径求值中的隐式展开最多只能深入一层。

例如，在宽松模式下查询上述 GPS 数据时，可以不必理会其中的轨迹段存储在数组中这一点：

```shell
'lax $.track.segments.location'
```

在严格模式下，指定路径必须与所查询 JSON 文档的结构完全匹配，才能返回 SQL/JSON 项，因此使用上述路径表达式会报错。要得到与宽松模式相同的结果，必须显式展开 segments 数组：

```shell
'strict $.track.segments[*].location'
```

在宽松模式下使用 `.**` 访问操作符可能产生意外结果。例如，以下查询会将每个 HR 值选取两次：

```shell
lax $.**.HR
```

这是因为 `.**` 访问操作符既选取 segments 数组，也选取它的每个元素，而宽松模式下的 `.HR` 访问操作符会自动展开数组。为避免意外结果，建议只在严格模式下使用 `.**` 访问操作符。以下查询只会选取每个 HR 值一次：

```shell
strict $.**.HR
```

### 正则表达式 {#regular-expressions}

SQL/JSON 路径表达式允许使用 `like_regex` 过滤器，将文本与正则表达式进行匹配。例如，以下 SQL/JSON 路径查询会以不区分大小写的方式，匹配数组中所有以英语元音字母开头的字符串：

```shell
'$[*] ? (@ like_regex "^[aeiou]" flag "i")'
```

可选的标志字符串可以包含以下一个或多个字符：`i` 表示不区分大小写匹配；`m` 允许 `^` 和 `$` 在换行处匹配；`s` 允许 `.` 匹配换行符；`q` 将整个模式视为字面文本（使其成为简单的子串匹配）。

SQL/JSON 标准的正则表达式定义来自 `LIKE_REGEX` 操作符，而该操作符使用 XQuery 标准。Apache Cloudberry 目前不支持 `LIKE_REGEX` 操作符。因此，`like_regex` 过滤器使用 [POSIX 正则表达式](https://www.postgresql.org/docs/12/functions-matching.html#FUNCTIONS-POSIX-REGEXP)中描述的 POSIX 正则表达式引擎实现。这导致其行为与标准 SQL/JSON 存在一些细微差异，详见[与 XQuery（LIKE_REGEX）的差异](https://www.postgresql.org/docs/12/functions-matching.html#POSIX-VS-XQUERY)。但需注意，其中所述的标志字母不兼容问题不适用于 SQL/JSON，因为它会将 XQuery 标志字母转换为 POSIX 引擎所需的形式。

请记住，`like_regex` 的模式参数是一个 JSON 路径字符串字面量，须按照 jsonpath 类型部分给出的规则编写。特别是，在正则表达式中使用的所有反斜杠都必须写两次。例如，要匹配根文档中只包含数字的字符串值：

```shell
$.* ? (@ like_regex "^\\d+$")
```

### SQL/JSON 路径操作符和方法 {#sqljson-path-operators-and-methods}

下表介绍 `jsonpath` 可用的操作符和方法：

| 操作符/方法 | 描述 | 示例 JSON | 示例查询 | 结果 |
|-----------------|-------------|--------------|---------------|--------|
| `+`（一元） | 遍历 SQL/JSON 序列的一元正号操作符 | `{"x": [2.85, -14.7, -9.4]}` | `+ $.x.floor()` | `2, -15, -10` |
| `-`（一元） | 遍历 SQL/JSON 序列的一元负号操作符 | `{"x": [2.85, -14.7, -9.4]}` | `- $.x.floor()` | `-2, 15, 10` |
| `+`（二元） | 加法 | `[2]` | `2 + $[0]` | `4` |
| `-`（二元） | 减法 | `[2]` | `4 - $[0]` | `2` |
| `*` | 乘法 | `[4]` | `2 * $[0]` | `8` |
| `/` | 除法 | `[8]` | `$[0] / 2` | `4` |
| `%` | 取模 | `[32]` | `$[0] % 10` | `2` |
| `type()` | SQL/JSON 项的类型 | `[1, "2", {}]` | `$[*].type()` | `"number", "string", "object"` |
| `size()` | SQL/JSON 项的大小 | `{"m": [11, 15]}` | `$.m.size()` | `2` |
| `double()` | 将 SQL/JSON 数字或字符串转换为近似浮点数 | `{"len": "1.9"}` | `$.len.double() * 2` | `3.8` |
| `ceiling()` | 大于或等于 SQL/JSON 数字的最小整数 | `{"h": 1.3}` | `$.h.ceiling()` | `2` |
| `floor()` | 小于或等于 SQL/JSON 数字的最大整数 | `{"h": 1.3}` | `$.h.floor()` | `1` |
| `abs()` | SQL/JSON 数字的绝对值 | `{"z": -0.3}` | `$.z.abs()` | `0.3` |
| `keyvalue()` | 对象的键值对序列，表示为一个数组，其中每一项包含三个字段（`"key"`、`"value"` 和 `"id"`）。`"id"` 是该键值对所属对象的唯一标识符。 | `{"x": "20", "y": 32}` | `$.keyvalue()` | `{"key": "x", "value": "20", "id": 0}, {"key": "y", "value": 32, "id": 0}` |

### SQL/JSON 过滤表达式元素 {#sqljson-filter-expression-elements}

下表介绍 `jsonpath` 可用的过滤表达式元素：

| 值/谓词 | 描述 | 示例 JSON | 示例查询 | 结果 |
|-----------------|-------------|--------------|---------------|--------|
| `==` | 相等操作符 | `[1, 2, 1, 3]` | `$[*] ? (@ == 1)` | `1, 1` |
| `!=` | 不等操作符 | `[1, 2, 1, 3]` | `$[*] ? (@ != 1)` | `2, 3` |
| `<>` | 不等操作符（与 `!=` 相同） | `[1, 2, 1, 3]` | `$[*] ? (@ <> 1)` | `2, 3` |
| `<` | 小于操作符 | `[1, 2, 3]` | `$[*] ? (@ < 2)` | `1` |
| `<=` | 小于或等于操作符 | `[1, 2, 3]` | `$[*] ? (@ <= 2)` | `1, 2` |
| `>` | 大于操作符 | `[1, 2, 3]` | `$[*] ? (@ > 2)` | `3` |
| `>=` | 大于或等于操作符 | `[1, 2, 3]` | `$[*] ? (@ >= 2)` | `2, 3` |
| `true` | 用于与 JSON `true` 字面量比较的值 | `[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]` | `$[*] ? (@.parent == true)` | `{"name": "Chris", "parent": true}` |
| `false` | 用于与 JSON `false` 字面量比较的值 | `[{"name": "John", "parent": false}, {"name": "Chris", "parent": true}]` | `$[*] ? (@.parent == false)` | `{"name": "John", "parent": false}` |
| `null` | 用于与 JSON `null` 值比较的值 | `[{"name": "Mary", "job": null}, {"name": "Michael", "job": "driver"}]` | `$[*] ? (@.job == null) .name` | `"Mary"` |
| `&&` | 布尔 AND | `[1, 3, 7]` | `$[*] ? (@ > 1 && @ < 5)` | `3` |
| `\|\|` | 布尔 OR | `[1, 3, 7]` | `$[*] ? (@ < 1 \|\| @ > 5)` | `7` |
| `!` | 布尔 NOT | `[1, 3, 7]` | `$[*] ? (!(@ < 5))` | `7` |
| `like_regex` | 检查第一个操作数是否匹配第二个操作数给出的正则表达式；可选的 `flag` 字符串用于指定匹配方式的调整。 | `["abc", "abd", "aBdC", "abdacb", "babc"]` | `$[*] ? (@ like_regex "^ab.*c" flag "i")` | `"abc", "aBdC", "abdacb"` |
| `starts with` | 检查第二个操作数是否为第一个操作数的起始子串 | `["John Smith", "Mary Stone", "Bob Johnson"]` | `$[*] ? (@ starts with "John")` | `"John Smith"` |
| `exists` | 检查路径表达式是否至少匹配一个 SQL/JSON 项 | `{"x": [1, 2], "y": [2, 4]}` | `strict $.* ? (exists (@ ? (@[*] > 2)))` | `2, 4` |
| `is unknown` | 检查布尔条件是否为 `unknown` | `[-1, 2, 7, "infinity"]` | `$[*] ? ((@ > 0) is unknown)` | `"infinity"` |
