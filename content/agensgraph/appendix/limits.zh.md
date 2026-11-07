---
title: 限制
linkTitle: 限制
description: AgensGraph 的两个限制来自它赋予每个顶点和边的身份标识。
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/limits.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 的两个限制来自它赋予每个顶点和边的身份标识。其余限制属于 PostgreSQL，因为图是模式，标签是表。

## 图限制 {#graph-limits}

每个顶点和边都带有一个 `graphid` 类型的身份标识，其布局决定了图可达到的两个限制。`graphid` 是一个拆分成两部分的 64 位无符号整数。高 16 位是**标签 id**，低 48 位是**本地 id**，即行在其标签内的序列号。因此，身份标识会打印成两个数字：`movie[3.7]` 表示标签 3、第 7 行。

| 限制 | 值 | 来源 |
| --- | --- | --- |
| 每图的标签数 | 65,535 | 16 位标签 id。0 保留为无效标签 id，因此可用范围是 1 到 65,535。 |
| 每标签的行数 | 281,474,976,710,655 | 48 位本地 id：2<sup>48</sup> − 1。 |
| 标签名长度 | 63 字节 | PostgreSQL 的标识符长度。 |

图本身没有单独的数量限制：图是模式，而 PostgreSQL 对每个数据库中的模式数没有限制。大量图会消耗关系，因为每个图都会创建一个序列和两个自己的根标签。

`graphid` 的两部分都会做范围检查。任一部分越界时，构造函数都会拒绝：

```sql
SELECT graphid(65536, 1);
```

```
ERROR:  labid out of range: 65536
```

```sql
SELECT graphid(1, 281474976710656);
```

```
ERROR:  locid out of range: 281474976710656
```

解析 `graphid` 字面量时，会返回同样两条消息，但不带越界值：`SELECT '65536.1'::graphid` 抛出 `labid out of range`。

发放这些数字的计数器是普通序列，因此可以检查它们。每个图有一个用于标签 id 的 `ag_label_seq`，每个标签有一个用于本地 id 的 `<label>_id_seq`：

```sql
SELECT sequencename, max_value FROM pg_sequences
WHERE schemaname = 'moviekb' AND sequencename IN ('ag_label_seq', 'movie_id_seq');
```

```
 sequencename |    max_value    
--------------+-----------------
 ag_label_seq |           65535
 movie_id_seq | 281474976710655
```

`ag_label_seq` 会循环，创建标签时会跳过已占用的编号，所以删除标签会释放其 id 供复用。没有空闲 id 时，创建标签失败：

```
ERROR:  no more new labels are available
```

每个新图都会带两个标签：标签 id 为 1 的 `ag_vertex` 和标签 id 为 2 的 `ag_edge`。它们是所有顶点标签和边标签继承的两个根。因此，用户自己的标签可用 id 为 65,533 个。

## 超过 63 字节的标签名会被截断 {#a-label-name-over-63-bytes-is-truncated}

标识符长度是 63 字节。更长的标签名会被截到 63 字节并发出提示。因此，**前 63 字节相同的两个标签名是同一个标签**。第二条 `CREATE VLABEL` 会看见第一条：

```cypher
CREATE VLABEL a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_aaa;
CREATE VLABEL a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_bbb;
```

```
NOTICE:  identifier "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_aaa" will be truncated to "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes"
CREATE VLABEL
NOTICE:  identifier "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_bbb" will be truncated to "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes"
ERROR:  label "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes" already exists
```

这种情况会在模式中造成隐患，因为模式找不到标签时会创建标签，而不会有任何失败。写入上述两个名称会把两批行放进同一个标签：

```cypher
CREATE (:a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_aaa {via:'aaa'});
CREATE (:a_label_name_that_is_deliberately_longer_than_sixty_three_bytes_bbb {via:'bbb'});
MATCH (n) RETURN label(n) AS lab, n.via ORDER BY n.via;
```

```
                                lab                                |  via  
-------------------------------------------------------------------+-------
 "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes" | "aaa"
 "a_label_name_that_is_deliberately_longer_than_sixty_three_bytes" | "bbb"
```

让标签名保持在 63 字节内，并让前 63 字节彼此不同。限制单位是字节而不是字符，所以使用多字节文字的名称会更早达到限制。

## 图会遇到的 PostgreSQL 限制 {#postgresql-limits-a-graph-runs-into}

标签是表，因此图受数据库其余部分相同的限制。下表是图操作会触及的限制。PostgreSQL 的 [Limits](https://www.postgresql.org/docs/18/limits.html) 附录列有完整清单。

| 限制 | 值 | 对图的意义 |
| --- | --- | --- |
| 关系大小 | 32 TB | 一个标签的存储量，按默认 8 kB 块大小计算。超过后需要分区，或拆分成子标签。 |
| 字段大小 | 1 GB | 一个顶点或边的整个属性映射，因为属性存成一个 `jsonb` 字段。超长值会先被压缩并移出行外。 |
| 每个关系的列数 | 1600 | 只有把属性提升为列时才会触及。顶点标签初始有两列，边标签有四列。 |
| 标识符长度 | 63 字节 | 标签名、图名、属性索引名和变量名。属性*键*不是标识符，不受此限制。 |
| 每表行数 | 受关系大小约束 | 48 位本地 id 远大于此，因此首先遇到的是存储限制。 |
| 每表索引数 | 无限制 | 一个标签上的属性索引。 |

> [!NOTE]
> 除 1 GB 字段大小外，没有任何限制约束一个元素可持有的属性数量，或一个属性可嵌套的深度。不过，读取属性的成本会随映射大小增长，因为要访问一个键就必须取出整个映射。用 [`ALTER VLABEL`](/zh/agensgraph/reference/ddl/alter-label/) 把该键提升为列是解决办法。

## 另见 {#see-also}

- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)——这些限制对应的存储布局
- [标签继承](/zh/agensgraph/concepts/label-inheritance/)——把一个大标签拆成多个
- [数据定义](/zh/agensgraph/reference/ddl/)——创建标签和索引的语句
