---
title: What is Citus?
description: Learn what Citus is and the core architecture concepts including nodes, sharding models, table types, shards, colocation, and query execution.
weight: 10
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/what-is-citus?view=citus-14
upstream_ref: citus-14; a4ec7e731f6c
---

Citus is an open source PostgreSQL extension that scales PostgreSQL horizontally. You can start on a single node and grow to a distributed cluster. Because Citus is an extension (not a fork), you keep native PostgreSQL compatibility, features, ecosystem tools, and extensions.

Key capabilities include:

- Distributed tables (row-based and schema-based sharding)
- Reference tables for dimension/shared data
- Colocated joins and distributed query planner
- Parallel query execution across workers
- Columnar storage option
- Query from any node in MX mode (since Citus 11.0)

Typically, you adopt Citus to improve performance and scalability for multitenant SaaS, real-time analytics dashboards, time series, and microservices state management.

Ways to use Citus:

1. **Open source**: [Download Citus](https://www.citusdata.com/download/) or build from the [GitHub repository](https://github.com/citusdata/citus).
2. **Managed service**: Use [elastic clusters on Azure Database for PostgreSQL Flexible server](https://techcommunity.microsoft.com/blog/adforpostgresql/postgres-horizontal-scaling-with-elastic-clusters-on-azure-database-for-postgres/4303508).

The following sections merge the former "overview" and "concepts" articles into a single consolidated guide.

## Architecture concepts {#architecture-concepts}

This section orients you to the building blocks that make Citus distributed: how nodes coordinate, how data is partitioned, the table abstractions you can choose from, and how queries execute in parallel.

### Nodes and cluster {#nodes-and-cluster}

Citus is a PostgreSQL extension that lets commodity servers (*nodes*) coordinate in a shared-nothing architecture. Together, nodes form a *cluster* that can store more data and use more CPU cores than a single machine. You scale by adding worker nodes.

### Coordinator and workers {#coordinator-and-workers}

Each cluster has one *coordinator* node and one or more *worker* nodes. Internal Citus metadata tables track worker health, node addresses, and shard placement, and Citus syncs this metadata to every node. Applications connect to the coordinator or, in MX mode (since Citus 11.0), to any worker node. The node that receives a query routes or parallelizes it based on table distribution metadata. For details on the receiving-node model, see [Query processing in Citus](/citus/reference/reference-processing/#query-entry-points-and-mx-mode).

For each query, the receiving node either:

- Routes it to a single worker (when all required data is local to that worker), or
- Parallelizes it across workers (when data spans shards)

### Sharding models {#sharding-models}

> [!NOTE]
> For comprehensive documentation on sharding models in managed Azure environments, see [Sharding models in Azure Cosmos DB for PostgreSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/concepts-sharding-models).

Citus supports two sharding models, each with different tradeoffs:

| Model | Description | Best for | Notes |
| --- | --- | --- | --- |
| Row-based sharding | Shared schema; tenants distinguished by a distribution column (sharding key) within tables | High density multitenant, IoT, time series | Requires adding a distribution column and query filters; most hardware efficient |
| Schema-based sharding | Separate schema per tenant (introduced in Citus 12.0) | Microservices, heterogeneous tenant schemas, minimal app changes | Lower tenant density; simpler onboarding; set `search_path` per tenant |

#### Row-based sharding {#row-based-sharding}

Classic Citus model: one database, shared schema. A designated `dist_column` identifies tenant or distribution key and determines shard assignment. Densely packs tenants for maximum hardware efficiency. Requires schema and application query adjustments to include and filter by the distribution column.

Benefits:

- Highest tenant density
- Best performance characteristics

Drawbacks:

- Requires schema and query changes
- Uniform schema across tenants

#### Schema-based sharding {#schema-based-sharding}

Introduced in Citus 12.0. Each tenant (or microservice) lives in its own schema; schemas are mapped to shard groups. Query changes are minimal – often only setting the correct `search_path`.

Benefits:

- Heterogeneous schemas allowed
- Minimal application and query changes
- Easier migration path

Drawbacks:

- Fewer tenants per node compared to row-based

### Table types {#table-types}

> [!NOTE]
> For detailed documentation on table types in managed Azure environments, see [Table types in Azure Cosmos DB for PostgreSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/concepts-nodes#table-types).

Citus exposes multiple table paradigms:

| Type | Purpose | Notes |
| --- | --- | --- |
| Distributed | Horizontally sharded across workers | Requires distribution column (except schema-based) |
| Reference | Fully replicated small table on every worker | Ideal for dimension/enumeration data |
| Local | Regular PostgreSQL table (not sharded) | Lives only on coordinator unless managed |
| Local managed | Local table registered in metadata | Queried cluster-wide; displayed as `local` in `citus_tables` |
| Schema table | Table in a distributed schema (schema-based sharding) | Automatically colocated; no explicit shard key |

#### Distributed tables {#distributed-tables}

Appear as normal tables but are backed by per-shard tables (for example, `table_1001`). DDL changes propagate to all shards. Create with distribution helpers (see [creating and distributing tables](/citus/reference/reference-ddl/#creating-and-distributing-tables)).

##### Distribution column {#distribution-column}

Deterministic hashing of the distribution column maps rows to shards. A good choice drives performance and enables colocation. See distributed data modeling guidance.

#### Reference tables {#reference-tables}

Replicated single-shard tables present on every worker. Avoid network overhead for common lookups (for example, product categories). Writes use two-phase commit for consistency. See [reference tables](/citus/reference/reference-ddl/#reference-tables).

#### Local and local managed tables {#local-and-local-managed-tables}

Regular tables on the coordinator. Optionally promoted to "managed" via `citus_add_local_table_to_metadata` (or foreign key autoregistration with `enable_local_ref_fkeys`) so you can access them from any node.

#### Schema tables {#schema-tables}

In schema-based sharding, tables inside a distributed schema automatically become colocated distributed tables (no manual shard key selection). Displayed as `schema` in `citus_tables`.

### Shards and placements {#shards-and-placements}

Distributed tables are divided into shards that the system stores as ordinary tables on workers (for example, `github_events_102027`). Coordinator metadata (such as `pg_dist_shard`) maps hash ranges to shard IDs. *Placements* map shard IDs to worker nodes. For durability, replication uses PostgreSQL streaming replication outside of Citus metadata.

### Colocation {#colocation}

Place related tables' shards together (same hash mapping) for local joins. For example, `stores`, `products`, and `purchases` share `store_id`. Colocation reduces cross-node data movement. See [table colocation](/citus/modeling/data-modeling/#table-colocation).

### Query parallelism and execution flow {#query-parallelism-and-execution-flow}

The receiving node (coordinator or, in MX mode, any worker) decomposes multishard queries into per-shard *tasks*. Task execution tries to balance:

- Concurrency (parallel connections per worker)
- Connection overhead (slow start ramp-up)
- Worker resource conservation (idle connection caps)

Key settings:

| Setting | Purpose |
| --- | --- |
| `max_adaptive_executor_pool_size` | Caps simultaneous connections per worker per query |
| `executor_slow_start_interval` | Gradually increases parallelism to avoid overload |
| `max_cached_conns_per_worker` | Limits idle cached connections per worker per session |
| `max_shared_pool_size` | Global safety limit on total worker connections |

## Related content {#related-content}

- [PostgreSQL at any scale with Citus](/citus/overview/postgresql-citus-scale/)
- [Multitenant applications tutorial](/citus/tutorials/tutorial-multi-tenant/)
