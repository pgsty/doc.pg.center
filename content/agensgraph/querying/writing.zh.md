---
title: 写入图
linkTitle: 写入图
description: 写入子句本身几乎没有值得称为模式匹配的过程。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/writing.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


写入子句本身几乎没有值得称为模式匹配的过程。它接收来自前面子句的行，并对每行做某件事。因此，除最早的第一个 `CREATE` 外，每个写入都遵循同一形状：先查找，再写入。

这就是本页的整体计划。它按需要顺序讲解写入子句：`CREATE`、`MERGE`、`SET`、`REMOVE`、`DELETE`，最后介绍事务对图做什么。每个子句的正式语法见参考：[`CREATE`](/zh/agensgraph/reference/clauses/create/)、[`MERGE`](/zh/agensgraph/reference/clauses/merge/)、[`SET`](/zh/agensgraph/reference/clauses/set/)、[`REMOVE`](/zh/agensgraph/reference/clauses/remove/)、[`DELETE`](/zh/agensgraph/reference/clauses/delete/)。

这些示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行，并在结束时恢复原状；这样你可以顺序读完整页，其他页面打印的计数仍然对应。

## 创建新事物 {#making-something-new}

`CREATE` 搭配一个不绑定既有事物的模式会创建顶点：

```cypher
CREATE (p:person {name: 'Gloria Foster'}) RETURN p;
```

```
                   p                    
----------------------------------------
 person[4.153]{"name": "Gloria Foster"}
```

`RETURN` 可选，标签必选：未指定标签创建的顶点会落入 `ag_vertex`，而边始终必须有标签。结果中的 id 取决于标签序列当前到达的位置，所以你看到的会不同。

要连接两个已存在的事物，先找到它们，再创建边。无法给一个尚未匹配到的顶点写边：

```cypher
MATCH (p:person {name: 'Gloria Foster'}), (m:movie {title: 'The Matrix'})
CREATE (p)-[r:acted_in {role: 'The Oracle'}]->(m)
RETURN r;
```

```
                        r                        
-------------------------------------------------
 acted_in[5.71][4.153,3.1]{"role": "The Oracle"}
```

边输出为 `label[id][start,end]{properties}`。这里的 `(p)` 和 `(m)` 不带标签和属性映射。它们是对已绑定变量的引用；如果给其中一个加标签，它就会变成一个*新*顶点。

长度超过一个元素的 `CREATE` 模式会创建其中的所有内容：

```cypher
CREATE (d:person {name: 'Marc Caro'})-[:directed]->(f:movie {title: 'The City of Lost Children', year: 1995})
RETURN d.name AS director, f.title AS film;
```

```
  director   |            film             
-------------+-----------------------------
 "Marc Caro" | "The City of Lost Children"
```

`INSERT` 是同一子句的 ISO/IEC 39075 拼写，接受相同模式：`INSERT (:person {name: 'Ada Lovelace'})`。参见 [`INSERT`](/zh/agensgraph/reference/clauses/insert/)。

## 仅在不存在时创建 {#making-something-only-if-it-is-not-there}

`MERGE` 匹配自己的模式，只在匹配不到任何内容时创建它：

```cypher
MERGE (p:person {name: 'Gloria Foster'}) RETURN p;
```

```
                   p                    
----------------------------------------
 person[4.153]{"name": "Gloria Foster"}
```

这里找到的是上一节的顶点，而不是再创建一个。要小心它*按什么*匹配：整个模式，包括映射中的每个属性。多加一个属性后，模式不再描述你已有的顶点，于是 `MERGE` 会创建一个确实符合该模式的顶点：

```cypher
MERGE (p:person {name: 'Gloria Foster', born: 1933}) RETURN p;
```

```
                          p                           
------------------------------------------------------
 person[4.155]{"born": 1933, "name": "Gloria Foster"}
```

现在有两个：

```cypher
MATCH (p:person {name: 'Gloria Foster'}) RETURN id(p) AS id, p.born AS born ORDER BY id;
```

```
  id   | born 
-------+------
 4.153 | 
 4.155 | 1933
```

