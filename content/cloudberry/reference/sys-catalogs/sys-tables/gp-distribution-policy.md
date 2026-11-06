---
title: "gp_distribution_policy"
description: "The `gp_distribution_policy` table in the `pg_catalog` schema contains information about Apache Cloudberry tables and their policy for distributing table data across the segments."
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-distribution-policy.md"
---

This table is populated only on the coordinator. This table is not globally shared, meaning each database has its own copy of this table.

|column|type|references|description|
|------|----|----------|-----------|
|`localoid`|oid| `pg_class.oid` |The table object identifier (OID).|
|`policytype`|char| |The table distribution policy:<br/><br/>`p` - Partitioned policy. Table data is distributed among segment instances.<br/><br/>`r` - Replicated policy. Table data is replicated on each segment instance.|
|`numsegments`|integer| |The number of segment instances on which the table data is distributed.|
|`distkey`|int2vector| `pg_attribute.attnum` |The column number(s) of the distribution column(s).|
|`distclass`|oidvector|`pg_opclass.oid`|The operator class identifier(s) of the distribution column(s).|
