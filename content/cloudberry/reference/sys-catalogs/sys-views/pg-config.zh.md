---
title: "pg_config"
description: "`pg_config` 视图显示所安装的 Cloudberry/PostgreSQL 的编译时配置参数。"
weight: 150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-config.md"
---

其中包括安装目录、编译器标志和版本详情等信息。通常只有超级用户才能访问。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`name`|text| |参数名称。|
|`setting`|text| |参数值。|
