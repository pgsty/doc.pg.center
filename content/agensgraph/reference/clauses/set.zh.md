---
title: "SET"
linkTitle: "SET"
description: "修改查询已绑定的顶点和边的属性。"
type: docs
weight: 130
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/set.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

修改查询已绑定的顶点和边的属性。

## 语法 {#synopsis}

```text
SET { target = expression | target += expression } [, ...]
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`SET` 给前面子句已绑定的元素写入属性。具体效果取决于左操作数和所用运算符。

| 写法 | 效果 |
| --- | --- |
| `n.key = expression` | 设置单个属性。键不存在时会添加它。 |
| `n.key = NULL` | 删除该键。 |
| `n = {…}` | 用映射**替换**全部属性。映射中没有的键会被删除。 |
| `n = other` | 用 `other` 的全部属性替换 `n` 的全部属性。 |
| `n += {…}` | 将映射**合并**到已有属性中。更新列出的键，保留其余键。 |

- 同一 `SET` 中的多项赋值用逗号分隔，按从左到右的顺序执行。
- `SET` 对每条输入行执行一次。若 `MATCH` 找到 10 个顶点，就会更新 10 个顶点。
- `SET` 需要已绑定的变量，不能引入变量或作为查询首句。它必须位于 `MATCH`、`MERGE` 或其他绑定变量的子句之后。
- `SET` 可以结束查询。若要查看结果，可追加 [`RETURN`](/zh/agensgraph/reference/clauses/return/)。
- `SET` 只写入属性，无法添加或更改标签。
- [`MERGE`](/zh/agensgraph/reference/clauses/merge/) 中的 `ON CREATE SET` 和 `ON MATCH SET` 使用相同的赋值语法。

## 参数 {#parameters}

target
: 属性引用 `variable.key`，可嵌套为 `variable.key.subkey`。如果要替换或合并全部属性，就直接写元素变量。

expression
: 要存储的值，可以是任何 Cypher 表达式，如字面量、其他元素的属性、算术表达式、`CASE` 表达式、列表或映射。对 `+=` 或以元素变量为左操作数的 `=`，右侧必须是映射或另一个图元素。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。最后一个示例会撤销这些修改。

### 设置一个属性 {#set-one-property}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```

```
UPDATE 1
```

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.runtime = 150
RETURN properties(m) AS props;
```

```
                                props
---------------------------------------------------------------------
 {"year": 2020, "genre": "Action", "title": "Tenet", "runtime": 150}
(1 row)
```

`properties()` 返回全部属性，很容易看出 `SET` 改了什么。

### 在一个子句中设置多个属性 {#set-several-properties-in-one-clause}

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.genre = 'Sci-Fi', m.runtime = 151
RETURN properties(m) AS props;
```

```
                                props
---------------------------------------------------------------------
 {"year": 2020, "genre": "Sci-Fi", "title": "Tenet", "runtime": 151}
(1 row)
```

### 用 NULL 删除属性 {#remove-a-property-with-null}

将属性赋为空值，默认会删除该键。

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.runtime = NULL
RETURN properties(m) AS props;
```

```
                        props
-----------------------------------------------------
 {"year": 2020, "genre": "Sci-Fi", "title": "Tenet"}
(1 row)
```

用 [`REMOVE`](/zh/agensgraph/reference/clauses/remove/) 能更直接地表达删除操作。

### 用 += 合并映射 {#merge-a-map-with}

`+=` 更新映射所列的键，其他键保持原样。

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m += {runtime: 150, imax: true}
RETURN properties(m) AS props;
```

```
                                       props
-----------------------------------------------------------------------------------
 {"imax": true, "year": 2020, "genre": "Sci-Fi", "title": "Tenet", "runtime": 150}
(1 row)
```

### 用 = 替换全部属性 {#replace-the-whole-bag-with}

若左侧直接写元素变量，`=` 会清除映射中没有的所有键。此处 `genre`、`runtime` 和 `imax` 都消失了。

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m = {title: 'Tenet', year: 2020}
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

两个运算符最容易混淆之处在于，`=` 会整体替换，`+=` 只更新指定键。

