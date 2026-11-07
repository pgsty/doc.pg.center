---
title: 并发创建索引
linkTitle: 并发索引
description: OrioleDB 原生 B 树并发构建的状态、变更暂存、恢复和限制。
weight: 80
type: docs
search_keywords: ["OrioleDB", "concurrent index", "CREATE INDEX CONCURRENTLY", "并发索引"]
upstream_link: https://www.orioledb.com/docs/architecture/concurrent-index
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-list
---


OrioleDB 在 PostgreSQL 现有的 `DefineIndex(concurrent=true)` 多阶段编排之上实现 `CREATE INDEX CONCURRENTLY`（CIC）。本页说明两层如何协作、磁盘产物的结构，以及安全性保证。

目前有两条路径：

- **原生 B 树**：`USING orioledb`，或者在未启用 `index_bridging` 的表上使用 `USING btree`，且没有 `WITH(orioledb_index=false)`。采用下文的 BUILDING 状态与暂存机制，支持 UNIQUE。
- **桥接索引**：任意非 B 树访问方法、带 `WITH(orioledb_index=false)` 的 B 树，或启用了 `index_bridging` 的表上的 B 树。它是以 `bridge_ctid` 为键的标准 PostgreSQL 索引，ambuild 进入 `bridged_ambuild` / `btbuild`。非唯一 CIC 使用 PostgreSQL 机制，没有 OrioleDB 专有的 BUILDING 状态或暂存文件。唯一 CIC 会降级为普通构建，或在严格模式下被拒绝，因为 `orioledb_index_validate_scan` 尚不能补齐桥接路径第 2 阶段构建期间提交的行。

本页其余部分介绍原生 B 树路径。

## 为什么 OrioleDB 的 CIC 不同 {#why-cic-is-different-in-orioledb}

堆访问方法的 CIC 能够工作，是因为 `heap_update` / `heap_insert` 会对 `pg_index` 中所有 `indisready=true` 的条目调用 `index_insert`，无论构建是否完成。并发写入者会在批量装载的同时维护新索引。

OrioleDB 将二级索引成员信息存储在自己的系统树 `SYS_TREES_O_INDICES` 中，而不是 `pg_index`。写入者的 `o_tbl_index_insert` 遍历 `OTableDescr` 中的 `OIndex` 列表。如果只是放开 PostgreSQL 的限制，而没有额外机制，构建快照期间的写入者会看不到二级索引，只写主键树，导致构建提交时二级索引更新悄然丢失。

因此，CIC 必须在构建开始**之前**让写入者看到正在构建的索引，使其将修改写入构建者稍后可以排空的旁路。这条旁路就是每个后端自己的**暂存文件（spool）**。

## 索引生命周期：`OIndexState` {#index-lifecycle-oindexstate}

`OIndex` 系统树记录新增一列，保存索引生命周期状态。下文使用两个术语：写入者将变更追加到 CIC 暂存文件而非直接写入索引，称为**捕获**；**追赶模式**指未来版本若要基于持续变化的快照而非固定快照构建索引，所需要的协议。该模式必须在扫描尚未结束时将写入者切换到索引，下列未使用状态也据此命名。

``` c
typedef enum
{
    OINDEX_STATE_VALID = 0,         /* fully built, all readers/writers OK */
    OINDEX_STATE_BUILDING_PHASE_1,  /* not reached: catchup mode opens capture */
    OINDEX_STATE_BUILDING_PHASE_2,  /* build pending, writers capture to spool */
    OINDEX_STATE_BUILDING_PHASE_3,  /* not reached: catchup mode writes direct */
    OINDEX_STATE_BUILDING_PHASE_4   /* not reached: catchup mode drain barrier */
} OIndexState;
```

本版本代码只会进入 `VALID` 和 `BUILDING_PHASE_2`。另外三个状态预先定义，是因为状态会持久化到系统树记录中：以后新增的值虽然新二进制文件能读，旧二进制文件却无法识别；预先保留一个暂未使用的值没有成本，还能保持编号稳定。这些名称对应未来追赶模式所需的阶段：`PHASE_1` 在扫描前开启捕获，`PHASE_3` 在扫描结束后让写入者直接维护索引，`PHASE_4` 用于最终排空屏障。

