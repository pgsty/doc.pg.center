---
title: "pg_user_mapping"
description: "The system catalog table `pg_user_mapping` stores the mappings from local user to remote user."
weight: 450
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-user-mapping.md"
---

You must have administrator privileges to view this catalog. Access to this catalog is restricted from normal users, use the `pg_user_mappings` view instead.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |The object ID|
|`umuser`|oid|pg_authid.oid|OID of the local role being mapped, 0 if the user mapping is public.|
|`umserver`|oid|pg_foreign_server.oid|OID of the foreign server that contains this mapping|
|`umoptions`|ARRAY| |User mapping-specific options, as "keyword=value" strings.|
