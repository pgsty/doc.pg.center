---
title: "关于并发控制"
description: "Apache Cloudberry 使用 PostgreSQL 多版本并发控制（MVCC）模型管理堆表上的并发事务。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/product-principles/about-mvcc.md"
---

数据库管理系统中的并发控制允许并发查询在保证数据库完整性的同时得到正确结果。传统数据库使用两阶段锁协议，既阻止事务修改已被其他并发事务读取的数据，也阻止并发事务读取或写入已被其他事务更新的数据。用于协调事务的锁会增加数据库争用，降低总体事务吞吐量。

Apache Cloudberry 使用 PostgreSQL 多版本并发控制（MVCC）模型管理堆表的并发。使用 MVCC 时，每个查询在启动时都基于数据库快照运行。运行期间，查询看不到其他并发事务所做的变更，因此可以看到一致的数据库视图。读取行的查询不会因为等待写入行的事务而阻塞。反过来，写入行的查询也不会被读取行的事务阻塞。与使用锁协调读写事务访问的传统数据库系统相比，这种方式支持大得多的并发量。

> **注意** AO 表使用与本节讨论的 MVCC 模型不同的并发控制模型进行管理。AO 表面向“只写一次、多次读取”的应用，这类应用从不执行行级更新，或只极少执行行级更新。

## 快照 {#snapshots}

MVCC 模型依赖系统管理多个数据行版本的能力。查询在启动时基于数据库快照运行。快照是语句或事务开始时可见的行集合。快照确保查询在整个执行期间都能看到一致且有效的数据库视图。

每个事务都会获得唯一的*事务 ID*（XID），这是一个递增的 32 位值。新事务启动时，会分配下一个 XID。未包含在事务中的 SQL 语句会被视为单语句事务——系统会隐式添加 `BEGIN` 和 `COMMIT`。这与某些数据库系统中的自动提交类似。

> **注意** Apache Cloudberry 只为涉及 DDL 或 DML 操作的事务分配 XID，而这类事务通常是唯一需要 XID 的事务。

事务插入行时，XID 会与该行一起保存在系统列 `xmin` 中。事务删除行时，XID 会保存在系统列 `xmax` 中。更新行会被视为删除和插入，因此 XID 会保存到当前行的 `xmax` 以及新插入行的 `xmin` 中。`xmin` 和 `xmax` 列与事务完成状态一起，指定该行版本可见的事务范围。事务可以看到所有小于 `xmin` 的事务的影响，因为这些事务保证已经提交；但看不到大于或等于 `xmax` 的任何事务的影响。

多语句事务还必须记录事务中插入行的命令（`cmin`）或删除行的命令（`cmax`），这样事务才能看到该事务中前面命令所做的变更。命令序列只在事务期间有意义，因此事务开始时会将序列重置为 0。

XID 是数据库的属性。每个 Segment 数据库都有自己的 XID 序列，不能与其他 Segment 数据库的 XID 进行比较。Coordinator 使用集群范围的*会话 ID 编号*（称为 `gp_session_id`）与 Segment 协调分布式事务。Segment 会维护分布式事务 ID 与本地 XID 的映射。Coordinator 使用两阶段提交协议协调跨所有 Segment 的分布式事务。如果任何一个 Segment 上的事务失败，所有 Segment 上的事务都会回滚。

可以使用 `SELECT` 语句查看任意行的 `xmin`、`xmax`、`cmin` 和 `cmax` 列：

```sql
SELECT xmin, xmax, cmin, cmax, * FROM <tablename>;
```

由于是在 Coordinator 上运行 `SELECT` 命令，XID 是分布式事务 ID。如果可以在单个 Segment 数据库中运行该命令，`xmin` 和 `xmax` 值则会是该 Segment 的本地 XID。

