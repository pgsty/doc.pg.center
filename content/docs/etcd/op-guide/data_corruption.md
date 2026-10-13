---
title: Data Corruption
weight: 5000
description: etcd data corruption and recovery
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/data_corruption.md"
aliases: [/etcd/op-guide/data_corruption/]
---

etcd has built in automated data corruption detection to prevent member state from diverging.

> [!NOTE]
> In etcd 3.7, use the feature gates and duration flags below. The former experimental corruption-check flags have been removed; see [configuration options](/docs/etcd/op-guide/configuration/#feature-gates).

## Enabling data corruption detection

Data corruption detection can be done using:
* Initial check, enabled with `--feature-gates=InitialCorruptCheck=true` flag.
* Periodic check of:
  * Compacted revision hash, enabled with `--feature-gates=CompactHashCheck=true` flag.
  * Latest revision hash, enabled with `--corrupt-check-time` flag.

Initial check will be executed during bootstrap of etcd member.
Member will compare its persistent state vs other members and exit if there is a mismatch.

Both periodic check will be executed by the cluster leader in a cluster that is already running.
Leader will compare its persistent state vs other members and raise a CORRUPT ALARM if there is a mismatch.
Both checks serve the same purpose, however they are both worth enabling to balance performance and time to detection.
* Compacted revision hash check - requires regular compaction, minimal performance cost, handles slow followers.
* Latest revision hash check - high performance cost, doesn't handle slow followers or frequent compactions.

### Compacted revision hash check

When enabled using `--feature-gates=CompactHashCheck=true` flag, check will be executed once every minute.
This can be adjusted using `--compact-hash-check-time` flag using format: `1m` - every minute, `1h` - every hour.
This check extends compaction to also calculate checksum that can be compared between cluster members.
Doesn't cause additional database scan making it very cheap, but requiring a regular compaction in cluster.

### Latest revision hash check

Enabled using `--corrupt-check-time` flag, requires providing an execution period in format: `1m` - every minute, `1h` - every hour.
Recommended period is a couple of hours due to a high performance cost.
Running a check requires computing a checksum by scanning entire etcd content at given revision.

## Restoring a corrupted member

There are three ways to restore a corrupted member:
* Purge member persistent state
* Replace member
* Restore whole cluster

After the corrupted member is restored, CORRUPT ALARM can be removed.

### Purge member persistent state

Members state can be purged by:
1. Stopping the etcd instance.
2. Backing up etcd data directory.
3. Moving out the `snap` subdirectory from the etcd data directory.
6. Starting `etcd` with `--initial-cluster-state=existing` and cluster members listed in `--initial-cluster`.

Etcd member is expected to download up-to-date snapshot from the leader.

### Replace member

Member can be replaced by:
1. Stopping the etcd instance.
2. Backing up the etcd data directory.
3. Removing the data directory.
4. Removing the member from cluster by running `etcdctl member remove`.
5. Adding it back by running `etcdctl member add`
6. Starting `etcd` with `--initial-cluster-state=existing` and cluster members listed in `--initial-cluster`.

### Restore whole cluster

Cluster can be restored by saving a snapshot from current leader and restoring it to all members.
Run `etcdctl snapshot save` against the leader and follow [restoring a cluster procedure](/docs/etcd/op-guide/recovery/).
