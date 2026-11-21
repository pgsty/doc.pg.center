---
title: "DROP SEQUENCE"
description: "Removes a sequence."
weight: 1290
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sql-stmts/drop-sequence.md"
---

## Synopsis {#synopsis}

```sql
DROP SEQUENCE [IF EXISTS] <name> [, ...] [CASCADE | RESTRICT]
```

## Description {#description}

`DROP SEQUENCE` removes sequence number generators. You must own the sequence to drop it (or be a superuser).

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the sequence does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of the sequence to remove.

**`CASCADE`**

Automatically drop objects that depend on the sequence, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the sequence if any objects depend on it. This is the default.

## Examples {#examples}

Remove the sequence `myserial`:

```sql
DROP SEQUENCE myserial;
```

## Compatibility {#compatibility}

`DROP SEQUENCE` conforms to the SQL standard, except that the standard allows only one sequence to be dropped per command. Also, the `IF EXISTS` option is a Apache Cloudberry extension.

## See also {#see-also}

[ALTER SEQUENCE](/cloudberry/reference/sql-stmts/alter-sequence/), [CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/)
