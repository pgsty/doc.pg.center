---
title: Citus 实用函数参考
description: 介绍 Citus 提供的用户定义函数及其在标准 SQL 命令之外的分布式能力。
weight: 30
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/api-udf?view=citus-14
upstream_ref: citus-14; 09f28e144ad9
translation_status: translated
---

本节介绍 Citus 提供的用户定义函数。这些函数在标准 SQL 命令之外，为 Citus 提供更多分布式能力。

## 表与分片 DDL {#table-and-shard-ddl}

以下用于创建和修改分布式表及分片的数据定义语言（DDL）命令，是管理 Citus 分布式数据库的重要工具。

### citus_schema_distribute {#citus_schema_distribute}

将现有普通模式转换为分布式模式。每个分布式模式自动关联独立的共置组，其中新建的表会自动成为共置分布式表，无需分片键。分布模式的过程会自动将模式分配并迁移到集群中的一个现有节点。

#### 参数 {#arguments}

**schemaname**：要分布的模式名称。

#### 返回值 {#return-value}

无。

#### 示例 {#example}

分布名为 `tenant_a`、`tenant_b` 和 `tenant_c` 的三个模式。

```sql
SELECT citus_schema_distribute('tenant_a');
SELECT citus_schema_distribute('tenant_b');
SELECT citus_schema_distribute('tenant_c');
```

更多示例参见 [Citus 微服务教程](/citus/tutorials/tutorial-micro-services/)。

### citus_schema_undistribute {#citus_schema_undistribute}

将现有分布式模式转换回普通模式，将其中的表和数据从当前节点迁回集群的协调节点。

#### 参数 {#arguments-1}

**schemaname**：要取消分布的模式名称。

#### 返回值 {#return-value-1}

无。

#### 示例 {#example-1}

将三个分布式模式转换回普通模式。

```sql
SELECT citus_schema_undistribute('tenant_a');
SELECT citus_schema_undistribute('tenant_b');
SELECT citus_schema_undistribute('tenant_c');
```

更多示例参见 [Citus 微服务教程](/citus/tutorials/tutorial-micro-services/)。

### citus_schema_move {#citus_schema_move}

将分布式模式从一个节点移动到另一个节点。

可以采用阻塞或非阻塞方式移动模式。阻塞方式会在移动期间暂停对模式中各表的所有修改；非阻塞方式依赖 PostgreSQL 10 的逻辑复制，避免阻塞写入。

#### 参数 {#arguments-2}

**schema_id**：要移动的分布式模式的 Oid。如果以字符串字面量提供模式名称，它会自动转换为 oid。

**target_node_name**：接收分布式模式的目标节点的 DNS 名称。

**target_node_port**：目标工作节点上数据库服务器监听的端口。

**shard_transfer_mode**：（可选）指定复制方法：PostgreSQL 逻辑复制或跨工作节点的 COPY 命令。可选值如下：

- *auto*：默认值。可使用逻辑复制时要求具备副本标识，否则使用旧行为。
- *force_logical*：即使模式中的表没有副本标识，也使用逻辑复制。复制期间，对这些表的并发更新或删除语句会失败。
- *block_writes*：对模式中缺少主键或副本标识的表使用 COPY，并阻塞写入。

#### 返回值 {#return-value-2}

无。

#### 示例 {#example-2}

```sql
SELECT citus_schema_move('schema-name', 'to_host', 5432);
```

### create_distributed_table {#create_distributed_table}

`create_distributed_table()` 定义分布式表；如果采用哈希分布，还会创建分片。需提供表名、分布列以及可选的分布方式。函数插入元数据，将表标记为分布式表。不指定分布方式时，默认使用哈希分布，并根据分片数配置在工作节点创建分片。如果表中已有数据，函数会自动将其分布到工作节点，但不会删除协调节点表中的数据。残留的本地数据无法通过 Citus 查询访问，还可能在协调节点上引发无关的约束违例。可使用 `truncate_local_data_after_distributing_table` 删除这些数据。

#### 参数 {#arguments-3}

**table_name**：要分布的表名。

**distribution_column**：用于分布表的列。

**colocate_with**：（可选）将当前表加入另一个表的共置组。默认情况下，分布列类型与分片数相同的表会共置。之后可以使用 `update_distributed_table_colocation` 解除共置。`colocate_with` 可设为 *default*、表示创建新共置组的 *none*，或要与之共置的另一个表名。（参见 `colocation_groups`。）

`colocate_with` 的 *default* 值会建立隐式共置关系。对于有关联或需要连接的表，这通常有益。但两个无关的表如果恰好使用相同类型的分布列，意外共置可能降低分片再平衡性能，因为它们的分片会不必要地“级联”移动。可使用 `update_distributed_table_colocation` 解除隐式共置。

如果新的分布式表与其他表无关，请指定 `colocate_with => 'none'`。

**shard_count**：（可选）新分布式表的分片数。指定 `shard_count` 后，`colocate_with` 不能设为 *none* 以外的值。要修改现有表或共置组的分片数，请使用 `alter_distributed_table`。

`shard_count` 的取值范围为 *1* 到 *64000*。选择合适值的指南参见 `prod_shard_count`。

#### 返回值 {#return-value-3}

无。

#### 示例 {#example-3}

本例告知数据库，应对 *repo_id* 列进行哈希来分布 *github_events* 表。

```sql
SELECT create_distributed_table('github_events', 'repo_id');

-- alternatively, to be more explicit:
SELECT create_distributed_table('github_events', 'repo_id',
                                colocate_with => 'github_repo');
```

更多示例参见 `ddl`。

### truncate_local_data_after_distributing_table {#truncate_local_data_after_distributing_table}

分布表后，截断所有本地行，防止过时的本地记录引发约束违例。截断会级联到通过外键引用指定表的表。为保护引用完整性，如果引用方的表尚未分布，就不能截断，必须先将这些表也分布：

`ERROR: cannot truncate a table referenced in a foreign key constraint by a local table`

对于分布式表，截断协调节点的本地数据是安全的，因为分布时已有行已复制到工作节点。

#### 参数 {#arguments-4}

**table_name**：分布式表的名称，要截断的是它在协调节点上的本地对应表。

#### 返回值 {#return-value-4}

无。

#### 示例 {#example-4}

```sql
-- requires that argument is a distributed table
SELECT truncate_local_data_after_distributing_table('public.github_events');
```

### undistribute_table {#undistribute_table}

`undistribute_table()` 执行 `create_distributed_table` 或 `create_reference_table` 的逆操作。取消分布时，Citus 将各分片数据移回协调节点的本地表（前提是能容纳全部数据），然后删除分片。

对于具有外键或被外键引用的表，除非将 `cascade_via_foreign_keys` 设为 *true*，否则 Citus 不会取消分布。若该参数为 *false* 或省略，必须先手动删除外键约束。

#### 参数 {#arguments-5}

**table_name**：要取消分布的分布式表或参考表名称。

**cascade_via_foreign_keys**：（可选）设为 *true* 时，`undistribute_table` 也会取消分布所有通过外键与 `table_name` 关联的表。此参数可能影响大量表，需谨慎使用。

#### 返回值 {#return-value-5}

无。

#### 示例 {#example-5}

本例先分布 `github_events` 表，再取消分布。

```sql
-- first distribute the table
SELECT create_distributed_table('github_events', 'repo_id');

-- undo that and make it local again
SELECT undistribute_table('github_events');
```

### alter_distributed_table {#alter_distributed_table}

`alter_distributed_table()` 用于修改分布式表的分布列、分片数或共置属性。

#### 参数 {#arguments-6}

**table_name**：要修改的分布式表名称。

**distribution_column**：（可选）新的分布列名称。

**shard_count**：（可选）新的分片数。

**colocate_with**：（可选）要与当前分布式表共置的表。可设为 *default*、表示创建新共置组的 *none*，或另一个表的名称。

**cascade_to_colocated**：（可选）设为 *true* 时，`shard_count` 和 `colocate_with` 的修改也会应用到此前与该表共置的所有表，并保持共置关系。设为 *false* 则解除当前共置关系。

