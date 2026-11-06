---
title: "DISCARD"
description: "丢弃会话状态。"
weight: 980
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/discard.md"
---

## 概要 {#synopsis}

```sql
DISCARD { ALL | PLANS | SEQUENCES | TEMPORARY | TEMP }
```

## 描述 {#description}

`DISCARD` 释放与数据库会话关联的内部资源。此命令可用于部分或完全重置会话状态。它有几个子命令，用于释放不同类型的资源；`DISCARD ALL` 变体涵盖所有其他子命令，并且还会重置其他状态。

Apache Cloudberry 不支持在事务中调用 `DISCARD ALL`。

## 参数 {#parameters}

**`PLANS`**

释放所有缓存的查询计划，使下次使用相关预备语句时必须重新规划。

**`SEQUENCES`**

丢弃所有缓存的序列相关状态，包括所有已预分配但尚未由 `nextval()` 返回的序列值。（关于预分配序列值的说明，见 [CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/)。）

**`TEMPORARY/TEMP`**

删除当前会话创建的所有临时表。

**`ALL`**

释放与当前会话关联的所有临时资源，并将会话重置为初始状态。目前，此操作等效于依次执行以下语句：

```sql
    CLOSE ALL;
    SET SESSION AUTHORIZATION DEFAULT;
    RESET ALL;
    DEALLOCATE ALL;
    UNLISTEN *;
    SELECT pg_advisory_unlock_all();
    DISCARD PLANS;
    DISCARD SEQUENCES;
    DISCARD TEMP;
```

## 注意事项 {#notes}

`DISCARD ALL` 不能在事务块中运行。

## 兼容性 {#compatibility}

`DISCARD` 是 Apache Cloudberry 的扩展。
