---
title: "pg_am"
description: "The `pg_am` table in the `pg_catalog` schema stores information about index access methods."
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-am.md"
---

There is one row for each index access method supported by the system.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |Row identifier (hidden attribute; must be explicitly selected)|
|`amname`|name| |Name of the access method|
|`amhandler`|regproc| | OID of a handler function responsible for supplying information about the access method|
|`amtype`|char| |`t` for table (including materialized views), `i` for index|
