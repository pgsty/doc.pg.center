---
title: "pg_sequence"
description: "The system catalog table `pg_sequence` contains information about sequences."
weight: 330
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-sequence.md"
---

Some information about sequences, such as the name and the schema, is stored in the [pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/) system table.

|column|type|references|description|
|------|----|----------|-----------|
|`seqrelid`|oid|`pg_class.oid` |OID of the `pg_class` entry for this sequence|
|`seqtypid`|oid|`pg_type.oid`|Data type of the sequence|
|`seqstart`|bigint| |Start value of the sequence|
|`seqincrement`|bigint| |Increment value of the sequence|
|`seqmax`|bigint| |Maximum value of the sequence|
|`seqmin`|bigint| |Minimum value of the sequence|
|`seqcache`|bigint| |Cache size of the sequence|
|`seqcycle`|boolean| |Whether the sequence cycles|