> **注意** Apache Cloudberry 会将复制表的所有行分发到每个 Segment，因此每一行都会在每个 Segment 上复制一份。每个 Segment 实例都维护自己的系统列 `xmin`、`xmax`、`cmin` 和 `cmax` 值，以及系统列 `gp_segment_id` 和 `ctid` 的值。Apache Cloudberry 不允许用户查询访问复制表的这些系统列，因为在查询中对它们求值时不存在单一、明确的值。

## 事务 ID 回卷 {#transaction-id-wraparound}

MVCC 模型使用事务 ID（XID）确定查询或事务开始时哪些行可见。XID 是 32 位值，因此从理论上讲，数据库可以运行超过 40 亿个事务，直到该值溢出并回卷到零。但是，Apache Cloudberry 对 XID 使用*模 2³²* 算术，使事务 ID 能够回卷，就像时钟在十二点回到起点一样。对于任意给定的 XID，大约有 20 亿个过去的 XID 和 20 亿个未来的 XID。这种机制会持续工作，直到某个行版本经过约 20 亿个事务仍然存在，此时它会突然被视为新行。为防止这种情况，Cloudberry 使用一个名为 `FrozenXID` 的特殊 XID；与任何普通 XID 比较时，它总是被视为更旧。必须在 20 亿个事务内将行的 `xmin` 替换为 `FrozenXID`，这是 `VACUUM` 命令执行的功能之一。

每 20 亿个事务至少清理一次数据库，可以防止 XID 回卷。Apache Cloudberry 会监控事务 ID，并在需要执行 `VACUUM` 时发出警告。

当大量事务 ID 不再可用、但尚未发生事务 ID 回卷时，系统会发出警告：

```
WARNING: database "<database_name>" must be vacuumed within <number_of_transactions> transactions
```

发出警告后，必须执行 `VACUUM`。如果不执行 `VACUUM`，Apache Cloudberry 会在事务 ID 回卷发生前达到限制时停止创建事务，以避免可能的数据丢失，并发出以下错误：

```
FATAL: database is not accepting commands to avoid wraparound data loss in database "<database_name>"
```

服务器配置参数 `xid_warn_limit` 和 `xid_stop_limit` 控制显示警告和错误的时机。`xid_warn_limit` 参数指定发出警告时，距离 `xid_stop_limit` 还有多少个事务 ID。`xid_stop_limit` 参数指定发出错误且无法创建新事务时，距离事务 ID 回卷还有多少个事务 ID。

## 事务隔离级别 {#transaction-isolation-levels}

SQL 标准定义了四个事务隔离级别。其中最严格的是可串行化（Serializable）；标准将其定义为：一组可串行化事务的任何并发执行，都保证产生与按某种顺序逐个运行这些事务相同的效果。其他三个级别根据并发事务之间交互产生的现象定义，这些现象在相应级别不得发生。标准指出，由于可串行化的定义，这些现象在该级别都不可能发生。

各级别禁止的现象如下：

- *脏读*——事务读取并发的未提交事务写入的数据。
- *不可重复读*——事务重新读取之前已经读取的数据，却发现数据已被另一个事务修改（该事务在首次读取之后提交）。
- *幻读*——事务重新执行返回满足搜索条件的一组行的查询，却发现满足条件的行集合由于另一个最近提交的事务而发生变化。
- *串行化异常*——一组事务成功提交的结果与按任意顺序逐个运行这些事务的所有可能结果都不一致。

下表描述 SQL 标准定义的四个事务隔离级别及相应行为。

|隔离级别|脏读|不可重复读|幻读|串行化异常|
|-----|----------|--------------|------------|------|
|`READ UNCOMMITTED`|允许，但 Apache Cloudberry 不允许|可能|可能|可能|
|`READ COMMITTED`|不可能|可能|可能|可能|
|`REPEATABLE READ`|不可能|不可能|允许，但 Apache Cloudberry 不允许|可能|
|`SERIALIZABLE`|不可能|不可能|不可能|不可能|

Apache Cloudberry 只实现了两个不同的事务隔离级别，尽管可以请求上述四个级别中的任意一个。Apache Cloudberry 的 `READ UNCOMMITTED` 级别表现为 `READ COMMITTED`，而 `SERIALIZABLE` 级别会退回到 `REPEATABLE READ`。

