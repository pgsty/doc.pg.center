---
title: "gp_fastsequence"
description: "The `gp_fastsequence` table in the `pg_catalog` schema contains information about append-optimized and column-oriented tables."
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-fastsequence.md"
---

The `last_sequence` value indicates maximum row number currently used by the table.

|column|type|references|description|
|------|----|----------|-----------|
|`objid`|oid| `pg_class.oid` |Object id of the `pg_aoseg.pg_aocsseg_*` table used to track append-optimized file segments.|
|`objmod`|bigint| |Object modifier.|
|`last_sequence`|bigint| |The last sequence number used by the object.|
