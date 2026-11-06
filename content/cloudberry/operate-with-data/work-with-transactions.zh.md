---
title: "在 Apache Cloudberry 中使用事务"
linkTitle: "使用事务"
description: "事务可将多条 SQL 语句组合成一个操作，要么全部生效，要么全部不生效。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/work-with-transactions.md"
---

Apache Cloudberry 提供以下 SQL 事务命令：

- `BEGIN` 或 `START TRANSACTION` 开始一个事务块。
- `END` 或 `COMMIT` 提交事务的结果。
- `ROLLBACK` 放弃事务，不保留任何更改。
- `SAVEPOINT` 在事务中标记一个位置，以支持部分回滚。可以回滚保存点之后执行的命令，同时保留保存点之前执行的命令。
- `ROLLBACK TO SAVEPOINT` 将事务回滚到指定保存点。
- `RELEASE SAVEPOINT` 销毁事务中的保存点。

## 事务隔离级别 {#transaction-isolation-levels}

Apache Cloudberry 接受以下标准 SQL 事务隔离级别：

- `READ UNCOMMITTED` 和 `READ COMMITTED` 的行为都与标准的 `READ COMMITTED` 相同。
- `REPEATABLE READ` 和 `SERIALIZABLE` 的行为都与 `REPEATABLE READ` 相同。

下面介绍 Apache Cloudberry 各事务隔离级别的行为。

### 读未提交与读已提交 {#read-uncommitted-and-read-committed}

Apache Cloudberry 不允许任何命令看到其他并发事务尚未提交的更新，因此 `READ UNCOMMITTED` 与 `READ COMMITTED` 的行为相同。`READ COMMITTED` 提供快速、简单的部分事务隔离。`SELECT`、`UPDATE` 和 `DELETE` 命令基于查询开始时获取的数据库快照进行操作。

`SELECT` 查询：

- 能看到查询开始前已提交的数据。
- 能看到本事务中执行的更新。
- 看不到事务外未提交的数据。
- 如果并发事务在本事务首次读取后提交，则有可能看到该并发事务所做的更改。

如果其他并发事务在两次查询之间提交更改，同一事务中连续执行的 `SELECT` 查询可能看到不同的数据。`UPDATE` 和 `DELETE` 命令只能找到在命令开始前已提交的行。

`READ COMMITTED` 事务隔离允许并发事务在 `UPDATE` 或 `DELETE` 找到某一行之前修改或锁定该行。对于执行复杂查询和更新、且要求数据库视图保持一致的应用程序，`READ COMMITTED` 事务隔离可能不够。

### 可重复读与可串行化 {#repeatable-read-and-serializable}

SQL 标准定义的 `SERIALIZABLE` 事务隔离确保并发执行的事务产生的结果，与这些事务逐个串行执行时相同。在 Apache Cloudberry 中指定 `SERIALIZABLE` 时，会退回到 `REPEATABLE READ`。`REPEATABLE READ` 事务无需代价高昂的锁定，就能防止脏读、不可重复读和幻读，但 Apache Cloudberry 无法检测并发事务执行期间所有影响可串行性的交互。应检查并发事务，识别那些即使禁止并发更新同一数据仍无法避免的交互。可以使用显式表锁，或引入一个代表冲突的虚拟行并要求冲突事务更新该行，来防止这些交互。

在 `REPEATABLE READ` 事务中，`SELECT` 查询：

- 看到的是事务开始时的数据快照，而不是事务中当前查询开始时的快照。
- 只能看到查询开始前已提交的数据。
- 能看到本事务中执行的更新。
- 看不到事务外未提交的数据。
- 看不到并发事务所做的更改。
- 在同一事务内连续执行的 `SELECT` 命令始终看到相同的数据。
- `UPDATE`、`DELETE`、`SELECT FOR UPDATE` 和 `SELECT FOR SHARE` 命令只能找到命令开始前已提交的行。如果并发事务已更新、删除或锁定目标行，`REPEATABLE READ` 事务会等待该并发事务提交或回滚更改。如果并发事务提交更改，`REPEATABLE READ` 事务就会回滚；如果并发事务回滚更改，`REPEATABLE READ` 事务就可以提交自己的更改。

Apache Cloudberry 的默认事务隔离级别是 `READ COMMITTED`。要更改某个事务的隔离级别，可以在通过 `BEGIN` 开始事务时声明隔离级别，也可以在事务开始后使用 `SET TRANSACTION` 命令。

## 另请参阅 {#see-also}

- [事务并发控制](/cloudberry/operate-with-data/transactional-concurrency-control/)
- [插入、更新和删除行](/cloudberry/operate-with-data/operate-with-db-objects/insert-update-delete-rows/)