表中还显示，Apache Cloudberry 的 `REPEATABLE READ` 实现不允许幻读。根据 SQL 标准，这是可接受的，因为标准规定了特定隔离级别必须避免哪些异常；提供更高保证是允许的。

以下各节详细介绍可用隔离级别的行为。

*重要*：某些 Apache Cloudberry 数据类型和函数对事务行为有特殊规则。特别是，序列发生的变更（因此也包括使用 `serial` 声明的列计数器的变更）会立即对所有其他事务可见，并且不会在执行变更的事务中止时回滚。

### 读未提交隔离级别 {#read-uncommitted-isolation-level}

Apache Cloudberry 的默认隔离级别是 `READ COMMITTED`。事务使用此隔离级别时，`SELECT` 查询（不带 `FOR UPDATE/SHARE` 子句）只能看到查询开始前已提交的数据；它既看不到未提交的数据，也看不到并发事务在查询执行期间提交的变更。实际上，`SELECT` 查询看到的是查询开始运行瞬间的数据库快照。但是，`SELECT` 确实能看到自己事务中之前执行的更新所产生的影响，即使这些更新尚未提交。还要注意，即使两个连续的 `SELECT` 命令位于同一个事务中，如果其他事务在第一个 `SELECT` 开始后、第二个 `SELECT` 开始前提交了变更，这两个命令也可能看到不同的数据。

就搜索目标行而言，`UPDATE`、`DELETE`、`SELECT FOR UPDATE` 和 `SELECT FOR SHARE` 命令的行为与 `SELECT` 相同：它们只查找命令开始时已经提交的目标行。但是，找到目标行时，该行可能已经被另一个并发事务更新（或删除或锁定）。此时，待更新者会等待第一个更新事务提交或回滚（如果它仍在进行）。如果第一个更新者回滚，其影响就会被抵消，第二个更新者可以继续更新最初找到的行。如果第一个更新者提交，且它删除了该行，第二个更新者就会忽略该行；否则，第二个更新者会尝试对该行的更新版本应用操作。系统会重新评估命令的搜索条件（`WHERE` 子句），检查该行的更新版本是否仍满足搜索条件。如果满足，第二个更新者就会使用更新后的行版本继续操作。对于 `SELECT FOR UPDATE` 和 `SELECT FOR SHARE`，这意味着更新后的行版本会被锁定并返回给客户端。

带 `ON CONFLICT DO UPDATE` 子句的 `INSERT` 行为类似。在 `READ COMMITTED` 模式下，每个待插入行要么被插入，要么被更新。除非发生无关错误，否则必定出现其中一种结果。如果冲突来自另一个事务，而该事务的影响对 `INSERT ` 尚不可见，则 `UPDATE` 子句仍会影响该行，即使该行的任何版本按通常方式对命令都不可见。

带 `ON CONFLICT DO NOTHING` 子句的 `INSERT` 可能因为另一个事务的结果而不插入某行，即使该事务的影响对 `INSERT` 快照不可见。同样，这只会发生在 `READ COMMITTED` 模式下。

由于上述规则，更新命令可能看到不一致的快照：它可以看到并发更新命令对自己正尝试更新的相同行所产生的影响，却看不到这些命令对数据库中其他行产生的影响。这种行为使 `READ COMMITTED` 模式不适合涉及复杂搜索条件的命令；但对于更简单的情况，它恰好适用。例如，考虑使用以下事务更新银行余额：

```sql
BEGIN;
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
COMMIT;
```

如果两个此类事务并发尝试修改账户 `12345` 的余额，我们显然希望第二个事务从该账户行的更新版本开始。由于每个命令只影响一个预先确定的行，让它访问该行的更新版本不会造成麻烦的不一致。

