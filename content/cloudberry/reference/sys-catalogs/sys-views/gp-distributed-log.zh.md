---
title: "gp_distributed_log"
description: "`gp_distributed_log` 视图包含分布式事务及其关联的本地事务的状态信息。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-distributed-log.md"
---

分布式事务是涉及修改 Segment 实例上数据的事务。Apache Cloudberry 的分布式事务管理器确保各 Segment 保持同步。此视图可用于查看分布式事务的状态。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`segment_id`|smallint|gp_segment_configuration.content|Segment 的内容 ID。Coordinator 始终为 -1（无内容）。|
|`dbid`|smallint|gp_segment_configuration.dbid|Segment 实例的唯一 ID。|
|`distributed_xid`|xid| |全局事务 ID。|
|`status`|text| |分布式事务的状态（Committed 或 Aborted）。|
|`local_transaction`|xid| |本地事务 ID。|
