---
title: 帮助与支持
description: 查找 Citus 社区支持、问题排查入口与 PostgreSQL 版本兼容信息。
weight: 50
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/help-support?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

- 常见疑问的解答见[常见问题](/citus/overview/faq-citus/)。
- [集群管理](/citus/operations/cluster-management/)介绍数据库扩容、租户隔离与故障处理。
- 查询较慢时，可按[查询性能调优](/citus/operations/performance-tuning/)中的步骤排查。
- 加入 [Slack 频道](https://slack.citusdata.com)，向 Citus 社区提问。
- 11.x 及更早版本的文档见[文档存档](https://github.com/citusdata/citus_docs)。

## PostgreSQL 兼容性 {#postgresql-compatibility}

Citus 软件包面向特定的 PostgreSQL 主版本构建。请按下表选择匹配的版本；表格按版本从新到旧排列。

| Citus 版本 | 兼容的 PostgreSQL 版本 | 该 Citus 版本是否受支持 |
| --- | --- | --- |
| 14.x | 18, 17, 16 | 是 |
| 13.x | 17, 16, 15 | 是 |
| 12.1 | 16, 15, 14 | 是 |
| 12.0 | 15, 14 | 否 |
| 11.1 - 11.3 | 15, 14, 13 | 否 |
| 11.0 | 14, 13 | 否 |
| 10.2 | 14, 13, 12 | 否 |
| 10.1 | 13, 12 | 否 |
| 10.0 | 13, 12, 11 | 否 |
| 9.5 | 13, 12, 11 | 否 |
| 9.0 - 9.4 | 12, 11 | 否 |
| 8.x | 11, 10 | 否 |
| 7.x | 10, 9.6 | 否 |
| 6.x | 9.6, 9.5 | 否 |
| 5.2 | 9.5 | 否 |

## 相关内容 {#related-content}

- [常见问题](/citus/overview/faq-citus/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