#### 返回值 {#return-value-6}

无。

#### 示例 {#example-6}

```sql
-- change distribution column
SELECT alter_distributed_table('github_events', distribution_column:='event_id');

-- change shard count of all tables in colocation group
SELECT alter_distributed_table('github_events', shard_count:=6, cascade_to_colocated:=true);

-- change colocation
SELECT alter_distributed_table('github_events', colocate_with:='another_table');
```

### alter_table_set_access_method {#alter_table_set_access_method}

`alter_table_set_access_method()` 用于修改表的访问方法，例如堆或列式存储。

#### 参数 {#arguments-7}

- **table_name**：要修改访问方法的表名。
- **access_method**：新的访问方法名称。

#### 返回值 {#return-value-7}

无。

#### 示例 {#example-7}

```sql
SELECT alter_table_set_access_method('github_events', 'columnar');
```

### remove_local_tables_from_metadata {#remove_local_tables_from_metadata}

不再需要在 Citus 元数据中保留本地表时，可使用 `remove_local_tables_from_metadata()` 将其移除。更多信息参见 `enable_local_ref_fkeys`。

通常，将本地表加入 Citus 元数据有特定原因，例如它与参考表之间存在外键。不过，禁用 `enable_local_reference_foreign_keys` 后，Citus 会停止管理这种情况下的元数据。多余的元数据可能一直保留，直到手动清理。

#### 参数 {#arguments-8}

无。

#### 返回值 {#return-value-8}

无。

### create_reference_table {#create_reference_table}

`create_reference_table()` 用于定义小型参考表或维度表。提供表名后，函数创建只有一个分片的分布式表，并将该分片复制到每个工作节点。

#### 参数 {#arguments-9}

**table_name**：要分布的小型维度表或参考表名称。

#### 返回值 {#return-value-9}

无。

#### 示例 {#example-8}

本例告知数据库，应将 nation 表定义为参考表。

```sql
SELECT create_reference_table('nation');
```

### citus_add_local_table_to_metadata {#citus_add_local_table_to_metadata}

`citus_add_local_table_to_metadata()` 将本地 PostgreSQL 表加入 Citus 元数据。主要用途是让协调节点的本地表可从集群任意节点访问，在其他节点发起查询时尤其有用。本地表的数据仍保存在协调节点，仅将表结构和元数据发送到工作节点。

将本地表加入元数据有少量开销，因为 Citus 必须在 `partition_table` 中跟踪它。加入元数据的本地表具有与参考表相同的限制，参见 `ddl` 和 `citus_sql_reference`。

调用 `undistribute_table` 后，Citus 会自动从元数据中移除转换得到的本地表，解除这些限制。

#### 参数 {#arguments-10}

**table_name**：协调节点上要加入 Citus 元数据的表名。

**cascade_via_foreign_keys**：（可选）设为 *true* 时，`citus_add_local_table_to_metadata` 会自动将与指定表有外键关系的其他表也加入元数据。此参数可能影响大量表，需谨慎使用。

#### 返回值 {#return-value-10}

无。

#### 示例 {#example-9}

本例告知数据库，应将 nation 表定义为可从任意节点访问的协调节点本地表：

```sql
SELECT citus_add_local_table_to_metadata('nation');
```

### update_distributed_table_colocation {#update_distributed_table_colocation}

`update_distributed_table_colocation()` 更新分布式表的共置关系，也可以用于解除共置。Citus 会将分布列类型相同的两个表隐式共置，对于有关联且需要连接的表，这很有用。如果 A、B 共置，对 A 再平衡时 B 也会一起再平衡；若 B 没有副本标识，再平衡就会失败。此时可以使用该函数解除隐式共置。

此函数不会实际移动任何数据。

#### 参数 {#arguments-11}

**table_name**：要更新共置关系的表名。

**colocate_with**：要与之共置的表。

要解除某表的共置关系，请指定 `colocate_with => 'none'`。

#### 返回值 {#return-value-11}

无。

#### 示例 {#example-10}

本例将 `table A` 的共置关系更新为与 `table B` 共置。

```sql
SELECT update_distributed_table_colocation('A', colocate_with => 'B');
```

假设 `table A` 和 `table B` 已隐式共置，可用以下命令解除共置：

```sql
SELECT update_distributed_table_colocation('A', colocate_with => 'none');
```

现在假设 `table A`、`table B`、`table C` 和 `table D` 共置，而希望 `table A` 与 `table B` 共置、`table C` 与 `table D` 共置：

```sql
SELECT update_distributed_table_colocation('C', colocate_with => 'none');
SELECT update_distributed_table_colocation('D', colocate_with => 'C');
```

如果有一个名为 `none` 的哈希分布表，要更新其共置关系，请运行：

```sql
SELECT update_distributed_table_colocation('"none"', colocate_with => 'some_other_hash_distributed_table');
```

### create_distributed_function {#create_distributed_function}

将函数从协调节点传播到工作节点，并标记为分布式执行。在协调节点调用分布式函数时，Citus 根据 `distribution_arg_name` 的值选择执行函数的工作节点。在工作节点执行可以提高并行度，让代码靠近分片数据，从而降低延迟。

执行分布式函数时，PostgreSQL 搜索路径不会从协调节点传播到工作节点，因此函数代码应使用数据库对象的完全限定名称。此外，函数产生的通知不会显示给用户。

#### 参数 {#arguments-12}

**function_name**：要分布的函数名。必须在括号中包含参数类型，因为 PostgreSQL 允许多个函数同名。例如，`'foo(int)'` 与 `'foo(int, text)'` 不同。

**distribution_arg_name**：（可选）用于分布的参数名。为方便使用，或在参数没有名称时，可以使用 `'$1'` 等位置占位符。如果不指定此参数，只会在工作节点上创建 `function_name` 指定的函数。

**colocate_with**：（可选）如果分布式函数读写分布式表（更一般地说，是读写某个 `colocation_groups`），务必通过 `colocate_with` 参数指定该表，以确保每次调用都在持有相关分片的工作节点上运行。

#### 返回值 {#return-value-12}

无。

#### 示例 {#example-11}

```sql
-- an example function which updates a hypothetical
-- event_responses table which itself is distributed by event_id
CREATE OR REPLACE FUNCTION
  register_for_event(p_event_id int, p_user_id int)
RETURNS void LANGUAGE plpgsql AS $fn$
BEGIN
  INSERT INTO event_responses VALUES ($1, $2, 'yes')
  ON CONFLICT (event_id, user_id)
  DO UPDATE SET response = EXCLUDED.response;
END;
$fn$;

-- distribute the function to workers, using the p_event_id argument
-- to determine which shard each invocation affects, and explicitly
-- colocating with event_responses which the function updates
SELECT create_distributed_function(
  'register_for_event(int, int)', 'p_event_id',
  colocate_with := 'event_responses'
);
```

### alter_columnar_table_set {#alter_columnar_table_set}

