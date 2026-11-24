---
title: "MERGE"
linkTitle: "MERGE"
description: "若模式已存在就匹配它，否则创建它。两种情况下都会绑定模式中的变量。"
type: docs
weight: 120
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/merge.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


若模式已存在就匹配它，否则创建它。两种情况下都会绑定模式中的变量。

## 语法 {#synopsis}

```text
MERGE pattern    [ ON { CREATE | MATCH } SET set_item [, set_item ] ... ] ...
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`MERGE` 将 [`MATCH`](/zh/agensgraph/reference/clauses/match/) 和 [`CREATE`](/zh/agensgraph/reference/clauses/create/) 合为一个子句。找到整个模式时，其行为与 `MATCH` 相同，否则与 `CREATE` 相同。两种情况下都会绑定模式中的变量，后续查询可以直接使用。

理解 `MERGE` 只需记住它匹配的是**整个模式**。

- 整个模式匹配时，不会写入任何数据。
- 只要缺少一部分，就会**创建整个模式**，即使图中其他位置已有其中一些元素。例如，合并 `(a)-[:e]->(b)` 时，若 `a` 与 `b` 已存在但边不存在，系统除了创建边，还会另建一个 `a` 和一个 `b`。
- 如果不确定哪些元素已经存在，就**逐个元素合并**。先用独立的 `MERGE` 绑定每个顶点，再用一个 `MERGE` 合并它们之间的边。这样写的 `MERGE` 具有幂等性。

还需遵循以下规则。

- `MERGE` **只能接受一个模式**。用逗号分隔多个模式会报语法错误，应写成多个 `MERGE` 子句。
- `ON CREATE SET` 仅在创建模式时执行，`ON MATCH SET` 仅在匹配成功时执行。两者可以任意顺序并用，各自接受一个 [`SET`](/zh/agensgraph/reference/clauses/set/) 赋值列表。
- 模式中的属性也参与匹配。`MERGE (m:movie {title: 'Tenet'})` 只匹配 `title` 恰好等于 `Tenet` 的 `movie`。仅仅拥有 `title` 属性并不足以匹配。
- `MERGE` 对每条输入行执行一次，可作为查询的首句、中间子句或末句。

## 参数 {#parameters}

pattern
: 使用 [`MATCH`](/zh/agensgraph/reference/clauses/match/) 语法的一个路径模式。每个属性都用作匹配条件，在创建时也作为要设置的属性。

ON CREATE SET
: 仅在创建模式时执行的赋值。

ON MATCH SET
: 仅在找到模式时执行的赋值。

set_item
: 按 [`SET`](/zh/agensgraph/reference/clauses/set/) 语法书写的赋值：`variable.property = expression`、`variable = map` 或 `variable += map`。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。最后一个示例会撤销这些修改。

### 创建或查找顶点 {#create-the-vertex-or-find-it}

首次执行会创建顶点。

```cypher
MERGE (m:movie {title: 'Tenet'}) RETURN m.title AS film, m.year AS year;
```

```
  film   | year
---------+------
 "Tenet" |
(1 row)
```

模式中只有 `title`，所以 `year` 尚未设置。第二次执行时找到同一顶点，不再写入。

```cypher
MERGE (m:movie {title: 'Tenet'}) RETURN m.title AS film, m.year AS year;
```

```
  film   | year
---------+------
 "Tenet" |
(1 row)
```

```cypher
MATCH (m:movie {title: 'Tenet'}) RETURN count(*) AS rows;
```

```
 rows
------
 1
(1 row)
```

### 创建与匹配时设置不同的属性 {#set-different-properties-on-create-and-on-match}

先清除先前的结果。

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 1
```

```cypher
MERGE (m:movie {title: 'Tenet'})
ON CREATE SET m.year = 2020, m.source = 'created'
ON MATCH SET m.source = 'matched'
RETURN m.title AS film, m.year AS year, m.source AS source;
```

```
  film   | year |  source
---------+------+-----------
 "Tenet" | 2020 | "created"
(1 row)
```

再次执行同一语句会进入另一个分支。

```cypher
MERGE (m:movie {title: 'Tenet'})
ON CREATE SET m.year = 2020, m.source = 'created'
ON MATCH SET m.source = 'matched'
RETURN m.title AS film, m.year AS year, m.source AS source;
```

```
  film   | year |  source
---------+------+-----------
 "Tenet" | 2020 | "matched"
(1 row)
```

`ON MATCH SET` 没有修改 `year`，所以它保留创建时设置的值。

