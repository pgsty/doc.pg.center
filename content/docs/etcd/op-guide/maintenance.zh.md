---
title: 维护
weight: 4450
description: 周期性集群维护指南
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/maintenance.md"
aliases: [/etcd/op-guide/maintenance/]
---

## 概述 {#overview}

etcd 集群需要定期维护以保持可靠性。根据 etcd 应用的需求，此类维护通常可以自动化执行，且无需停机或显著降低性能。

本文所述的 etcd 维护操作均用于管理 etcd 键空间所占用的存储资源。若未能充分控制键空间大小，系统将通过存储空间配额进行防护；当 etcd 成员可用空间不足时，配额将触发集群范围的告警，使系统进入受限操作的维护模式。为避免键空间写入空间耗尽，必须对 etcd 键空间历史数据执行压缩。存储空间本身可通过整理碎片来回收。此外，定期对 etcd 成员状态进行快照备份，可实现对因操作失误导致的意外逻辑数据丢失或数据损坏的恢复。

## Raft 日志保留 {#raft-log-retention}

`etcd --snapshot-count` 配置在执行压缩前需在内存中保留的已应用 Raft 条目数量。当 `--snapshot-count` 达到时，服务器会先将快照数据持久化到磁盘，然后截断旧的条目。当慢速跟随者请求的日志索引早于已压缩的索引时，领导者会发送快照，强制跟随者覆盖其状态。

较高的 `--snapshot-count` 会在生成快照前将更多 Raft 条目保留在内存中，从而导致 [内存使用量持续较高](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156)。由于领导者会更长时间保留最新的 Raft 条目，缓慢的跟随者有更多时间在领导者生成快照前完成追赶。`--snapshot-count` 是较高内存使用与缓慢跟随者更高可用性之间的权衡。

