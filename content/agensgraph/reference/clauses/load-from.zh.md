---
title: LOAD FROM 子句
linkTitle: LOAD FROM 子句
description: 把普通表或视图读入 Cypher 管道，每个表行对应一个工作行。
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/load-from.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


把普通表或视图读入 Cypher 管道，每个表行对应一个工作行。

## 语法概要 {#synopsis}

```text
LOAD FROM table_name AS alias
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`LOAD FROM` 是关系型源子句。它扫描一张表，并把每一行绑定到 *alias*；这些列随后可以在管道更后面的任何位置以
`alias.column` 读取。因为图和表位于同一个数据库中，所以这不需要导入步骤，也不需要外部数据包装器。

- 别名的列保留其 **SQL 类型**。`numeric(3,1)` 列上的 `r.score`
  是 numeric，因此 `r.score > 8.5` 是 numeric 比较，不是 jsonb 比较。
- 别名本身是**行值**。投影它会得到 jsonb 对象形式的行，因此
  `CREATE (:label = to_jsonb(alias))` 就是整行加载。
- `LOAD FROM` 可以**开启**查询，也可以跟在其他子句之后；一个查询中可以出现多个。它永远不会结束查询。
- 该子句**没有自己的 `WHERE`**。请用后面的 [`MATCH`](/zh/agensgraph/reference/clauses/match/)
  `WHERE`、[`WITH`](/zh/agensgraph/reference/clauses/with/) `WHERE` 或
  [`FILTER`](/zh/agensgraph/reference/clauses/filter/) 过滤。
- `SELECT` 能读取的任何对象都可用：表、视图、模式限定名称。

## 参数 {#parameters}

table_name
: 要读取的表或视图的名称，可选模式限定。它必须存在且可读；未知名称会引发
  `relation "..." does not exist`。

alias
: 绑定到每一行的名称。列用 `alias.column` 读取，整行用 `alias` 读取。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行；该数据集包含普通表
`rating`。

### 读取表 {#read-a-table}

```cypher
LOAD FROM rating AS r
RETURN r.title AS title, r.source AS source, r.score AS score
ORDER BY title, source
LIMIT 4;
```

```
        title        |  source   | score
---------------------+-----------+-------
 "Avatar"            | "critics" | 7.9
 "Blade Runner"      | "critics" | 8.1
 "Blade Runner 2049" | "critics" | 8.0
 "Elysium"           | "critics" | 6.6
(4 rows)
```

值带引号是因为 Cypher `RETURN` 会把输出列装箱为 jsonb，而不是因为这些列本身是
jsonb。它们的 SQL 类型不变：

```cypher
LOAD FROM rating AS r RETURN pg_typeof(r.score) AS t LIMIT 1;
```

```
     t
-----------
 "numeric"
(1 row)
```

### 将表连接到图 {#join-a-table-to-the-graph}

先加载表，再对它进行匹配。关系列与图属性会被直接比较：

```cypher
LOAD FROM rating AS r
MATCH (m:movie {title: r.title})
WHERE r.source = 'critics' AND r.score > 8.5
RETURN m.title AS film, m.year AS year, r.score AS score
ORDER BY score DESC;
```

```
             film             | year | score
------------------------------+------+-------
 "Inception"                  | 2010 | 8.8
 "The Matrix"                 | 1999 | 8.7
 "Interstellar"               | 2014 | 8.7
 "Terminator 2: Judgment Day" | 1991 | 8.6
(4 rows)
```

### 读取整行 {#read-a-whole-row}

单独投影别名即可把行作为映射取出：

```cypher
LOAD FROM rating AS r RETURN r LIMIT 2;
```

```
                              r
-------------------------------------------------------------
 {"score": 8.7, "title": "The Matrix", "source": "critics"}
 {"score": 9.1, "title": "The Matrix", "source": "audience"}
(2 rows)
```

### 读取视图 {#read-a-view}

`SELECT` 能读取的任何关系都是有效来源：

```cypher
CREATE VIEW critic AS SELECT title, score FROM rating WHERE source = 'critics';
```

```
CREATE VIEW
```

```cypher
LOAD FROM critic AS c
RETURN c.title AS film, c.score AS score
ORDER BY score DESC
LIMIT 3;
```

```
      film      | score
----------------+-------
 "Inception"    | 8.8
 "Interstellar" | 8.7
 "The Matrix"   | 8.7
(3 rows)
```

```cypher
DROP VIEW critic;
```

```
DROP VIEW
```

### 从表行构建顶点 {#build-vertices-from-table-rows}

命名你需要的属性：

```cypher
CREATE TABLE tmp_people (name text, born int);
INSERT INTO tmp_people VALUES ('Ana Lily Amirpour', 1980), ('Rian Johnson', 1973);
```

```
CREATE TABLE
INSERT 0 2
```

```cypher
LOAD FROM tmp_people AS t
CREATE (:person {name: t.name, born: t.born});
```

```
UPDATE 2
```

也可以用 `= expression` 取代映射字面量，把整行作为属性映射：

```cypher
LOAD FROM tmp_people AS t
CREATE (:person = to_jsonb(t));
```

```
UPDATE 2
```

撤销两次加载并删除表：

```cypher
MATCH (p:person) WHERE p.name IN ['Ana Lily Amirpour', 'Rian Johnson'] DETACH DELETE p;
```

```
UPDATE 4
```

```cypher
DROP TABLE tmp_people;
```

```
DROP TABLE
```

## 说明 {#notes}

`LOAD FROM` 只负责读取。它没有自己的批量加载机制、并行写入器或错误路由。其后的
`CREATE` 会通过图写入路径逐行插入。若要加载大表，以及了解能让加载更快的索引和日志设置，请参见[加载数据](/zh/agensgraph/guides/loading-data/)。

## 另见 {#see-also}

- [`CREATE`](/zh/agensgraph/reference/clauses/create/)——把加载的行转换成顶点和边的子句
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)——把加载的行连接到图
- [`WITH`](/zh/agensgraph/reference/clauses/with/)——过滤和聚合加载的行
- [组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)——另一个方向：SQL 中的 Cypher 查询
- [加载数据](/zh/agensgraph/guides/loading-data/)——实用加载指南
