---
title: "gp_distributed_xacts"
description: "`gp_distributed_xacts` 视图包含 Apache Cloudberry 分布式事务的信息。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-distributed-xacts.md"
---

分布式事务是涉及修改 Segment 实例上数据的事务。Apache Cloudberry 的分布式事务管理器确保各 Segment 保持同步。此视图可用于查看当前活动的会话及其关联的分布式事务。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`distributed_xid`|xid| |分布式事务在整个 Apache Cloudberry 阵列中使用的事务 ID。|
|`state`|text| |此会话当前与分布式事务有关的状态。|
|`distributed_id`|text| |分布式事务标识符。它由两部分组成：唯一的时间戳和分布式事务编号。|
|`gp_session_id`|int| |与此事务关联的 Apache Cloudberry 会话的 ID。|
|`xmin_distributed _snapshot`|xid| |此事务启动时，所有未结束事务中的最小分布式事务编号。用于 MVCC 分布式快照。|
