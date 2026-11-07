---
title: Cypher 兼容性
linkTitle: Cypher 兼容性
description: AgensGraph 的 Cypher 与其他实现足够接近，大多数查询可以原样迁移。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/cypher-compatibility.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 的 Cypher 与其他实现足够接近，大多数查询可以原样迁移。但它也足够不同，少数查询会失败，或者更糟：成功并返回不同答案。本附录列出这些差异，并给出服务端抛出的错误或返回的结果，便于你在移植查询表现异常时识别原因。

以下示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行，且 `graph_path` 设为 `moviekb`。

两个结构事实解释了后文的大部分内容。顶点恰好有一个标签，因为标签是表，而行只属于一张表。另外，Cypher 查询是 PostgreSQL 查询，所以词法分析器、类型系统和错误码都是 PostgreSQL 的。

## 不存在的构造 {#constructs-that-do-not-exist}

### 一个关系模式带多个类型 {#several-types-on-one-relationship-pattern}

关系模式最多接受一个类型：

```cypher
MATCH (p:person)-[r:acted_in|directed]->(m:movie) RETURN count(r);
```

```
ERROR:  multiple types for relationship not supported
```

变长形式（`-[r:acted_in|directed*1..2]->`）和 `shortestpath()` 内部会返回同一错误。`-[r:acted_in|:directed]->` 拼法是普通语法错误。请匹配无类型边，然后测试标签：

```cypher
MATCH (p:person)-[r]->(m:movie)
WHERE label(r) IN ['acted_in','directed']
RETURN count(r);
```

```
 count 
-------
 46
```

点标签交替以同样方式失败。`MATCH (n:person|movie)` 在 `|` 处是语法错误；GQL 标准定义的其他标签表达式运算符 `:person&movie`、`:!person` 和 `:%` 也如此。

### 顶点上的标签集合 {#a-label-set-on-a-vertex}

没有标签集合，也无法更改顶点已有的标签。以下每条语句都会在第二个冒号处抛出语法错误：

```cypher
MATCH (n:person {name:'Keanu Reeves'}) SET n:actor RETURN n;
MATCH (n:person {name:'Keanu Reeves'}) REMOVE n:actor RETURN n;
MATCH (n:person:movie) RETURN count(n);
CREATE (:aa:bb);
```

```
ERROR:  syntax error at or near ":"
```

标签继承是替代方案。`CREATE VLABEL actor INHERITS (person)` 创建一个独立标签，匹配父标签时也会返回它。因此 `MATCH (n:person)` 也找到 actor，而 `MATCH (n:person ONLY)` 排除它们。顶点是作为 actor 创建的，而不是后来提升为 actor。见[标签继承](/zh/agensgraph/concepts/label-inheritance/)。

### FOREACH {#foreach}

```cypher
FOREACH (x IN [1,2] | CREATE (:zz {v:x}));
```

```
ERROR:  syntax error at or near "FOREACH"
```

`UNWIND` 和 GQL 的 `FOR` 语句都可以迭代列表：

```cypher
UNWIND [1,2] AS x RETURN x;
```

```
 x 
---
 1
 2
```

二者后面都可以跟写子句，因此 `UNWIND list AS x CREATE (…)` 覆盖 `FOREACH` 体的用途。

### CREATE UNIQUE {#create-unique}

```cypher
MATCH (a:person {name:'Keanu Reeves'}), (b:movie {title:'Avatar'})
CREATE UNIQUE (a)-[:acted_in]->(b);
```

```
ERROR:  syntax error at or near "UNIQUE"
```

使用 `MERGE`：它先匹配模式，只在没有匹配时创建。这里边已经存在，所以 `MERGE` 返回现有边而不是添加第二条：

```cypher
MATCH (a:person {name:'Sam Worthington'}), (b:movie {title:'Avatar'})
MERGE (a)-[r:acted_in]->(b)
RETURN id(r);
```

```
  id  
------
 5.21
```

### LOAD CSV {#load-csv}

```cypher
LOAD CSV WITH HEADERS FROM 'file:///tmp/movies.csv' AS row RETURN row;
```

