---
title: 创建和修改分布式对象（DDL）
description: 本文介绍如何使用 Citus 中的数据定义语言（DDL）创建和修改分布式对象。
weight: 60
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/reference-ddl?view=citus-14
upstream_ref: citus-14; be6cf64ecd13
translation_status: translated
---

以下各节介绍如何在 Citus 中使用数据定义语言（DDL）创建和修改分布式对象。

## 创建和分布模式 {#creating-and-distributing-schemas}

Citus 12.0 引入了基于模式的分片，允许将整个模式分布到集群中。每个分布式模式会自动关联一个独立的共置组。在这些模式中创建的表会自动成为共置的分布式表，无需指定分片键。

在 Citus 中，可以通过两种方式分布模式：

1. 在协调节点手动调用 `citus_schema_distribute` 函数：

   ```sql
   SELECT citus_schema_distribute('user_service');
   ```

   这种方式也可以将现有的普通模式转换为分布式模式。

   > [!NOTE]
   > 只有不包含分布式表和参考表的模式才能进行分布。
2. 启用 `enable_schema_based_sharding` 配置变量：

   ```sql
   SET citus.enable_schema_based_sharding TO ON;
   
   CREATE SCHEMA AUTHORIZATION user_service;
   ```

   可以仅对当前会话修改此变量，也可以在 `postgresql.conf` 中永久设置。将其设置为 `ON` 后，新创建的所有模式默认都是分布式模式。

分布模式时，Citus 会自动将其分配并迁移到集群中的一个现有节点。后台分片再平衡器在平衡集群时，会将这些模式及其中的所有表纳入考虑，选择最优的移动方案，在集群节点之间迁移模式。

要将模式还原为普通 PostgreSQL 模式，请在协调节点调用 `citus_schema_undistribute`：

```sql
SELECT citus_schema_undistribute('user_service');
```

`user_service` 模式中的表和数据会从当前节点迁回集群的协调节点。