`serialize_o_index` 将 `OIndex.state` 保存为末尾的单个字节。CIC 之前的版本写出的记录会反序列化为 `OINDEX_STATE_VALID`，因此无需显式迁移即可兼容旧目录数据。

填充描述符时，`o_index_fill_descr` 会将状态同步到每个 `OIndexDescr`，同时保存 `OIndexDescr.builderOxid`，即 CIC 会话的 `createOxid`。捕获钩子用它在 DML 热路径中定位暂存目录。

其他后端通过 OIndex 系统树默认使用的**进行中快照**（`o_non_deleted_snapshot`，CSN 类别为 `INPROGRESS`）看到进行中的状态变化。跨后端可见性并不严格依赖 SI 失效通知，因为系统树读取会获取最新的已提交版本。

## 每个后端的暂存文件 {#per-backend-spool}

每个访问正在执行 CIC 的表中行的后端，都会向自己的文件追加捕获条目：

```
orioledb_data/cic_<datoid>_<reloid>_<builderOxid>/spool_<backendid>.bin
```

每次 CIC 的目录由 `cic_spool_ensure_dir` 在第 1 阶段开始时创建一次。各后端在首次追加时延迟打开自己的 `spool_<backendid>.bin`，并保留文件描述符直到退出或调用 `cic_spool_close_local`。无需后端间协调：每个后端写私有文件，由构建者合并。

每条暂存记录包含：

| 字段 | 用途 |
|----|----|
| `undoPosition` | 生成该条目的 `UndoLogRegular` 位置 |
| `fileSeq` | 文件内单调递增计数器，undoPos 相同时用于排序 |
| `opType` | `INSERT` / `DELETE` / `REVERSE_INSERT` / `REVERSE_DELETE` |
| `keyFormatFlags` | 重建键字节所需的 `OTuple` 标志 |
| `tupleFormatFlags` | 重建元组字节所需的 `OTuple` 标志 |
| `keyLength` | 后续键载荷的长度 |
| `tupleLength` | 后续叶子元组载荷的长度 |