```
ERROR:  syntax error at or near "CSV"
```

导入路径经过表。`COPY` 或外部表把 CSV 放进关系，`LOAD FROM` 把它的行变成图元素：

```sql
CREATE TABLE people_src (name text, age int);
INSERT INTO people_src VALUES ('Ann', 30), ('Bo', 41);
```

```cypher
LOAD FROM people_src AS r CREATE (:person {name: r.name, age: r.age});
```

```
UPDATE 2
```

```sql
DROP TABLE people_src;
```

完整流程见[加载数据](/zh/agensgraph/guides/loading-data/)，包括外部表包装。

### 匿名箭头 `-->` 与 `--` {#the-anonymous-arrows----and---}

`--` 与 SQL 一样开始注释，所以匿名箭头会静默结束语句：

```cypher
MATCH (a:movie)-->(b) RETURN count(*);
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

`<--` 的失败方式不同，因为 `<` 在注释开始前已被消费：

```cypher
MATCH (a:movie)<--(b) RETURN count(*);
```

```
ERROR:  syntax error at end of input
```

写带方括号的形式。`-[]->`、`<-[]-` 和 `-[]-` 都可用：

```cypher
MATCH (a:movie)-[]->(b) RETURN count(*);
```

```
 count 
-------
 11
```

### 映射投影 {#map-projection}

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN m {.title, .year};
```

```
ERROR:  syntax error at or near "{"
```

显式构造映射。映射构造器是普通表达式：

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN {title: m.title, year: m.year};
```

```
             ?column?              
-----------------------------------
 {"year": 2009, "title": "Avatar"}
```

`properties(m)` 返回整个映射，覆盖 `m {.*}`。

### 模式推导式 {#pattern-comprehension}

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN [(m)<-[:acted_in]-(p) | p.name];
```

```
ERROR:  syntax error at or near ":"
```

子查询表达式完成同样工作，并且读起来更像语言的其他部分：

```cypher
MATCH (m:movie {title:'Avatar'})
RETURN COLLECT { MATCH (m)<-[:acted_in]-(p) RETURN p.name };
```

```
        array        
---------------------
 ["Sam Worthington"]
```

### `reduce()`、`extract()` 与 `filter()` {#reduce-extract-and-filter}

三者都不存在。

```cypher
RETURN reduce(acc = 0, x IN [1,2,3] | acc + x);
```

```
ERROR:  variable does not exist
```

`extract()` 和 `filter()` 则是语法错误，因为 `extract` 和 `filter` 已被占用。`extract` 被 SQL 的 `EXTRACT(field FROM source)` 占用，`filter` 被 GQL 的 `FILTER` 语句占用。

列表推导式覆盖 `extract()` 和 `filter()`，并且三种拼法都可用：

```cypher
RETURN [x IN [1,2,3] | x * 10], [x IN [1,2,3] WHERE x > 1], [x IN [1,2,3] WHERE x > 1 | x * 10];
```

```
   ?column?   | ?column? | ?column? 
--------------+----------+----------
 [10, 20, 30] | [2, 3]   | [20, 30]
```

折叠操作可在 Cypher 结果之上用 SQL 聚合；如果折叠就是求和，也可用 `sum()`。

### 裸模式作为谓词 {#a-bare-pattern-as-a-predicate}

模式不是布尔表达式：

```cypher
MATCH (m:movie) WHERE (m)<-[:acted_in]-() RETURN count(m);
```

```
ERROR:  syntax error at or near ":"
```

把它包在 `exists()` 或 GQL 的 `EXISTS { }` 子查询表达式中：

```cypher
MATCH (m:movie) WHERE exists((m)<-[:acted_in]-()) RETURN count(m);
```

```
 count 
-------
 18
```

### 反引号标识符 {#backtick-quoted-identifiers}

反引号不是引号字符：

```cypher
MATCH (m:`movie`) RETURN count(m);
```

