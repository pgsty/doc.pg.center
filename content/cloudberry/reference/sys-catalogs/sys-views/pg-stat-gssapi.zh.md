---
title: "pg_stat_gssapi"
description: "`pg_stat_gssapi` 视图按连接提供与 GSSAPI（通用安全服务应用程序接口）身份验证和加密有关的统计信息。"
weight: 240
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-gssapi.md"
---

每一行对应一个后端进程，包含是否使用 GSSAPI 身份验证、主体名称、是否启用加密以及是否委派凭据等信息。可以使用 `pid` 列将此视图与 `pg_stat_activity` 或 `pg_stat_replication` 连接，以获取各连接的更多详细信息。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`pid`|integer| |后端的进程 ID。|
|`gss_authenticated boolean`|boolean| |如果此连接使用了 GSSAPI 身份验证，则为 true。|
|`principal`|text| |用于验证此连接身份的主体；如果此连接未使用 GSSAPI 身份验证，则为 NULL。如果主体名称长于 `NAMEDATALEN`（标准构建中为 64 个字符），此字段会被截断。|
|`encrypted`|boolean| |如果此连接正在使用 GSSAPI 加密，则为 true。|
