---
title: "Apache Cloudberry 中的事务并发控制"
linkTitle: "事务并发控制"
description: "了解 Apache Cloudberry 中的 MVCC、事务隔离、锁模式和全局死锁检测。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/transactional-concurrency-control.md"
---

本文介绍 Apache Cloudberry 的事务并发控制，包括：

- [MVCC 机制](#mvcc-mechanism)
- [锁模式](#lock-modes)
- [全局死锁检测器](#global-deadlock-detector)

## MVCC 机制 {#mvcc-mechanism}

Apache Cloudberry 和 PostgreSQL 不使用锁来进行并发控制，而是通过称为多版本并发控制（MVCC）的多版本模型维护数据一致性。MVCC 为每个数据库会话提供事务隔离，使每个查询事务都能看到一致的数据快照，确保事务观察到的数据保持一致，不受其他并发事务影响。

不过，事务具体能看到哪些数据更改，取决于其隔离级别。默认隔离级别为“READ COMMITTED”，事务可以看到其他已提交事务所做的数据更改。如果隔离级别设为“REPEATABLE READ”，该事务中的查询看到的就是事务开始时的数据，而看不到其他事务在此期间所做的更改。可以使用 `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ` 语句，以“REPEATABLE READ”隔离级别开始事务。

由于 MVCC 不使用显式锁进行并发控制，锁争用得以减少，Apache Cloudberry 因而能够在多用户环境中保持合理的性能。查询（读取）数据时获取的锁，不会与写入数据时获取的锁冲突。

## 锁模式 {#lock-modes}

Apache Cloudberry 提供多种锁模式，控制对表中数据的并发访问。大多数 Apache Cloudberry SQL 命令会自动获取适当的锁，确保命令执行期间，引用的表不会被删除或以不兼容的方式修改。对于难以适应 MVCC 行为的应用程序，可以使用 `LOCK` 命令获取显式锁。不过，正确使用 MVCC 通常能获得更好的性能。

|锁模式|相关 SQL 命令|与之冲突的锁模式|
|---------|-----------------------|--------------|
|ACCESS SHARE|`SELECT`|ACCESS EXCLUSIVE|
|ROW SHARE|`SELECT...FOR lock_strength`|EXCLUSIVE, ACCESS EXCLUSIVE|
|ROW EXCLUSIVE|`INSERT`, `COPY`|SHARE, SHARE ROW EXCLUSIVE, EXCLUSIVE, ACCESS EXCLUSIVE|
|SHARE UPDATE EXCLUSIVE|`ANALYZE`|SHARE UPDATE EXCLUSIVE, SHARE, EXCLUSIVE, ACCESS EXCLUSIVE|
|SHARE|`CREATE INDEX`|ROW EXCLUSIVE, SHARE UPDATE EXCLUSIVE, SHARE ROW EXCLUSIVE, EXCLUSIVE, ACCESS EXCLUSIVE|
|SHARE ROW EXCLUSIVE| |ROW EXCLUSIVE, SHARE UPDATE EXCLUSIVE, SHARE, SHARE ROW EXCLUSIVE, EXCLUSIVE, ACCESS EXCLUSIVE|
|EXCLUSIVE|`DELETE`, `UPDATE`, `SELECT...FOR lock_strength`, `REFRESH MATERIALIZED VIEW CONCURRENTLY`|ROW SHARE, ROW EXCLUSIVE, SHARE UPDATE EXCLUSIVE, SHARE, SHARE ROW EXCLUSIVE, EXCLUSIVE, ACCESS EXCLUSIVE|
|ACCESS EXCLUSIVE|`ALTER TABLE`, `DROP TABLE`, `TRUNCATE`, `REINDEX`, `CLUSTER`, `REFRESH MATERIALIZED VIEW`（不带 `CONCURRENTLY`）、`VACUUM FULL`|ACCESS SHARE, ROW SHARE, ROW EXCLUSIVE, SHARE UPDATE EXCLUSIVE, SHARE, SHARE ROW EXCLUSIVE, EXCLUSIVE, ACCESS EXCLUSIVE|

> [!NOTE] 注意
> 默认情况下，全局死锁检测器处于禁用状态，Apache Cloudberry 会为 `UPDATE` 和 `DELETE` 获取限制更严格的 `EXCLUSIVE` 锁，而不是 PostgreSQL 中的 `ROW EXCLUSIVE` 锁。
>
> 启用全局死锁检测器后：
>
> - 对堆表执行的某些 `DELETE` 和 `UPDATE` 操作使用 `ROW EXCLUSIVE` 锁模式。参阅[全局死锁检测器](#global-deadlock-detector)。

## 全局死锁检测器 {#global-deadlock-detector}

Apache Cloudberry 的全局死锁检测器后台工作进程会收集所有 Segment 上的锁信息，并使用有向算法检测本地死锁和全局死锁。该算法使 Apache Cloudberry 能够放宽对堆表并发更新和删除的限制。（对于 AO/CO 表，Apache Cloudberry 仍使用表级锁，限制并发的 `UPDATE`、`DELETE` 和 `SELECT...FOR lock_strength` 操作。）

默认情况下，全局死锁检测器处于禁用状态，Apache Cloudberry 会串行执行对堆表的并发 `UPDATE` 和 `DELETE` 操作。要允许这些更新并发执行，并由全局死锁检测器判断是否存在死锁，可以将 `postgresql.conf` 配置文件中的参数 `gp_enable_global_deadlock_detector` 设为 `on`，然后重启数据库。

启用全局死锁检测器后，启动 Apache Cloudberry 时会自动在 Coordinator 主机上启动该后台工作进程。可以通过 `postgresql.conf` 配置文件中的服务器配置参数 `gp_global_deadlock_detector_period`，设置全局死锁检测器收集和分析锁等待数据的间隔。

如果全局死锁检测器确定存在死锁，就会取消与参与死锁的最晚开始的事务关联的一个或多个后端进程，以解除死锁。

对于以下类型的事务，全局死锁检测器判定存在死锁时，只有一个事务能够成功。其他事务会失败，并报错说明不允许并发更新同一行。

- 对堆表同一行执行的并发事务：第一个事务执行更新操作，后续事务执行更新或删除，且查询计划包含 Motion 算子。
- 由基于 Postgres 的规划器执行、更新堆表同一分布键的并发事务。
- 由 GPORCA 优化器执行、更新哈希表同一行的并发事务。

> [!TIP] 提示
> Apache Cloudberry 按服务器配置参数 `deadlock_timeout` 指定的间隔进行本地死锁检测。由于本地与全局死锁检测算法不同，取消哪些进程可能取决于 Apache Cloudberry 先触发哪一种检测器。

> [!TIP] 提示
> 如果启用了服务器配置参数 `lock_timeout`，且其值小于 `deadlock_timeout` 和 `gp_global_deadlock_detector_period`，Apache Cloudberry 会在该会话触发死锁检查之前取消语句。

要查看所有 Segment 上的锁等待信息，请执行用户定义函数 `gp_dist_wait_status()`。通过该函数的输出，可以确定哪些事务在等待锁、哪些事务持有锁、锁的类型和模式、等待者与持有者的会话标识符，以及事务在哪些 Segment 上运行。`gp_dist_wait_status()` 函数的输出示例如下：

```sql
SELECT * FROM pg_catalog.gp_dist_wait_status();

-[ RECORD 1 ]----+--------------
segid            | 0
waiter_dxid      | 11
holder_dxid      | 12
holdTillEndXact  | t
waiter_lpid      | 31249
holder_lpid      | 31458
waiter_lockmode  | ShareLock
waiter_locktype  | transactionid
waiter_sessionid | 8
holder_sessionid | 9
-[ RECORD 2 ]----+--------------
segid            | 1
waiter_dxid      | 12
holder_dxid      | 11
holdTillEndXact  | t
waiter_lpid      | 31467
holder_lpid      | 31250
waiter_lockmode  | ShareLock
waiter_locktype  | transactionid
waiter_sessionid | 9
holder_sessionid | 8
```

全局死锁检测器为解除死锁而取消事务时，会报告以下错误消息：

```
ERROR:  canceling statement due to user request: "cancelled by global deadlock detector"
```

### 全局死锁检测器对 UPDATE 和 DELETE 的兼容性 {#global-deadlock-detector-update-and-delete-compatibility}

全局死锁检测器可以管理堆表上以下类型的 `UPDATE` 和 `DELETE` 命令的并发更新：

- 对单表执行简单 `UPDATE`。由基于 Postgres 的规划器更新非分布键。命令不包含 `FROM` 子句，`WHERE` 子句中也不包含子查询。

    ```sql
    UPDATE t SET c2 = c2 + 1 WHERE c1 > 10;
    ```

-   对单表执行简单 `DELETE`。命令的 `FROM` 或 `WHERE` 子句中不包含子查询。

    ```sql
    DELETE FROM t WHERE c1 > 10;
    ```

- 拆分 `UPDATE`。对于基于 Postgres 的规划器，`UPDATE` 命令更新分布键。

    ```sql
    UPDATE t SET c = c + 1; -- c is a distribution key
    ```

    对于 GPORCA，`UPDATE` 命令更新分布键或引用分布键。

    ```sql
    UPDATE t SET b = b + 1 WHERE c = 10; -- c is a distribution key
    ```

- 复杂 `UPDATE`。`UPDATE` 命令包含多表连接。

    ```sql
    UPDATE t1 SET c = t1.c+1 FROM t2 WHERE t1.c = t2.c;
    ```

    或者，命令的 `WHERE` 子句中包含子查询。

    ```sql
    UPDATE t SET c = c + 1 WHERE c > ALL(SELECT * FROM t1);
    ```

- 复杂 `DELETE`。复杂 `DELETE` 命令与复杂 `UPDATE` 类似，涉及多表连接或子查询。

    ```sql
    DELETE FROM t USING t1 WHERE t.c > t1.c;
    ```

下表列出全局死锁检测器能够管理的并发 `UPDATE` 或 `DELETE` 命令。例如，对同一表行执行的并发简单 `UPDATE` 命令可由全局死锁检测器管理。如果并发执行复杂 `UPDATE` 和简单 `UPDATE`，则只有一个 `UPDATE` 会执行，另一个 `UPDATE` 会返回错误。

|命令|简单 `UPDATE`|简单 `DELETE`|拆分 `UPDATE`|复杂 `UPDATE`|复杂 `DELETE`|
|-------|---------------|---------------|--------------|----------------|----------------|
|简单 `UPDATE`|是|是|否|否|否|
|简单 `DELETE`|是|是|否|是|是|
|拆分 `UPDATE`|否|否|否|否|否|
|复杂 `UPDATE`|否|是|否|否|否|
|复杂 `DELETE`|否|是|否|否|是|

## 另请参阅 {#see-also}

- [使用事务](/cloudberry/operate-with-data/work-with-transactions/)
- [插入、更新和删除行](/cloudberry/operate-with-data/operate-with-db-objects/insert-update-delete-rows/)
