---
title: 手动查询传播
description: 介绍如何在高级场景中绕过 Citus 协调节点，手动传播查询。
weight: 90
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/reference-propagation?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

用户发出查询后，Citus 协调节点将其拆分为较小的查询片段，每个片段都可以在工作节点的一个分片上独立运行。通过这种处理，Citus 可以将每个查询分散到整个集群执行。

不过，查询的拆分方式，以及哪些查询会被传播，取决于查询类型。在某些高级场景中，手动控制这种行为会很有用。Citus 提供了实用函数，可将 SQL 传播到工作节点、分片或共置的分片放置。

手动传播查询会绕过协调节点的逻辑、锁定和其他所有一致性检查。这些函数是最后的手段，用来执行 Citus 原本不支持直接运行的语句。请谨慎使用，以免造成数据不一致和死锁。

## 在所有工作节点上运行 {#running-on-all-workers}

粒度最粗的执行方式是广播一条语句，让所有工作节点执行。这种命令适合查看各工作节点整个数据库的属性。

```sql
-- List the work_mem setting of each worker database
SELECT run_command_on_workers($cmd$ SHOW work_mem; $cmd$);
```

要在所有节点（包括工作节点和协调节点）上运行，请使用 `run_command_on_all_nodes()`。

> [!NOTE]
> 不应使用此命令在工作节点上创建数据库对象，因为这会增加自动添加工作节点的难度。

> [!NOTE]
> `run_command_on_workers` 函数和本节的其他手动传播命令，只能执行返回单行单列结果的查询。

## 在所有分片上运行 {#running-on-all-shards}

下一级粒度是在某个分布式表的所有分片上执行命令。例如，要直接在工作节点上读取表的属性，这种方式就很有用。在工作节点本地运行的查询可以完整访问表统计信息等元数据。

`run_command_on_shards` 函数对每个分片执行一条 SQL 命令，并提供分片名称供命令插值使用。下面的示例利用各工作节点上的 `pg_class` 表估算每个分片的行数，进而估算整个分布式表的行数。注意其中的 `%s`：函数运行时会将它替换为各分片的名称。

```sql
-- Get the estimated row count for a distributed table by summing the
-- estimated counts of rows for each shard.
SELECT sum(result::bigint) AS estimated_count
  FROM run_command_on_shards(
    'my_distributed_table',
    $cmd$
      SELECT reltuples
        FROM pg_class c
        JOIN pg_catalog.pg_namespace n on n.oid=c.relnamespace
       WHERE (n.nspname || '.' || relname)::regclass = '%s'::regclass
         AND n.nspname NOT IN ('citus', 'pg_toast', 'pg_catalog')
    $cmd$
  );
```

`run_command_on_colocated_placements` 是 `run_command_on_shards` 的一个实用配套函数。它将共置分布式表的*两个*分片放置名称插入查询中。每对放置总是位于同一个工作节点，因此可以使用完整的 SQL 功能。这样就能通过触发器等高级 SQL 功能关联这些表：

```sql
-- Suppose we have two distributed tables
CREATE TABLE little_vals (key int, val int);
CREATE TABLE big_vals    (key int, val int);
SELECT create_distributed_table('little_vals', 'key');
SELECT create_distributed_table('big_vals',    'key');

-- We want to synchronize them so that every time little_vals
-- are created, big_vals appear with double the value
--
-- First we make a trigger function, which will
-- take the destination table placement as an argument
CREATE OR REPLACE FUNCTION embiggen() RETURNS TRIGGER AS $$
  BEGIN
    IF (TG_OP = 'INSERT') THEN
      EXECUTE format(
        'INSERT INTO %s (key, val) SELECT ($1).key, ($1).val*2;',
        TG_ARGV[0]
      ) USING NEW;
    END IF;
    RETURN NULL;
  END;
$$ LANGUAGE plpgsql;

-- Next we relate the co-located tables by the trigger function
-- on each co-located placement
SELECT run_command_on_colocated_placements(
  'little_vals',
  'big_vals',
  $cmd$
    CREATE TRIGGER after_insert AFTER INSERT ON %s
      FOR EACH ROW EXECUTE PROCEDURE embiggen(%L)
  $cmd$
);
```

## 限制 {#limitations}

- 对于多语句事务，没有防止死锁的保护措施。
- 没有防止查询中途失败及其引发不一致的保护措施。
- 查询结果缓存在内存中，因此这些函数无法处理大型结果集。
- 如果无法连接到某个节点，函数会提前报错退出。
- 请务必小心，错误操作可能造成严重后果！

## 相关内容 {#related-content}

- [查询处理参考](/citus/reference/reference-processing/)
- [Citus SQL 参考概述](/citus/reference/)
