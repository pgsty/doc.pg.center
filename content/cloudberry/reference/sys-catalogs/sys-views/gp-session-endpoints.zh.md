---
title: "gp_session_endpoints"
description: "`gp_session_endpoints` 视图列出当前会话用户在当前会话中声明的所有活动并行检索游标所创建的端点。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-session-endpoints.md"
---

端点仅在定义并行检索游标的事务存续期间存在，或在游标关闭时消失。

|列|类型|引用|说明|
|----|----|----------|-----------|
|gp_segment_id|integer| |QE 的端点 `gp_segment_id`。|
|auth_token|text| |检索会话的身份验证令牌。|
|cursorname|text| |并行检索游标的名称。|
|sessionid|integer| |创建并行检索游标的会话的标识符。|
|hostname|varchar(64)| |用于检索端点数据的主机名称。|
|port|integer| |用于检索端点数据的端口号。|
|username|text| |会话用户（而非当前用户）的名称；*必须以此用户身份发起检索会话*。|
|state|text| |端点的状态；有效状态包括：<br/><br/>READY：端点已准备好供检索。<br/><br/>ATTACHED：端点已附接到一个检索连接。<br/><br/>RETRIEVING：检索会话此刻正在从端点检索数据。<br/><br/>FINISHED：端点的数据已全部检索完毕。<br/><br/>RELEASED：由于出错，端点已释放，连接已关闭。|
|endpointname|text| |端点标识符；需将此标识符提供给 `RETRIEVE` 命令。|
