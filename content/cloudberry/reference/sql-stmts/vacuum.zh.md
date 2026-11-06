---
title: "VACUUM"
description: "回收数据库中的垃圾空间，并可选地进行分析。"
weight: 1790
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/vacuum.md"
---

## 语法概要 {#synopsis}

```sql
VACUUM [({ FULL | FREEZE | VERBOSE | ANALYZE | DISABLE_PAGE_SKIPPING | SKIP_LOCKED | INDEX_CLEANUP } [, ...])] [<table> [(<column> [, ...] )]]
        
VACUUM [FULL] [FREEZE] [VERBOSE] [<table>]

VACUUM [FULL] [FREEZE] [VERBOSE] ANALYZE
              [<table> [(<column> [, ...] )]]

VACUUM AO_AUX_ONLY <ao_table>
```

## 说明 {#description}

`VACUUM` 回收已删除元组占用的存储空间。在 Apache Cloudberry 的正常运行过程中，已删除或因更新而过时的元组不会从表中物理移除；在执行 `VACUUM` 之前，它们仍然保留在磁盘上。因此，必须定期执行 `VACUUM`，尤其是对频繁更新的表。

不带参数时，`VACUUM` 处理当前数据库中的每个表。带参数时，`VACUUM` 只处理指定表。

`VACUUM ANALYZE` 对每个选定表先执行 `VACUUM`，再执行 `ANALYZE`。这种组合形式很适合日常维护脚本。有关其处理过程的更多详情，请参阅 [ANALYZE](/cloudberry/reference/sql-stmts/analyze/)。

`VACUUM`（不带 `FULL`）会将表和索引中已删除或过时的数据标记为可供将来重用，并且只有在空间位于表末尾且容易获得表的排他锁时，才会回收空间供重用。表开头或中间的未用空间保持原样。对于堆表，此形式不会获取排他锁，因此可以与表的正常读写并行执行。不过，多余空间在大多数情况下不会返还给操作系统，只会保留以供同一表重用。`VACUUM FULL` 将表的全部内容重写到一个没有多余空间的新磁盘文件中，从而将未用空间返还给操作系统。此形式慢得多，并且在处理每个表时需要持有该表的排他锁。

对于 AO 表，`VACUUM` 首先清理索引，然后依次压实各个 段文件，最后清理辅助关系并更新统计信息，从而压实表。在每个 Segment 上，将当前 段文件中的可见行复制到新的 段文件，然后安排删除当前文件，并使新文件可用。对 AO 表执行普通 `VACUUM` 时，在压实 段文件期间仍允许对表进行扫描、插入、删除和更新。不过，在删除当前 段文件并启用新文件时，会短暂获取 Access Exclusive 锁。

`VACUUM FULL` 会执行更深入的处理，包括跨块移动元组，尽量将表压实到最少的磁盘块数。此形式慢得多，并且在处理每个表时需要持有该表的 Access Exclusive 锁。Access Exclusive 锁保证持锁者是唯一以任何方式访问该表的事务。

选项列表用括号括起时，选项可以按任意顺序书写。不使用括号时，必须严格按上面显示的顺序指定选项。带括号的语法是在 Apache Cloudberry 6.0 中加入的；不带括号的语法已弃用。

