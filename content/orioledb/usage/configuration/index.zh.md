---
title: 配置参数
linkTitle: 配置参数
description: OrioleDB 的内存、恢复、压缩、回退与调试参数参考。
weight: 20
type: docs
search_keywords: ["OrioleDB", "configuration", "GUC", "parameters", "参数"]
upstream_link: https://www.orioledb.com/docs/usage/configuration
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-sliders
---


## 主要参数 {#main-parameters}

所有 GUC 参数都需要重启 postmaster 才能生效。

### `orioledb.main_buffers` {#orioledbmain_buffers}

|             |       |
|-------------|-------|
| **默认值** | 64 MB |

用于缓存 OrioleDB 表热点数据页的共享内存大小。该参数类似于内置的 `shared_buffers` GUC 参数。如果只使用 OrioleDB 表，建议先设置为内存的 1/4，并将 `shared_buffers` 设为默认的 `128 MB`。如果 OrioleDB 表和堆表的使用量相当，则可分别为此参数和 `shared_buffers` 分配内存的 1/8。

### `orioledb.undo_buffers` {#orioledbundo_buffers}

|             |      |
|-------------|------|
| **默认值** | 1 MB |

用于保存旧行版本和旧页版本的共享内存环形缓冲区大小。

每种撤销类型的环形缓冲区至少为 `max_procs * 2 * O_MAX_UNDO_RECORD_SIZE` 字节。因此，`max_procs` 较大时，启动时实际分配的缓冲区可能大于此 GUC 指定的大小。

### `orioledb.recovery_pool_size` {#orioledbrecovery_pool_size}

|             |     |
|-------------|-----|
| **默认值** | 3   |

基于行级 WAL 执行恢复的工作进程数。

将 `orioledb.recovery_pool_size` 与 `orioledb.recovery_idx_pool_size` 之和提高到可用 CPU 核心数的 50%～100%，可以加快集群恢复。`max_worker_processes` 必须大于两者之和，否则 OrioleDB 会在恢复时退回到单进程索引构建或单进程恢复。

### `orioledb.recovery_idx_pool_size` {#orioledbrecovery_idx_pool_size}

|             |     |
|-------------|-----|
| **默认值** | 3   |

恢复期间并行构建索引的工作进程数。

将 `orioledb.recovery_pool_size` 与 `orioledb.recovery_idx_pool_size` 之和提高到可用 CPU 核心数的 50%～100%，可以加快集群恢复。`max_worker_processes` 必须大于两者之和，否则 OrioleDB 会在恢复时退回到单进程索引构建或单进程恢复。

### `orioledb.recovery_queue_size` {#orioledbrecovery_queue_size}

|             |      |
|-------------|------|
| **默认值** | 8 MB |

恢复工作进程相关消息队列的共享内存大小。

### `orioledb.checkpoint_completion_ratio` {#orioledbcheckpoint_completion_ratio}

|             |     |
|-------------|-----|
| **默认值** | 0.5 |

OrioleDB 表的检查点时间占整个检查点时间的比例。如果只使用 OrioleDB 表，建议设为 `1.0`。

### `orioledb.serializable` {#orioledbserializable}

|             |              |
|-------------|--------------|
| **默认值** | `table_lock` |

决定 OrioleDB 如何处理客户端请求的 SERIALIZABLE 隔离级别。OrioleDB 没有实现真正的 SSI 谓词锁；此枚举参数从以下三种近似处理方式中选择一种：

- `table_lock`（默认）：对 SERIALIZABLE 事务访问的每个关系获取重量级 `ExclusiveLock`。访问同一张表的两个 SERIALIZABLE 事务通过锁管理器串行执行；SERIALIZABLE 写事务会阻塞该表上并发的非 SERIALIZABLE 写事务（`RowExclusiveLock`），但不影响非 SERIALIZABLE 读事务（`AccessShareLock`）。行为正确，但粒度较粗，互不冲突的并发工作负载也会退化为串行执行。
- `error`：以 `ERRCODE_FEATURE_NOT_SUPPORTED` 拒绝 SERIALIZABLE 事务，这是此前的行为。
- `repeatable_read`：仅对 OrioleDB 表将 SERIALIZABLE 视为 `REPEATABLE READ`，不获取额外锁，因为基于 CSN 的快照已经提供事务内稳定的读取。同一事务中的堆表仍照常使用 PostgreSQL 的 SSI。

