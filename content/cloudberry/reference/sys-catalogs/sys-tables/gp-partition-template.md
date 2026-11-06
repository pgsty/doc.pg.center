---
title: "gp_partition_template"
description: "The `gp_partition_template` system catalog table in the `pg_catalog` schema describes the relationship between a partitioned table and the sub-partition template defined at each level in the partition hierarchy."
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/gp-partition-template.md"
---

> [!NOTE]
> Apache Cloudberry supports sub-partition templates only for partitioned tables that you create with the classic syntax.

Each sub-partition template has a dependency on the existence of a template at the next lower level of the hierarchy.

|column|type|references|description|
|------|----|----------|-----------|
|`relid`| oid | `pg_class.oid` | The object identifier of the root partitioned table. |
|`level`|smallint| | The level of the partition in the hierarchy. The levels are numbered as follows: level `0` is the root partitioned table itself, level `1` represents the direct child/children of the root partitioned table, and so forth. The leaf partitions have the highest level number.|
|`template`| `pg_node_tree` | | Expression representation of the sub-partition template defined for each partition at this level of the hierarchy. |