对于可以从集群任意节点执行的分布式模式表 DDL，另见[允许从任意节点对分布式模式表执行的 DDL](#ddls-allowed-from-any-node-for-distributed-schema-tables)。

## 传播模式 {#propagating-schemas}

即使不使用基于模式的分片，也可以将模式传播到整个集群。例如，为了按行分片，可以在非默认模式中创建普通分布式表。

从 Citus 13.3 开始，集群中任意节点都可以将 `CREATE SCHEMA`、`DROP SCHEMA` 和 `ALTER SCHEMA` 命令传播到其他所有节点，无论该模式是否用于基于模式的分片（即是否在启用 `citus.enable_schema_based_sharding` 时创建）。

## 创建和分布表 {#creating-and-distributing-tables}

创建分布式表时，首先定义表结构。与普通 PostgreSQL 表一样，使用 [CREATE TABLE](http://www.postgresql.org/docs/current/static/sql-createtable.html) 语句定义表。

```sql
CREATE TABLE github_events
(
    event_id bigint,
    event_type text,
    event_public boolean,
    repo_id bigint,
    payload jsonb,
    repo jsonb,
    actor jsonb,
    org jsonb,
    created_at timestamp
);
```

接着，使用 `create_distributed_table()` 函数指定分布列，并在工作节点上创建分片。

```sql
SELECT create_distributed_table('github_events', 'repo_id');
```

该函数告知 Citus：应对 `repo_id` 列的值进行哈希，按该列分布 `github_events` 表。函数还会根据 `citus.shard_count` 的配置值在工作节点上创建分片。

本例共创建 `citus.shard_count` 个分片，每个分片负责哈希令牌空间的一部分。创建完成后，函数将全部分布式元数据保存在协调节点上。

每个分片都有一个唯一的分片 ID。在工作节点上，分片表现为名为 `tablename_shardid` 的普通 PostgreSQL 表，其中 `tablename` 是分布式表名，`shardid` 是该分片的唯一 ID。可以连接工作节点的 PostgreSQL 实例，查看单个分片或对其执行命令。

现在就可以向分布式表插入数据并执行查询了。本节所用用户定义函数的更多信息，参见 [Citus 实用函数](/citus/reference/api-udf/)。

### 参考表 {#reference-tables}

上一节介绍了将表分成多个水平分片的方法。另一种方式是将整个表分为一个分片，再将该分片复制到每个工作节点。以这种方式分布的表称为*参考表*，适合存储集群中多个节点需要频繁访问的数据。

以下表通常适合作为参考表：

- 需要与大型分布式表连接的小表。
- 多租户应用中没有租户 ID 列或不属于特定租户的表。有时，为减少迁移工作，即使某个表关联租户，只要目前缺少租户 ID，用户也可能将它设为参考表。
- 需要跨多列唯一约束且规模足够小的表。

例如，一个多租户电商网站需要为各店铺的交易计算销售税。税务信息并不属于某个特定租户，因此适合集中存放在共享表中。面向美国的参考表可以如下定义：

```sql
-- a reference table

CREATE TABLE states (
  code char(2) PRIMARY KEY,
  full_name text NOT NULL,
  general_sales_tax numeric(4,3)
);

-- distribute it to all workers

SELECT create_reference_table('states');
```

现在，计算购物车税额之类的查询可以与 `states` 表连接而不产生网络开销，还可以为州代码添加外键，以加强验证。

用户定义函数 `create_reference_table` 不仅将表分布为单个复制分片，还会在 Citus 元数据表中将其标记为参考表。修改这种表时，Citus 自动执行两阶段提交（[2PC](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)），提供强一致性保证。

对于现有分布式表，可以运行以下命令将其改为参考表：

```sql
SELECT undistribute_table('table_name');
SELECT create_reference_table('table_name');
```

多租户应用使用参考表的另一个例子参见 `mt_ref_tables`。

### 分布协调节点上的数据 {#distributing-coordinator-data}

将现有 PostgreSQL 数据库转换为 Citus 集群的协调节点后，可以高效地分布其中各表的数据，同时将对应用的中断降到最低。

前面介绍的 `create_distributed_table` 既适用于空表，也适用于非空表。对于非空表，它会自动将表中的行分布到整个集群。出现“NOTICE: Copying data from local table...”消息就表示正在分布数据。例如：

```sql
CREATE TABLE series AS SELECT i FROM generate_series(1,1000000) i;
SELECT create_distributed_table('series', 'i');
NOTICE:  Copying data from local table...
NOTICE:  copying the data has completed
DETAIL:  The local data in the table is no longer visible, but is still on disk.
HINT:  To remove the local data, run: SELECT truncate_local_data_after_distributing_table($$public.series$$)
 create_distributed_table
 --------------------------

 (1 row)
```

数据迁移期间，表上的写入会被阻塞。函数提交后，等待中的写入会按分布式查询处理；如果函数失败，这些查询仍在本地执行。读取可以照常继续，并在函数提交后转为分布式查询。

如果表 A 有指向表 B 的外键，应先分布被引用的表 B，再分布 A。顺序错误会导致报错：

```text
ERROR: cannot create foreign key constraint
DETAIL: Referenced table must be a distributed table or a reference table.
```

如果无法按正确顺序分布，可以先删除外键，分布表后再重新创建外键。

分布完成后，使用 `truncate_local_data_after_distributing_table` 删除本地数据。分布式表残留的本地数据无法通过 Citus 查询访问，还可能在协调节点上引发无关的约束违例。

从外部数据库迁移数据时，例如从 Amazon RDS 迁移到 `cloud_topic`，应先使用 `create_distributed_table` 创建 Citus 分布式表，再将数据复制进去。直接复制到分布式表可避免耗尽协调节点的存储空间。

## 表共置 {#colocating-tables}

共置是有策略地划分数据，将相关信息保存在同一机器上，以便高效执行关系操作，同时让整个数据集仍能横向扩展。更多说明和示例参见[共置组表](/citus/reference/api-metadata/#colocation-group-table)。

Citus 自动将表划入共置组。要手动控制表所属的共置组，可以使用 `create_distributed_table` 的可选参数 `colocate_with`。如果不关心共置关系，可以省略该参数；默认值为 `'default'`，会将该表与分布列类型、分片数相同的其他默认共置表分到同一组。要解除或更新这种隐式共置关系，请使用 `update_distributed_table_colocation()`。

```sql
-- these tables are implicitly co-located by using the same
-- distribution column type and shard count with the default
-- co-location group

SELECT create_distributed_table('A', 'some_int_col');
SELECT create_distributed_table('B', 'other_int_col');
```

如果新表与其隐式共置组中的其他表没有关联，请指定 `colocated_with => 'none'`。

```sql
-- not co-located with other tables

SELECT create_distributed_table('A', 'foo', colocate_with => 'none');
```

将互不相关的表分到独立的共置组，可以提高分片再平衡性能，因为同组分片会一起移动。

对于相关的表（例如需要互相连接的表），应显式设置共置。合理共置带来的收益比再平衡开销更重要。

要显式共置多个表，可以先分布其中一个，再将其余表加入它的共置组。例如：

```sql
-- distribute stores
SELECT create_distributed_table('stores', 'store_id');

-- add to the same group as stores
SELECT create_distributed_table('orders', 'store_id', colocate_with => 'stores');
SELECT create_distributed_table('products', 'store_id', colocate_with => 'stores');
```

共置组信息保存在 `pg_dist_colocation` 表中，`pg_dist_partition` 则记录各表所属的共置组。

## 删除和截断表 {#dropping-and-truncating-tables}

使用标准 PostgreSQL `DROP TABLE` 命令删除分布式表，或使用 `TRUNCATE` 清空其中的所有行。与普通表一样，`DROP TABLE` 会删除目标表上的索引、规则、触发器和约束。此外，它还会删除工作节点上的分片并清理元数据。

Citus 还支持从任意节点对 Citus 表执行 `TRUNCATE`。

从 Citus 13.3 开始，也可以从任意节点对分布式模式中的表执行 `DROP TABLE`。

```sql
DROP TABLE github_events;
```

## 修改表 {#modifying-tables}

Citus 自动传播多种 DDL 语句。在协调节点修改分布式表时，工作节点上的分片也会更新。有些 DDL 需要手动传播，另一些则被禁止，例如修改分布列的语句。尝试执行不支持自动传播的 DDL 会报错，协调节点上的表保持不变。

以下列出可以传播的 DDL 类型。可以通过配置参数启用或禁用自动传播。

> [!NOTE]
> 对于分布式模式中的表，其中一些 DDL 也可以从任意节点执行。参见[允许从任意节点对分布式模式表执行的 DDL](#ddls-allowed-from-any-node-for-distributed-schema-tables)。

### 添加或修改列 {#adding-or-modifying-columns}

Citus 自动传播大多数 [ALTER TABLE](https://www.postgresql.org/docs/current/static/ddl-alter.html) 命令。添加列或修改默认值的方式与单机 PostgreSQL 相同：

```sql
-- Adding a column

ALTER TABLE products ADD COLUMN description text;

-- Changing default value

ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
```

也可以对现有列作较大调整，例如重命名或修改数据类型。不过，不能修改分布列的数据类型。该列决定 Citus 如何在集群中分布表数据，修改其类型需要移动数据。

尝试修改分布列的数据类型会报错：

```sql
-- assuming store_id is the distribution column
-- for products, and that it has type integer

ALTER TABLE products
ALTER COLUMN store_id TYPE text;

/*
ERROR:  cannot execute ALTER TABLE command involving partition column
*/
```

一种变通方法是先切换分布列（[alter_distributed_table](/citus/reference/api-udf/#alter_distributed_table)），修改原列后再切换回来。

### 添加或删除约束 {#adding-or-removing-constraints}

使用 Citus 时，仍可享有关系数据库的安全保障，包括数据库约束。更多信息参见 PostgreSQL [文档](https://www.postgresql.org/docs/current/static/ddl-constraints.html)。由于分布式系统的特点，Citus 不会跨工作节点检查唯一性约束或引用完整性。

在共置分布式表之间设置外键时，外键必须包含分布列，因此可能需要使用复合键。

以下情况可以创建外键：

- 两个本地（非分布式）表之间；
- 两个参考表之间；
- 参考表与本地表之间（通过 `enable_local_ref_fkeys` 控制，默认启用）；
- 两个共置分布式表之间，且外键包含分布列；
- 分布式表引用参考表。

不支持从参考表指向分布式表的外键。

对于本地表指向参考表的外键，Citus 支持所有[引用动作](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)；对于反向外键（参考表指向本地表），则不支持 `ON DELETE/UPDATE CASCADE`。

> [!NOTE]
> 主键和唯一性约束必须包含分布列。仅在非分布列上添加它们会报错。

以下示例展示如何在分布式表上创建主键和外键：

```sql
--
-- Adding a primary key
-- --------------------

-- We'll distribute these tables on the account_id. The ads and clicks
-- tables must use compound keys that include account_id.

ALTER TABLE accounts ADD PRIMARY KEY (id);
ALTER TABLE ads ADD PRIMARY KEY (account_id, id);
ALTER TABLE clicks ADD PRIMARY KEY (account_id, id);

-- Next distribute the tables

SELECT create_distributed_table('accounts', 'id');
SELECT create_distributed_table('ads',      'account_id');
SELECT create_distributed_table('clicks',   'account_id');

--
-- Adding foreign keys
-- -------------------

-- Note that this can happen before or after distribution, as long as
-- there exists a uniqueness constraint on the target column(s) which
-- can only be enforced before distribution.

ALTER TABLE ads ADD CONSTRAINT ads_account_fk
  FOREIGN KEY (account_id) REFERENCES accounts (id);
ALTER TABLE clicks ADD CONSTRAINT clicks_ad_fk
  FOREIGN KEY (account_id, ad_id) REFERENCES ads (account_id, id);
```

同样，唯一性约束也应包含分布列：

```sql
-- Suppose we want every ad to use a unique image. Notice we can
-- enforce it only per account when we distribute by account id.

ALTER TABLE ads ADD CONSTRAINT ads_unique_image
  UNIQUE (account_id, image_url);
```

非空约束可以应用于任意列，无论是否为分布列，因为检查非空约束无需访问其他工作节点。

```sql
ALTER TABLE ads ALTER COLUMN image_url SET NOT NULL;
```

### 使用 NOT VALID 约束 {#using-not-valid-constraints}

有时需要对新行强制执行约束，同时允许已有的不合规行保持不变。Citus 借助 PostgreSQL 的“NOT VALID”约束标记，对 CHECK 约束和外键提供这种支持。

例如，某个应用将用户资料存放在参考表中。

```sql
-- we're using the "text" column type here, but a real application
-- might use "citext" which is available in a PostgreSQL contrib module

CREATE TABLE users ( email text PRIMARY KEY );
SELECT create_reference_table('users');
```

随着时间推移，表中可能混入一些无效地址。

```sql
INSERT INTO users VALUES
   ('foo@example.com'), ('hacker12@aol.com'), ('lol');
```

现在希望验证地址，但 PostgreSQL 通常不允许添加已有行无法满足的 CHECK 约束。不过，它*允许*添加标记为 not valid 的约束：

```sql
ALTER TABLE users
ADD CONSTRAINT syntactic_email
CHECK (email ~
   '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
) NOT VALID;
```

这种方式可以成功添加约束，并保护新插入的行。

```sql
INSERT INTO users VALUES ('fake');

/*
ERROR:  new row for relation "users_102010" violates
        check constraint "syntactic_email_102010"
DETAIL:  Failing row contains (fake).
*/
```

之后，数据库管理员可以在非高峰时段修复无效行，再重新验证约束。

```sql
-- later, attempt to validate all rows
ALTER TABLE users
VALIDATE CONSTRAINT syntactic_email;
```

有关 NOT VALID 和 VALIDATE CONSTRAINT 的更多信息，参见 PostgreSQL 文档的 [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) 部分。

### 添加和删除索引 {#adding-and-removing-indices}

Citus 支持添加和删除[索引](https://www.postgresql.org/docs/current/static/sql-createindex.html)：

```sql
-- Adding an index

CREATE INDEX clicked_at_idx ON clicks USING BRIN (clicked_at);

-- Removing an index

DROP INDEX clicked_at_idx;
```

添加索引需要获取写锁，这在多租户记录系统中可能不合适。为尽量减少应用停机时间，可以改为[并发](https://www.postgresql.org/docs/current/static/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY)创建索引。这比常规索引构建需要更多工作、耗时更长，但构建期间可以继续正常操作，因此适合在生产环境中添加索引。

```sql
-- Adding an index without locking table writes

CREATE INDEX CONCURRENTLY clicked_at_idx ON clicks USING BRIN (clicked_at);
```

## 安全标签与权限 {#security-labels-and-permissions}

从 Citus 13.1 开始：

- 支持从任意节点管理表和列的 `SECURITY LABEL`。
- 协调节点会自动传播针对表列的 `GRANT/REVOKE` 权限操作。

## 类型与函数 {#types-and-functions}

创建自定义 SQL 类型和用户定义函数时，Citus 会自动将其传播到工作节点。不过，在包含分布式操作的事务中创建这些数据库对象时，需要有所权衡。

Citus 使用每个工作节点上的多个连接，跨分片并行执行 `create_distributed_table()` 等操作。但创建数据库对象时，Citus 每个工作节点只使用一个连接来传播对象。将这两类操作放在同一个事务中可能出问题，因为并行连接无法看到通过单个连接创建但尚未提交的对象。

考虑以下事务块：创建一个类型和一张表，加载数据，再分布该表。

```sql
BEGIN;

-- type creation over a single connection:
CREATE TYPE coordinates AS (x int, y int);
CREATE TABLE positions (object_id text primary key, position coordinates);

-- data loading thus goes over a single connection:
SELECT create_distributed_table('positions', 'object_id');
\COPY positions FROM 'positions.csv'

COMMIT;
```

在 Citus 11.0 之前，Citus 会推迟在工作节点上创建类型，并在创建分布式表时单独提交该类型。这使 `create_distributed_table()` 中的数据复制能够并行进行，但也意味着该类型未必始终存在于工作节点上；如果事务回滚，类型仍会留在工作节点上。

从 Citus 11.0 开始，默认行为优先保证协调节点和工作节点之间的模式一致性。这也有一个缺点：如果同一事务中先执行了并行命令，再传播对象，事务就无法完成，如下面代码块中的 ERROR 所示：

```sql
BEGIN;
CREATE TABLE items (key text, value text);
-- parallel data loading:
SELECT create_distributed_table('items', 'key');
\COPY items FROM 'items.csv'
CREATE TYPE coordinates AS (x int, y int);

ERROR: cannot run type command because there was a parallel operation on a distributed table in the transaction
```

遇到此问题时，可以尝试以下两种变通方法之一：

1. 将 `citus.create_object_propagation` 设置为 `deferred`，恢复旧的对象传播行为。这可能使各节点上存在的数据库对象不一致。
2. 将 `citus.multi_shard_modify_mode` 设置为 `sequential`，禁用节点内并行。同一事务中的数据加载可能会变慢。

## 允许从任意节点对分布式模式表执行的 DDL {#ddls-allowed-from-any-node-for-distributed-schema-tables}

除 Citus 表原本支持的 DDL 外，从 Citus 13.3 开始，还支持从任意节点执行以下 DDL 来管理分布式模式中的表：

- `CREATE / DROP / ALTER TABLE`
- `CREATE / DROP / ALTER INDEX`
- `CREATE / DROP / ALTER TRIGGER`

## 视图与物化视图管理 DDL {#view-and-materialized-view-management-ddl}

从 Citus 13.3 开始，`CREATE VIEW`、`CREATE MATERIALIZED VIEW`、`DROP VIEW` 和 `ALTER VIEW` 命令会从任意节点传播到集群中的其他所有节点。

## 数据库与角色管理 DDL {#database-and-role-management-ddl}

Citus 13.1 扩展了自动传播能力，简化角色和数据库管理。协调节点现在会自动传播：

- `ALTER DATABASE SET / OWNER TO`
- 数据库上的 `GRANT/REVOKE` 权限操作
- `COMMENT ON DATABASE` / `COMMENT ON ROLE`
- `REASSIGN OWNED BY`

此外，Citus 会传播**从任意节点**发出的部分角色和数据库管理命令：

- `CREATE DATABASE` / `DROP DATABASE`
- `CREATE ROLE` / `DROP ROLE` / `ALTER ROLE` / 角色上的 `GRANT/REVOKE` 权限操作
- 角色上的 `SECURITY LABEL`

## 手动修改 {#manual-modification}

大多数 DDL 命令会自动传播，参见 [citus.enable_ddl_propagation](/citus/reference/api-guc/#citusenable_ddl_propagation-boolean)。对于其他命令，可以手动传播修改，参见[手动查询传播](/citus/reference/reference-propagation/)。

## 相关内容 {#related-content}

- [数据修改语言（DML）操作参考](/citus/reference/reference-dml/)
- [SQL 参考](/citus/reference/reference-sql/)
- [Citus SQL 参考概述](/citus/reference/)