在 `READ COMMITTED` 模式下，更复杂的用法可能产生不符合预期的结果。例如，一个 `DELETE` 命令正在处理数据，而另一个命令同时修改这些数据，使一些行进入该删除命令的筛选范围，另一些行退出该范围；假设 `website` 是一个两行表，`website.hits` 的值分别为 `9` 和 `10`：

```sql
BEGIN;
UPDATE website SET hits = hits + 1;
-- run from another session:  DELETE FROM website WHERE hits = 10;
COMMIT;
```

即使 `UPDATE` 前后都存在 `website.hits = 10` 的行，`DELETE` 也不会产生任何效果。这是因为更新前行值为 `9` 的行被跳过，而 `UPDATE` 完成、`DELETE` 获取锁后，新行值已经不是 `10`，而是 `11`，不再满足条件。

由于 `READ COMMITTED` 模式会为每个命令启动一个新快照，该快照包含截至当时已提交的所有事务，因此同一事务中的后续命令无论如何都会看到并发事务已提交的影响。上面的问题在于，单条命令是否看到绝对一致的数据库视图。

`READ COMMITTED` 模式提供的部分事务隔离足以满足许多应用的需求；该模式快速且易于使用，但并不适合所有情况。执行复杂查询和更新的应用，可能需要比 `READ COMMITTED` 模式提供的更严格一致的数据库视图。

### 可重复读隔离级别 {#repeatable-read-isolation-level}

`REPEATABLE READ` 隔离级别只能看到事务开始前已提交的数据；它既看不到未提交的数据，也看不到并发事务在事务执行期间提交的变更。（但是，查询可以看到自己事务中之前执行的更新所产生的影响，即使这些更新尚未提交。）这比 SQL 标准对该隔离级别要求的保证更强，可以避免上表中描述的所有现象。如前所述，这是标准明确允许的，因为标准只描述每个隔离级别必须提供的最低保护。

`REPEATABLE READ` 隔离级别与 `READ COMMITTED` 的区别在于，`REPEATABLE READ` 事务中的查询看到的是事务中第一条非事务控制语句开始时的快照，而不是事务中当前语句开始时的快照。单个事务中的连续 `SELECT` 命令看到相同数据；它们看不到事务自身开始后由其他事务提交的变更。

使用该级别的应用必须准备好因串行化失败而重试事务。

就搜索目标行而言，`UPDATE`、`DELETE`、`SELECT FOR UPDATE` 和 `SELECT FOR SHARE` 命令的行为与 `SELECT` 相同：它们只会找到事务开始时已经提交的目标行。但是，找到目标行时，该行可能已经被另一个并发事务更新（或删除或锁定）。此时，`REPEATABLE READ` 事务会等待第一个更新事务提交或回滚（如果它仍在进行）。如果第一个更新者回滚，其影响会被抵消，`REPEATABLE READ` 事务可以继续更新最初找到的行。但如果第一个更新者提交（并且确实更新或删除了该行，而不只是锁定该行），Apache Cloudberry 会回滚 `REPEATABLE READ` 事务，并显示以下消息：

```
ERROR:  could not serialize access due to concurrent update
```

这是因为 `REPEATABLE READ` 事务不能修改或锁定在 `REPEATABLE READ` 事务开始后被其他事务更改的行。

应用收到此错误消息时，应中止当前事务，并从头重试整个事务。第二次执行时，事务会将之前提交的变更作为数据库初始视图的一部分，因此使用新行版本作为新事务更新的起点不存在逻辑冲突。

注意，可能只需要重试更新事务；只读事务不会发生串行化冲突。

`REPEATABLE READ` 模式严格保证每个事务看到完全稳定的数据库视图。但是，这个视图不一定总与同一级别的并发事务按某种串行顺序（一次一个）执行时的结果一致。例如，即使是该级别的只读事务，也可能看到控制记录已更新为表示批处理完成，却看不到逻辑上属于该批处理的某条明细记录，因为它读取的是控制记录的旧版本。如果不谨慎使用显式锁来阻塞冲突事务，在此隔离级别运行事务来强制执行业务规则，通常无法正确工作。

