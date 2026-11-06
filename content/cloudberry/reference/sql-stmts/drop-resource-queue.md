---
title: "DROP RESOURCE QUEUE"
description: "Removes a resource queue."
weight: 1240
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-resource-queue.md"
---

## Synopsis {#synopsis}

```sql
DROP RESOURCE QUEUE <queue_name>
```

## Description {#description}

This command removes a resource queue from Apache Cloudberry. To drop a resource queue, the queue cannot have any roles assigned to it, nor can it have any statements waiting in the queue. Only a superuser can drop a resource queue.

## Parameters {#parameters}

**`queue_name`**

The name of a resource queue to remove.

## Notes {#notes}

Use [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) to remove a user from a resource queue.

To see all the currently active queries for all resource queues, perform the following query of the `pg_locks` table joined with the `pg_roles` and `pg_resqueue` tables:

```sql
SELECT rolname, rsqname, locktype, objid, pid, 
mode, granted FROM pg_roles, pg_resqueue, pg_locks WHERE 
pg_roles.rolresqueue=pg_locks.objid AND 
pg_locks.objid=pg_resqueue.oid;
```

To see the roles assigned to a resource queue, perform the following query of the `pg_roles` and `pg_resqueue` system catalog tables:

```sql
SELECT rolname, rsqname FROM pg_roles, pg_resqueue WHERE 
pg_roles.rolresqueue=pg_resqueue.oid;
```

## Examples {#examples}

Remove a role from a resource queue (and move the role to the default resource queue, `pg_default`):

```sql
ALTER ROLE bob RESOURCE QUEUE NONE;
```

Remove the resource queue named `adhoc`:

```sql
DROP RESOURCE QUEUE adhoc;
```

## Compatibility {#compatibility}

The `DROP RESOURCE QUEUE` statement is a Apache Cloudberry extension.

## See also {#see-also}

[ALTER RESOURCE QUEUE](/cloudberry/reference/sql-stmts/alter-resource-queue/), [CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/), [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/)
