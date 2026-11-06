---
title: "gp_version_at_initdb"
description: "The `gp_version_at_initdb` table in the `pg_catalog` schema is populated on the coordinator and each segment in the Apache Cloudberry system."
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-version-at-initdb.md"
---

It identifies the version of Apache Cloudberry used when the system was first initialized. This table is defined in the `pg_global` tablespace, meaning it is globally shared across all databases in the system.

|column|type|references|description|
|------|----|----------|-----------|
|`schemaversion`|smallint| |Schema version number.|
|`productversion`|text| |Product version number.|