```
ERROR:  syntax error at or near "`"
```

标识符按 SQL 方式用双引号括起：`MATCH (m:"movie")`。这对 2.18 中变为保留的词很重要。见[关键字](/zh/agensgraph/appendix/keywords/)。

### 时间、空间与 geodistance 构造器 {#temporal-spatial-and-geodistance-constructors}

`duration()`、`distance()` 和 `haversin()` 不存在：

```cypher
RETURN haversin(1.0);
```

```
ERROR:  function haversin(numeric) does not exist
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

`point()` 和 `timestamp()` 的失败更令人困惑，因为各自与 PostgreSQL 名称冲突。`point({x:1, y:2})` 找到 PostgreSQL 的几何 `point`，其重载接受浮点对和其他几何对象，所以调用是歧义而不是不存在：

```cypher
RETURN point({x:1, y:2});
```

```
ERROR:  function point(jsonb) is not unique
HINT:  Could not choose a best candidate function. You might need to add explicit type casts.
```

`timestamp()` 是语法错误，因为 `timestamp` 是类型名。

`datetime()` 存在，但它是另一个函数，而且最需要注意。它接受时区或日期部分列表，从不接受 ISO-8601 字符串。把时间戳字符串传给它会把字符串当作时区读取：

```cypher
RETURN datetime('2020-01-01T00:00:00');
```

```
ERROR:  time zone "2020-01-01T00:00:00" not recognized
```

它确实接受时区名，或九个日期部分：

```cypher
RETURN datetime(2020, 1, 1, 0, 0, 0, 0, 0, 'UTC');
```

```
       datetime        
-----------------------
 "2020-01-01T00:00:00"
```

从字符串得到时间戳请转换：`'2020-01-01'::date`、`'2020-01-01 00:00'::timestamptz`。`CURRENT_DATE` 和 `CURRENT_TIMESTAMP` 作为裸关键字可用。时长是 PostgreSQL interval，可从 SQL 用 `::interval` 访问。空间工作经过 PostgreSQL 扩展，图查询访问它的方式与向量搜索相同。见[向量搜索](/zh/agensgraph/guides/search/vector/)。

### `db.*` 过程 {#the-db-procedures}

没有 `db` 命名空间：

```cypher
CALL db.labels();
```

```
ERROR:  schema "db" does not exist
```

目录回答同样问题。`ag_label` 列出图的标签。见[图目录](/zh/agensgraph/system-catalogs/catalogs/)。

### PROFILE {#profile}

```cypher
PROFILE MATCH (m:movie) RETURN count(m);
```

```
ERROR:  syntax error at or near "PROFILE"
```

`EXPLAIN` 可用，并带 PostgreSQL 选项：`EXPLAIN (ANALYZE, BUFFERS) MATCH …`。

## 行为差异 {#behaviour-that-differs}

### RETURN 产生的每一列都是 jsonb {#every-column-a-return-produces-is-jsonb}

属性读取是 `jsonb` 值，并保持到投影之后。因此字符串会带 JSON 引号打印：

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN m.title, pg_typeof(m.title);
```

```
  title   | pg_typeof 
----------+-----------
 "Avatar" | "jsonb"
```

`::text` 不会去掉引号。它渲染 jsonb 值，引号也包括在内。要得到普通标量，请在 Cypher 外的 SQL 中提取：

```psql
SELECT t #>> '{}' AS title
FROM (MATCH (m:movie) RETURN m.title AS t) q
ORDER BY title LIMIT 1;
```

```
  title   
----------
 Avatar
```

见[SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。

### `ORDER BY 2` 不排序 {#order-by-2-sorts-nothing}

排序键中的整数是常量，不是输出列号。按同一常量排序不会改变顺序，也不会警告：

```cypher
MATCH (m:movie) RETURN m.title AS t, m.year AS y ORDER BY 2 LIMIT 5;
```

```
             t              |  y   
----------------------------+------
 "The Matrix Resurrections" | 2021
 "Inception"                | 2010
 "Interstellar"             | 2014
 "Avatar"                   | 2009
 "Blade Runner"             | 1982
```

写出键名。`ORDER BY y` 按预期排序。整数形式在 SQL 中确实可用，那里整数排序键表示该位置的输出列。因此把 Cypher 包在 `SELECT … ORDER BY 2` 中也能排序。

```cypher
MATCH (m:movie) RETURN m.title AS t, m.year AS y ORDER BY y LIMIT 5;
```

```
              t               |  y   