### 将一个元素的属性复制给另一个元素 {#copy-one-elements-properties-to-another}

右侧可写另一个元素，这会复制它的全部属性。

```cypher
CREATE (:person {name: 'Stand-in'});
```

```
UPDATE 1
```

```cypher
MATCH (p:person {name: 'Stand-in'}), (k:person {name: 'Keanu Reeves'})
SET p = k
RETURN properties(p) AS props;
```

```
                 props
----------------------------------------
 {"born": 1964, "name": "Keanu Reeves"}
(1 row)
```

现在有两个顶点的 `name` 都是 `Keanu Reeves`。

```cypher
MATCH (p:person {name: 'Keanu Reeves'}) RETURN count(*) AS keanus;
```

```
 keanus
--------
 2
(1 row)
```

复制全部属性时，用于标识元素的属性也会复制。两个顶点仍各自独立，边不会复制。

### 设置边的属性 {#set-a-property-on-an-edge}

边和顶点以相同方式接受属性。

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'})
SET r.credited = true
RETURN properties(r) AS props;
```

```
               props
-----------------------------------
 {"role": "Neo", "credited": true}
(1 row)
```

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'})
SET r.credited = NULL
RETURN properties(r) AS props;
```

```
      props
-----------------
 {"role": "Neo"}
(1 row)
```

`MATCH` 只找到属于原 Keanu Reeves 顶点的那条边，前面创建的副本没有边。

### 清空属性 {#empty-a-bag}

用空映射替换可删除所有属性，同时保留元素。

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m = {}
RETURN properties(m) AS props;
```

```
 props
-------
 {}
(1 row)
```

现在无法用属性值找到这个顶点。所以下面的清理操作会查找缺少 `title` 的顶点，而不是查找 `Tenet`。

### 撤销示例中的修改 {#undo-the-examples}

```cypher
MATCH (m:movie) WHERE m.title IS NULL DETACH DELETE m;
MATCH (p:person) WHERE p.name = 'Keanu Reeves' AND NOT EXISTS { MATCH (p)-[]->() } DETACH DELETE p;
```

```
UPDATE 1
UPDATE 1
```

## 注意事项 {#notes}

默认配置 `allow_null_properties = off` 使 `SET n.key = NULL` 删除属性。启用该设置后，键会保留，值为 JSON null。

```cypher
SET allow_null_properties = true;
CREATE (m:movie {title: 'Tenet', year: 2020})
SET m.runtime = NULL
RETURN properties(m) AS props;
```

```
SET
                       props
---------------------------------------------------
 {"year": 2020, "title": "Tenet", "runtime": null}
(1 row)
```

```cypher
SET allow_null_properties = false;
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
SET
UPDATE 1
```

存储 null 与缺少键有区别。两种情况下 `m.runtime IS NULL` 都为真，但保留的键会出现在 `properties()` 中，用 `jsonb` 检测键也能找到它。

## 兼容性 {#compatibility}

### 设置标签（ISO/IEC 39075 §13.3） {#setting-a-label-isoiec-39075-133}

标准的 `<set label item>` 可为元素添加标签，写作 `SET n:blockbuster` 或 `SET n IS blockbuster`。AgensGraph 不接受这两种写法。

```cypher
MATCH (m:movie {title: 'Inception'}) SET m:blockbuster RETURN m.title;
```

```
ERROR:  syntax error at or near ":"
LINE 1: MATCH (m:movie {title: 'Inception'}) SET m:blockbuster RETUR...
                                                  ^
```

标签对应元素所在的表，在创建元素时就已确定。要将顶点移至其他标签，须在目标标签下创建顶点，再删除原顶点。

## 另请参阅 {#see-also}

- [`REMOVE`](/zh/agensgraph/reference/clauses/remove/)：按名称删除属性
- [`MERGE`](/zh/agensgraph/reference/clauses/merge/)：`ON CREATE SET` 和 `ON MATCH SET`
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：绑定由 `SET` 修改的元素
- [`DELETE`](/zh/agensgraph/reference/clauses/delete/)：删除元素
