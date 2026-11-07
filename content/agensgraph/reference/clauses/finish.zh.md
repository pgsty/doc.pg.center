---
title: FINISH 子句
linkTitle: FINISH 子句
description: 结束查询而不投影任何内容：工作会执行，查询返回空结果。
type: docs
weight: 200
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/finish.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**  **2.18 新增**

结束查询而不投影任何内容：工作会执行，查询返回空结果。

## 语法概要 {#synopsis}

```text
FINISH
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

每个查询都必须以 `RETURN`、`FINISH` 或写子句结束。`FINISH`
表示“不产生结果”的结尾：它不接收参数、不投影列，并关闭语句。

- `FINISH` 必须是**最后一个**子句。其后的任何内容都会引发 `FINISH must be at
  the end of the query`。
- 在读取之后，`FINISH` 会丢弃行。规划器把它实现为 `LIMIT 0`，因此扫描会被打开，但不会取回任何行。
- 在写入之后，写入仍会发生。`FINISH` 只抑制投影。
- 以 `FINISH` 结尾的查询返回**空结果**：没有列，也没有行。`psql`
  会把它打印为 `--` 表头加 `(0 rows)`，而 `\gdesc` 会报告
  `The command has no result, or the result has no columns.`
- 以 `FINISH` 结尾的写入仍报告普通命令标签，而不是结果；例如创建一个顶点时为
  `UPDATE 1`。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

只为执行计划运行读取，不取回任何内容。Cypher 没有对应写法。没有
`RETURN` 且没有写子句的 Cypher 查询会被拒绝：

```cypher
MATCH (m:movie) FINISH;
```

```
--
(0 rows)
```

### 执行写入而不回读结果 {#perform-a-write-without-reading-the-result-back}

当你不想把创建的元素发送回客户端时，应使用 `CREATE … FINISH`：

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'}) FINISH;
```

```
UPDATE 1
```

顶点已存在：

```cypher
MATCH (m:movie {title: 'Tenet'}) RETURN m.title AS film, m.year AS year;
```

```
  film   | year
---------+------
 "Tenet" | 2020
(1 row)
```

### 确认 FINISH 之后读取没有成本 {#confirm-that-a-read-costs-nothing-after-finish}

执行计划显示该子句编译出的 `LIMIT 0`，它位于永远不会取回数据的扫描之上：

```cypher
EXPLAIN (COSTS OFF) MATCH (m:movie) FINISH;
```

```
        QUERY PLAN
---------------------------
 Limit
   ->  Seq Scan on movie m
(2 rows)
```

写入计划保留其写入节点，因为写入不是可选的：

```cypher
EXPLAIN (COSTS OFF) CREATE (:movie {title: 'Tenet'}) FINISH;
```

```
  QUERY PLAN
--------------
 Graph Create
   ->  Result
(2 rows)
```

### 结束不投影任何内容的已排序查询 {#end-a-sorted-query-that-projects-nothing}

`ORDER BY`、`SKIP`、`OFFSET` 和 `LIMIT` 都是独立子句，但没有一个能结束查询。
`FINISH` 会关闭以这些子句结尾的管道：

```cypher
MATCH (m:movie) ORDER BY m.year LIMIT 3 FINISH;
```

```
--
(0 rows)
```

去掉 `FINISH` 后，同一查询会引发 `Cypher query must end with RETURN,
FINISH or update clause`。

## 说明 {#notes}

在需要结果的位置不接受 `FINISH`。`CALL { }` 主体必须投影内容，因此以
`FINISH` 结尾的主体会引发
`CALL subquery must RETURN at least one variable`。以 `FINISH`
结尾的查询也不能作为 [`NEXT`](/zh/agensgraph/reference/clauses/next/) 的左操作数。这会引发
`FINISH cannot be followed by NEXT`。

> [!NOTE]
> `finish` 在 2.18 中成为保留关键字。它仍可作为模式中的标签名不加引号使用，即
> `MATCH (n:finish)`，这是升级后的数据库所需的行为。它不能用作变量名、
> `CREATE VLABEL` 名称或 SQL 标识符；在这些位置请写 `"finish"` 或改名。属性键和
> `RETURN` 别名不受影响。

## 兼容性 {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> 实现 GQL *primitive result statement*（ISO/IEC 39075:2024 §14.10）中的
> `FINISH`。标准规定 `FINISH` 具有“空类型”，并把执行结果设为“成功但省略结果”，这正对应上面的空且无列结果。
>
> - **支持**——`FINISH` 作为读查询的终止语句，以及数据修改查询的终止语句；在后一种情况下，标准本身也使其成为隐式（§13.1）。
> - **不支持**——`FINISH` 作为集合运算的一个分支；标准同样禁止这种用法（§14.2，Syntax Rule 5）。AgensGraph
>   会将其拒绝为列数不匹配：`each UNION query must have the same number of columns`。
>
> 在 [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)中跟踪状态。

### openCypher {#opencypher}

openCypher 没有 `FINISH`。在那里，读查询必须以 `RETURN`
结束，写查询可以以其写子句结束。AgensGraph 也接受后一种形式，因此
`FINISH` 补充的是读取场景，而不是替换既有功能。

## 另见 {#see-also}

- [`RETURN`](/zh/agensgraph/reference/clauses/return/)——结束查询的另一种方式
- [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/) 与 [`SKIP` 和 `LIMIT`](/zh/agensgraph/reference/clauses/skip-and-limit/)——需要终止子句的子句
- [`NEXT`](/zh/agensgraph/reference/clauses/next/) **GQL**——`FINISH` 唯一不能位于其前的子句
- [`INSERT`](/zh/agensgraph/reference/clauses/insert/) **GQL**——适合以 `FINISH` 结束的写入
- [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)
