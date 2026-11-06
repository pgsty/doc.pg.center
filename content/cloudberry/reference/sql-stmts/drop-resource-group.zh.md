---
title: "DROP RESOURCE GROUP"
description: "删除资源组。"
weight: 1230
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-resource-group.md"
---

## 概要 {#synopsis}

```sql
DROP RESOURCE GROUP <group_name>
```

## 描述 {#description}

此命令从 Apache Cloudberry 中删除资源组。只有超级用户才能删除资源组。删除资源组后，该组预留的内存和 CPU 资源会归还给 Apache Cloudberry。

要删除角色资源组，该组不能分配给任何角色，且组内不能有等待或运行中的语句。如果删除为外部组件创建的资源组，行为由外部组件决定。例如，删除已分配给 PL/Container 运行时的资源组，会停止该组中运行的容器。

不能删除预定义的 `admin_group` 和 `default_group` 资源组。

## 参数 {#parameters}

**`group_name`**

要删除的资源组名称。

## 注意事项 {#notes}

不能在显式事务或子事务中提交 `DROP RESOURCE GROUP` 命令。

使用 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 取消为特定用户或角色分配的资源组。

执行以下查询，查看所有资源组当前的全部活动查询：

```sql
SELECT usename, query, waiting, pid,
    rsgid, rsgname, rsgqueueduration 
  FROM pg_stat_activity;
```

要查看资源组分配情况，对 `pg_roles` 和 `pg_resgroup` 系统目录表执行以下查询：

```sql
SELECT rolname, rsgname 
  FROM pg_roles, pg_resgroup
  WHERE pg_roles.rolresgroup=pg_resgroup.oid;
```

## 示例 {#examples}

取消分配给某角色的资源组。此操作随后会将默认资源组 `default_group` 分配给该角色：

```sql
ALTER ROLE bob RESOURCE GROUP NONE;
```

删除名为 `adhoc` 的资源组：

```sql
DROP RESOURCE GROUP adhoc;
```

## 兼容性 {#compatibility}

`DROP RESOURCE GROUP` 语句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER RESOURCE GROUP](/cloudberry/reference/sql-stmts/alter-resource-group/), [CREATE RESOURCE GROUP](/cloudberry/reference/sql-stmts/create-resource-group/), [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/)
