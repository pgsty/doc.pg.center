---
title: "ALTER PROTOCOL"
description: "Changes the definition of a protocol."
weight: 220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-protocol.md"
---

## Synopsis {#synopsis}

```sql
ALTER PROTOCOL <name> RENAME TO <newname>

ALTER PROTOCOL <name> OWNER TO <newowner>
```

## Description {#description}

`ALTER PROTOCOL` changes the definition of a protocol. Only the protocol name or owner can be altered.

You must own the protocol to use `ALTER PROTOCOL`. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on schema of the protocol.

These restrictions are in place to ensure that altering the owner only makes changes that could by made by dropping and recreating the protocol. Note that a superuser can alter ownership of any protocol.

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of an existing protocol.

**`newname`**

The new name of the protocol.

**`newowner`**

The new owner of the protocol.

## Examples {#examples}

To rename the protocol `GPDBauth` to `GPDB_authentication`:

```sql
ALTER PROTOCOL GPDBauth RENAME TO GPDB_authentication;
```

To change the owner of the `GPDB_authentication` protocol to `joe`:

```sql
ALTER PROTOCOL GPDB_authentication OWNER TO joe;
```

## Compatibility {#compatibility}

There is no `ALTER PROTOCOL` statement in the SQL standard.

## See also {#see-also}

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/), [CREATE PROTOCOL](/cloudberry/reference/sql-stmts/create-protocol/), [DROP PROTOCOL](/cloudberry/reference/sql-stmts/drop-protocol/)
