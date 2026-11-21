---
title: Distributed shard discovery
description: Describe getShardMap and listShards responses implemented by documentdb_distributed.
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/contrib/documentdb_distributed/shard-discovery.md
weight: 30
---

The [documentdb_distributed extension](/documentdb/reference/commands/contrib/documentdb_distributed/overview/) implements `getShardMap` and `listShards` responses from cluster node metadata. These describe node groups and their members, not the distribution of every document or collection.

Availability of these wire APIs is subject to provider gateway integration.

<span id="get-shard-map"></span>

## getShardMap {#getshardmap}

```javascript
db.adminCommand({ getShardMap: 1 })
```

The command implementation has no command-specific argument parsing. It returns `ok` and, when eligible node groups exist, the following fields:

| Field | Description |
| --- | --- |
| **`map`** | A document mapping `shard_<groupid>` names to strings containing the group name and its active member-node names. |
| **`hosts`** | A document mapping each active member-node name to its shard-group name. |
| **`nodes`** | A document keyed by member-node name, with each node's `role`, `active`, and `cluster` values. Inactive members can appear here even though they are excluded from the active host mapping. |
{.fields}

For illustration, a deployment with one eligible group and one active primary member could return:

```json
{
  "ok": 1,
  "map": { "shard_1": "shard_1/node_default_2" },
  "hosts": { "node_default_2": "shard_1" },
  "nodes": {
    "node_default_2": { "role": "primary", "active": true, "cluster": "default" }
  }
}
```

These are illustrative identifiers, not required node names. A `shard_1` group name can identify a destination for [`moveCollection`](/documentdb/reference/commands/contrib/documentdb_distributed/movecollection/), but confirm that the group has an active primary node before using it.

<span id="list-shards"></span>

## listShards {#listshards}

See the dedicated [`listShards` command reference](/documentdb/reference/commands/contrib/documentdb_distributed/listshards/) for command syntax, response fields, an illustrative result, and gateway availability. Its group identifiers can be used to choose a `moveCollection` destination.

Both implementations select nodes marked `shouldhaveshards` in the cluster metadata. If no eligible nodes exist, the implementation can return only `{ ok: 1 }` without the mapping fields or array.

## Other distributed metadata {#other-distributed-metadata}

The extension's query hooks also add distributed collection metadata. `listCollections` with `addDistributedMetadata` includes `shardCount` and `colocationId`. The config-shard and config-chunk query hooks expose node-group and placement information for the distributed layout.

These hooks do not add a new wire command for each metadata field. See [distributed collection and placement metadata](/documentdb/reference/commands/contrib/documentdb_distributed/colocation/#distributed-collection-and-placement-metadata) for the fields, namespace availability, and `config.collections` behavior, and the [collection metadata reference](/documentdb/reference/commands/administration/listcollections/) for existing command options.

## Implementation {#implementation}

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/) for the source revision.

The extension provides `command_get_shard_map` and `command_list_shards`. Its SQL installation scripts do not create standalone `get_shard_map` or `list_shards` functions; the provider gateway must integrate the distributed implementations.

Source: [distributed node and colocation code](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/internal/pg_documentdb_distributed/src/colocation/shard_colocation.c), `command_get_shard_map`, `command_list_shards`, `GetShardMapNodes`, `WriteShardMap`, `WriteShardList`, and `UpdateColocationHooks`.
