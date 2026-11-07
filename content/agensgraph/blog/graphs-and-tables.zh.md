---
title: 图与表共用一个引擎
linkTitle: 图与表共用一个引擎
description: 解释 AgensGraph 如何在一个事务边界内保存属性图、关系表并复用 PostgreSQL 运维能力。
type: docs
date: 2026-11-07
tags:
- AgensGraph
- PostgreSQL
- 图数据库
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/what-is-agensgraph.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
summary: 从上游文档出发，解释 AgensGraph 的多模型边界。
---

图数据库很容易变成第二套事实系统：应用需要决定事实存在哪里、如何跨边界传递，以及哪个事务先提交。

AgensGraph 选择了另一条路：图由 PostgreSQL 对象组成。图是模式，标签是表，顶点和边是行。属性图模型为模式和路径提供了适合图的表达方式，而 PostgreSQL 保留了熟悉的运维边界。

## 有用的边界

Cypher 写入与 SQL 写入都写入同一个数据库中的表，因此可以在同一个事务中提交。角色、行级安全、`EXPLAIN`、备份、流复制和 PostgreSQL 协议也都属于同一套系统。

当问题跨越两种模型时，这个边界很实用：

```sql
SELECT f.title, r.stars
FROM (MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
      RETURN m.title AS title) AS f
JOIN my_ratings r ON r.title = f.title #>> '{}'
ORDER BY r.stars DESC;
```

图模式先找出电影，SQL 再把结果连接到关系表中的评分，中间不需要导出任务。

## 适合什么场景

当图和表属于同一个系统、团队已经掌握 PostgreSQL 运维，且查询需要把遍历与聚合或连接组合起来时，这种模型很合适。如果需求是跨机器分片的分布式图存储，或超大规模的全图算法引擎，就应该选择专门的系统。

[什么是 AgensGraph](/zh/agensgraph/get-started/what-is-agensgraph/)页面介绍模型、边界和 2.18 的变化；[图如何存储在 PostgreSQL 中](/zh/agensgraph/concepts/graph-on-postgresql/)进一步说明表和身份。
