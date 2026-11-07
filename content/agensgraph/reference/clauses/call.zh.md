---
title: CALL 子句
linkTitle: CALL 子句
description: 在查询管道内运行例程。
type: docs
weight: 220
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/call.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**  **2.18 新增**

在查询管道内运行例程。该例程可以是名称已固定的函数，其结果行会连接到工作表；也可以是内联编写的子查询。

## 语法概要 {#synopsis}

```text
[ OPTIONAL ] CALL function( [ argument [, argument ] ... ] ) YIELD yield_list
[ OPTIONAL ] CALL [ variable_scope ] { subquery }
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`CALL` 有两种形式，采用哪一种由紧跟关键字之后的词法单元决定：

- `CALL` 后接**名称**时是命名例程形式。它调用一个函数，并把必需的
  `YIELD` 列表中列出的列添加到工作行。参见
  [`CALL … YIELD`](/zh/agensgraph/reference/clauses/call-yield/)。
- `CALL` 后接 `(` 或 `{` 时是内联形式。它运行花括号中的子查询，并可选择是否对每个输入行运行一次。参见
  [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/)。

`OPTIONAL` 可以加在任一形式之前。它会保留例程或子查询未产生结果行的输入行，并把该调用本应返回的所有内容绑定为
null。参见[`OPTIONAL CALL`](/zh/agensgraph/reference/clauses/optional-call/)。

### CALL 调用什么 {#what-call-invokes}

在 GQL 中，`CALL` 调用的对象是*过程*。AgensGraph 没有自己的过程目录。
`CALL … YIELD` 会按 PostgreSQL 的普通函数解析名称，而原生安装没有注册任何过程。

```sql
SELECT count(*) AS procedures FROM pg_proc WHERE prokind = 'p';
```

```
 procedures
------------
          0
(1 row)
```

因此，这里的“调用过程”就是“调用函数”。任何函数都可用，其形状决定 `YIELD` 可以命名什么：

| 函数形状 | `YIELD` 看到的内容 |
| --- | --- |
| 标量函数，例如 `length(text)` | 一列，以函数名命名 |
| 集合返回函数，例如 `generate_series(int, int)` | 一列，以函数名命名；每个元素一行 |
| 复合函数或 `RETURNS TABLE`，例如 `jsonb_each_text(jsonb)` | 每个输出字段一列，使用字段名 |
| 以上任一种，且使用函数自身名称 | 整行；前提是没有输出列使用该名称。返回 `RETURNS SETOF vertex` 的函数会以这种方式产出顶点 |

yield 项只能是这些内容，不能是其他内容。函数未返回的名称会被拒绝，即使查询更早位置已经绑定了同名变量。

PostgreSQL 自身的 `CALL` 语句是另一回事：它是顶层 SQL 语句，要求真实的
过程，并且不是 Cypher 子句。二者不重叠，各自都会拒绝对方的目标。

## 参数 {#parameters}

function
: 要调用的函数的名称。如果 `search_path` 找不到它，请加上模式限定。过程会被拒绝：
  `<name>() is a procedure`，提示为 `To call a
  procedure, use CALL`。

argument
: 值表达式，对每个输入行求值。参数可以引用查询更早位置绑定的变量，这会使调用成为相关调用。属性访问产生
  `jsonb`，因此当参数是其他类型时应进行转换。

variable_scope
: 内联子查询可以看见哪些外部变量：`(v, w)` 表示只看见列出的变量，`(*)`
  表示全部变量，`()` 表示不导入任何变量。**省略该子句不会导入任何变量**。参见
  [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/)；该页首先说明的就是这条规则。

yield_list
: `*`，或函数的一个或多个输出列；每一列都可以用 `AS` 重命名。该列表是必需的。参见
  [`CALL … YIELD`](/zh/agensgraph/reference/clauses/call-yield/)。

subquery
: 以 `RETURN` 结尾的只读查询。写子句会被拒绝。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

调用集合返回函数，并把其结果行连接到匹配的电影：

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_array_elements_text(m.embedding) YIELD jsonb_array_elements_text AS d
RETURN d ORDER BY d;
```

```
       d
---------------
 "-0.07594558"
 "-0.11921061"
 "0.04081754"
 "0.29592122"
(4 rows)
```

### 用子查询逐行计算值 {#compute-a-value-per-row-with-a-subquery}

内联形式可为每个输入行回答一个问题，同时让主体不进入主模式：

```cypher
MATCH (m:movie {genre: 'Adventure'})
CALL (m) { MATCH (p:person)-[:acted_in]->(m) RETURN count(p) AS cast_size }
RETURN m.title AS film, cast_size;
```

```
      film       | cast_size
-----------------+-----------
 "Jurassic Park" | 1
(1 row)
```

### 尝试调用过程 {#try-to-call-a-procedure}

过程是 `CALL … YIELD` 唯一不接受的一类例程：

```sql
CREATE PROCEDURE noop() LANGUAGE sql AS 'SELECT 1';
```

```
CREATE PROCEDURE
```

```cypher
MATCH (m:movie) CALL noop() YIELD * RETURN count(*);
```

```
ERROR:  noop() is a procedure
LINE 1: MATCH (m:movie) CALL noop() YIELD * RETURN count(*);
                        ^
HINT:  To call a procedure, use CALL.
```

而函数是 SQL `CALL` 语句唯一不接受的一类例程：

```sql
CALL generate_series(1, 3);
```

```
ERROR:  generate_series(integer, integer) is not a procedure
LINE 1: CALL generate_series(1, 3);
             ^
HINT:  To call a function, use SELECT.
```

## 说明 {#notes}

词法分析器通过向前查看一个词法单元来区分两种形式。因此 `call` 仍可用作普通标识符：
`MATCH (call:movie) RETURN count(call)` 仍然有效，SQL 语句 `CALL myproc()` 也一样。

命名例程形式是**中间**子句：它不能开启查询，也不能结束查询。内联形式可以开启查询，但只有在没有作用域子句时才可以。前面没有任何子句却使用作用域子句时，会引发
`CALL has no preceding clause to import
variables from`。

## 兼容性 {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> 在 §14.5 *call query statement* 的查询位置实现 GQL *call procedure statement* 和
> *procedure call*（ISO/IEC 39075:2024 §15.1）。
>
> - **支持**——标准定义的两种过程调用形式，即 §15.2 的内联调用与
>   §15.3 的命名调用；两者都可加可选的 `OPTIONAL` 前缀。
> - **不支持**——*call data-modifying procedure statement*（§13.6）：被调用的例程或子查询不得写入图。同样不支持的还有
>   GQL 过程目录——§17.5 的过程引用会解析为 PostgreSQL 函数，并且标准中的
>   `QUERY PROCEDURE` 标识没有对应物。
> - **偏差**——标准允许命名调用省略 `YIELD` 子句（§15.3）。AgensGraph 要求该子句。
>
> 在 [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)中跟踪状态。

### openCypher {#opencypher}

openCypher 的 `CALL db.labels()` 过程调用风格可以映射到命名形式，但名称不同：这里没有
`db.*` 或 `dbms.*` 命名空间。请改用 PostgreSQL 目录和 `\dGv` / `\dGe`
元命令，或直接读取 [ag_label](/zh/agensgraph/system-catalogs/catalogs/)。

删除示例创建的例程：

```sql
DROP PROCEDURE noop();
```

## 另见 {#see-also}

- [`CALL … YIELD`](/zh/agensgraph/reference/clauses/call-yield/) **GQL**——命名例程形式的详细说明
- [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) **GQL**——内联形式及其导入列表
- [`OPTIONAL CALL`](/zh/agensgraph/reference/clauses/optional-call/) **GQL**——保留输入行的形式
- [子查询值表达式](/zh/agensgraph/reference/clauses/subquery-expressions/) **GQL**——作为表达式而非子句的子查询
- [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)
