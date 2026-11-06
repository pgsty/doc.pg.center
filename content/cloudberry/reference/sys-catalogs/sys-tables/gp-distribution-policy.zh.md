---
title: "gp_distribution_policy"
description: "`pg_catalog` 模式中的 `gp_distribution_policy` 表记录 Apache Cloudberry 表及其在各个 Segment 之间分布数据的策略。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-distribution-policy.md"
---

此表只在 Coordinator 上填充。此表不在全局共享，即每个数据库都有自己的副本。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`localoid`|oid| `pg_class.oid` |表的对象标识符（OID）。|
|`policytype`|char| |表的分布策略：<br/><br/>`p` — 分片策略。表数据分布在各个 Segment 实例上。<br/><br/>`r` — 复制策略。表数据复制到每个 Segment 实例上。|
|`numsegments`|integer| |存储该表分布数据的 Segment 实例数。|
|`distkey`|int2vector| `pg_attribute.attnum` |分布列的列号。|
|`distclass`|oidvector|`pg_opclass.oid`|分布列的操作符类标识符。|