### `orioledb.checksums_enabled` {#orioledbchecksums_enabled}

|             |     |
|-------------|-----|
| **默认值** | on  |

只读参数，显示是否启用 OrioleDB 页面校验和。无论 PostgreSQL 集群的 `data_checksums` 设置如何，OrioleDB 始终存储并验证页面校验和。

## 高级配置选项 {#advanced-config-options}

### `orioledb.free_tree_buffers` {#orioledbfree_tree_buffers}

|             |      |
|-------------|------|
| **默认值** | 8 MB |

压缩表块分配器元数据的共享内存大小。处理大型压缩表时，建议增大该值。

### `orioledb.catalog_buffers` {#orioledbcatalog_buffers}

|             |      |
|-------------|------|
| **默认值** | 8 MB |

表元数据的共享内存大小。处理大量表时，建议增大该值。

### `orioledb.temp_buffers` {#orioledbtemp_buffers}

|             |       |
|-------------|-------|
| **默认值** | 64 MB |

每个后端进程用于 OrioleDB 临时表的本地页面池大小。增大该值可以改善大型临时表的性能。这部分内存在各后端的私有内存中分配，而非共享内存；因此，内存消耗会随访问 OrioleDB 临时表的后端数量增长。

### `orioledb.system_undo_circular_buffer_fraction` {#orioledbsystem_undo_circular_buffer_fraction}

|             |     |
|-------------|-----|
| **默认值** | 0.1 |

`orioledb.undo_buffers` 中用于系统表旧行版本和旧页版本的比例。DDL 密集型工作负载建议增大该值。它替代了已弃用的 `orioledb.undo_system_buffers`，后者以绝对内存大小指定同一用途的空间。

`orioledb.undo_buffers` 中扣除 `orioledb.system_undo_circular_buffer_fraction` 与 `orioledb.regular_block_undo_circular_buffer_fraction` 之和后，剩余部分预留给普通表的行级撤销日志。

### `orioledb.regular_block_undo_circular_buffer_fraction` {#orioledbregular_block_undo_circular_buffer_fraction}

|             |      |
|-------------|------|
| **默认值** | 0.45 |

`orioledb.undo_buffers` 中用于普通表块级撤销日志的比例。

`orioledb.undo_buffers` 中扣除 `orioledb.system_undo_circular_buffer_fraction` 与 `orioledb.regular_block_undo_circular_buffer_fraction` 之和后，剩余部分预留给普通表的行级撤销日志。

### `orioledb.xid_buffers` {#orioledbxid_buffers}

|             |     |
|-------------|-----|
| **默认值** | 1MB |

OrioleDB 内存中 xid 缓冲区的大小。每 MB 可容纳约 6.5 万个对应于未结束事务的 xid 条目。如果事务速率很高，可以考虑增大该参数。

### `orioledb.bgwriter_num_workers` {#orioledbbgwriter_num_workers}

|             |     |
|-------------|-----|
| **默认值** | 1   |

在后台刷出 OrioleDB 表脏页的后台写进程数。对于 CPU 核心较多的系统，建议设置为大于 `1` 的值。

### `orioledb.max_io_concurrency` {#orioledbmax_io_concurrency}

|             |         |
|-------------|---------|
| **默认值** | 0（关闭） |

OrioleDB 并行发出的 I/O 操作数上限。当操作系统内核成为高并发 I/O 的瓶颈时，建议设置该参数。

### `orioledb.device_filename` {#orioledbdevice_filename}

|             |         |
|-------------|---------|
| **默认值** | 未设置 |

块设备模式下使用的块设备路径。

### `orioledb.device_length` {#orioledbdevice_length}