### 可串行化隔离级别 {#serializable-isolation-level}

Apache Cloudberry 不完全支持 `SERIALIZABLE` 级别。该级别保证一组并发运行的事务产生的结果，与这些事务按顺序逐个运行时产生的结果相同。如果指定 `SERIALIZABLE`，Apache Cloudberry 会退回到 `REPEATABLE READ`。MVCC 快照隔离（SI）模型无需高成本锁定，就能防止脏读、不可重复读和幻读；但 Apache Cloudberry 中某些 `SERIALIZABLE` 事务之间还可能发生其他交互，阻止事务真正实现可串行化。这些异常通常可归因于 Apache Cloudberry 不执行*谓词锁定*，也就是说，一个事务中的写入可能影响另一个并发事务之前读取的结果。

## 设置事务隔离级别 {#set-the-transaction-isolation-level}

Apache Cloudberry 的默认事务隔离级别由服务器配置参数 `default_transaction_isolation` 指定，初始值为 `READ COMMITTED`。

在会话中设置 `default_transaction_isolation` 时，可以指定该会话中所有事务的默认事务隔离级别。

要为当前事务设置隔离级别，可以使用 [`SET TRANSACTION`](/cloudberry/reference/sql-stmts/set-transaction/) SQL 命令。务必在任何 `SELECT`、`INSERT`、`DELETE`、`UPDATE` 或 `COPY` 语句之前设置隔离级别：

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
...
COMMIT;
```

也可以在 `BEGIN` 语句中指定隔离模式：

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

## 从表中清除死行 {#remove-dead-rows-from-tables}

更新或删除行会在表中留下该行的过期版本。当任何活动事务都不再引用过期行时，可以将其删除，并重新使用它占用的空间。`VACUUM` 命令会将过期行使用的空间标记为可重新使用。

表中积累过期行时，必须扩展磁盘文件以容纳新行。由于运行查询需要更多磁盘 I/O，性能会下降。这种情况称为*膨胀*，应通过定期清理表来管理。

`VACUUM` 命令（不带 `FULL`）可以与其他查询并发运行。它会将过期行之前使用的空间标记为空闲，并更新空闲空间映射。Apache Cloudberry 之后需要为新行分配空间时，会先查询表的空闲空间映射，查找包含可用空间的页。如果没有找到，就会向文件追加新页。

`VACUUM`（不带 `FULL`）不会合并页，也不会减小表在磁盘上的大小。它回收的空间只能通过空闲空间映射使用。为防止磁盘文件持续增长，必须足够频繁地运行 `VACUUM`。所需的 `VACUUM` 频率取决于表中更新和删除的频率（插入只会添加新行）。频繁更新的表可能每天需要运行多次 `VACUUM`，确保可以通过空闲空间映射找到可用空间。执行大量更新或删除行的事务后运行 `VACUUM` 同样重要。

`VACUUM FULL` 命令会重写表，去除过期行，将表缩小到最小大小。它会检查表中的每个页，并将可见行上移到尚未填满的页中，然后丢弃空页。`VACUUM FULL` 完成前会锁定表。与常规 `VACUUM` 命令相比，该操作成本很高；定期清理可以避免或推迟执行它。最好在维护期间运行 `VACUUM FULL`。`VACUUM FULL` 的另一种替代方式是使用 `CREATE TABLE AS` 语句重新创建表，然后删除旧表。

可以运行 `VACUUM VERBOSE tablename`，获取按 Segment 划分的报告，其中包含删除的死行数、受影响的页数以及包含可用空闲空间的页数。

查询 `pg_class` 系统表，了解表在所有 Segment 上使用的页数。务必先对表运行 `ANALYZE`，以获取准确数据。

```sql
SELECT relname, relpages, reltuples FROM pg_class WHERE relname='<tablename>';
```

另一个有用工具是 `gp_toolkit` 模式中的 `gp_bloat_diag` 视图。该视图通过比较表实际使用的页数与预期页数，识别表中的膨胀。
