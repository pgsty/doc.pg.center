---
title: "gp_configuration_history"
description: "`pg_catalog` 模式中的 `gp_configuration_history` 表记录与故障检测和恢复操作相关的系统变更信息。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-configuration-history.md"
---

`fts_probe` 进程会向此表记录数据，某些相关管理工具（例如 `gprecoverseg` 和 `gpinitsystem`）也会如此。例如，向系统添加新的 Segment 和镜像 Segment 时，相应事件的记录会写入 `gp_configuration_history`。

此表中存储的事件描述可能有助于排查严重的系统问题。

此表只在 Coordinator 上填充。它定义在 `pg_global` 表空间中，因此由系统中的所有数据库全局共享。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`time`|timestamp with time zone| |事件记录的时间戳。|
|`dbid`|smallint| `gp_segment_configuration.dbid` |系统分配的 ID，用于唯一标识一个 Segment（或 Coordinator）实例。|
| `desc` |text| |事件的文本描述。|
