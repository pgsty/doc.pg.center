---
title: 确定应用程序类型
description: 了解哪种 Citus 应用类型最接近你的应用，以便在 Citus 集群上高效执行查询。
weight: 10
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/app-type?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

要在 Citus 集群上高效执行查询，必须将数据合理地分布到各台机器上。具体的分布方式取决于应用类型及其查询模式。

适合 Citus 的应用大致分为两类。数据建模的第一步，就是判断你的应用更接近哪一类。

## 速览 {#at-a-glance}

| 多租户应用 | 实时应用 |
| --- | --- |
| 数据库模式中有时包含数十乃至数百张表 | 表的数量较少 |
| 每次查询只涉及一个租户（公司或商店） | 包含聚合的较简单分析查询 |
| 为 Web 客户端提供服务的在线事务处理（OLTP）工作负载 | 大量摄入数据，且数据大多不会再修改 |
| 为各租户提供分析查询的在线分析处理（OLAP）工作负载 | 通常围绕一张大型事件表展开 |

## 示例与特征 {#examples-and-characteristics}

**多租户应用**

这类应用通常是面向其他公司、账户或组织提供服务的 SaaS 应用。大多数 SaaS 应用本质上采用关系模型，天然具备一个跨节点分布数据的维度：按 tenant_id 分片即可。

Citus 可以将数据库横向扩展到支持数百万租户，而无需重新设计应用架构。你仍然可以保留所需的关系语义，例如连接、外键约束、事务、ACID 和一致性。

- **示例**：为其他企业托管店面的网站，例如数字营销解决方案或销售自动化工具。
- **特征**：查询只涉及单个租户，而不需要跨租户连接信息。这既包括为 Web 客户端提供服务的 OLTP 工作负载，也包括为各租户提供分析查询的 OLAP 工作负载。数据库模式中有数十乃至数百张表，也往往表明适合采用多租户数据模型。

使用 Citus 扩展多租户应用，只需对应用代码做少量修改。我们支持 Ruby on Rails 和 Django 等常用框架。

**实时分析**

这类应用需要大规模并行处理，协调数百个 CPU 核心，快速完成数值、统计或计数查询。Citus 将 SQL 查询拆分并分配到多个节点并行执行，使得在数十亿条记录上进行亚秒级实时查询成为可能。

如果你的应用符合其中一种情况，下一步就是决定如何在 Citus 集群中对数据分片。如 [架构概念](/citus/overview/what-is-citus/#architecture-concepts)一节所述，Citus 根据表中分布列的哈希值，将行分配到各个分片。为保证性能，数据库管理员选择的分布列必须与典型查询的访问模式相匹配。

## 相关内容 {#related-content}

- [迁移概述](/citus/migration/migration/)
- [数据建模](/citus/modeling/data-modeling/)
- [什么是 Azure Cosmos DB for PostgreSQL？](/citus/overview/what-is-citus/)
