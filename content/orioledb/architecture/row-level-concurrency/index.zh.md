---
title: 行级并发
linkTitle: 行级并发
description: OrioleDB 行级并发与 PostgreSQL 堆表的差异，以及事务 ID 分配的影响。
weight: 60
type: docs
search_keywords: ["OrioleDB", "row level concurrency"]
upstream_link: https://www.orioledb.com/docs/architecture/row-level-concurrency
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-lock
---


OrioleDB 的行级并发尽可能接近普通 PostgreSQL 表。但由于 OrioleDB 使用索引组织表，仍然存在一些差异。

## 更新主键 {#update-of-the-primary-key}

在索引组织表中，更新主键通常是少见的非常规操作。与普通更新不同，主键更新以删除后插入的方式实现。并发更新和删除无法沿着这次更新继续追踪，可能报错。如下例所示，会话 1 并发更新主键，导致会话 2 报错。

``` sql
CREATE TABLE tbl
(
  id int4 primary key,
  value numeric NOT NULL
) USING orioledb;

INSERT INTO tbl VALUES (1, 0.0);
```

会话 1：

``` bash
> BEGIN;
> UPDATE tbl SET id = 2 WHERE id = 1;
UPDATE 1
```

会话 2：

``` bash
> BEGIN;
> UPDATE tbl SET value = value + 1 WHERE id = 1;
(waiting)
> COMMIT;
COMMIT
ERROR:  tuple to be locked has its primary key changed due to concurrent update
> ROLLBACK;
ROLLBACK
```

## 跟随更新链 {#following-the-update-chain}

如果某行被删除，随后立即插入主键相同的新行，并发更新或删除可能将新行视为旧行的新版本。如下例所示，会话 1 删除一行，再插入主键相同的新行；会话 2 原本打算更新最初的行，最终却更新了新插入的行。

``` sql
CREATE TABLE tbl
(
  id int4 primary key,
  value numeric NOT NULL
) USING orioledb;

INSERT INTO tbl VALUES (1, 0.0);
```

会话 1：

``` bash
> BEGIN;
> DELETE FROM tbl WHERE id = 1;
DELETE 1
> INSERT INTO tbl VALUES (1, 0.0);
INSERT 0 1
```

会话 2：

``` bash
> BEGIN;
> UPDATE tbl SET value = value + 1 WHERE id = 1;
(waiting)
> COMMIT;
COMMIT
UPDATE 1
> COMMIT;
COMMIT
```

## 事务 ID 分配与堆关系 {#transaction-id-allocation-and-heap-relations}

对于完全限定在 OrioleDB 表内的操作，OrioleDB 使用虚拟事务 ID（Virtual XID）优化并发，绕过完整 PostgreSQL 事务 ID（XID）的分配，以及堆关系所需的相关 WAL 开销。

在 OrioleDB 事务中修改任何 PostgreSQL `heap` 关系，都会强制分配完整 XID，改变并发执行路径，使虚拟 XID 优化失效。

### 序列生成的开销 {#sequence-generation-overhead}

PostgreSQL 序列基于 `heap` 关系实现。`nextval()` 会修改序列关系，触发完整 XID 分配。要保留 OrioleDB 的事务优化：

- **启用序列缓存：** 使用 `CACHE` 配置序列，例如 `CREATE SEQUENCE my_seq CACHE 100;`。
- **工作机制：** 只有获取整批缓存值的那次 `nextval()` 调用需要修改堆并分配完整 XID，后续调用从会话内存取值。
- **工作负载影响：** 对大量小事务的负载，这项优化可能至关重要。对大事务而言，单次 XID 分配的成本已被充分摊薄。
