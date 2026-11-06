---
title: "DROP RESOURCE QUEUE"
description: "删除资源队列。"
weight: 1240
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-resource-queue.md"
---

## 概要 {#synopsis}

```sql
DROP RESOURCE QUEUE <queue_name>
```

## 描述 {#description}

此命令从 Apache Cloudberry 中删除资源队列。要删除资源队列，不能有角色分配给该队列，且队列中不能有等待的语句。只有超级用户才能删除资源队列。

## 参数 {#parameters}

**`queue_name`**

要删除的资源队列名称。

## 注意事项 {#notes}

使用 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 将用户从资源队列中移出。

要查看所有资源队列当前的全部活动查询，对 `pg_locks` 表与 `pg_roles`、`pg_resqueue` 表执行以下连接查询：

```sql
SELECT rolname, rsqname, locktype, objid, pid, 
mode, granted FROM pg_roles, pg_resqueue, pg_locks WHERE 
pg_roles.rolresqueue=pg_locks.objid AND 
pg_locks.objid=pg_resqueue.oid;
```

要查看分配给资源队列的角色，对 `pg_roles` 和 `pg_resqueue` 系统目录表执行以下查询：

```sql
SELECT rolname, rsqname FROM pg_roles, pg_resqueue WHERE 
pg_roles.rolresqueue=pg_resqueue.oid;
```

## 示例 {#examples}

将角色从资源队列中移出（并移至默认资源队列 `pg_default`）：

```sql
ALTER ROLE bob RESOURCE QUEUE NONE;
```

删除名为 `adhoc` 的资源队列：

```sql
DROP RESOURCE QUEUE adhoc;
```

## 兼容性 {#compatibility}

`DROP RESOURCE QUEUE` 语句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER RESOURCE QUEUE](/cloudberry/reference/sql-stmts/alter-resource-queue/), [CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/), [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/)