`alter_columnar_table_set()` 用于修改[列式表](/citus/tutorials/tutorial-time-series/#archive-with-columnar-storage)的设置。对非列式表调用会报错。除表名外，所有参数均可选。

查询下表可查看所有列式表的当前选项：

```sql
SELECT * FROM columnar.options;
```

使用以下全局用户配置（GUC）可以覆盖新建表的列式存储默认设置：

- columnar.compression
- columnar.compression_level
- columnar.stripe_row_count
- columnar.chunk_row_count

#### 参数 {#arguments-13}

**table_name**：列式表名。

**chunk_row_count**：（可选）新插入数据每个块的最大行数。不修改现有数据块，因此旧块的行数可能超过此上限。默认值为 *10000*。

**stripe_row_count**：（可选）新插入数据每个条带的最大行数。不修改现有条带，因此旧条带的行数可能超过此上限。默认值为 *150000*。

**compression**：（可选）新插入数据的压缩类型，可选 *none*、*pglz*、*zstd*、*lz4* 和 *z4hc*。不对已有数据重新压缩或解压缩。若编译时包含相应支持，建议默认使用 *zstd*。

**compression_level**：（可选）取值范围为 *1* 到 *19*。若压缩方法不支持所选级别，则采用最接近的级别。

#### 返回值 {#return-value-13}

无。

#### 示例 {#example-12}

```sql
SELECT alter_columnar_table_set(
  'my_columnar_table',
  compression => 'none',
  stripe_row_count => 10000);
```

### create_time_partitions {#create_time_partitions}

`create_time_partitions()` 按指定时间间隔创建分区，覆盖指定时间范围。

#### 参数 {#arguments-14}

**table_name**：要创建新分区的表，类型为 `regclass`。该表必须仅按一列分区，列类型为 `date`、`timestamp` 或 `timestamptz`。

**partition_interval**：新分区采用的时间间隔，例如 `'2 hours'` 或 `'1 month'`。

**end_at**：（`timestamptz`）创建分区直至此时刻。最后一个分区包含 `end_at`，不再创建更晚的分区。

**start_from**：（`timestamptz`，可选）第一个分区应包含 `start_from` 时刻，默认值为 `now()`。

#### 返回值 {#return-value-14}

如果需要创建新分区，返回 *True*；如果所有分区都已存在，返回 *False*。

#### 示例 {#example-13}

```sql
-- create a year's worth of monthly partitions
-- in table foo, starting from the current time

SELECT create_time_partitions(
  table_name         := 'foo',
  partition_interval := '1 month',
  end_at             := now() + '12 months'
);
```

### drop_old_time_partitions {#drop_old_time_partitions}

`drop_old_time_partitions()` 删除时间区间位于指定时间戳之前的所有分区。也可以考虑使用 `alter_old_partitions_set_access_method`，以列式存储压缩旧分区，而非删除。

#### 参数 {#arguments-15}

**table_name**：要删除分区的表，类型为 `regclass`。该表必须仅按一列分区，列类型为 `date`、`timestamp` 或 `timestamptz`。

**older_than**：（`timestamptz`）删除范围上界小于或等于 `older_than` 的分区。

#### 返回值 {#return-value-15}

无。

#### 示例 {#example-14}

```sql
-- drop partitions that are over a year old

CALL drop_old_time_partitions('foo', now() - interval '12 months');
```

### alter_old_partitions_set_access_method {#alter_old_partitions_set_access_method}

在[时序数据](/citus/tutorials/tutorial-time-series/)场景中，按时间分区，并将旧分区压缩为只读列式存储。

#### 参数 {#arguments-16}

**parent_table_name**：要修改其分区的表，类型为 `regclass`。该表必须仅按一列分区，列类型为 `date`、`timestamp` 或 `timestamptz`。

**older_than**：（`timestamptz`）修改范围上界小于或等于 `older_than` 的分区。

**new_access_method**：（`name`）行式存储使用 *heap*，列式存储使用 *columnar*。

#### 返回值 {#return-value-16}

无。

#### 示例 {#example-15}

```sql
CALL alter_old_partitions_set_access_method(
  'foo', now() - interval '6 months',
  'columnar'
);
```

## 元数据与配置信息 {#metadata--configuration-information}

### citus_add_node {#citus_add_node}

> [!NOTE]
> 运行此函数需要数据库超级用户权限。

`citus_add_node()` 将新节点加入 Citus 元数据表 `pg_dist_node`，从而注册到集群中，同时将参考表复制到新节点。

在单节点集群中运行 `citus_add_node` 前，请先运行 `set_coordinator_host`。

#### 参数 {#arguments-17}

**nodename**：要添加的新节点的 DNS 名称或 IP 地址。

**nodeport**：工作节点上 PostgreSQL 监听的端口。

**groupid**：一个主服务器及其备用服务器组成的组，仅与流复制有关。应将 `groupid` 设置为大于零的值，因为零保留给协调节点。默认值为 *-1*。

**noderole**：指定节点为 *primary* 或 *secondary*，默认 *primary*。

- **nodecluster**：集群名称，默认 *default*。

#### 返回值 {#return-value-17}

`pg_dist_node` 中新插入行的 `nodeid` 列。

#### 示例 {#example-16}

```sql
select * from citus_add_node('new-node', 12345);
 citus_add_node
-----------------
               7
(1 row)
```

### citus_update_node {#citus_update_node}

> [!NOTE]
> 运行此函数需要数据库超级用户权限。

`citus_update_node()` 修改已注册在 Citus 元数据表 `pg_dist_node` 中的节点的主机名和端口。

#### 参数 {#arguments-18}

- **node_id**：`pg_dist_node` 表中的节点 ID。
- **node_name**：更新后的节点 DNS 名称或 IP 地址。
- **node_port**：工作节点上 PostgreSQL 监听的端口。

#### 返回值 {#return-value-18}

无。

#### 示例 {#example-17}

```sql
select * from citus_update_node(123, 'new-address', 5432);
```

### citus_set_node_property {#citus_set_node_property}

`citus_set_node_property()` 修改 Citus 元数据表 `pg_dist_node` 中的属性。目前只支持修改 `shouldhaveshards`。

#### 参数 {#arguments-19}

**node_name**：节点的 DNS 名称或 IP 地址。

- **node_port**：工作节点上 PostgreSQL 监听的端口。

**property**：要修改的 `pg_dist_node` 列，目前仅支持 `shouldhaveshards`。

**value**：该列的新值。

#### 返回值 {#return-value-19}

无。

#### 示例 {#example-18}

```sql
SELECT * FROM citus_set_node_property('localhost', 5433, 'shouldhaveshards', false);
```

### citus_add_inactive_node {#citus_add_inactive_node}

> [!NOTE]
> 运行此函数需要数据库超级用户权限。

`citus_add_inactive_node` 与 `citus_add_node` 类似，也在 `pg_dist_node` 中注册新节点。但它将新节点标记为非活动，因此不存放任何分片，也不会复制参考表。

#### 参数 {#arguments-20}

**nodename**：要添加的新节点的 DNS 名称或 IP 地址。

**nodeport**：工作节点上 PostgreSQL 监听的端口。

**groupid**：由一个主服务器及零个或多个备用服务器组成的组，仅与流复制有关。默认值为 *-1*。

**noderole**：指定节点为 *primary* 或 *secondary*，默认 *primary*。

- **nodecluster**：集群名称，默认 *default*。

#### 返回值 {#return-value-20}

`pg_dist_node` 中新插入行的 `nodeid` 列。

#### 示例 {#example-19}

```sql
select * from citus_add_inactive_node('new-node', 12345);
 citus_add_inactive_node
--------------------------
                        7
(1 row)
```

### citus_activate_node {#citus_activate_node}

> [!NOTE]
> 运行此函数需要数据库超级用户权限。

`citus_activate_node` 在 Citus 元数据表 `pg_dist_node` 中将节点标记为活动，并将参考表复制到该节点。适用于通过 `citus_add_inactive_node` 添加的节点。

#### 参数 {#arguments-21}

**nodename**：要添加的新节点的 DNS 名称或 IP 地址。

**nodeport**：工作节点上 PostgreSQL 监听的端口。

#### 返回值 {#return-value-21}

`pg_dist_node` 中新插入行的 `nodeid` 列。

#### 示例 {#example-20}

```sql
select * from citus_activate_node('new-node', 12345);
 citus_activate_node
----------------------
                    7
(1 row)
```

### citus_disable_node {#citus_disable_node}

> [!NOTE]
> 运行此函数需要数据库超级用户权限。

`citus_disable_node` 与 `citus_activate_node` 的作用相反。它在 `pg_dist_node` 中将节点标记为非活动，将其暂时移出集群，同时删除该节点上的所有参考表放置。再次运行 `citus_activate_node` 可重新激活节点。

#### 参数 {#arguments-22}

**nodename**：要禁用节点的 DNS 名称或 IP 地址。

**nodeport**：工作节点上 PostgreSQL 监听的端口。

#### 返回值 {#return-value-22}

无。

#### 示例 {#example-21}

```sql
select * from citus_disable_node('new-node', 12345);
```

### citus_add_secondary_node {#citus_add_secondary_node}

> [!NOTE]
> 运行此函数需要数据库超级用户权限。

`citus_add_secondary_node()` 为集群中的现有主节点注册一个新的备用节点，更新 Citus 元数据表 `pg_dist_node`。

#### 参数 {#arguments-23}

**nodename**：要添加的新节点的 DNS 名称或 IP 地址。

**nodeport**：工作节点上 PostgreSQL 监听的端口。

- **primaryname**：该备用节点所对应主节点的 DNS 名称或 IP 地址。
- **primaryport**：主节点上 PostgreSQL 监听的端口。
- **nodecluster**：集群名称，默认 *default*。

#### 返回值 {#return-value-23}

插入 `pg_dist_node` 的备用节点记录的 `nodeid` 列。

#### 示例 {#example-22}

```sql
select * from citus_add_secondary_node('new-node', 12345, 'primary-node', 12345);
 citus_add_secondary_node
---------------------------
                         7
(1 row)
```

### citus_remove_node {#citus_remove_node}

> [!NOTE]
> 运行此函数需要数据库超级用户权限。

`citus_remove_node()` 从 `pg_dist_node` 元数据表中删除节点。如果节点上仍有分片放置，则返回错误。调用前应先迁出该节点的分片。

#### 参数 {#arguments-24}

**nodename**：要删除节点的 DNS 名称。

**nodeport**：工作节点上 PostgreSQL 监听的端口。

#### 返回值 {#return-value-24}

无。

#### 示例 {#example-23}

```sql
select citus_remove_node('new-node', 12345);
 citus_remove_node
--------------------

(1 row)
```

### citus_get_active_worker_nodes {#citus_get_active_worker_nodes}

`citus_get_active_worker_nodes()` 返回活动工作节点的主机名和端口号列表。

#### 参数 {#arguments-25}

无。

#### 返回值 {#return-value-25}

返回元组列表，每个元组包含以下信息：

- **node_name**：工作节点的 DNS 名称。
- **node_port**：工作节点上数据库服务器监听的端口。

#### 示例 {#example-24}

```sql
SELECT * from citus_get_active_worker_nodes();
```

```text
 node_name | node_port
-----------+-----------
 localhost |      9700
 localhost |      9702
 localhost |      9701

(3 rows)
```

### citus_backend_gpid {#citus_backend_gpid}

`citus_backend_gpid()` 返回服务当前会话的 PostgreSQL 后端的全局进程标识符（GPID）。GPID 同时编码了 Citus 集群中的节点以及该节点上 PostgreSQL 的操作系统进程 ID。

Citus 扩展了 PostgreSQL 的[服务器信号函数](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL-TABLE) `pg_cancel_backend()` 和 `pg_terminate_backend()`，使其接受 GPID。因此，在一个节点调用这些函数，可以影响另一个节点上运行的后端。

#### 参数 {#arguments-26}

无。

#### 返回值 {#return-value-26}

整数 GPID，形式为 `(NodeId * 10,000,000,000) + ProcessId`。

#### 示例 {#example-25}

```sql
SELECT citus_backend_gpid();
```

```text
  citus_backend_gpid
--------------------
  10000002055
```

### citus_check_cluster_node_health {#citus_check_cluster_node_health}

检查所有节点之间的连通性。如果有 N 个节点，则检查它们之间全部 N<sup>2</sup> 个连接。

#### 参数 {#arguments-27}

无。

#### 返回值 {#return-value-27}

返回元组列表，每个元组包含以下信息：

- **from_nodename**：源工作节点的 DNS 名称。
- **from_nodeport**：源工作节点上数据库服务器监听的端口。
- **to_nodename**：目标工作节点的 DNS 名称。
- **to_nodeport**：目标工作节点上数据库服务器监听的端口。
- **result**：是否成功建立连接。

#### 示例 {#example-26}

```sql
SELECT * FROM citus_check_cluster_node_health();
```

```text
 from_nodename │ from_nodeport │ to_nodename │ to_nodeport │ result
---------------+---------------+-------------+-------------+--------
 localhost     |          1400 | localhost   |        1400 | t
 localhost     |          1400 | localhost   |        1401 | t
 localhost     |          1400 | localhost   |        1402 | t
 localhost     |          1401 | localhost   |        1400 | t
 localhost     |          1401 | localhost   |        1401 | t
 localhost     |          1401 | localhost   |        1402 | t
 localhost     |          1402 | localhost   |        1400 | t
 localhost     |          1402 | localhost   |        1401 | t
 localhost     |          1402 | localhost   |        1402 | t

 (9 rows)
```

### citus_set_coordinator_host {#citus_set_coordinator_host}

向最初以单节点形式创建的 Citus 集群添加工作节点时，应使用此函数。协调节点注册新工作节点时，会将 `local_hostname` 的值作为协调节点主机名，默认是 *localhost*。这样工作节点就会尝试连接自身的 *localhost* 来访问协调节点，显然不正确。

在单节点集群中，应先调用 `citus_set_coordinator_host`，再调用 `citus_add_node`。

#### 参数 {#arguments-28}

**host**：协调节点的 DNS 名称。

**port**：（可选）协调节点监听 PostgreSQL 连接的端口，默认为 `current_setting('port')`。

**node_role**：（可选）默认为 *primary*。

**node_cluster**：（可选）默认为 *default*。

#### 返回值 {#return-value-28}

无。

#### 示例 {#example-27}

```sql
-- assuming we're in a single-node cluster

-- first establish how workers should reach us
SELECT citus_set_coordinator_host('coord.example.com', 5432);

-- then add a worker
SELECT * FROM citus_add_node('worker1.example.com', 5432);
```

### get_shard_id_for_distribution_column {#get_shard_id_for_distribution_column}

Citus 根据每行的分布列值和表的分布方式，将分布式表的各行分配到分片。通常管理员无需了解精确映射，但在手动维护数据库或仅仅想了解分布情况时，确定某行所在分片可能很有用。`get_shard_id_for_distribution_column` 为哈希分布表和参考表提供这一信息。

#### 参数 {#arguments-30}

- **table_name**：分布式表。
- **distribution_value**：分布列的值。

#### 返回值 {#return-value-30}

Citus 为指定表中该分布列值分配的分片 ID。

#### 示例 {#example-29}

```sql
SELECT get_shard_id_for_distribution_column('my_table', 4);
```

```text
 get_shard_id_for_distribution_column
--------------------------------------
                               540007
(1 row)
```

### column_to_column_name {#column_to_column_name}

将 `pg_dist_partition` 的 `partkey` 列转换为文本列名，可用于确定分布式表的分布列。

详细说明参见 `finding_dist_col`。

#### 参数 {#arguments-31}

- **table_name**：分布式表。
- **column_var_text**：`pg_dist_partition` 表中的 `partkey` 值。

#### 返回值 {#return-value-31}

**table_name** 的分布列名称。

#### 示例 {#example-30}

```sql
-- get distribution column name for products table

SELECT column_to_column_name(logicalrelid, partkey) AS dist_col_name
  FROM pg_dist_partition
 WHERE logicalrelid='products'::regclass;
```

输出：

```text
┌───────────────┐
│ dist_col_name │
├───────────────┤
│ company_id    │
└───────────────┘
```

### citus_relation_size {#citus_relation_size}

获取指定分布式表全部分片使用的磁盘空间。包括*主分支（main fork）*的大小，但不包括分片的可见性映射和空闲空间映射。

#### 参数 {#arguments-32}

**logicalrelid**：分布式表名。

#### 返回值 {#return-value-32}

bigint 类型的字节数。

#### 示例 {#example-31}

```sql
SELECT pg_size_pretty(citus_relation_size('github_events'));
```

```text
    pg_size_pretty
    --------------
    23 MB
```

### citus_table_size {#citus_table_size}

获取指定分布式表全部分片使用的磁盘空间，不含索引，但包括 TOAST、空闲空间映射和可见性映射。

#### 参数 {#arguments-33}

**logicalrelid**：分布式表名。

#### 返回值 {#return-value-33}

bigint 类型的字节数。

#### 示例 {#example-32}

```sql
SELECT pg_size_pretty(citus_table_size('github_events'));
```

```text
    pg_size_pretty
    --------------
    37 MB
```

### citus_total_relation_size {#citus_total_relation_size}

获取指定分布式表全部分片使用的总磁盘空间，包括所有索引和 TOAST 数据。

#### 参数 {#arguments-34}

**logicalrelid**：分布式表名。

#### 返回值 {#return-value-34}

bigint 类型的字节数。

#### 示例 {#example-33}

```sql
SELECT pg_size_pretty(citus_total_relation_size('github_events'));
```

```text
    pg_size_pretty
    --------------
    73 MB
```

### citus_stat_statements_reset {#citus_stat_statements_reset}

删除 `citus_stat_statements` 中的所有行。此函数独立于 `pg_stat_statements_reset()`；若要重置全部统计信息，应同时调用这两个函数。

#### 参数 {#arguments-35}

无。

#### 返回值 {#return-value-35}

无。

### citus_stat_counters_reset {#citus_stat_counters_reset}

将指定数据库的 Citus 统计计数器重置为零。计数器可通过 [`citus_stat_counters` 视图](/citus/reference/api-metadata/#citus-stat-counters-view)和 [`citus_stat_counters()`](#citus_stat_counters) 函数查询。需要超级用户权限。

#### 参数 {#arguments-36}

**database_id**：（可选）要重置统计信息的数据库 OID。传入 `NULL`、`0` 或省略参数，表示重置当前数据库。

#### 返回值 {#return-value-36}

无。

#### 示例 {#examples}

```sql
-- reset stats for the current database
SELECT citus_stat_counters_reset();

-- explicitly pass 0 for current database
SELECT citus_stat_counters_reset(0);

-- reset stats for a specific database by OID; no-op if it doesn't exist
SELECT citus_stat_counters_reset(12345);
```

> [!CAUTION]
> 由于并发访问，少数情况下并非所有活动后端都会立即重置计数器。`citus_stat_counters` 的 `stats_reset` 列显示最近一次重置的时间戳。

### citus_stat_counters {#citus_stat_counters}

返回一个或多个数据库的 Citus 统计计数器。指标与 [`citus_stat_counters` 视图](/citus/reference/api-metadata/#citus-stat-counters-view)相同，但函数还能返回已删除数据库的统计信息，而视图会过滤掉这些记录。

#### 参数 {#arguments-37}

**database_id**：（可选）要查询的数据库 OID。传入 `NULL`、`0` 或省略参数，表示返回所有数据库的统计信息。

#### 返回值 {#return-value-37}

返回一组行，包含以下列：

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `database_id` | oid | 数据库 OID。 |
| `connection_establishment_succeeded` | bigint | 成功建立的节点间连接数。 |
| `connection_establishment_failed` | bigint | 失败的连接尝试数。 |
| `connection_reused` | bigint | 复用缓存连接的次数。 |
| `query_execution_single_shard` | bigint | 访问单个分片的查询或子计划数。 |
| `query_execution_multi_shard` | bigint | 访问多个分片的查询或子计划数。 |
| `stats_reset` | timestamptz | 最近一次重置的时间戳；从未重置时为 NULL。 |

#### 示例 {#examples-1}

```sql
-- get stats for all databases
SELECT * FROM citus_stat_counters();

-- get stats for a specific database
SELECT * FROM citus_stat_counters(12345);

-- get stats for the current database only
SELECT *
FROM citus_stat_counters(
  (SELECT oid FROM pg_database WHERE datname = current_database())
);
```

> [!NOTE]
> - 只有启用 `citus.enable_stat_counters` 才采集统计信息，默认值为 false。禁用后，已有统计信息仍可查询。
> - 统计信息保存在内存中，服务器重启后重置。
> - 如果指定从未使用过的数据库 OID，返回空结果集。

## 集群管理与修复函数 {#cluster-management-and-repair-functions}

### citus_move_shard_placement {#citus_move_shard_placement}

将一个分片及其共置分片从一个节点移动到另一个节点。通常在分片再平衡时由系统间接使用，无需直接调用。

数据移动可以采用阻塞或非阻塞方式。阻塞方式会在移动期间暂停对分片的所有修改；非阻塞方式依赖 PostgreSQL 10 逻辑复制，以避免阻塞分片写入。

移动成功后，函数删除源节点上的分片。如果任一步骤失败，则报错，并保持源节点和目标节点不变。

#### 参数 {#arguments-38}

**shard_id**：要移动的分片 ID。

**source_node_name**：持有健康分片放置的源节点的 DNS 名称。

**source_node_port**：源工作节点上数据库服务器监听的端口。

**target_node_name**：持有无效分片放置的目标节点的 DNS 名称。

**target_node_port**：目标工作节点上数据库服务器监听的端口。

**shard_transfer_mode**：（可选）指定复制方式：PostgreSQL 逻辑复制或跨工作节点的 COPY 命令。可选值如下：

- *auto*：默认值。可使用逻辑复制时要求具备副本标识，否则采用旧行为，例如 *PostgreSQL 9.6* 上的分片修复方式。
- *force_logical*：即使表没有副本标识也使用逻辑复制。复制期间，对该表的并发更新或删除语句会失败。
- *block_writes*：对缺少主键或副本标识的表使用 COPY，并阻塞写入。

> [!NOTE]
> 从 11.0 版本开始，Citus 社区版支持全部分片传输模式。

#### 返回值 {#return-value-38}

无。

#### 示例 {#example-34}

```sql
SELECT citus_move_shard_placement(12345, 'from_host', 5432, 'to_host', 5432);
```

### citus_rebalance_start {#citus_rebalance_start}

`citus_rebalance_start()` 移动表分片，使其在工作节点之间分布得更均匀。函数启动后台再平衡作业后立即返回。

再平衡过程先计算必要的移动列表，使集群的不平衡程度处于指定阈值内，再逐个将分片放置从源节点移到目标节点，并更新对应元数据。

为判断分片是否*均匀分布*，系统给每个分片分配一个代价。默认策略 *by_disk_size* 根据分片大小计算代价；*by_shard_count* 则给每个分片分配代价 1，适用于以下情况：

1. 各分片大小大致相同。
2. 各分片承受的流量大致相同。
3. 所有工作节点的规格和类型相同。
4. 分片未被固定在特定工作节点上。

如果任何一个条件不成立，*by_shard_count* 都可能生成不合理的再平衡计划。

可以通过 `rebalance_strategy` 参数自定义策略。

运行 `citus_rebalance_start` 前，可先调用 `get_rebalance_table_shards_plan` 查看并核实计划执行的操作。

> [!NOTE]
> Citus 13.2 改进了再平衡性能：
> 
> - 启用 `parallel_transfer_colocated_shards`，可在保持依赖顺序的同时并行移动共置分片。
> - 启用 `parallel_transfer_reference_tables`，可通过独立后台任务复制参考表分片。
> - 提高 `max_worker_processes`、`citus.max_background_task_executor` 和 `citus.max_background_task_executors_per_node`，以利用并行能力。
> - 锁定机制改用每分片的咨询锁及较宽松的共置锁（RowExclusiveLock），取消了全局复制锁。

#### 参数 {#arguments-39}

**threshold**：（可选）0.0 到 1.0 之间的浮点数，表示节点利用率相对平均利用率允许的最大偏差比例。例如，指定 *0.1* 时，再平衡器会尝试使所有节点的分片数相同，允许 ±10% 的偏差。具体而言，会尝试将各工作节点的利用率收敛到 (1 - threshold) * average_utilization ... (1 + threshold) * average_utilization 范围内。

**drain_only**：（可选）设为 *true* 时，仅迁出 `pg_dist_node` 中 `shouldhaveshards` 为 *false* 的工作节点上的分片，不移动其他分片。

**rebalance_strategy**：（可选）[pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table) 中的策略名称。省略时使用表中标记的默认策略。

**parallel_transfer_colocated_shards**：（可选，默认 *false*）设为 *true* 时，共置分片可在保持依赖顺序的前提下并行移动。

**parallel_transfer_reference_tables**：（可选，默认 *false*）设为 *true* 时，每个参考表分片由独立的后台任务复制。

#### 返回值 {#return-value-39}

无。

#### 示例 {#example-35}

以下示例尝试在默认阈值内完成分片再平衡。

```sql
SELECT citus_rebalance_start();
NOTICE:  Scheduling...
NOTICE:  Scheduled as job 1337.
DETAIL:  Rebalance scheduled as background job 1337.
HINT:  To monitor progress, run: SELECT details FROM citus_rebalance_status();
```

### citus_rebalance_status {#citus_rebalance_status}

`citus_rebalance_start` 立即返回，而再平衡在后台继续运行。使用 `citus_rebalance_status()` 可以监控进度。

#### 示例 {#example-36}

选择状态结果中的全部列，可获取再平衡的概况。以下命令展示作业的基本状态：

```sql
SELECT * FROM citus_rebalance_status();
```

```text
 job_id | state   | job_type  |           description           |          started_at           |          finished_at          | details
--------+---------+-----------+---------------------------------+-------------------------------+-------------------------------+-----------
      4 | running | rebalance | Rebalance colocation group 1    | 2022-08-09 21:57:27.833055+02 | 2022-08-09 21:57:27.833055+02 | { ... }
```

再平衡的详细信息以 JSON 格式保存在 `details` 列中：

```sql
SELECT details FROM citus_rebalance_status();
```

```json
{
    "phase": "copy",
    "phase_index": 1,
    "phase_count": 3,
    "last_change":"2022-08-09 21:57:27",
    "colocations": {
        "1": {
            "shard_moves": 30,
            "shard_moved": 29,
            "last_move":"2022-08-09 21:57:27"
        },
        "1337": {
            "shard_moves": 130,
            "shard_moved": 0
        }
    }
}
```

### citus_rebalance_stop {#citus_rebalance_stop}

如果存在正在运行的再平衡，则取消它。

#### 参数 {#arguments-40}

无。

#### 返回值 {#return-value-40}

无。

### citus_rebalance_wait {#citus_rebalance_wait}

阻塞等待正在运行的再平衡完成。如果调用 `citus_rebalance_wait()` 时没有再平衡在运行，则立即返回。

此函数适合用于脚本或基准测试。

#### 参数 {#arguments-41}

无。

#### 返回值 {#return-value-41}

无。

### rebalance_table_shards {#rebalance_table_shards}

> [!WARNING]
> `rebalance_table_shards()` 已弃用。从 Citus v11.2 开始，请改用 `citus_rebalance_start`。

### get_rebalance_table_shards_plan {#get_rebalance_table_shards_plan}

返回 `citus_rebalance_start` 计划执行的分片移动，但不实际执行。虽然不常见，`get_rebalance_table_shards_plan` 返回的计划可能与使用相同参数调用 `citus_rebalance_start` 时略有不同，因为两个函数不同时执行，两次调用之间集群状态（如磁盘空间）可能发生变化。

#### 参数 {#arguments-42}

参数是 `citus_rebalance_start` 参数的超集：`relation`、`threshold`、`max_shard_moves`、`excluded_shard_list` 和 `drain_only`。各参数含义参见该函数文档。

#### 返回值 {#return-value-42}

返回元组，包含以下列：

- **table_name**：分片所属的表。
- **shardid**：待移动的分片 ID。
- **shard_size**：大小，单位为字节。
- **sourcename**：源节点主机名。
- **sourceport**：源节点端口。
- **targetname**：目标节点主机名。
- **targetport**：目标节点端口。

### get_rebalance_progress {#get_rebalance_progress}

> [!NOTE]
> Citus v11.2 引入了 `citus_rebalance_status`，其输出比 `get_rebalance_progress` 更容易理解。

分片再平衡启动后，`get_rebalance_progress()` 显示涉及的每个分片的进度，跟踪 `citus_rebalance_start()` 规划并执行的移动。

#### 参数 {#arguments-43}

无。

#### 返回值 {#return-value-43}

返回元组，包含以下列：

- **sessionid**：再平衡监控进程的 PostgreSQL PID。
- **table_name**：正在移动的分片所属的表。
- **shardid**：对应分片的 ID。
- **shard_size**：分片大小，单位为字节。
- **sourcename**：源节点主机名。
- **sourceport**：源节点端口。
- **targetname**：目标节点主机名。
- **targetport**：目标节点端口。
- **progress**：0 = 等待移动；1 = 正在移动；2 = 已完成。
- **source_shard_size**：源节点上分片的大小，单位为字节。
- **target_shard_size**：目标节点上分片的大小，单位为字节。

#### 示例 {#example-37}

```sql
SELECT * FROM get_rebalance_progress();
```

```text
┌───────────┬────────────┬─────────┬────────────┬───────────────┬────────────┬───────────────┬────────────┬──────────┬───────────────────┬───────────────────┐
│ sessionid │ table_name │ shardid │ shard_size │ sourcename    │ sourceport │ targetname    │ targetport │ progress │ source_shard_size │ target_shard_size │
├───────────┼────────────┼─────────┼────────────┼───────────────┼────────────┼───────────────┼────────────┼──────────┼───────────────────┼───────────────────┤
│      7083 │ foo        │ 102008  │    1204224 │ n1.foobar.com │       5432 │ n4.foobar.com │       5432 │        0 │           1204224 │                 0 │
│      7083 │ foo        │ 102009  │    1802240 │ n1.foobar.com │       5432 │ n4.foobar.com │       5432 │        0 │           1802240 │                 0 │
│      7083 │ foo        │ 102018  │     614400 │ n2.foobar.com │       5432 │ n4.foobar.com │       5432 │        1 │            614400 │            354400 │
│      7083 │ foo        │ 102019  │       8192 │ n3.foobar.com │       5432 │ n4.foobar.com │       5432 │        2 │                 0 │              8192 │
└───────────┴────────────┴─────────┴────────────┴───────────────┴────────────┴───────────────┴────────────┴──────────┴───────────────────┴───────────────────┘
```

### citus_add_rebalance_strategy {#citus_add_rebalance_strategy}

向 [pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table) 表添加一行。

#### 参数 {#arguments-44}

各参数的详细说明参见 [pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table) 中的对应列。

- **name**：新策略的标识符。
- **shard_cost_function**：计算每个分片“代价”的函数标识符。
- **node_capacity_function**：衡量节点容量的函数标识符。
- **shard_allowed_on_node_function**：判断哪些分片可放置在哪些节点上的函数标识符。
- **default_threshold**：浮点阈值，控制节点之间累计分片代价的平衡精度。
- **minimum_threshold**：（可选）保护下限，指定 `citus_rebalance_start()` 的 threshold 参数允许的最小值。默认值为 *0*。

#### 返回值 {#return-value-44}

无。

### citus_set_default_rebalance_strategy {#citus_set_default_rebalance_strategy}

更新 [pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table)，将参数指定的策略设为分片再平衡的默认策略。

#### 参数 {#arguments-45}

**name**：[pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table) 中的策略名称。

#### 返回值 {#return-value-45}

无。

#### 示例 {#example-38}

```sql
SELECT citus_set_default_rebalance_strategy('by_disk_size');
```

### citus_remote_connection_stats {#citus_remote_connection_stats}

`citus_remote_connection_stats()` 返回到各远程节点的活动连接数。

#### 参数 {#arguments-46}

无。

#### 示例 {#example-39}

```sql
SELECT * from citus_remote_connection_stats();
```

```text
    hostname    | port | database_name | connection_count_to_node
----------------+------+---------------+--------------------------
 citus_worker_1 | 5432 | postgres      |                        3
(1 row)
```

### citus_drain_node {#citus_drain_node}

`citus_drain_node()` 将指定节点上的分片迁移到其他节点，目标节点在 `pg_dist_node` 中的 `shouldhaveshards` 必须为 *true*。从集群移除节点（例如关闭其物理服务器）前，应先调用此函数。

#### 参数 {#arguments-47}

**nodename**：要排空的节点主机名。

**nodeport**：要排空的节点端口号。

**shard_transfer_mode**：（可选）指定复制方式：PostgreSQL 逻辑复制或跨工作节点的 COPY 命令。可选值如下：

- *auto*：默认值。可使用逻辑复制时要求具备副本标识，否则采用旧行为，例如 *PostgreSQL 9.6* 上的分片修复方式。
- *force_logical*：即使表没有副本标识也使用逻辑复制。复制期间，对该表的并发更新或删除语句会失败。
- *block_writes*：对缺少主键或副本标识的表使用 COPY，并阻塞写入。

> [!NOTE]
> 从 11.0 版本开始，Citus 社区版支持全部分片传输模式。

**rebalance_strategy**：（可选）[pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table) 中的策略名称。省略时使用表中标记的默认策略。

#### 返回值 {#return-value-46}

无。

#### 示例 {#example-40}

移除单个节点（例如使用 PostgreSQL 标准端口的 '10.0.0.1'）的典型步骤如下：

1. 排空节点。

   ```sql
   SELECT * from citus_drain_node('10.0.0.1', 5432);
   ```
2. 等待命令完成。
3. 移除节点。

排空多个节点时，应改用 `citus_rebalance_start`，让 Citus 提前规划，以最少的分片移动次数完成操作。

1. 对每个待移除节点运行以下代码：

   ```sql
   SELECT * FROM citus_set_node_property(node_hostname, node_port, 'shouldhaveshards', false);
   ```
2. 使用 `citus_rebalance_start` 一次性排空所有这些节点：

   ```sql
   SELECT * FROM citus_rebalance_start(drain_only := true);
   ```
3. 等待排空再平衡完成。
4. 移除节点。

从 Citus 13.2 开始，以下函数支持基于快照添加节点：注册一个克隆节点（异步流复制副本），再将其提升为工作节点，以尽量减少数据移动。

### citus_add_clone_node {#citus_add_clone_node}

将流复制副本注册为现有工作节点的克隆。

#### 参数 {#arguments-48}

**clone_host**：克隆节点主机名。

**clone_port**：克隆节点端口。

**primary_host**：源工作节点主机名。

**primary_port**：源工作节点端口。

#### 返回值 {#return-value-47}

注册的克隆节点 ID。

#### 示例 {#example-41}

```sql
SELECT citus_add_clone_node('clone-node', 5432, 'primary-node', 5432);
```

### citus_add_clone_node_with_nodeid {#citus_add_clone_node_with_nodeid}

通过源工作节点 ID 注册克隆节点。

#### 参数 {#arguments-49}

**clone_host**：克隆节点主机名。

**clone_port**：克隆节点端口。

**primary_node_id**：源工作节点 ID。

#### 返回值 {#return-value-48}

注册的克隆节点 ID。

#### 示例 {#example-42}

```sql
SELECT citus_add_clone_node_with_nodeid('clone-node', 5432, 7);
```

### citus_remove_clone_node {#citus_remove_clone_node}

从集群中移除克隆节点。

#### 参数 {#arguments-50}

**clone_host**：克隆节点主机名。

**clone_port**：克隆节点端口。

#### 返回值 {#return-value-49}

无。

#### 示例 {#example-43}

```sql
SELECT citus_remove_clone_node('clone-node', 5432);
```

### citus_remove_clone_node_with_nodeid {#citus_remove_clone_node_with_nodeid}

通过节点 ID 移除克隆节点。

#### 参数 {#arguments-51}

**clone_node_id**：要移除的克隆节点 ID。

#### 返回值 {#return-value-50}

无。

#### 示例 {#example-44}

```sql
SELECT citus_remove_clone_node_with_nodeid(9);
```

### get_snapshot_based_node_split_plan {#get_snapshot_based_node_split_plan}

提升克隆节点前，预览源工作节点与克隆节点之间的分片分布计划。

#### 参数 {#arguments-52}

**primary_host**：源工作节点主机名。

**primary_port**：源工作节点端口。

**clone_host**：克隆节点主机名。

**clone_port**：克隆节点端口。

**rebalance_strategy**：（可选）[pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table) 中的策略名称。

#### 返回值 {#return-value-51}

返回一组行，展示计划的分片分布，例如 table_name、shardid、shard_size、sourcename、sourceport、targetname 和 targetport。

#### 示例 {#example-45}

```sql
SELECT * FROM get_snapshot_based_node_split_plan('primary-node', 5432, 'clone-node', 5432);
```

### citus_promote_clone_and_rebalance {#citus_promote_clone_and_rebalance}

将克隆提升为工作节点，并在源工作节点与提升后的克隆之间进行分片再平衡。

> [!IMPORTANT]
> - 再平衡仅影响源工作节点及其克隆，不影响其他工作节点。
> - 克隆必须是正在从源节点进行复制的异步流复制副本。
> - 函数会短暂阻塞写入以保证一致性，并串行执行放置变更。

#### 参数 {#arguments-53}

**clone_node_id**：要提升的克隆节点 ID。

**rebalance_strategy**：（可选，默认 *by_disk_size*）[pg_dist_rebalance_strategy](/citus/reference/api-metadata/#rebalancer-strategy-table) 中的策略名称。

**catchup_timeout_seconds**：（可选，默认 *300*）等待副本追平的超时时间。

#### 返回值 {#return-value-52}

表示是否成功的布尔值。

#### 示例 {#example-46}

```sql
SELECT citus_promote_clone_and_rebalance(9);
```

### isolate_tenant_to_new_shard {#isolate_tenant_to_new_shard}

> [!NOTE]
> 从 11.0 版本开始，Citus 社区版包含 `isolate_tenant_to_new_shard` 函数。

创建一个新分片，存放分布列具有指定单一值的所有行。这对多租户场景尤其有用：可以将大租户独立放到自己的分片中，最终迁移到独立的物理节点。

更深入的说明参见 `tenant_isolation`。

#### 参数 {#arguments-54}

- **table_name**：要为其创建新分片的表名。
- **tenant_id**：要分配给新分片的分布列值。
- **cascade_option**：（可选）设为 *CASCADE* 时，还会对当前表所属 `colocation_groups` 中的所有表分别隔离出相应分片。

#### 返回值 {#return-value-53}

- **shard_id**：新建分片的唯一 ID。

#### 示例 {#examples-2}

创建新分片，存放租户 *135* 的 lineitems 数据：

```sql
SELECT isolate_tenant_to_new_shard('lineitem', 135);
```

```text
┌─────────────────────────────┐
│ isolate_tenant_to_new_shard │
├─────────────────────────────┤
│                      102240 │
└─────────────────────────────┘
```

### citus_create_restore_point {#citus_create_restore_point}

暂时阻塞集群的所有写入，并在所有节点上创建命名恢复点。它类似于 [pg_create_restore_point](https://www.postgresql.org/docs/current/static/functions-admin.html#FUNCTIONS-ADMIN-BACKUP)，但作用于所有节点，并确保各节点的恢复点一致。

此函数可用于时间点恢复和创建集群分支。

> [!TIP]
> **适用于 MX 的安全恢复点。** 在 Citus 14 中，`citus_create_restore_point()` 可安全用于 MX（多写入节点）集群。函数现在会：
> 
> - 连接所有节点，包括元数据节点和非元数据节点；
> - 在远程节点开始协调事务；
> - 在**所有元数据节点**上对 `pg_dist_transaction` 获取 `ExclusiveLock`，阻塞 2PC 提交决策；
> - 在协调节点上锁定 `pg_dist_node` 和 `pg_dist_partition`，阻塞拓扑和 DDL 变更；
> - 在所有节点并行创建恢复点；
> - 关闭连接时释放锁，隐式执行 ROLLBACK。
> 
> Citus 2PC 将提交决策记录在 `pg_dist_transaction` 中，因此持有 `ExclusiveLock` 就能建立明确的一致性分界点，而无需等待所有事务退出。已经记录提交信息的预备事务会完成，其余事务则被阻塞。
> 
> **向后兼容性：** 函数签名和返回类型不变，仅使用协调节点的模式下行为不变。

#### 参数 {#arguments-55}

**name**：要创建的恢复点名称。

#### 返回值 {#return-value-54}

**coordinator_lsn**：恢复点在协调节点预写日志（WAL）中的日志序列号。

#### 示例 {#examples-3}

```sql
select citus_create_restore_point('foo');
```

```text
┌────────────────────────────┐
│ citus_create_restore_point │
├────────────────────────────┤
│ 0/1EA2808                  │
└────────────────────────────┘
```

### citus_cluster_changes_block {#citus_cluster_changes_block}

> [!NOTE]
> 适用于 Citus 13.3 及更高版本，以及 Citus 14.1 及更高版本。

在集群范围内阻塞分布式写入提交、模式变更和拓扑变更，以便为集群所有节点创建一致的磁盘快照备份。此函数与 [`citus_cluster_changes_unblock`](#citus_cluster_changes_unblock) 配合使用，并可通过 [`citus_cluster_changes_block_status`](#citus_cluster_changes_block_status) 观察状态。

Citus 使用两阶段提交（2PC）提交分布式写事务，将提交决策记录在协调节点的 `pg_dist_transaction` 中。因此，未协调而分别创建的节点磁盘快照，可能将进行中的 2PC 事务捕获为不一致状态，例如协调节点已写入提交记录，但工作节点尚未执行 `COMMIT PREPARED`。恢复这类快照可能造成无法修复的数据不一致。

`citus_cluster_changes_block()` 启动专用后台工作进程，在一个长事务中执行以下操作来解决此问题：

- 在协调节点上对 `pg_dist_node`、`pg_dist_partition` 和 `pg_dist_transaction` 获取 `ExclusiveLock`。
- 在每个元数据工作节点上，对 `pg_dist_partition` 和 `pg_dist_transaction` 执行 `LOCK TABLE … IN EXCLUSIVE MODE`。（`pg_dist_node` 特意只在协调节点锁定，因为节点管理不委派给工作节点。）

2PC 提交路径需要在 `pg_dist_transaction` 上获取 `RowExclusiveLock` 来记录提交决策，而该锁模式与 `ExclusiveLock` 冲突。因此，成功获取锁可保证函数返回前，所有进行中的 2PC 事务均已完成，包括每个工作节点上的 `COMMIT PREPARED`；阻塞保持期间也无法开始新的提交决策。这样便建立了明确的分界：锁之前的操作已在所有节点完整提交，锁之后的操作尚未开始。

> [!IMPORTANT]
> 读取查询和单分片写入**不会**被阻塞。经过 2PC 的多分片或跨节点写入会**排队等待**，而非被中止；调用 `citus_cluster_changes_unblock()` 后可正常继续。

> [!NOTE]
> `citus_cluster_changes_block()` 保持阻塞期间，仅保证没有 2PC 提交决策跨越快照边界。WAL 刷盘、快照编排以及各节点磁盘快照的执行时机，仍由操作人员负责。

函数阻塞等待，直到获取集群范围的锁或达到 `timeout_ms`。如果超时，或保持阻塞期间任一工作节点连接断开，后台工作进程会释放所有锁并结束事务。

#### 参数 {#arguments-56}

**timeout_ms**：（可选）阻塞的最长持续时间，单位为毫秒。达到该时长后，即使未调用 `citus_cluster_changes_unblock()`，后台工作进程也会自动释放锁并退出。默认值为 `300000`（5 分钟），允许范围为 `1` 到 `1800000`（30 分钟），超出范围会报错。

#### 返回值 {#return-value-55}

阻塞生效且集群范围内所有锁均已获取后，返回 `true`。如果未能在 `timeout_ms` 内获取锁、远程节点不可达，或已经存在活动阻塞，则报错。

#### 所需权限 {#required-privileges}

- 必须在协调节点执行。
- 需要超级用户权限；已撤销 `PUBLIC` 对该函数的执行权限。

#### 示例 {#example-47}

```sql
-- Block the cluster for up to 60 seconds while a snapshot is taken.
SELECT citus_cluster_changes_block(60000);
```

```text
 citus_cluster_changes_block
-----------------------------
 t
(1 row)
```

```sql
-- Trigger per-node disk snapshots from your orchestration tooling here.

-- Release the block.
SELECT citus_cluster_changes_unblock();
```

### citus_cluster_changes_unblock {#citus_cluster_changes_unblock}

向 [`citus_cluster_changes_block`](#citus_cluster_changes_block) 启动的后台工作进程发送信号，释放所有集群范围的锁并退出。此函数幂等：没有活动阻塞时调用不会报错，只返回 `false`。

阻塞由专用后台工作进程维持，而非调用会话持有，因此任意会话都可以调用 `citus_cluster_changes_unblock()`，包括与发起 `citus_cluster_changes_block()` 不同的会话。这使得操作人员连接断开后仍能安全解除阻塞。

#### 参数 {#arguments-57}

无。

#### 返回值 {#return-value-56}

成功释放活动阻塞时返回 `true`；没有活动阻塞时返回 `false`，保持幂等，且此时绝不报错。

#### 所需权限 {#required-privileges-1}

- 必须在协调节点执行。
- 需要超级用户权限；已撤销 `PUBLIC` 对该函数的执行权限。

#### 示例 {#example-48}

```sql
SELECT citus_cluster_changes_unblock();
```

```text
 citus_cluster_changes_unblock
-------------------------------
 t
(1 row)
```

### citus_cluster_changes_block_status {#citus_cluster_changes_block_status}

返回由 [`citus_cluster_changes_block`](#citus_cluster_changes_block) 和 [`citus_cluster_changes_unblock`](#citus_cluster_changes_unblock) 管理的集群范围阻塞的当前状态。可通过此函数在自动化或可观测性工具中监控备份协调过程。

函数检查后台工作进程是否存活，并自动清理进程崩溃后遗留的过时状态，保证报告的 `state` 始终反映集群的实际情况。

#### 参数 {#arguments-58}

无。

#### 返回值 {#return-value-57}

返回一行，包含以下列：

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `text` | 阻塞的当前状态：`inactive`、`starting`、`active`、`releasing` 或 `error`。 |
| `worker_pid` | `int` | 持有锁的后台工作进程的进程 ID。`state = inactive` 时为 `NULL`。 |
| `requestor_pid` | `int` | 调用 `citus_cluster_changes_block()` 的后端进程 ID。`state = inactive` 时为 `NULL`。 |
| `block_start_time` | `timestamptz` | 开始阻塞的时间。`state = inactive` 时为 `NULL`。 |
| `timeout_ms` | `int` | 传入 `citus_cluster_changes_block()` 的 `timeout_ms` 参数。`state = inactive` 时为 `NULL`。 |
| `node_count` | `int` | 阻塞覆盖的节点数，包括协调节点和元数据工作节点。`state = inactive` 时为 `NULL`。 |

状态机：`inactive` → `starting` → `active` → `releasing` → `inactive`；失败时转为 `→ error`。

#### 所需权限 {#required-privileges-2}

- 必须在协调节点执行。
- 任意角色均可读取。函数只暴露非敏感状态，特意允许没有超级用户权限的监控工具使用。

#### 示例 {#example-49}

```sql
SELECT * FROM citus_cluster_changes_block_status();
```

```text
 state  | worker_pid | requestor_pid |       block_start_time        | timeout_ms | node_count
--------+------------+---------------+-------------------------------+------------+------------
 active |      24578 |         24501 | 2026-05-04 09:12:33.412+00    |      60000 |          3
(1 row)
```

## 相关内容 {#related-content}

- [元数据表和视图](/citus/reference/api-metadata/)
- [配置参数](/citus/reference/api-guc/)
- [什么是 Azure Cosmos DB for PostgreSQL？](/citus/overview/what-is-citus/)
