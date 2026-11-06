---
title: "DROP INDEX"
description: "Removes an index."
weight: 1130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-index.md"
---

## Synopsis {#synopsis}

```sql
DROP INDEX [ CONCURRENTLY ] [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP INDEX` drops an existing index from the database system. To run this command you must be the owner of the index.

## Parameters {#parameters}

**`CONCURRENTLY`**

Drop the index without locking out concurrent selects, inserts, updates, and deletes on the index's table. A normal `DROP INDEX` acquires an `ACCESS EXCLUSIVE` lock on the table, blocking other accesses until the index drop can be completed. With this option, the command instead waits until conflicting transactions have completed.

There are several caveats to be aware of when using this option. Only one index name can be specified, and the `CASCADE` option is not supported. (Thus, an index that supports a `UNIQUE` or `PRIMARY KEY` constraint cannot be dropped this way.) Also, regular `DROP INDEX` commands can be performed within a transaction block, but `DROP INDEX CONCURRENTLY` cannot.

**`IF EXISTS`**

Do not throw an error if the index does not exist. A notice is issued in this case.

**`name`**

The name (optionally schema-qualified) of an index to remove.

**`CASCADE`**

Automatically drop objects that depend on the index, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the index if any objects depend on it. This is the default.

## Examples {#examples}

Remove the index `title_idx`:

```sql
DROP INDEX title_idx;
```

## Compatibility {#compatibility}

`DROP INDEX` is a Apache Cloudberry language extension. There are no provisions for indexes in the SQL standard.

## See also {#see-also}

[`ALTER INDEX`](/cloudberry/reference/sql-stmts/alter-index/), [`CREATE INDEX`](/cloudberry/reference/sql-stmts/create-index/)