|             |      |
|-------------|------|
| **默认值** | 1 GB |

块设备的长度。

### `orioledb.use_mmap` {#orioledbuse_mmap}

|             |     |
|-------------|-----|
| **默认值** | off |

指定是否通过 `mmap` 访问块设备。对于 NVRAM，建议设为 `on`。

### `orioledb.default_compress` {#orioledbdefault_compress}

|             |                     |
|-------------|---------------------|
| **默认值** | -1（不压缩） |

表数据结构默认的块级压缩级别。

### `orioledb.default_primary_compress` {#orioledbdefault_primary_compress}

|             |                     |
|-------------|---------------------|
| **默认值** | -1（不压缩） |

表主键默认的块级压缩级别。

### `orioledb.default_toast_compress` {#orioledbdefault_toast_compress}

|             |                     |
|-------------|---------------------|
| **默认值** | -1（不压缩） |

表中 TOAST 值默认的块级压缩级别。

### `orioledb.table_description_compress` {#orioledbtable_description_compress}

|             |     |
|-------------|-----|
| **默认值** | off |

在 `orioledb_table_description` 中显示压缩列。

### `orioledb.use_sparse_files` {#orioledbuse_sparse_files}

|             |     |
|-------------|-----|
| **默认值** | off |

通过在数据文件中打洞，将写时复制释放的空间归还给文件系统。

OrioleDB 将修改后的页面写入新位置，并释放旧位置。被释放的块必须等到释放它的那次检查点完成后，才能再次使用。在这两个时点之间，块占用磁盘但不保存有效数据，因此写入密集的工作负载可能使数据文件达到实际数据量的数倍。数据文件从不截断，所以这个大小形成高水位，不会自行下降。启用此选项后，已释放的块会被打洞，空间立即归还给文件系统。

文件的*长度*不变，变化的只是文件系统为其计算的实际占用空间。启用后，`ls -l` 和 `du --apparent-size` 仍报告高水位，而 `du` 和 `df` 报告实际使用量，两者可能相差数倍。读取表观大小的监控结果会显得不准确。

需要文件系统支持打洞（`FALLOC_FL_PUNCH_HOLE`）；ext4、XFS 和 Btrfs 均支持。对于不支持的文件系统，OrioleDB 只记录一次警告，然后继续运行而不打洞。压缩表按区段而非块管理空间，因此不受此选项影响。

### `orioledb.strict_mode` {#orioledbstrict_mode}

|             |     |
|-------------|-----|
| **默认值** | off |

控制会话请求 OrioleDB 表尚不支持的功能时，OrioleDB 如何响应。设为 `off` 时，OrioleDB 发出 `WARNING`，随后回退到非并发版本或普通版本。设为 `on` 时则抛出 `ERROR`，有助于在测试和 CI 中发现意外回退。

## 基于撤销日志的回退选项（实验性） {#options-for-undo-based-rewind-experimental}

> [!WARNING]
>
> 回退是实验性功能，仅在开发构建（`IS_DEV=1`）中可用。生产构建无法开启 `orioledb.enable_rewind`。

### `orioledb.enable_rewind` {#orioledbenable_rewind}

|             |     |
|-------------|-----|
| **默认值** | off |

启用基于撤销日志的回退。

### `orioledb.rewind_max_time` {#orioledbrewind_max_time}

|             |     |
|-------------|-----|
| **默认值** | 500 |

事务相对于当前时间的最大年龄，单位为秒。超过该值后，事务条目会被标记完成并从缓冲区移除。这是回退的时间限制。

### `orioledb.rewind_max_transactions` {#orioledbrewind_max_transactions}

|             |       |
|-------------|-------|
| **默认值** | 86400 |

为回退保留的事务条目数上限。更早的事务条目会被标记完成并从缓冲区移除，因此该值限定了能够回退的最早位置。子事务也会占用回退缓冲区中的条目。

`orioledb.rewind_max_transactions` 和 `orioledb.rewind_max_time` 共同生效：事务只要超出其中任一阈值，就超出了可回退范围，无法再回退到该事务。