------------------------------+------
 "Blade Runner"               | 1982
 "The Terminator"             | 1984
 "Total Recall"               | 1990
 "Terminator 2: Judgment Day" | 1991
 "Jurassic Park"              | 1993
```

### `n.id` 不是身份标识 {#nid-is-not-the-identity}

`id` 是普通属性名。除非有人写入，否则它不存在：

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN m.id, id(m);
```

```
 id | id  
----+-----
    | 3.7
```

`id(m)` 返回身份标识，即打印为 *labid*`.`*locid* 的 `graphid`。两个部分的含义见[限制](/zh/agensgraph/appendix/limits/)。

### 裸 `CALL { }` 回答另一个问题 {#a-bare-call---answers-a-different-question}

子查询体看不到外层变量。名称会重新绑定为新的、无约束变量，因此体在整张图上运行，而不是当前行：

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 3;
```

```
        film         | cast_size 
---------------------+-----------
 "Avatar"            | 25
 "Blade Runner"      | 25
 "Blade Runner 2049" | 25
```

25 是图中全部 `acted_in` 边。写导入列表后，同一查询是正确的：

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL (m) { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 3;
```

```
        film         | cast_size 
---------------------+-----------
 "Avatar"            | 1
 "Blade Runner"      | 1
 "Blade Runner 2049" | 2
```

> [!IMPORTANT]
> 始终给 `CALL` 子查询导入列表——`CALL (v) { … }`、`CALL (*) { … }` 或 `CALL { WITH v … }`。三者都正确且一致。裸形式是这种差异中不抛错却回答另一个问题的唯一形态。

### `shortestpath` 端点必须是命名变量 {#shortestpath-endpoints-must-be-named-variables}

端点中的内联模式会被拒绝：

```cypher
MATCH p = shortestpath((:movie {title:'The Matrix'})-[:related_to*..4]->(:movie {title:'Inception'}))
RETURN length(p);
```

```
ERROR:  node must be a reference to a specific node
```

先绑定两个端点：

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
MATCH p = shortestpath((a)-[:related_to*..4]->(b))
RETURN length(p);
```

```
 length 
--------
 2
```

同一规则适用于 `allshortestpaths()` 和 `dijkstra()`。

### 未加引号的标签折叠为小写 {#an-unquoted-label-folds-to-lower-case}

标识符遵循 SQL 的折叠规则，所以混合大小写的标签会按小写查找：

```cypher
MATCH (m:Movie) RETURN count(m);
```

```
 count 
-------
 18
```

`Movie`、`MOVIE` 和 `movie` 是同一个标签。用带引号的混合大小写名称创建的标签，每次使用都必须加引号。

### 条件只接受布尔值 {#a-condition-takes-only-a-boolean}

读取属性并按真值解释会抛出转换错误，而不是测试是否非空：

```cypher
MATCH (m:movie {year: 1999}) WHERE m.title RETURN count(m);
```

```
ERROR:  cannot cast "The Matrix" (jsonb type string) to boolean
```

消息命名执行器先到达的值；因此无约束 `MATCH` 遍历多行时，报告的是碰巧先读到的那个值。

这适用于 `WHERE`、`FILTER`、`AND`、`OR`、`NOT`、`XOR`、`CASE WHEN` 和 `dijkstra()` 的限定条件。写出真正要做的测试，例如 `WHERE m.title IS NOT NULL` 或 `WHERE m.count <> 0`，或用 `::boolean` 显式转换。

### 缺失标签不是错误 {#a-missing-label-is-not-an-error}

命名了不存在标签的模式匹配不到内容，并返回行数 0：

```cypher
MATCH (n:no_such_label) RETURN count(n);
```

```
 count 
-------
 0
```

因此标签名中的拼写错误看起来像空结果。查询本应有结果却为空时，请检查 `ag_label` 的标签列表。

### `size()` 与 `length()` 是同一函数 {#size-and-length-are-the-same-function}

`size()` 是 `length()` 的另一种拼法；无论写哪个，输出列名都是 `length`：

```cypher
RETURN size([1,2,3]), size('abcd'), length('abcd');
```

```
 length | length | length 
