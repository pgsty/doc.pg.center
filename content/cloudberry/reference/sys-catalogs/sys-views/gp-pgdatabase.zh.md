---
title: "gp_pgdatabase"
description: "`gp_pgdatabase` 视图显示 Apache Cloudberry Segment 实例的状态，以及它们当前是镜像还是主实例。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-pgdatabase.md"
---

Apache Cloudberry 的故障检测和恢复工具在内部使用此视图来识别故障 Segment。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`dbid`|smallint|gp_segment_configuration.dbid|系统分配的 ID，是 Segment（或 Coordinator）实例的唯一标识符。|
|`isprimary`|boolean|gp_segment_configuration.role|此实例是否处于活动状态，即当前是否充当主 Segment（而非镜像）。|
|`content`|smallint|gp_segment_configuration.content|实例所存储数据部分的 ID。主 Segment 实例及其镜像具有相同的内容 ID。<br/><br/>对于 Segment，此值为 0 到 *N-1*，其中 *N* 是 Apache Cloudberry 中的 Segment 数量。<br/><br/>对于 Coordinator，此值为 -1。|
|`valid`|boolean|gp_segment_configuration.mode|此实例是否正在运行，且模式为 *s*（已同步）或 *n*（未同步）。|
|`definedprimary`|boolean|gp_segment_configuration.preferred_role|系统初始化时，此实例是否被定义为主实例（而非镜像）。|
