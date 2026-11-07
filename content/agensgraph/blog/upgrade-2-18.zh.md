---
title: AgensGraph 2.18 有哪些变化
linkTitle: AgensGraph 2.18 有哪些变化
description: 介绍 PostgreSQL 18 基础、GQL 增量、类型列提升，以及升级前必须验证的应用行为。
type: docs
date: 2026-11-07
tags:
- 版本
- 升级
- PostgreSQL
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/release_notes/2.18.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
summary: 一份带上游来源链接的 AgensGraph 2.18 升级检查表。
---

AgensGraph 2.18 把基础从 PostgreSQL 17.10 移到 PostgreSQL 18，加入相当一部分 GQL，提供类型列属性提升，改进图查询规划，并修复多类崩溃和错误结果。

应用升级时真正需要测试的是这些行为：

- `xor`、`current_graph`、`current_property_graph` 变为保留字；
- `WHERE`、`FILTER`、`AND`、`OR`、`NOT`、`XOR` 与 `CASE WHEN` 中的条件必须是布尔值；
- 对图元素执行 `collect()` 会返回图元素数组；
- `WITH … WHERE` 的分页顺序变为过滤、排序、再 `LIMIT`；
- 图写入上的行级安全策略得到正确执行；
- 2.17 的数据目录不能直接由 2.18 二进制启动。

稳妥的升级顺序是先清点标识符与查询结果，做一份已验证的备份，在集群副本上升级，重新运行 RLS 和分页测试，最后再处理生产数据目录。[版本说明](/zh/agensgraph/release-notes/2.18/)有完整变化，[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/)有操作步骤。
