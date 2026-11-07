---
title: 将现有应用迁移到 Citus
description: 介绍将现有应用迁移到 Microsoft Azure 上的 Citus 集群所需的步骤。
weight: 10
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

将现有应用迁移到 Citus 时，有时需要调整数据库模式和查询，才能获得最佳性能。Citus 为 PostgreSQL 增加了分布式功能，但基于行的分片并不能作为无需改动的替代方案，让所有工作负载都实现横向扩展。要构建高性能的 Citus 集群，需要考虑数据模型、工具以及所用 SQL 功能的选择。

Citus 还有一种运行模式，称为基于模式的分片。基于行的分片能够获得最佳性能和硬件利用效率；如果希望尽量减少迁移改动，可以考虑基于模式的分片。

## 步骤 1：优化模式 {#step-1-optimize-the-schema}

首先优化现有数据库模式，使其能够在多台机器上高效运行。

[模式迁移](/citus/migration/migration-schema/)

## 步骤 2：更新应用查询 {#step-2-update-application-queries}

接下来更新应用代码和查询，以适应模式变更。

[查询迁移](/citus/migration/migration-query/)

## 步骤 3：迁移生产数据 {#step-3-migrate-production-data}

在开发环境中测试这些变更后，最后一步是将生产数据迁移到 Citus 集群，并切换生产应用。我们提供了一些方法，可尽量缩短此步骤的停机时间。

[数据迁移](/citus/migration/migration-data/)

## 相关内容 {#related-content}

- [什么是 Citus？](/citus/overview/what-is-citus/)
- [使用 Citus 扩展 PostgreSQL 至任意规模](/citus/overview/postgresql-citus-scale/)