--------+--------+--------
 3      | 4      | 4
```

对模式调用 `size()` 统计匹配数，并把列命名为 `count`：

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN size((m)<-[:acted_in]-());
```

```
 count 
-------
 1
```

### `labels()` 总是返回一个标签 {#labels-always-returns-one-label}

`labels()` 存在并返回列表，但列表恰好有一个元素，因为顶点只有一个标签：

```cypher
MATCH (n:person) RETURN labels(n) LIMIT 1;
```

```
   labels   
------------
 ["person"]
```

`label(n)` 以标量返回这个标签，是应优先使用的形式。`type(r)` 和 `label(r)` 都可用于边。

### 对图元素执行 `collect()` 返回原生数组 {#collect-over-a-graph-element-returns-a-native-array}

收集顶点得到 `vertex[]`，不是图片列表，所以收集后的元素仍可用：

```cypher
MATCH (m:movie) RETURN pg_typeof(collect(m));
```

```
 pg_typeof  
------------
 "vertex[]"
```

```cypher
MATCH (m:movie) WITH collect(m) AS ms RETURN ms[0].title;
```

```
           title            
----------------------------
 "The Matrix Resurrections"
```

收集*属性*仍返回 jsonb 列表。

### 带边的顶点不会删除 {#a-vertex-with-edges-will-not-delete}

`DELETE` 拒绝留下悬空边：

```cypher
MATCH (m:movie {title:'Avatar'}) DELETE m;
```

```
ERROR:  Vertex with connected edges cannot be removed
HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
```

### 查询需要作用于某个图 {#a-query-needs-a-graph-to-run-against}

没有默认图。`graph_path` 未设置时，每条图语句都会被拒绝：

```cypher
RESET graph_path;
MATCH (m:movie) RETURN count(m);
```

```
ERROR:  graph_path is NULL
HINT:  Use SET graph_path
```

为会话设置，或在 `postgresql.conf` 或角色级别设置。见[配置](/zh/agensgraph/operations/configuration/)：

```cypher
SET graph_path = moviekb;
```

## AgensGraph 新增内容 {#agensgraph-additions}

这些内容在其他 Cypher 实现中没有对应物，使用它们的查询不能向外移植。

`MATCH (n:label ONLY)` 把匹配限制到一个标签，排除继承它的标签。不带 `ONLY` 时，匹配父标签也返回子标签。

`SET n += map` 把映射合并进属性，而不是替换属性：

```cypher
MATCH (n:person {name:'Keanu Reeves'}) SET n += {city:'Seoul'} RETURN properties(n);
```

```
                       properties                        
---------------------------------------------------------
 {"born": 1964, "city": "Seoul", "name": "Keanu Reeves"}
```

`LOAD FROM table AS r CREATE (…)` 从关系的行创建图元素，这是批量加载的工作方式。

`dijkstra((a)-[e:related_to]->(b), e.weight)` 查找加权最短路径。它尊重权重，因此最便宜路线不一定跳数最少：

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
MATCH p = dijkstra((a)-[e:related_to]->(b), e.weight)
RETURN [x IN nodes(p) | x.title];
```

```
                  ?column?                   
---------------------------------------------
 ["The Matrix", "Total Recall", "Inception"]
```

Cypher 查询是表表达式，标签是表，因此 SQL 与 Cypher 可在一条语句中混合：

```psql
SELECT q.title #>> '{}' AS film, r.score
FROM (MATCH (p:person)-[:directed]->(m:movie)
      WHERE p.name = 'Christopher Nolan'
      RETURN m.title AS title) q
JOIN rating r ON r.title = q.title #>> '{}'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score 
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
```

## 另见 {#see-also}

- [GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)——ISO/IEC 39075 的哪些部分受支持
- [关键字](/zh/agensgraph/appendix/keywords/)——2.18 保留的词及其影响
- [SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)——完整跨界方式
- [Cypher、GQL 和 SQL](/zh/agensgraph/concepts/languages/)——三种语言如何关联
