---
title: "pg_config"
description: "The `pg_config` view displays the compile-time configuration parameters of the Cloudberry/PostgreSQL installation."
weight: 150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-config.md"
---

It includes information such as installation directories, compiler flags, and version details. Access is typically restricted to superusers.

|column|type|references|description|
|------|----|----------|-----------|
|`name`|text| |The parameter name.|
|`setting`|text| |The parameter value.|