这些条目**不写 WAL，也不能从崩溃中恢复**。如果 CIC 未完成，重做时外层事务中止会回滚未建成的 `OIndex`，暂存目录则不再可达，详见下文[崩溃清理](#crash-cleanup)。

### 正确处理子事务的 REVERSE 操作 {#subxact-correct-reverse-op-emission}

写入者的事务或子事务中止时，必须补偿此前捕获的 INSERT/DELETE：REVERSE_INSERT 抵消先前的 INSERT，REVERSE_DELETE 抵消先前的 DELETE。

这通过现有的 `UndoLogRegular` 机制实现。`cic_spool_track_for_abort` 压入一个 `CICCaptureUndoItemType` 条目，内含正向操作的字节。`apply_undo_stack` 回退事务或子事务时，调用 `cic_capture_undo_callback`，追加操作类型反转的 REVERSE 补偿条目。由于 `apply_undo_stack` 已按子事务分段，因此自然具备正确的子事务语义。

### K 路归并重放 {#k-way-merge-replay}

排空时，`cic_spool_open_reader` 打开 CIC 目录中的所有 `spool_<n>.bin`，将各文件作为按 `(undoPosition, fileSeq)` 排序的二叉堆中的输入流。`cic_spool_replay_into` 遍历归并后的流，通过宽容的回调将每条记录应用到新索引：

- 键处已有存活元组：回调返回 `DoNothing`，不执行操作。
- 键处已有删除元组：回调返回 `Update`，原地替换。
- 键处没有元组：`o_btree_modify_insert_update` 写入新元组。

此过程在 `AccessExclusiveLock` 下执行，因此排空期间并发写入会被阻塞。

## 阶段编排 {#phase-orchestration}

PostgreSQL 与 OrioleDB 共同参与跨多个事务的流程：

```
PG phase 1: index_create (indisready=false, indislive=true), commit
PG WaitForLockers (phase-1):
   waits for xacts started before the new pg_index row was visible

PG phase 2: ambuild  ─────────────────►  orioledb_ambuild
                                          - cic_spool_ensure_dir
                                          - set o_index_initial_state_override
                                            = BUILDING_PHASE_2
                                          - take ShareLock on heap
                                          - o_define_index(skip_build=true)
                                          - reset override
                                          - o_invalidate_oids(tbl)
                                          - o_invalidate_oids(idx)
                                          - CacheInvalidateRelcacheByRelid
            commit (sets indisready=true)

PG WaitForLockers (phase-2):
   waits for xacts that did not yet see indisready=true

PG phase 3: validate_index ──────────► orioledb_index_validate_scan
                                       ─► o_define_index_concurrent_finish
                                          - recreate_table_descr_by_oids
                                          - build_secondary_index
                                            (uses PG's fresh phase-3 snapshot;
                                             concurrent DML continues to spool)
                                          - LockRelationOid(AccessExclusiveLock)
                                          - cic_spool_replay_into (drain)
                                          - covering scan (re-insert all
                                            primary rows; no-op on collision)
                                          - o_indices_set_state(VALID)
                                          - emit WAL_REC_CIC_INDEX_VALID
                                          - cic_spool_drop_dir
            commit (releases AccessExclusiveLock)

PG WaitForLockers (phase-3)
PG sets indisvalid=true
```

### 为什么必须这样切换锁 {#why-the-lock-dance-matters}

实现必须封闭两个跨后端竞争窗口。

1. **第 1 阶段的 ambuild 边界。** ambuild 提交的新 `OIndex` 状态为 `BUILDING_PHASE_2`。如果更新 OTable 时不获取 `ShareLock`，正在执行长 INSERT 的写入者可能在运行 `AcceptInvalidationMessages` 之前就结束，从而完全绕过新索引。`ShareLock` 与所有 DML 持有的 `RowExclusive` 冲突，因此写入者的下一条语句会在这里阻塞；等 ambuild 事务提交、释放锁时，SI 失效通知已全局可见。

2. **第 3 阶段切换。** 排空、补漏扫描、状态翻转和暂存目录删除都在 `AccessExclusiveLock` 下进行。否则，SI 失效通知后正在刷新缓存 `OTableDescr` 的写入者，可能越过状态切换继续写暂存记录，随后这些记录与目录一起被删除。锁仅覆盖排空、补漏、翻转和删目录这一短暂窗口，提交时释放。

### 补漏扫描 {#covering-scan}

`build_secondary_index` 有意在获取 `AccessExclusiveLock` **之前**运行，这正是“并发”构建的意义。因此，在批量装载的主键顺序扫描之后、二级树排序与写入完成之前，写入者可能提交一行只存在于主键树中的数据，导致二级索引缺行。

为弥补这一缺口，获取 `AccessExclusiveLock` 并排空暂存文件后，`o_define_index_concurrent_finish` 在锁内重新扫描主键树，通过宽容回调将每个可见行插入二级索引。批量装载已写入的行不做任何操作，遗漏行则补入。

### 在捕获热路径上重读系统树状态 {#sys-tree-state-re-read-on-the-capture-hot-path}

还有一个细微竞争：写入者的 `o_tbl_index_insert` 从描述符缓存读取 `id->state`。状态已翻转并提交、但 SI 消息尚未到达该后端的短暂窗口内，缓存仍可能显示 BUILDING，而磁盘状态已经是 VALID，暂存目录也已删除。此时追加暂存数据，会把行写进已经孤立的 inode，再也没有排空过程读取它。

修复方式是：缓存状态不为 VALID 时，在进入暂存分支之前，先从系统树重读 OIndex 状态，这只是一次成本很低的进行中快照查找。如果最新状态为 VALID，就继续执行普通索引写入。

## 备库重放 {#standby-replay}

索引对读者可见时，CIC 会写一条用于可观测性的阶段 WAL 记录 `WAL_REC_CIC_INDEX_VALID`，其重做处理器不执行操作。`WAL_REC_CIC_WRITERS_DIRECT` 和 `WAL_REC_CIC_DRAIN_BARRIER` 也已定义，但从不写出。与未使用的 `OIndexState` 一样，它们只是为追赶模式预留编号，避免以后新增记录编号导致旧二进制文件无法识别。

所有修改数据的操作都通过 OrioleDB 标准 WAL 通道完成：

- `o_tables_update`（目录）重放 OTable 变化。
- `o_indices` 的 set_state 通过通用系统树更新路径重放 BUILDING → VALID。
- `build_secondary_index` 的批量装载写入经过普通页面 WAL。
- 排空时每行的 `o_btree_modify` 调用经过普通页面 WAL。

因此，备库无需阶段记录专有的重做逻辑也能收敛。`test/t/concurrent_index_test.py` 中的 `test_cic_streaming_replica` 验证了这一点。

## 崩溃清理 {#crash-cleanup}

如果在 OIndex 切换为 VALID 之前崩溃，CIC 会留下：

1. 未建成的 `OIndex` 系统树记录，WAL 重做时由外层事务中止回滚。
2. 装满暂存文件的 `cic_<datoid>_<reloid>_<oxid>/` 目录。它不写 WAL，重做无法回滚它。

`cic_spool_cleanup_orphans()` 扫描 `orioledb_data/` 中所有 `cic_*` 条目并删除。它在 WAL 恢复结束时，由 OrioleDB 资源管理器的 `rm_cleanup` 回调执行，紧接现有恢复收尾工作。

## 测试 {#tests}

`test/t/concurrent_index_test.py` 覆盖：

- `test_cic_basic`：无并发 DML 的最小正常路径。
- `test_cic_unique_native`：无重复值的原生 UNIQUE CIC。
- `test_cic_unique_native_rejects_existing_dup`：tuplesort 的 enforceUnique 检出快照中的重复值。
- `test_cic_unique_native_rejects_concurrent_dup`：两个并发写入者插入不同主键、相同二级值，排空后的唯一字段遍历检出重复。
- `test_cic_bridged_gin`：经 PostgreSQL 机制执行桥接 GIN CIC。
- `test_cic_bridged_unique_btree`：安全降级桥接 UNIQUE CIC。
- `test_cic_bridged_unique_concurrent_insert`：构建过程中暂停的写入者不会导致完成后的唯一索引缺行。
- `test_cic_concurrent_writes`：构建期间写线程运行，排空暂存后索引完整。
- `test_cic_writer_spans_all_phases`：写入者以小事务跨越所有阶段，最终 `pk_cnt` 必须等于 `idx_cnt`。
- `test_cic_streaming_replica`：主库 CIC 完成后，备库收敛。
- `test_cic_streaming_replica_failing_expr`：某行的索引表达式出错时，副本仍能追上，而不会卡住。
- `test_cic_crash_orphan_cleanup`：SIGKILL 引发 WAL 恢复后，`rm_cleanup` 删除预先放置的 `cic_*/spool_*.bin`。

## 限制 {#limitations}

- 桥接 UNIQUE CIC 默认降级为普通 `CREATE UNIQUE INDEX`；启用 `orioledb.strict_mode` 时则拒绝执行。并发实现还需要在桥接路径第 3 阶段遍历主键树，完成等价于 PostgreSQL 堆验证扫描的工作。

- 目前不支持在构建窗口内由*同一个*事务创建并消除重复值的 **DEFERRABLE INITIALLY DEFERRED UNIQUE** 模式。暂存会重放每个事件，`INSERT v1; INSERT v1; DELETE v1` 形成三条记录；排空时两个 INSERT 被写到不同叶子键上，因为 val + PK 不同，排空后的唯一字段遍历会在等价 DELETE 生效前看到两者。上游 PostgreSQL CIC 也不支持这种模式：它在第 2 阶段后设置 `indisready=true`，因此即使约束可延迟，写入者自己的下一次 INSERT 也会立即报错。

- `BUILDING_PHASE_1/3/4` 为未来追赶模式预留，目前只使用 `VALID` 和 `BUILDING_PHASE_2`，参见[索引生命周期](#index-lifecycle-oindexstate)。

- 对 OrioleDB 表的主键索引执行 `REINDEX CONCURRENTLY` 会报错：

  ```
  ERROR:  cannot REINDEX CONCURRENTLY primary index "<name>" on an orioledb table
  ```

  原因是主键索引*就是*表本身；并发重建意味着重写每一行，而不是在旁边构建二级结构。`REINDEX TABLE CONCURRENTLY` 会跳过主键，只重建二级索引。

- 阶段转换 WAL 记录用于可观测性，重做端不处理。未来版本可能用它们驱动备库追赶模式的切换。