自 v3.2 起，`--snapshot-count` 的默认值已 [从 10,000 改为 100,000](https://github.com/etcd-io/etcd/pull/7160)。

从性能角度而言，`--snapshot-count` 超过 100,000 可能会影响写入吞吐量。内存中对象数量过多会减慢 [Go GC 标记阶段 `runtime.scanobject`](https://golang.org/src/runtime/mgc.go)，且内存回收不频繁会导致分配变慢。性能表现因工作负载和系统环境而异。然而，通常情况下，压缩过于频繁会影响集群可用性及写入吞吐量；压缩过于稀疏同样有害，会向 Go 垃圾回收器施加过大压力。更多研究结果请参见 [Understanding Performance Aspects of etcd and Raft](https://www.slideshare.net/mitakeh/understanding-performance-aspects-of-etcd-and-raft)。

## 历史压缩：v3 API 键值数据库 {#history-compaction-v3-api-key-value-database}

由于 etcd 会保留键空间的完整历史记录，因此应定期执行压缩以避免性能下降及最终存储空间耗尽。执行压缩操作会丢弃指定键空间修订版本之前所有被覆盖键的相关信息。这些键所占用的空间随后将可用于键空间的额外写入操作。

键空间可通过 `etcd` 的时间窗口历史保留策略自动执行压缩，或通过 `etcdctl` 手动执行压缩。`etcdctl` 方法可对压缩过程提供细粒度控制，而自动压缩适用于仅需保留一段时间键历史的应用场景。

`etcdctl` 执行压缩的过程如下：

```sh
# compact up to revision 3
$ etcdctl compact 3
```

执行压缩后的修订版本之前的所有修订版本将变得不可访问：

```sh
$ etcdctl get --rev=2 somekey
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

### 自动压缩 {#auto-compaction}

`etcd` 可通过设置 `--auto-compaction-mode` 和 `--auto-compaction-retention` 选项自动对键空间执行压缩。压缩模式有两种：`periodic`（默认）和 `revision`。

#### 周期性压缩 {#periodic-compaction}

周期性压缩保留基于时间的键空间历史窗口：

```sh
# keep one hour of history
$ etcd --auto-compaction-retention=1h
```

保留值指定要保留的历史记录量。一条记录在创建后约经过该时长才会被压缩。这确保了慢速监听器仍能在保留窗口内完成追赶。

当保留周期大于 1 小时时，etcd 每小时执行一次压缩，同时保持完整的保留窗口。当保留周期为 1 小时或更短时，etcd 按保留周期间隔执行压缩。

例如，使用 `--auto-compaction-retention=10h` 时，etcd 首次压缩前等待 10 小时，之后每隔一小时执行一次压缩：

```text
0hr  (rev = 1)
1hr  (rev = 10)
...
8hr  (rev = 80)
9hr  (rev = 90)
10hr (rev = 100, Compact(1))
11hr (rev = 110, Compact(10))
...
```

推荐值取决于具体使用场景：

- 对同一键频繁更新：较短周期，例如 `1h` 或 `30m`
- 更新频率较低：较长周期，例如 `24h`、`48h` 或 `72h`
- 通用默认值：`10h`

#### 修订版本压缩 {#revision-compaction}

修订版本压缩保留固定数量的修订版本：

```sh
# keep 1000 revisions
$ etcd --auto-compaction-mode=revision --auto-compaction-retention=1000
```

etcd 每 5 分钟检查一次，并对 `"latest revision" - 1000` 执行压缩。例如，当最新修订版本为 30000 时，它将对修订版本 29000 执行压缩。

## 碎片整理 {#defragmentation}

执行键空间压缩后，后端数据库可能会出现内部碎片。内部碎片是指后端数据库中虽已空闲但仍在占用存储空间的区域。压缩旧版修订版本会通过在后端数据库中留下空隙，导致 `etcd` 出现内部碎片。这些碎片空间可供 `etcd` 使用，但对主机文件系统不可用。换句话说，删除应用数据不会释放磁盘空间。

碎片整理过程会将这部分存储空间释放回文件系统。碎片整理按成员分别执行，以避免引发集群范围内的延迟峰值。

要整理 etcd 成员的碎片，请使用 `etcdctl defrag` 命令：

```sh
$ etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
```

> [!WARNING]
> 请注意，对运行中的成员执行碎片整理会阻塞系统读写数据，直至其状态重建完成

> [!WARNING]
> 请注意，碎片整理请求不会在集群中复制。也就是说，该请求仅应用于本地节点。请在 `--endpoints` 标志或 `--cluster` 标志中指定所有成员，以自动发现集群中的所有成员。

对与默认端点关联的集群中的所有端点执行碎片整理操作：

```bash
$ etcdctl defrag --cluster
Finished defragmenting etcd member[http://127.0.0.1:2379]
Finished defragmenting etcd member[http://127.0.0.1:22379]
Finished defragmenting etcd member[http://127.0.0.1:32379]
```

要直接对 etcd 数据目录进行碎片整理，且 etcd 未运行时，请使用以下命令：

```sh
etcdutl defrag --data-dir <path-to-etcd-data-dir>
```

## 空间配额 {#space-quota}

`etcd` 中的存储配额确保集群以可靠方式运行。若无存储配额，当键空间过度增长时，`etcd` 可能出现性能下降，或直接耗尽存储空间，导致集群行为不可预测。若任一成员的键空间后端数据库超过存储配额，`etcd` 将触发集群级告警，使集群进入仅接受键读取和删除操作的维护模式。只有在键空间中释放足够空间、完成后端数据库碎片整理，并清除存储配额告警后，集群方可恢复常规运行。

默认情况下，`etcd` 设置了一个适用于大多数应用的保守空间配额，但可通过命令行以字节为单位进行配置：

```sh
# set a very small 16 MiB quota
$ etcd --quota-backend-bytes=$((16*1024*1024))
```

空间配额可由循环触发：

```sh
# fill keyspace
$ while [ 1 ]; do dd if=/dev/urandom bs=1024 count=1024  | ETCDCTL_API=3 etcdctl put key  || break; done
...
Error:  rpc error: code = 8 desc = etcdserver: mvcc: database space exceeded
# confirm quota space is exceeded
$ ETCDCTL_API=3 etcdctl --write-out=table endpoint status
+----------------+------------------+-----------+---------+-----------+-----------+------------+
|    ENDPOINT    |        ID        |  VERSION  | DB SIZE | IS LEADER | RAFT TERM | RAFT INDEX |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
| 127.0.0.1:2379 | bf9071f4639c75cc | 2.3.0+git | 18 MB   | true      |         2 |       3332 |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
# confirm alarm is raised
$ ETCDCTL_API=3 etcdctl alarm list
memberID:13803658152347727308 alarm:NOSPACE
```

删除过多的键空间数据并整理后端数据库，可使集群恢复至配额限制范围内：

```sh
# get current revision
$ rev=$(ETCDCTL_API=3 etcdctl --endpoints=:2379 endpoint status --write-out="json" | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')
# compact away all old revisions
$ ETCDCTL_API=3 etcdctl compact $rev
compacted revision 1516
# defragment away excessive space
$ ETCDCTL_API=3 etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
# disarm alarm
$ ETCDCTL_API=3 etcdctl alarm disarm
memberID:13803658152347727308 alarm:NOSPACE
# test puts are allowed again
$ ETCDCTL_API=3 etcdctl put newkey 123
OK
```

指标 `etcd_mvcc_db_total_size_in_use_in_bytes` 表示执行历史压缩后的实际数据库使用量，而 `etcd_debugging_mvcc_db_total_size_in_bytes` 显示包含待整理碎片的空闲空间在内的数据库大小。后者仅在前者接近其值时增加，这意味着当这两个指标均接近配额时，必须执行历史压缩以避免触发空间配额限制。

`etcd_debugging_mvcc_db_total_size_in_bytes` 从 v3.4 版本起重命名为 `etcd_mvcc_db_total_size_in_bytes`。

> [!WARNING]
> 对于 Put/Txn/LeaseGrant 请求，可能会收到 `ErrGRPCNoSpace` 错误，但写入请求仍可能在后端数据库中成功，因为 etcd 在 API 层和内部 Apply 层均检查空间配额，而 Apply 层仅会触发 `NOSPACE` 告警，不会阻塞事务的继续执行。

## 快照备份 {#snapshot-backup}

定期对 `etcd` 集群进行快照，可为 etcd 键空间提供持久化备份。通过定期对 etcd 成员的后端数据库进行快照，`etcd` 集群可恢复至某个时间点且状态已知良好的状态。

使用 `etcdctl` 执行快照操作：

```sh
$ etcdctl snapshot save backup.db
$ etcdutl --write-out=table snapshot status backup.db
+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| fe01cf57 |       10 |          7 | 2.1 MB     |
+----------+----------+------------+------------+
```