所以，在包含你所知全部信息的映射上使用 `MERGE` 会制造重复；在*标识*事物的键上使用 `MERGE`，随后应用其余值，才是幂等的。`ON CREATE SET` 和 `ON MATCH SET` 正是为此存在：

```cypher
MERGE (p:person {name: 'Joe Pantoliano'})
  ON CREATE SET p.born = 1951, p.seen = 1
  ON MATCH SET p.seen = p.seen + 1
RETURN p;
```

```
                                p                                 
------------------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano", "seen": 1}
```

再运行一次，只有 `ON MATCH` 分支触发：

```
                                p                                 
------------------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano", "seen": 2}
```

`MERGE` 对边的处理方式相同，而匹配边模式意味着同时匹配边的标签、方向、属性映射*以及*两个端点。先用 `MATCH` 绑定端点，让 `MERGE` 只对这条边做决定。这条边已经存在，所以不会创建任何内容：

```cypher
MATCH (p:person {name: 'Christopher Nolan'}), (m:movie {title: 'Inception'})
MERGE (p)-[r:directed]->(m) RETURN r;
```

```
            r             
--------------------------
 directed[6.8][4.8,3.5]{}
```

继续之前，先恢复只有一个 Gloria Foster：

```cypher
MATCH (p:person {name: 'Gloria Foster', born: 1933}) DELETE p;
```

