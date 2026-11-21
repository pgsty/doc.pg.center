---
title: "pg_namespace"
description: "The `pg_namespace` system catalog table stores namespaces. A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts."
weight: 220
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-namespace.md"
---

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |Row identifier (hidden attribute; must be explicitly selected)|
|`nspname`|name| |Name of the namespace|
|`nspowner`|oid|pg_authid.oid|Owner of the namespace|
|`nspacl`|ARRAY| |Access privileges as given by `GRANT` and `REVOKE`|
