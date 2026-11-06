---
title: "pg_auth_members"
description: "The `pg_auth_members` system catalog table in the `pg_catalog` schema shows the membership relations between roles."
weight: 160
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-auth-members.md"
---

Any non-circular set of relationships is allowed. Because roles are system-wide, `pg_auth_members` is shared across all databases of a Apache Cloudberry system.

|column|type|references|description|
|------|----|----------|-----------|
|`roleid`|oid|`pg_authid.oid`|ID of the parent-level (group) role|
|`member`|oid|`pg_authid.oid`|ID of a member role|
|`grantor`|oid|`pg_authid.oid`|ID of the role that granted this membership|
|`admin_option`|boolean| |True if role member might grant membership to others|