标识属性上的唯一约束是这种纪律的持久版本，因为它会拒绝重复数据，而不是依赖你写对 `MERGE`。参见[索引与约束](/zh/agensgraph/querying/indexes-and-constraints/#constraints)。

## 修改属性 {#changing-properties}

对单个属性使用 `SET` 会添加或替换它：

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p.born = 1933 RETURN p;
```

```
                          p                           
------------------------------------------------------
 person[4.153]{"born": 1933, "name": "Gloria Foster"}
```

`SET p += { ... }` 合并一个映射，添加键并覆盖冲突的键：

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p += {died: 2001, city: 'Chicago'} RETURN p;
```

```
                                           p                                           
---------------------------------------------------------------------------------------
 person[4.153]{"born": 1933, "city": "Chicago", "died": 2001, "name": "Gloria Foster"}
```

`SET p = { ... }` 替换整个属性映射。不在新映射中的一律消失：

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p = {name: 'Gloria Foster', born: 1933} RETURN p;
```

```
                          p                           
------------------------------------------------------
 person[4.153]{"born": 1933, "name": "Gloria Foster"}
```

`+=` 与 `=` 的区别，就是 `UPDATE ... SET one_column` 与替换整行的区别；二者很容易输错。

赋 null 不会存储 null，而是删除属性：

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p.born = NULL RETURN p;
```

```
                   p                    
----------------------------------------
 person[4.153]{"name": "Gloria Foster"}
```

因此设置为 null 的属性和从未存在的属性是同一状态，事后无法区分。`allow_null_properties` 会改变这一点并存储 null；它默认关闭。`REMOVE` 是同一操作的显式写法：

```cypher
MATCH (p:person {name: 'Joe Pantoliano'}) REMOVE p.seen RETURN p;
```

```
                           p                           
-------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano"}
```

边属性的写法与顶点属性完全相同：

```cypher
MATCH (:person {name: 'Gloria Foster'})-[r:acted_in]->(:movie {title: 'The Matrix'})
SET r.credited = true RETURN r;
```

```
                                 r                                 
-------------------------------------------------------------------
 acted_in[5.71][4.153,3.1]{"role": "The Oracle", "credited": true}
```

> [!NOTE]
> 提升属性是“属性可以保存任何值”的唯一例外。一旦某个键背后有类型列，JSON 类型不适合该列的写入就会中止。参见[把属性提升为列](/zh/agensgraph/querying/typed-columns/#what-promotion-costs-you)。

## 删除事物 {#removing-things}

`DELETE` 删除匹配到的内容并把它返回，所以你能看到删掉了什么：

```cypher
MATCH (p:person {name: 'Joe Pantoliano'}) DELETE p RETURN p;
```

```
                           p                           
-------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano"}
```

仍带有边的顶点不能删除，因为缺少端点的边不可能存在：

```cypher
MATCH (p:person {name: 'Gloria Foster'}) DELETE p;
```

```
ERROR:  Vertex with connected edges cannot be removed
HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
```

可以自己删除边：

```cypher
MATCH (:person {name: 'Gloria Foster'})-[r:acted_in]->() DELETE r RETURN r;
```

```
                                 r                                 
-------------------------------------------------------------------
 acted_in[5.71][4.153,3.1]{"role": "The Oracle", "credited": true}
```

也可以使用 `DETACH DELETE`，它会连同每条接触该顶点的边一起删除顶点：

```cypher
MATCH (d:person {name: 'Marc Caro'}) DETACH DELETE d;
MATCH (f:movie {title: 'The City of Lost Children'}) DETACH DELETE f;
MATCH (p:person {name: 'Gloria Foster'}) DELETE p;
```

数据集现在恢复为原状：

```cypher
MATCH (n) RETURN count(n) AS elements;
```

```
 elements 
----------
 46
```

这个拒绝是保护，不是麻烦。对枢纽顶点执行 `DETACH DELETE` 可能删除远超你预期的内容；所以先匹配打算失去的边，并在删除前计数。

## 读取刚写入的内容 {#reading-what-you-just-wrote}

写入子句不是语句的终点。它的输出行会继续沿流水线传递，其后的读取看到的是写入留下的图：

```cypher
CREATE (:person {name: 'Gloria Foster'})
WITH 1 AS done
MATCH (p:person {name: 'Gloria Foster'})
RETURN count(p) AS found;
```

```
 found 
-------
 1
```

规划器的安排方式是在下一个读取运行前物化写入效果。这是“eager”计划，`EXPLAIN` 也会如此标记。[调优查询](/zh/agensgraph/querying/performance/#the-settings-that-change-plan-shape)介绍其代价以及禁止它的设置。

## 事务 {#transactions}

图是数据库中的表，所以写图就是普通的事务性写入。没有需要启用的开关，也没有第二个提交要考虑：一个事务中的 Cypher 写入和 SQL 写入要么一起提交，要么一起回滚。

```sql
CREATE TABLE import_log (what text, at timestamptz DEFAULT now());
```

```cypher
BEGIN;
CREATE (:person {name: 'Gloria Foster'});
INSERT INTO import_log (what) VALUES ('added Gloria Foster');
MATCH (p:person {name: 'Gloria Foster'}) RETURN count(p) AS found;
```

```
 found 
-------
 1
```

事务内两个写入都存在。回滚后两个都不存在：

```cypher
ROLLBACK;
MATCH (p:person {name: 'Gloria Foster'}) RETURN count(p) AS found;
```

```
 found 
-------
 0
```

```sql
SELECT count(*) AS logged FROM import_log;
```

```
 logged 
--------
      0
```

```sql
DROP TABLE import_log;
```

作为 PostgreSQL 会带来的一切也适用于这里：隔离级别、保存点、标签表上的 `SELECT ... FOR UPDATE`、两个会话写同一顶点时的死锁检测。如果需要，批量加载可以就是一个事务；事务内的 `CREATE GRAPH` 也像任何 DDL 一样回滚。

反方向存在两道关卡。除非打开 `enable_graph_dml`，用 SQL `INSERT`、`UPDATE`、`DELETE` 或 `MERGE` 向标签写行会被拒绝。除非打开 `enable_graph_ddl`，用 `ALTER TABLE` 改变标签形状也会被拒绝。两者都可能让图目录描述的内容不再成立。参见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-is-deliberately-closed-off)。

## 接下来去哪里 {#where-to-go-next}

* [加载数据](/zh/agensgraph/guides/loading-data/)——批量加载，包括对既有表使用 `LOAD FROM`。
* [组合查询](/zh/agensgraph/querying/composing/)——`WITH`、`UNWIND` 和聚合，它们在写入子句之前都很有用。
* [安全](/zh/agensgraph/operations/security/)——标签上的授权和行级安全。
