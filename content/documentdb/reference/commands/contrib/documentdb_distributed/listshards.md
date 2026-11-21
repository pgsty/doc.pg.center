---
title: listShards
description: List DocumentDB distributed node groups and their active members with documentdb_distributed.
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/listShards.md
weight: 60
---

Lists node groups and their active member-node names using the [documentdb_distributed extension](/documentdb/reference/commands/contrib/documentdb_distributed/overview/#prerequisites-and-installation). These are placement groups, not the physical backing shards of individual collections.

Run the command against the `admin` database on a gateway integrated with the distributed implementation:

```javascript
db.adminCommand({ listShards: 1 })
```

| Parameter | Description |
| --- | --- |
| **`listShards`** | (Required) The command marker, conventionally `1`. The distributed implementation has no command-specific options. |
{.fields}

## Response {#response}

For illustration, a deployment with one eligible group and one active primary member could return:

```json
{
  "ok": 1,
  "shards": [
    { "_id": "shard_1", "nodes": "shard_1/node_default_2" }
  ]
}
```

| Field | Description |
| --- | --- |
| **`ok`** | `1` on success. |
| **`shards`** | An array of eligible node groups. When no eligible groups exist, the implementation can omit this field and return only `{ ok: 1 }`. |
| **`shards._id`** | A node-group name in `shard_<groupid>` form. Use this value as `moveCollection.toShard`, rather than a physical shard identifier. |
| **`shards.nodes`** | The group name, `/`, and comma-separated active member-node names. These names are metadata identifiers, not host connection strings. |
{.fields}

The implementation selects nodes marked `shouldhaveshards` in the cluster metadata. It lists active members in `nodes`, but does not include their roles. Before [moving a collection](/documentdb/reference/commands/contrib/documentdb_distributed/movecollection/#choose-a-destination), use [`getShardMap`](/documentdb/reference/commands/contrib/documentdb_distributed/shard-discovery/#getshardmap) to confirm that the chosen group has an active primary member. The illustrative identifiers above are not guaranteed to exist in your deployment.

## Availability {#availability}

Availability is subject to provider gateway implementations.

For the related config-shard metadata query and collection placement fields, see [distributed collection and placement metadata](/documentdb/reference/commands/contrib/documentdb_distributed/colocation/#distributed-collection-and-placement-metadata).

## Implementation {#implementation}

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/) for the source revision.

Source: [distributed node and colocation code](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/internal/pg_documentdb_distributed/src/colocation/shard_colocation.c), `command_list_shards`, `GetShardMapNodes`, and `WriteShardList`; default gateway: `pg_documentdb_gw/documentdb_gateway_core/src/postgres/documentdb_data_client.rs`, `execute_list_shards`.
