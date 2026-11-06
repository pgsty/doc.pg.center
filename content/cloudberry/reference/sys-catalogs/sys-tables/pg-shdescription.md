---
title: "pg_shdescription"
description: "The `pg_shdescription` system catalog table stores optional descriptions (comments) for shared database objects."
weight: 350
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-shdescription.md"
---

Descriptions can be manipulated with the `COMMENT` command and viewed with `psql`'s `d` meta-commands. See also [pg_description](/cloudberry/reference/sys-catalogs/sys-tables/pg-description/), which performs a similar function for descriptions involving objects within a single database. Unlike most system catalogs, `pg_shdescription` is shared across all databases of a Cloudberry system: there is only one copy of `pg_shdescription` per system, not one per database.

|column|type|references|description|
|------|----|----------|-----------|
|`objoid`|oid|any OID column|The OID of the object this description pertains to.|
|`classoid`|oid|pg_class.oid|The OID of the system catalog this object appears in|
|`description`|text| |Arbitrary text that serves as the description of this object.|
