---
title: "gp_segment_configuration"
description: "`pg_catalog` 模式中的 `gp_segment_configuration` 表记录镜像和 Segment 实例配置的信息。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-segment-configuration.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`dbid`|smallint| |Segment（或 Coordinator）实例的唯一标识符。|
|`content`|smallint| |Segment 实例的内容标识符。主 Segment 实例及其对应镜像的内容标识符始终相同。<br/><br/>对于 Segment，取值为 0 到 *N*-1，其中 *N* 是系统中主 Segment 的数量。<br/><br/>对于 Coordinator，值始终为 -1。|
|`role`|char| |Segment 当前运行的角色。取值为 `p`（主实例）或 `m`（镜像）。|
|`preferred_role`|char| |初始化时最初分配给 Segment 的角色。取值为 `p`（主实例）或 `m`（镜像）。|
|`mode`|char| |Segment 实例与其镜像副本之间的同步状态。取值为 `s`（已同步）或 `n`（未同步）。<br/><br/>对于 Coordinator Segment，此列始终显示 `n`；对于 Standby Coordinator Segment，此列始终显示 `s`，但这些值并不描述 Coordinator Segment 的同步状态。请使用 `gp_stat_replication` 确定 Coordinator 与 Standby Coordinator 之间的同步状态。|
|`status`|char| |Segment 实例的故障状态。取值为 `u`（正常运行）或 `d`（已停止）。|
|`port`|integer| |数据库服务器监听进程使用的 TCP 端口。|
|`hostname`|text| |Segment 主机的主机名。|
|`address`|text| |用于访问 Segment 主机上某个特定 Segment 实例的主机名。在没有为各网络接口配置主机名的系统中，此值可能与 `hostname` 相同。|
|`datadir`|text| |Segment 实例的数据目录。|
| `warehouseid` | oid |Segment 所属仓库的 ID。|
