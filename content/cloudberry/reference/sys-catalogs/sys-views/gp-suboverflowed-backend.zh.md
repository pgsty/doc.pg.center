---
title: "gp_suboverflowed_backend"
description: "`gp_suboverflowed_backend` 视图允许管理员识别后端发生子事务溢出的会话；子事务溢出可能导致系统中的查询性能下降，包括目录查询。"
weight: 130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-suboverflowed-backend.md"
---

|列|类型|说明|
|------|----|----------|
|`segid`|integer|发生子事务溢出的后端所在 Segment 的 ID。|
|`pids`|integer[]|此 Segment 上所有发生子事务溢出的后端的 PID 列表。|
