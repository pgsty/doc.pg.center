---
title: 什么是 AgensGraph
linkTitle: 什么是 AgensGraph
description: AgensGraph 是基于 PostgreSQL 的多模型数据库，属性图、关系表、Cypher、GQL 与 SQL 共用一个事务引擎。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/what-is-agensgraph.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


AgensGraph 是一个多模型数据库。一个服务端、一个数据库、一个连接。你的数据同时以**属性图**和**关系表**的形式存在，可以用 **Cypher**、**GQL** 或 **SQL** 查询。同一条语句中可以使用其中两种语言。

它构建在 PostgreSQL 之上。2.18 是 PostgreSQL 18 加上图模型，因此 PostgreSQL 提供的一切都原样随之而来：事务、角色和行级安全，`pg_dump` 和 `pg_basebackup`，流复制，规划器和 `EXPLAIN`，扩展生态，以及每个 PostgreSQL 驱动已经在使用的线协议。

## 它有什么不同 {#what-makes-it-different}

**图以 PostgreSQL 对象存储，而不是并列在数据库旁边。** 图是一个模式，标签是一张表，顶点是一行。没有需要额外同步的图存储，也没有需要跨越的桥接层；Cypher 写入和 SQL 写入会在同一个事务中提交，因为它们都写入同一个数据库中的表。[图如何存储在 PostgreSQL 中](/zh/agensgraph/concepts/graph-on-postgresql/)是让本手册其余部分变得清晰的关键页。

**遍历是一等查询，而不是你手写的递归连接。** “哪些影片与这部电影共享演员”“这两个人相距多远”“三跳之内能到达什么”都是模式：

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie)<-[:acted_in]-(co:person)
RETURN DISTINCT co.name AS co_actor ORDER BY co_actor;
```

```
       co_actor
----------------------
 "Carrie-Anne Moss"
 "Laurence Fishburne"
```

**扩展可以直接作用于图数据。** 普通表中的属性以 `jsonb` 保存，因此 `pgvector` 可以为顶点上的 embedding 建索引，PostgreSQL 全文搜索也可以为文本属性建索引。一条查询可以先找到语义相近的文档，再沿图关系扩展上下文。参见[向量搜索](/zh/agensgraph/guides/search/vector/)。

**GQL 这个 ISO 标准属于同一套语言。** 2.18 实现了 ISO/IEC 39075 的相当一部分，不需要单独的模式，也没有单独的解析器。`LET`、`NEXT`、`FILTER`、`FINISH`、`INSERT`、`FOR`、`CALL { }` 和子查询值表达式都可以在 Cypher 可用的地方使用。参见 [GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)。

## 适合谁 {#who-it-is-for}

它适合已经有关系数据、需要对这份数据提出图形状问题、又不想为了提问而运行第二个数据库的团队。常见形状是推荐和相似度，欺诈和风险链，权限和所有权层级，网络和依赖拓扑，以及检索增强生成背后的知识图谱。

在三种情况下它很合适：图和表属于同一个事实系统；你已经运维 PostgreSQL 并希望保留这些技能和工具；查询把遍历与聚合、连接或窗口函数混合使用。

如果需要把单个图跨机器分片的分布式图存储，或需要面向 PageRank、社区发现等全图算法并具规模的图分析引擎，它就是错误工具。AgensGraph 按 PostgreSQL 的方式扩展：一个主库、只读副本和纵向增长。

## 本版本包含什么 {#what-is-in-this-release}

- 以 PostgreSQL 18 为基础。
- 向 GQL 一致性迈出了一大步。
- 类型化列属性提升。它把高频 `jsonb` 属性变成真正可索引的列，同时不改变查询写法。参见[把属性提升为列](/zh/agensgraph/querying/typed-columns/)。
- 图遍历方面的规划器和估算改进。

升级前，若干变化需要应用侧关注，包括新的保留字，以及关于 `WHERE` 中可以出现什么的更严格规则。[版本说明](/zh/agensgraph/release-notes/2.18/)列出了这些变化，[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/)给出了流程。

## 下一步 {#next}

[安装 AgensGraph](/zh/agensgraph/get-started/install/)，然后加载本手册每一页都使用的[示例数据集](/zh/agensgraph/get-started/example-dataset/)，再[运行你的第一个查询](/zh/agensgraph/get-started/first-query/)。