### 整条路径一起 MERGE 会产生重复顶点 {#see-a-whole-pattern-merge-duplicate-a-vertex}

图中只有一位 Christopher Nolan，他还没有执导 `Tenet`。

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
MATCH (p:person {name: 'Christopher Nolan'}) RETURN count(*) AS nolans;
```

```
UPDATE 1
 nolans
--------
 1
(1 row)
```

由于边不存在，整条路径匹配失败，于是系统创建整条路径。

```cypher
MERGE (d:person {name: 'Christopher Nolan'})-[:directed]->(m:movie {title: 'Tenet'})
RETURN d.name AS director, m.title AS film;
```

```
      director       |  film
---------------------+---------
 "Christopher Nolan" | "Tenet"
(1 row)
```

```cypher
MATCH (p:person {name: 'Christopher Nolan'}) RETURN count(*) AS nolans;
```

```
 nolans
--------
 2
(1 row)
```

现在多出一个 Christopher Nolan 顶点。它没有 `born` 属性，也没有原顶点的边。使用 `MERGE` 时很容易犯这个错误。

### 分别合并每个元素 {#merge-one-element-at-a-time-instead}

先撤销修改，再逐个合并。

```cypher
MATCH (p:person {name: 'Christopher Nolan'})
WHERE NOT EXISTS { MATCH (p)-[:directed]->(:movie {title: 'Inception'}) }
DETACH DELETE p;
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 2
UPDATE 1
```

```cypher
MERGE (d:person {name: 'Christopher Nolan'})
MERGE (m:movie {title: 'Tenet'})
MERGE (d)-[:directed]->(m)
RETURN d.name AS director, m.title AS film;
```

```
      director       |  film
---------------------+---------
 "Christopher Nolan" | "Tenet"
(1 row)
```

```cypher
MATCH (p:person {name: 'Christopher Nolan'}) RETURN count(*) AS nolans;
```

```
 nolans
--------
 1
(1 row)
```

第一个 `MERGE` 匹配了已有的人物，第二个创建影片，第三个只创建边。再次执行这三个子句，数据不再变化。

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN count(*) AS edges;
```

```
 edges
-------
 3
(1 row)
```

无论执行多少次，结果始终是原始数据集中的两部影片，加上刚合并的一部。

### 拒绝多个模式 {#reject-more-than-one-pattern}

```cypher
MERGE (a:movie {title: 'A'}), (b:movie {title: 'B'});
```

```
ERROR:  syntax error at or near ","
LINE 1: MERGE (a:movie {title: 'A'}), (b:movie {title: 'B'});
                                    ^
```

请写成两个 `MERGE` 子句。

### 撤销示例中的修改 {#undo-the-examples}

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 2
```

## 注意事项 {#notes}

唯一约束能拦截这种重复，避免错误数据悄然写入。如果为 `person` 的 `name` 属性设置唯一约束，前面的整条路径合并就无法再创建一个 Nolan。

```cypher
CREATE CONSTRAINT unique_person_name ON person ASSERT name IS UNIQUE;
MERGE (d:person {name: 'Christopher Nolan'})-[:directed]->(m:movie {title: 'Tenet'})
RETURN d.name AS director, m.title AS film;
```

```
CREATE CONSTRAINT
ERROR:  conflicting key value violates exclusion constraint "unique_person_name"
DETAIL:  Key ((properties.'name'))=("Christopher Nolan") conflicts with existing key ((properties.'name'))=("Christopher Nolan").
```

系统不会创建任何内容，事务会报告失败原因。请在用于合并的键上声明约束。

## 兼容性 {#compatibility}

### MERGE 的标准地位 {#merge-is-not-a-gql-clause}

ISO/IEC 39075 没有 `MERGE`。其数据修改语句包括 `<insert statement>`（§13.2）、`<set statement>`（§13.3）、`<remove statement>`（§13.4）和 `<delete statement>`（§13.5）。AgensGraph 保留了 Cypher 的 `MERGE`。若只使用标准语法，可在 [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) 或 `EXISTS` 判断后执行 [`INSERT`](/zh/agensgraph/reference/clauses/insert/)。

## 另请参阅 {#see-also}

- [`CREATE`](/zh/agensgraph/reference/clauses/create/)：无条件写入
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：模式语法
- [`SET`](/zh/agensgraph/reference/clauses/set/)：`ON CREATE SET` 和 `ON MATCH SET` 使用的赋值语法
- [`DELETE`](/zh/agensgraph/reference/clauses/delete/)：删除合并时创建的内容
