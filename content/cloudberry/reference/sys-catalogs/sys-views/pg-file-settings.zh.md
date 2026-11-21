---
title: "pg_file_settings"
description: "`pg_file_settings` 视图提供服务器配置文件的摘要，显示各参数的名称、值、源文件、行号、是否成功应用以及相关错误消息。"
weight: 170
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-file-settings.md"
---

此视图有助于验证配置更改以及诊断配置文件中的问题。

|名称|类型|引用|说明|
|----|----|----------|-----------|
|`sourcefile`|text| |配置文件的完整路径名。|
|`sourceline`|integer| |条目在配置文件中的行号。|
|`seqno`|integer| |条目的处理顺序（1..n）。|
|`name`|text| |配置参数名称。|
|`setting`|text| |要赋给参数的值。|
|`applied`|boolean| |如果此值可以成功应用，则为 true。|
|`error`|text| |如果非空，则为说明此条目为何无法应用的错误消息。|
