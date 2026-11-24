---
title: "REMOVE"
linkTitle: "REMOVE"
description: "删除已绑定顶点和边的属性。"
type: docs
weight: 140
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/remove.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

删除已绑定顶点和边的属性。

## 语法 {#synopsis}

```text
REMOVE property_reference [, property_reference ] ...
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`REMOVE` 接受属性引用，并删除对应的键。它是 `SET n.key = NULL` 的简便写法，效果相同。

- 删除**不存在**的键不会报错，元素保持原样。
- 可用逗号分隔多个属性引用。
- 属性引用可以**嵌套**。`n.key.subkey` 删除内层键，保留外层映射。
- `REMOVE` 对每条输入行执行一次，所以 `MATCH` 找到多个元素时，每个元素都会删除相应属性。该子句自身不带 `WHERE`，请在 `MATCH` 中过滤。
- `REMOVE` 需要已绑定的变量，因此不能作为首句。它可以结束查询。若要查看结果，可追加 [`RETURN`](/zh/agensgraph/reference/clauses/return/)。
- `REMOVE` 只删除属性，不能删除标签或元素。删除元素需使用 [`DELETE`](/zh/agensgraph/reference/clauses/delete/)。

## 参数 {#parameters}

property_reference
: 已绑定元素的属性，写作 `variable.key`，也可以嵌套为 `variable.key.subkey`。单写元素变量会被拒绝。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。最后一个示例会撤销这些修改。

### 删除一个属性 {#remove-one-property}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action', runtime: 150, imax: true});
```

```
UPDATE 1
```

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.runtime
RETURN properties(m) AS props;
```

```
                               props
-------------------------------------------------------------------
 {"imax": true, "year": 2020, "genre": "Action", "title": "Tenet"}
(1 row)
```

### 一次删除多个属性 {#remove-several-at-once}

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.imax, m.genre
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

### 删除不存在的键 {#remove-a-key-that-is-not-there}

元素不变，也不会报错。

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.nosuchkey
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

### 删除嵌套映射中的键 {#remove-a-key-inside-a-nested-map}

属性值本身也可以是映射。

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.crew = {dop: 'Hoyte van Hoytema', editor: 'Jennifer Lame'}
RETURN properties(m) AS props;
```

```
                                               props
---------------------------------------------------------------------------------------------------
 {"crew": {"dop": "Hoyte van Hoytema", "editor": "Jennifer Lame"}, "year": 2020, "title": "Tenet"}
(1 row)
```

用点号访问内层键，可以保留映射中的其他内容。

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.crew.dop
RETURN properties(m) AS props;
```

```
                                 props
-----------------------------------------------------------------------
 {"crew": {"editor": "Jennifer Lame"}, "year": 2020, "title": "Tenet"}
(1 row)
```

指定外层键会删除整个映射。

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.crew
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

### 删除边的属性 {#remove-a-property-from-an-edge}

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
REMOVE r.credited
RETURN properties(r) AS props;
```

```
      props
-----------------
 {"role": "Neo"}
(1 row)
```

### 撤销示例中的修改 {#undo-the-examples}

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 1
```

## 注意事项 {#notes}

`REMOVE` 不接受单独的元素变量。若试图用这种方式清除全部属性，系统会拒绝操作，并提示改用 `SET` 的写法。

```cypher
MATCH (m:movie {title: 'Tenet'}) REMOVE m RETURN m.title;
```

```
ERROR:  cannot set property map to NULL
HINT:  use {} instead of NULL to remove all properties
```

`SET m = {}` 清空属性并保留元素，`DETACH DELETE m` 则直接删除元素。

## 兼容性 {#compatibility}

### 移除标签（ISO/IEC 39075 §13.4） {#removing-a-label-isoiec-39075-134}

标准的 `<remove label item>` 可从元素移除标签，写作 `REMOVE n:blockbuster` 或 `REMOVE n IS blockbuster`。AgensGraph 不接受这两种写法。

```cypher
MATCH (m:movie {title: 'Tenet'}) REMOVE m:movie RETURN m.title;
```

```
ERROR:  syntax error at or near ":"
LINE 1: MATCH (m:movie {title: 'Tenet'}) REMOVE m:movie RETURN m.tit...
                                                 ^
```

元素的标签就是它所在的表，因此标签在创建时已确定。添加标签也有同样的限制，见 [`SET`](/zh/agensgraph/reference/clauses/set/)。

## 另请参阅 {#see-also}

- [`SET`](/zh/agensgraph/reference/clauses/set/)：赋值形式，包括 `= NULL` 和 `= {}`
- [`DELETE`](/zh/agensgraph/reference/clauses/delete/)：删除元素
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：绑定需要删除属性的元素
