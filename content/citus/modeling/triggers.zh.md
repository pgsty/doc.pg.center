---
title: 分布式表上的触发器
description: 了解如何在 Citus 分布式表上使用触发器，自动执行行级数据操作。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/triggers?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

Citus 不支持在分布式表上创建触发器。作为变通方法，可以直接在工作节点上的表分片上手动创建触发器。

> [!NOTE]
> 通过这些变通方法创建的触发器不会自动应用到未来分片再均衡所创建的分片副本。再均衡后必须重新应用这些变通方法。

**只针对一张分布式表的触发器。**

假设我们希望为表中的每一行记录最后更新它的用户。可以添加一个 `author` 列保存该用户，并通过触发器赋值，而非为该列设置默认值。这样可以防止用户覆盖这条记录。

```sql
CREATE TABLE events (
  id bigserial PRIMARY KEY,
  description text NOT NULL,
  author name NOT NULL
);
SELECT create_distributed_table('events', 'id');
```

不过，这是分布式表，因此在协调节点上为该表创建单个触发器并不起作用。我们需要为该表的每个分片放置创建触发器。

```sql
-- First create a function that all these triggers will use.

CREATE OR REPLACE FUNCTION set_author() RETURNS TRIGGER AS $$
  BEGIN
    NEW.author := current_user;
    RETURN NEW;
  END;
$$ LANGUAGE plpgsql;

-- Now create a trigger for every placement

SELECT run_command_on_shards(
  'events',
  $cmd$
    CREATE TRIGGER events_set_author BEFORE INSERT OR UPDATE ON %s
      FOR EACH ROW EXECUTE PROCEDURE set_author()
  $cmd$
);
```

现在，如果尝试插入伪造数据，author 列至少会显示是谁进行了修改：

```sql
INSERT INTO events (description,author) VALUES ('a bad thing', 'wasnt-me');

TABLE events;
```

```text
┌────┬─────────────┬────────┐
│ id │ description │ author │
├────┼─────────────┼────────┤
│ 1 │ a bad thing │ citus │
└────┴─────────────┴────────┘
```

author 列显示的是“Citus”，而不是“wasnt-me”，说明用户无法伪造该列。

**共置表之间的触发器。**

当两张分布式表共置时，可以创建一个触发器，根据一张表的变化修改另一张表。方法仍然是在各个分片放置上创建触发器，但触发器必须建立在彼此共置的一对分片放置之间。Citus 提供了专用辅助函数 `run_command_on_colocated_placements` 来处理这种情况。

假设每向 `little_vals` 插入一个值，我们都希望向 `big_vals` 插入一个两倍大的值。

```sql
CREATE TABLE little_vals (key int, val int);
CREATE TABLE big_vals    (key int, val int);
SELECT create_distributed_table('little_vals', 'key');
SELECT create_distributed_table('big_vals',    'key');

-- This trigger function takes the destination placement as an argument

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

然后进行测试：

```sql
INSERT INTO little_vals VALUES (1, 42), (2, 101);
TABLE big_vals;
```

```text
┌─────┬─────┐
│ key │ val │
├─────┼─────┤
│   1 │ 84 │
│   2 │ 202 │
└─────┴─────┘
```

**参考表之间的触发器。**

> [!NOTE]
> **这种变通方法只在有限场景下安全。** 使用此类触发器向参考表插入数据时，必须确保目标表不会发生并发更新。无法保证并发更新、删除和插入命令应用到副本的顺序，参考表副本可能彼此不同步。对目标表的所有数据修改都必须只通过触发器完成。

参考表比分布式表简单，因为它们只有一个分片，并且会复制到所有工作节点。要通过触发器关联参考表，可以在所有工作节点上为该分片创建触发器。

假设我们要把 `insert_target` 中每次变更的作者记录到 `audit_table` 中，而这两张表都是参考表。只要只有触发器会更新 `audit_table`，这种结构就是安全的。

```sql
-- create the reference tables

CREATE TABLE insert_target (
  value text
);
CREATE TABLE audit_table(
  author name NOT NULL,
  value text
);
SELECT create_reference_table('insert_target');
SELECT create_reference_table('audit_table');
```

要在每个工作节点上创建更新 `audit_table` 的触发器，需要知道该表分片的名称。与其从元数据表中查找名称，再手动将它传给 `run_command_on_workers`，不如使用 `run_command_on_shards`。参考表在每个工作节点上恰好有一个分片放置，因此下面的命令正好可以完成任务。

```sql
SELECT run_command_on_shards(
  'audit_table',
  $cmd$
    CREATE OR REPLACE FUNCTION process_audit() RETURNS TRIGGER AS $$
      BEGIN
        INSERT INTO %s (author,value)
          VALUES (current_user,NEW.value);
        RETURN NEW;
      END;
    $$ LANGUAGE plpgsql;
  $cmd$
);

SELECT run_command_on_shards(
  'insert_target',
  $cmd$
    CREATE TRIGGER emp_audit
    AFTER INSERT OR UPDATE ON %s
      FOR EACH ROW EXECUTE PROCEDURE process_audit();
  $cmd$
);

INSERT INTO insert_target (value) VALUES ('inserted value');

TABLE audit_table;
```

```text
┌────────┬────────────────┐
│ author │     value      │
├────────┼────────────────┤
│ citus │ inserted value │
└────────┴────────────────┘
```

此表显示触发器已执行，并添加了一行包含 `author` 列的记录。

**从分布式表到参考表的触发器。**

这是不可能的。

## 相关内容 {#related-content}

- [DDL 命令](/citus/reference/reference-ddl/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
