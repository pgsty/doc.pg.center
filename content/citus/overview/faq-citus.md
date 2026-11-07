---
title: Frequently asked questions about Citus for PostgreSQL
description: Learn about common questions about Citus, including primary keys, adding nodes, rebalancing shards, and distributed table management.
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/faq-citus?view=citus-14
upstream_ref: citus-14; be6cf64ecd13
---

This article answers common questions about Citus for PostgreSQL. It covers topics like primary keys, node management, shard distribution, failover handling, and PostgreSQL feature support. If you're new to Citus, see [What is Citus?](/citus/overview/what-is-citus/).

## General {#general}

### Can I create primary keys on distributed tables? {#can-i-create-primary-keys-on-distributed-tables-}

Currently, Citus imposes a primary key constraint only if the distribution column is part of the primary key. This constraint ensures that you only need to check one shard to ensure uniqueness.

### Are there any PostgreSQL features not supported by Citus? {#are-there-any-postgresql-features-not-supported-by-citus-}

Since Citus provides distributed functionality by extending PostgreSQL, it uses the standard PostgreSQL SQL constructs. Most queries are supported, even when they combine data across the network from multiple database nodes. This support includes transactional semantics across nodes. For an up-to-date list of SQL coverage, see [Workarounds](/citus/reference/reference-workarounds/#workarounds).

What's more, Citus has 100% SQL support for queries that access a single node in the database cluster. These queries are common, for instance, in multitenant applications where different nodes store different tenants. For more information, see [What is Citus?](/citus/overview/what-is-citus/).

Remember that even with this extensive SQL coverage, data modeling can have a significant effect on query performance. For details on how Citus executes queries, see [Query processing](/citus/reference/reference-processing/).

### Can I run Citus on Microsoft Azure? {#can-i-run-citus-on-microsoft-azure-}

Yes, Citus is available as a managed service with [elastic clusters on Azure Database for PostgreSQL Flexible server](https://techcommunity.microsoft.com/blog/adforpostgresql/postgres-horizontal-scaling-with-elastic-clusters-on-azure-database-for-postgres/4303508).

## Cluster Management {#cluster-management}

### How do I add nodes to an existing Citus cluster? {#how-do-i-add-nodes-to-an-existing-citus-cluster-}

On the Citus managed service with elastic clusters on Azure Database for PostgreSQL, you can add nodes through the Azure portal or Azure CLI. With Citus open source, you can add nodes manually by calling the `citus_add_node` UDF with the hostname (or IP address) and port number of the new node.

Either way, after adding a node to an existing cluster, the new node doesn't contain any data (shards). Citus starts assigning any newly created shards to this node. To rebalance existing shards from the older nodes to the new node, Citus provides an open source shard rebalancer utility. For more information, see [Parallel rebalancing](/citus/operations/cluster-management/#parallel-rebalancing).

### How does Citus handle failure of a worker node? {#how-does-citus-handle-failure-of-a-worker-node-}

Citus uses PostgreSQL's streaming replication to replicate the entire worker node as-is. It replicates worker nodes by continuously streaming their WAL records to a standby. You can configure streaming replication on-premises yourself by consulting the [PostgreSQL replication documentation](https://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION).

### How does Citus handle failover of the coordinator node? {#how-does-citus-handle-failover-of-the-coordinator-node-}

Because the Citus coordinator node is similar to a standard PostgreSQL server, you can use regular PostgreSQL synchronous replication and failover to provide higher availability of the coordinator node. Many of our customers use synchronous replication in this way to add resilience against coordinator node failure. For more information on node failures, see [Dealing with node failures](/citus/operations/cluster-management/#dealing-with-node-failures).

### What if a worker node's address changes? {#what-if-a-worker-node-s-address-changes-}

If the hostname or IP address of a worker changes, you need to let the coordinator know by using `citus_update_node`:

```sql
-- update worker node metadata on the coordinator
-- (remember to replace 'old-address' and 'new-address'
--  with the actual values for your situation)

select citus_update_node(nodeid, 'new-address', nodeport)
  from pg_dist_node
 where nodename = 'old-address';
```

Until you execute this update, the coordinator isn't able to communicate with that worker for queries.

## Sharding and Distribution {#sharding-and-distribution}

### How do I choose the shard count when I hash-partition my data? {#how-do-i-choose-the-shard-count-when-i-hash-partition-my-data-}

You choose the shard count when you first distribute a table. You can set this value differently for each colocation group, and the optimal value depends on your use case. You can change the count after cluster creation, but it's difficult. Use these guidelines to choose the right size.

For the [multitenant application](/citus/tutorials/tutorial-multi-tenant/) use case, choose between 32 and 128 shards. For smaller workloads (less than 100 GB), start with 32 shards. For larger workloads, choose 64 or 128 shards. You can scale from 32 to 128 worker machines.

For the [real-time analytics](/citus/tutorials/tutorial-analytics/) use case, relate the shard count to the total number of cores on the workers. To ensure maximum parallelism, create enough shards on each node so that there's at least one shard per CPU core. Create a high number of initial shards, such as two or four times the number of current CPU cores. This setup allows for future scaling if you add more workers and CPU cores.

To choose a shard count for a table you want to distribute, update the `citus.shard_count` variable. This variable affects subsequent calls to `create_distributed_table`. For example:

```sql
SET citus.shard_count = 64;
-- any tables distributed at this point will have
-- sixty-four shards
```

For more information, see [choosing cluster size](/citus/operations/cluster-management/#choosing-cluster-size).

### How do I change the shard count for a hash partitioned table? {#how-do-i-change-the-shard-count-for-a-hash-partitioned-table-}

Citus has a function called `alter_distributed_table` that can change the shard count of a distributed table.

### Which shard contains data for a particular tenant? {#which-shard-contains-data-for-a-particular-tenant-}

Citus provides UDFs and metadata tables to determine the mapping of a distribution column value to a particular shard, and the shard placement on a worker node. For more information, see [Finding which shard contains data for a specific tenant](/citus/operations/diagnostic-queries/#finding-which-shard-contains-data-for-a-specific-tenant).

### I forgot the distribution column of a table, how do I find it? {#i-forgot-the-distribution-column-of-a-table--how-do-i-find-it-}

The Citus coordinator node metadata tables contain this information. For more information, see [Finding the distribution column for a table](/citus/operations/diagnostic-queries/#finding-the-distribution-column-for-a-table).

### Can I distribute a table by multiple keys? {#can-i-distribute-a-table-by-multiple-keys-}

No, you must choose a single column per table as the distribution column. A common scenario where you want to distribute by two columns is for time series data. However, for this case, use a hash distribution on a nontime column, and combine this approach with PostgreSQL partitioning on the time column. For more information, see [Time series data](/citus/modeling/data-modeling/#time-series-data).

### Can I shard by schema on Citus for multitenant applications? {#can-i-shard-by-schema-on-citus-for-multitenant-applications-}

Yes, Citus supports [schema-based sharding](/citus/overview/what-is-citus/#schema-based-sharding) starting with version 12.0.

## Queries and Performance {#queries-and-performance}

### How does Citus support count(distinct) queries? {#how-does-citus-support-count-distinct--queries-}

Citus can evaluate count(distinct) aggregates both in and across worker nodes. When Citus aggregates on a table's distribution column, Citus can push the counting down inside worker nodes and total the results. Otherwise, it can pull distinct rows to the coordinator and calculate there. If transferring data to the coordinator is too expensive, fast approximate counts are also available. For more information, see [Count(distinct) aggregates](/citus/reference/reference-sql/#countdistinct-aggregates).

### Why am I seeing an error about max_intermediate_result_size? {#why-am-i-seeing-an-error-about-max-intermediate-result-size-}

Citus has to use more than one step to run some queries that have subqueries or CTEs. By using [push-pull execution](/citus/reference/reference-processing/#subquery-and-cte-push-pull-execution), Citus pushes subquery results to all worker nodes for use by the main query. If these results are too large, this approach might cause unacceptable network overhead, or even insufficient storage space on the coordinator node, which accumulates and distributes the results.

Citus uses a configurable setting, `citus.max_intermediate_result_size`, to specify a subquery result size threshold at which the query is canceled. If you run into the error, it appears as:

```text
ERROR: the intermediate result size exceeds citus.max_intermediate_result_size (currently 1 GB)
DETAIL: Citus restricts the size of intermediate results of complex subqueries and CTEs to avoid accidentally pulling large result sets into once place.
HINT: To run the current query, set citus.max_intermediate_result_size to a higher value or -1 to disable.
```

As the error message suggests, you can (cautiously) increase this limit by altering the variable:

```sql
SET citus.max_intermediate_result_size = '3GB';
```

## Tables and Constraints {#tables-and-constraints}

### In which situations are uniqueness constraints supported on distributed tables? {#in-which-situations-are-uniqueness-constraints-supported-on-distributed-tables-}

Citus can enforce a primary key or uniqueness constraint only when the constrained columns contain the distribution column. If a single column constitutes the primary key, it needs to be the distribution column.

This restriction allows Citus to localize a uniqueness check to a single shard and let PostgreSQL on the worker node do the check efficiently.

### Why does pg_relation_size report zero bytes for a distributed table? {#why-does-pg-relation-size-report-zero-bytes-for-a-distributed-table-}

The data in distributed tables lives on the worker nodes (in shards), not on the coordinator. A true measure of distributed table size is obtained as a sum of shard sizes. Citus provides helper functions to query this information. For more information, see [Table management](/citus/operations/table-management/).

## Database Objects {#database-objects}

### How do I create database roles, functions, extensions, and other objects in a Citus cluster? {#how-do-i-create-database-roles--functions--extensions--and-other-objects-in-a-citus-cluster-}

Certain commands that you run on the coordinator node don't propagate to the worker nodes:

- `CREATE ROLE/USER`
- `CREATE DATABASE`
- `ALTER ... SET SCHEMA`
- `ALTER TABLE ALL IN TABLESPACE`
- `CREATE TABLE` (see [table types](/citus/overview/what-is-citus/#table-types))

For these types of objects, create them explicitly on all nodes. Citus provides a function to execute queries across all workers:

```sql
SELECT run_command_on_workers($cmd$
  /* the command to run */
  CREATE ROLE ...
$cmd$);
```

Learn more in [manual command propagation](/citus/reference/reference-propagation/). Also note that even after manually propagating `CREATE DATABASE`, you must still install Citus there. For more information, see [Creating a new database](/citus/operations/cluster-management/#creating-a-new-database).

As of Citus 13.1, additional database/role DDLs are auto-propagated. See [Database and role management DDL](/citus/reference/reference-ddl/#database-and-role-management-ddl) for details.

In the future, Citus automatically propagates more kinds of objects. The advantage of automatic propagation is that Citus automatically creates a copy on any newly added worker nodes. For more information, see [Distributed object table](/citus/reference/api-metadata/#distributed-object-table).

## Extensions and Storage {#extensions-and-storage}

### How does cstore_fdw work with Citus? {#how-does-cstore-fdw-work-with-citus-}

You don't need the cstore_fdw extension on PostgreSQL 12 and later, because Citus implements `columnar` storage directly. Unlike cstore_fdw, Citus' columnar tables support transactional semantics, replication, and pg_upgrade. Citus' query parallelization, seamless sharding, and high availability benefits combine powerfully with the superior compression and I/O utilization of columnar storage for large dataset archival and reporting.

## Migration and Legacy {#migration-and-legacy}

### What happened to pg_shard? {#what-happened-to-pg-shard-}

The pg_shard extension is deprecated and no longer supported.

The Citus team merged pg_shard's codebase into Citus to offer you a unified solution, starting with the open-source release of Citus v5.x. This solution provides advanced distributed query planning that previously only CitusDB customers enjoyed. It preserves the simple and transparent sharding and real-time writes and reads that pg_shard brought to the PostgreSQL ecosystem. Citus, the flagship product, provides a superset of the functionality of pg_shard. The Citus team provides migration steps to help existing users perform a drop-in replacement. For more information, please [contact us](https://www.citusdata.com/about/contact_us).

## Related content {#related-content}

- [What is Citus?](/citus/overview/what-is-citus/)
- [Tutorial: Design a multitenant database](/citus/tutorials/tutorial-multi-tenant/)
- [Tutorial: Design a real-time analytics dashboard](/citus/tutorials/tutorial-analytics/)
