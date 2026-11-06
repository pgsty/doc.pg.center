---
title: "pg_namespace"
description: "The `pg_namespace` system catalog table stores namespaces. A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts."
weight: 220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-namespace.md"
---

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |Row identifier (hidden attribute; must be explicitly selected)|
|`nspname`|name| |Name of the namespace|
|`nspowner`|oid|pg_authid.oid|Owner of the namespace|
|`nspacl`|ARRAY| |Access privileges as given by `GRANT` and `REVOKE`|