### `orioledb.rewind_buffers` {#orioledbrewind_buffers}

|             |     |
|-------------|-----|
| **默认值** | 1MB |

OrioleDB 内存中回退缓冲区的大小。每 MB 可容纳约 8000 个回退事务条目。如果内存充足，可将其设为接近（`orioledb.rewind_max_transactions` / 8000）MB，以避免将回退信息写入磁盘。

### `orioledb.logical_xid_buffers` {#orioledblogical_xid_buffers}

|             |       |
|-------------|-------|
| **默认值** | 512KB |

OrioleDB 内存中用于逻辑事务 ID 的缓冲区大小，这些 ID 分配给正在运行的子事务。每 MB 可容纳 800 万个运行中的子事务，因此默认值对应 400 万个子事务。

## 调试选项 {#debugging-options}

### `orioledb.debug_disable_pools_limit` {#orioledbdebug_disable_pools_limit}

|             |     |
|-------------|-----|
| **默认值** | off |

禁用 `orioledb.main_buffers`、`orioledb.free_tree_buffers` 和 `orioledb.catalog_buffers` 的最小值限制，用于调试。

### `orioledb.enable_stopevents` {#orioledbenable_stopevents}

|             |     |
|-------------|-----|
| **默认值** | off |

启用停止事件。

### `orioledb.trace_stopevents` {#orioledbtrace_stopevents}

|             |     |
|-------------|-----|
| **默认值** | off |

将所有停止事件跟踪记录到系统日志。

### `orioledb.debug_disable_bgwriter` {#orioledbdebug_disable_bgwriter}

|             |     |
|-------------|-----|
| **默认值** | off |

禁用后台写进程，用于调试。

### `orioledb.debug_checkpoint_timeout` {#orioledbdebug_checkpoint_timeout}

|             |                      |
|-------------|----------------------|
| **默认值** | `checkpoint_timeout` |

设置自动 WAL 检查点之间的最大时间间隔。将其设为小于 `checkpoint_timeout` 的值，可以使 OrioleDB 更频繁地执行检查点，以便测试。

### `orioledb.remove_old_checkpoint_files` {#orioledbremove_old_checkpoint_files}

|             |     |
|-------------|-----|
| **默认值** | on  |

检查点完成后删除临时的 \*.tmp 和 \*.map 文件。

### `orioledb.skip_unmodified_trees` {#orioledbskip_unmodified_trees}

|             |     |
|-------------|-----|
| **默认值** | on  |

检查点过程中跳过未修改树的读取。

### `orioledb.debug_max_bridge_ctid_blkno` {#orioledbdebug_max_bridge_ctid_blkno}

|             |     |
|-------------|-----|
| **默认值** | NA  |

设置桥接 ctid 的最大值，用于溢出测试。

### `orioledb.debug_disable_downlink_fastpath` {#orioledbdebug_disable_downlink_fastpath}

|             |     |
|-------------|-----|
| **默认值** | off |

禁用快速路径下行指针查找。启用后，`find_page()` 逐层向下查找，而不直接跳到缓存的下行指针。适用于需要 hikey 或下行指针停止事件的测试。

### `orioledb.replay_until_lsn` {#orioledbreplay_until_lsn}

|             |     |
|-------------|-----|
| **默认值** | NA  |

指定截止 LSN；恢复时 WAL 读取位置达到该 LSN 后，OrioleDB 会永久停止应用自己的 WAL 记录。`replay_until_lsn` 不得早于最近一次已完成 OrioleDB 检查点的 LSN。如果指定的值更早，则不会生效，并会在下次启动时记录警告。

> [!WARNING]
>
> 这是最后手段式的灾难恢复机制，性质与 `pg_resetwal` 完全相当。它会有意造成分裂状态：PostgreSQL 核心系统目录和标准堆表继续重放 WAL，而 OrioleDB 表停留在指定的 LSN。

[实验性 S3 模式的其他 GUC 参数](/zh/orioledb/usage/decoupled-storage/)
