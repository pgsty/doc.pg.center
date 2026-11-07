---
title: 迁移生产数据
description: 介绍将 PostgreSQL 数据库中的生产数据迁移到 Microsoft Azure 上的 Citus 集群的两种主要方式。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration-data?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

完成数据库模式和应用查询的调整、使其适用于 Citus 后，就可以进行最后一步了：将数据迁移到 Citus 集群，并将应用切换到新数据库。

数据迁移方式取决于允许的停机时间和数据量，但通常可以分为以下两类。

## 本节内容 {#in-this-section}

| 文章 | 说明 |
| --- | --- |
| [小型数据库迁移](/citus/migration/migration-data-small/) | 适用于迁移期间允许短暂停机的数据集。 |
| [大型数据库迁移](/citus/migration/migration-data-big/) | 适用于要求极短停机时间或零停机时间的大型数据集。 |

## 相关内容 {#related-content}

- [迁移现有应用](/citus/migration/migration/)
- [查询迁移](/citus/migration/migration-query/)
- [模式迁移](/citus/migration/migration-schema/)
