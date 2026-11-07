---
title: 使用场景
description: 深入了解 Citus 的典型使用场景与应用设计。
weight: 30
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/use-cases?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

完成[快速入门](/citus/installation/getting-started/)后，可以进一步了解 Citus 最常见的使用场景。

- [选择分布列](/citus/modeling/data-modeling/)通过一个广告分析应用示例，演示如何构建后端。文章介绍分布式系统的数据建模，包括如何调整现有的单机数据库模式，并说明扩容时常见的挑战及其解决方法。
- [使用 Citus 扩展构建可扩展的 PostgreSQL 指标后端](/citus/articles/metrics-dashboard/)介绍另一类主要场景：高速、高度并行的聚合查询。文章展示如何为事件数据的 Web 仪表盘设计后端模型，并讨论如何管理持续增长的数据，包括非结构化数据。

深入理解这些场景后，可阅读[迁移现有应用](/citus/migration/migration/)，将已有应用迁入 Citus。

## 相关内容 {#related-content}

- [多租户应用教程](/citus/tutorials/tutorial-multi-tenant/)
- [分析与仪表盘教程](/citus/tutorials/tutorial-analytics/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
