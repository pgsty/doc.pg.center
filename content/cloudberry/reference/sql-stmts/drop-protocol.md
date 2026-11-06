---
title: "DROP PROTOCOL"
description: "Removes a data access protocol from a database."
weight: 1220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-protocol.md"
---

## Synopsis {#synopsis}

```sql
DROP PROTOCOL [IF EXISTS] <name>
```

## Description {#description}

`DROP PROTOCOL` removes the specified protocol from a database. You specify a protocol name in the `CREATE EXTERNAL TABLE` command to read data from or write data to an external data source.

You must be a superuser or the protocol owner to drop a protocol.

> **Caution** If you drop a data access prococol, external tables that have been defined specifying the protocol will no longer be able to access the external data source.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the protocol does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name of an existing data access protocol.

## Notes {#notes}

Dropping a data access protocol, does not drop the protocol's call handlers. You must drop these functions manually.

Be sure to remove any shared libraries that were used by the protocol from the Apache Cloudberry hosts.

## Compatibility {#compatibility}

`DROP PROTOCOL` is a Apache Cloudberry extension.

## See also {#see-also}

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/), [CREATE PROTOCOL](/cloudberry/reference/sql-stmts/create-protocol/)