> **重要**：有关 `VACUUM`、`VACUUM FULL` 和 `VACUUM ANALYZE` 的用法，请参阅[注意事项](#notes)。

**输出**

指定 `VERBOSE` 时，`VACUUM` 会输出进度消息，指出当前正在处理的表，同时打印表的各种统计信息。

## 参数 {#parameters}

**`FULL`**

选择完整清理，这可能回收更多空间，但耗时明显更长，并会排他锁定表。此方法还需要额外磁盘空间，因为它会写入表的新副本，直到操作完成后才释放旧副本。通常只应在需要从表内回收大量空间时使用。

**`FREEZE`**

指定 `FREEZE` 相当于将服务器配置参数 `vacuum_freeze_min_age` 设为零后执行 `VACUUM`。有关 `vacuum_freeze_min_age` 的信息，请参阅“服务器配置参数”。

**`VERBOSE`**

为每个表打印详细的清理活动报告。

**`ANALYZE`**

更新优化器使用的统计信息，以确定运行查询的最有效方法。

**`DISABLE_PAGE_SKIPPING`**

通常，`VACUUM` 根据可见性映射跳过页面。它始终跳过已知所有元组均已冻结的页面；除积极清理之外，还会跳过已知所有元组对所有事务均可见的页面。此外，除积极清理之外，它还会跳过一些页面，以免等待其他会话结束使用这些页面。此选项禁止所有跳过页面的行为。只有怀疑可见性映射的内容有问题时才应使用此选项，而这通常只有在硬件或软件问题导致数据库损坏时才会发生。

**`SKIP_LOCKED`**

指定 `VACUUM` 开始处理关系时不等待任何冲突锁释放：如果无法立即、不经等待地锁定关系，就跳过该关系。注意，即使使用此选项，`VACUUM` 在打开关系的索引时仍可能阻塞。另外，`VACUUM ANALYZE` 在从分区、继承子表和某些类型的外表获取采样行时也可能阻塞。此外，`VACUUM` 通常会处理指定分区表的所有分区，但使用此选项时，如果分区表上存在冲突锁，`VACUUM` 会跳过所有分区。

**`INDEX_CLEANUP`**

指定 `VACUUM` 应尝试移除指向死亡元组的索引项。这通常是期望的行为，也是默认行为，除非对执行 `VACUUM` 的表将 `vacuum_index_cleanup` 设为 `false` 来覆盖它。当需要尽可能加快清理速度时，例如为了避免即将发生的事务 ID 回卷，将此选项设为 `false` 可能有用。但如果不定期清理索引，性能可能下降，因为随着表被修改，索引会积累死亡元组，表本身也会积累死亡行指针，而这些行指针只能在索引清理完成后移除。此选项对没有索引的表没有作用。使用 `FULL` 选项时，将忽略 `INDEX_CLEANUP` 选项。

**`AO_AUX_ONLY`**

对 AO 表的所有辅助表执行 `VACUUM`，不对 AO 表本身执行 `VACUUM`。如果对没有任何子分区的非 AO 表运行，则不执行任何操作。如果对具有 AO 分区的堆表运行，则清理该分区的辅助表。

**`<ao_table>`**

要清理其辅助表的表名，通常应为 AO 表。

**`<table>`**

要清理的特定表的名称（可用模式限定）。默认处理当前数据库中的所有表。

**`<column>`**

要分析的特定列的名称。默认为所有列。指定列列表就隐含启用 `ANALYZE`。

## 注意事项 {#notes}

`VACUUM` 不能在事务块内运行。

应频繁清理活跃数据库（至少每晚一次），以移除过时的行。添加或删除大量行之后，对受影响的表运行 `VACUUM ANALYZE` 命令可能有益。这会将所有近期变更的结果更新到系统目录中，使 Apache Cloudberry 查询优化器能在制定查询计划时作出更好的选择。

> **重要** PostgreSQL 有一个可选的独立服务器进程，称为 *autovacuum 守护进程*，用于自动执行 `VACUUM` 和 `ANALYZE` 命令。Apache Cloudberry 启用 autovacuum 守护进程，但只允许它对 Apache Cloudberry 模板数据库 `template0` 执行 `VACUUM` 操作。为 `template0` 启用 autovacuum 是因为不允许连接到 `template0`。autovacuum 守护进程对 `template0` 执行 `VACUUM` 操作，以管理事务 ID（XID），帮助避免 `template0` 中的事务 ID 回卷问题。

必须对用户定义的数据库手动执行 `VACUUM` 操作，以管理这些数据库中的事务 ID（XID）。

`VACUUM` 会大幅增加 I/O 流量，可能导致其他活跃会话的性能下降。因此，建议在数据库使用量较低时进行清理。

`VACUUM` 命令会跳过外部表和外表。

`VACUUM FULL` 会回收所有过时行的空间，但它需要在处理每个表时持有排他锁，成本很高，对于大型分布式 Apache Cloudberry 表可能需要很长时间才能完成。应在数据库维护时段执行 `VACUUM FULL` 操作。

不建议在日常维护中使用 `FULL` 选项，但它在特殊情况下可能有用。例如，已经删除或更新了表中大多数行，并希望表在物理上缩小，以减少磁盘占用并加快表扫描。`VACUUM FULL` 通常比普通 `VACUUM` 更能缩小表。

作为 `VACUUM FULL` 的替代方法，可以使用 `CREATE TABLE AS` 语句重新创建表，然后删除旧表。

对于 AO 表，`VACUUM` 需要足够的可用磁盘空间，以便在 `VACUUM` 期间容纳新的 段文件。如果某个 段文件中隐藏行占总行数的比例低于阈值（默认为 10），就不会压实该文件。可以通过服务器配置参数 `gp_appendonly_compaction_threshold` 配置此阈值。`VACUUM FULL` 忽略阈值，无论比例多少都会重写 段文件。可以使用服务器配置参数 `gp_appendonly_compaction` 禁用 AO 表的 `VACUUM`。有关这些服务器配置参数的信息，请参阅“服务器配置参数”。

如果在清理 AO 表时检测到并发的可串行化事务，则不会压实当前及后续 段文件。如果某个 段文件已经压实，但在删除原文件的事务中检测到并发的可串行化事务，则会跳过删除。这可能导致清理完成后仍有一两个 段文件处于“等待删除”状态。

## 示例 {#examples}

清理单个表 `onek`，为优化器分析该表，并打印详细的清理活动报告：

```sql
VACUUM (VERBOSE, ANALYZE) onek;
```

清理当前数据库中的所有表：

```sql
VACUUM;
```

只清理特定表：

```sql
VACUUM (VERBOSE, ANALYZE) mytable;
```

清理当前数据库中的所有表，并为查询优化器收集统计信息：

```sql
VACUUM ANALYZE;
```

## 兼容性 {#compatibility}

SQL 标准没有 `VACUUM` 语句。

## 另请参阅 {#see-also}

[ANALYZE](/cloudberry/reference/sql-stmts/analyze/)
