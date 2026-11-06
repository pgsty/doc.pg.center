---
title: "SET TRANSACTION"
description: "设置当前事务的特性。"
weight: 1720
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/set-transaction.md"
---

## 语法概要 {#synopsis}

```sql
SET TRANSACTION <transaction_mode> [, ...]
SET TRANSACTION SNAPSHOT <snapshot_id>
SET SESSION CHARACTERISTICS AS TRANSACTION <transaction_mode> [, ...] 
     [READ ONLY | READ WRITE]
     [NOT] DEFERRABLE

-- where <transaction_mode> is one of:

    ISOLATION LEVEL {SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED}
    READ WRITE | READ ONLY
    [NOT] DEFERRABLE

-- and <snapshot_id> is the id of the existing transaction whose snapshot you want this transaction to run with.
```

## 说明 {#description}

`SET TRANSACTION` 命令设置当前事务的特性，对后续事务没有影响。`SET SESSION CHARACTERISTICS` 设置会话中后续事务的默认特性。对于单个事务，可以用 `SET TRANSACTION` 覆盖这些默认值。

可设置的事务特性包括事务隔离级别、事务访问模式（读写或只读）和可延迟模式。另外，还可以选择快照，但只能用于当前事务，不能设为会话默认值。

> [!NOTE]
> 可延迟事务要求事务是可串行化的。Apache Cloudberry 不支持可串行化事务，因此包含 `DEFERRABLE` 子句不会产生任何效果。

事务的隔离级别决定了其他事务并发运行时，该事务能够看到哪些数据。

- **READ COMMITTED** — 语句只能看到在其开始之前已提交的行。这是默认值。
- **REPEATABLE READ** — 当前事务中的所有语句都只能看到在该事务执行第一条查询或数据修改语句之前已提交的行。

SQL 标准还定义了另外两个级别：`READ UNCOMMITTED` 和 `SERIALIZABLE`。在 Apache Cloudberry 中，`READ UNCOMMITTED` 按 `READ COMMITTED` 处理。如果指定 `SERIALIZABLE`，Apache Cloudberry 会回退到 `REPEATABLE READ`。

事务执行第一条查询或数据修改语句（`SELECT`、`INSERT`、`DELETE`、`UPDATE`、`FETCH` 或 `COPY`）之后，就不能再更改其隔离级别。

事务访问模式决定事务是读写还是只读。默认为读写。只读事务中禁止执行以下 SQL 命令：当写入目标表不是临时表时的 `INSERT`、`UPDATE`、`DELETE` 和 `COPY FROM`；所有 `CREATE`、`ALTER` 和 `DROP` 命令；`COMMENT`、`GRANT`、`REVOKE`、`TRUNCATE`；以及所执行命令属于上述命令之一的 `EXPLAIN ANALYZE` 和 `EXECUTE`。这是高层次的只读概念，并不阻止所有磁盘写入。

除非事务同时为 `SERIALIZABLE` 和 `READ ONLY`，否则 `DEFERRABLE` 事务属性不会产生任何效果。当事务设置了所有这些属性时，它可能会在首次获取快照时阻塞；之后就可以执行，而无需承担 `SERIALIZABLE` 事务通常的开销，也不会导致串行化失败或因串行化失败而被取消。此模式非常适合长时间运行的报表或备份。*由于 Apache Cloudberry 不支持可串行化事务，`DEFERRABLE` 事务属性在 Apache Cloudberry 中没有效果。*

`SET TRANSACTION SNAPSHOT` 命令允许新事务使用与某个现有事务相同的快照运行。现有事务必须已通过 `pg_export_snapshot()` 函数导出其快照。该函数返回一个快照标识符，必须将其传给 `SET TRANSACTION SNAPSHOT`，以指定要导入的快照。在此命令中，标识符必须写成字符串字面量，例如 `'000003A1-1'`。`SET TRANSACTION SNAPSHOT` 只能在事务开始时、执行第一条查询或数据修改语句（`SELECT`、`INSERT`、`DELETE`、`UPDATE`、`FETCH` 或 `COPY`）之前执行。此外，事务必须已经设置为 `SERIALIZABLE` 或 `REPEATABLE READ` 隔离级别（否则快照会立即被丢弃，因为 `READ COMMITTED` 模式会为每条命令获取新快照）。如果导入快照的事务使用 `SERIALIZABLE` 隔离级别，则导出快照的事务也必须使用该隔离级别。另外，非只读的可串行化事务不能从只读事务导入快照。

## 注意事项 {#notes}

如果未先执行 [START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/) 或 [`BEGIN`](/cloudberry/reference/sql-stmts/begin/) 就执行 `SET TRANSACTION`，则会发出警告，除此之外没有任何效果。

也可以直接在 `BEGIN` 或 `START TRANSACTION` 中指定所需的 transaction_modes，从而省去 `SET TRANSACTION`。但 `SET TRANSACTION SNAPSHOT` 不支持这种方式。

还可以通过配置参数 `default_transaction_isolation`、`default_transaction_read_only` 和 `default_transaction_deferrable` 设置或查看会话的默认事务模式。（实际上，`SET SESSION CHARACTERISTICS` 只是用 `SET` 设置这些变量的较冗长等价形式。）这意味着可以在配置文件中、通过 `ALTER DATABASE` 等方式设置默认值。

同样，可以通过配置参数 `transaction_isolation`、`transaction_read_only` 和 `transaction_deferrable` 设置或查看当前事务的模式。设置其中一个参数的效果与相应的 `SET TRANSACTION` 选项相同，且受到相同的设置时机限制。不过，不能在配置文件中设置这些参数，也不能通过实时 SQL 之外的任何来源设置它们。

## 示例 {#examples}

要开始一个与现有事务使用相同快照的新事务，首先从现有事务导出快照。这会返回快照标识符，例如：

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot();
 pg_export_snapshot
---------------------
 00000003-0000001B-1
(1 row)
```

然后，在新开启的事务开始时，将此快照标识符传给 `SET TRANSACTION SNAPSHOT` 命令：

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION SNAPSHOT '00000003-0000001B-1';
```

## 兼容性 {#compatibility}

这些命令由 SQL 标准定义，但 `DEFERRABLE` 事务模式和 `SET TRANSACTION SNAPSHOT` 形式除外，它们是 Apache Cloudberry 的扩展。

标准中的默认事务隔离级别是 `SERIALIZABLE`。Apache Cloudberry 的默认值是 `READ COMMITTED`。由于缺少谓词锁，Apache Cloudberry 并不完全支持 `SERIALIZABLE` 级别，因此在指定 `SERIALIZABLE` 时会回退到 `REPEATABLE READ` 级别。本质上，谓词锁系统通过限制写入的内容来防止幻读，而 Apache Cloudberry 使用的多版本并发控制模型（MVCC）通过限制读取的内容来防止幻读。

在 SQL 标准中，还可以用这些命令设置另一项事务特性：诊断区域的大小。这一概念特定于嵌入式 SQL，因此 Apache Cloudberry 服务器没有实现。

SQL 标准要求在连续的 transaction_modes 之间使用逗号，但出于历史原因，Apache Cloudberry 允许省略逗号。

## 另请参阅 {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/)
