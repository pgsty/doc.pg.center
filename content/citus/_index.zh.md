---
title: Citus 14 文档
linkTitle: Citus
description: 用 Citus 扩展 PostgreSQL：部署集群、设计分布式表、迁移应用，查阅 SQL、API 与技术文章。
weight: -4
type: docs
icon: fa-solid fa-table-cells-large
search_keywords: [Citus, 分布式 PostgreSQL, 分片, 多租户]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
outputs: [HTML, RSS, print, markdown, LLMSFULL]
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14
upstream_modified: true
author: 'Microsoft 与 Citus 原作者 · 中文整理：[PGSTY](https://pgsty.com/)'
cascade:
  type: docs
  upstream_source: citus
  upstream_modified: true
---

Citus 是 PostgreSQL 的开源扩展，提供分布式表与并行查询。你可以从单节点开始，随着数据量和负载增长逐步添加工作节点，继续使用 PostgreSQL 的 SQL、驱动和工具，构建多租户应用、实时分析、时序和微服务系统。

> [!NOTE] Citus 14 文档版本
> 本社区版本依据 **2026 年 11 月 7 日**采集的 Microsoft Learn **Citus 14** 文档整理。[来源与许可](/citus/attribution/)记录了上游版本、收录的博客文章和翻译原则。

- [概览](/citus/overview/) — 架构、分片模型、适用负载与常见问题。
- [安装部署](/citus/installation/) — Docker、Linux 软件包、单节点安装与集群部署。
- [教程](/citus/tutorials/) — 构建多租户、实时分析、时序和微服务应用。
- [数据建模](/citus/modeling/) — 分布键、共置、应用集成与触发器。
- [集群运维](/citus/operations/) — 管理表、诊断查询、优化性能与升级。
- [迁移指南](/citus/migration/) — 调整模式与查询、搬迁数据、适配应用框架。
- [SQL 与 API 参考](/citus/reference/) — 函数、配置、元数据、SQL 支持与执行原理。
- [专题与博客](/citus/articles/) — 十篇技术文章，涵盖 SaaS、聚合、HyperLogLog 等主题。
{.cards}

## 从这里开始 {#start}

**在本地体验**：按 [Docker 快速入门](/citus/installation/single-node-docker/)启动 Citus，再完成[多租户教程](/citus/tutorials/tutorial-multi-tenant/)。

**设计分布式应用**：先了解[适用场景与限制](/citus/overview/postgresql-citus-scale/)，再学习如何[选择分布列](/citus/modeling/data-modeling/)。

**管理生产集群**：从[集群管理](/citus/operations/cluster-management/)、[诊断查询](/citus/operations/diagnostic-queries/)与[配置参考](/citus/reference/api-guc/)开始。

## 阅读与导出 {#reading}

通过语言菜单切换中英文，或使用双语对照并排阅读。站内搜索覆盖标题、摘要与章节，并支持 API 名称检索；页面菜单支持打印和 Markdown 导出。[完整 Markdown 手册](/zh/citus/llms-full.txt)按阅读顺序汇总全套内容，并保留来源与许可信息。

原始文档：[Microsoft Learn](https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14)。项目源码：[citusdata/citus](https://github.com/citusdata/citus)。[来源、版权与整理说明](/citus/attribution/)。
