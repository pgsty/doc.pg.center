---
title: "LOCK"
description: "锁定表。"
weight: 1530
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/lock.md"
---

## 语法概要 {#synopsis}

```sql
LOCK [TABLE] [ONLY] name [ * ] [, ...] [IN <lockmode> MODE] [NOWAIT] [COORDINATOR ONLY]
```

其中 lockmode 为以下选项之一：

```sql
ACCESS SHARE | ROW SHARE | ROW EXCLUSIVE | SHARE UPDATE EXCLUSIVE 
| SHARE | SHARE ROW EXCLUSIVE | EXCLUSIVE | ACCESS EXCLUSIVE
```

## 说明 {#description}

`LOCK TABLE` 获取表级锁，必要时等待任何冲突锁释放。如果指定 `NOWAIT`，`LOCK TABLE` 不会等待获取所需锁：如果不能立即获取，就会停止命令并报错。一旦获取锁，就会持有到当前事务结束。没有 `UNLOCK TABLE` 命令；锁总是在事务结束时释放。

Apache Cloudberry 为引用表的命令自动获取锁时，总是使用限制最少的可行锁模式。`LOCK TABLE` 用于可能需要更严格加锁的场合。例如，应用以 `READ COMMITTED` 隔离级别运行事务，并需要确保事务期间表内数据保持稳定。为此，可以在查询前获取表的 `SHARE` 锁。这会阻止并发数据更改，并确保后续读取看到已提交数据的稳定视图，因为 `SHARE` 锁模式与写入者获取的 `ROW EXCLUSIVE` 锁冲突，而 `LOCK TABLE <name> IN SHARE MODE` 语句会等待所有并发持有 `ROW EXCLUSIVE` 模式锁的事务提交或回滚。因此，一旦获取该锁，就不存在尚未提交的写入；而且在释放锁前也无法开始新的写入。

要在 `REPEATABLE READ` 或 `SERIALIZABLE` 隔离级别下达到类似效果，必须在执行任何 `SELECT` 或数据修改语句之前执行 `LOCK TABLE`。`REPEATABLE READ` 或 `SERIALIZABLE` 事务的数据视图会在其第一条 `SELECT` 或数据修改语句开始时固定。事务稍后执行 `LOCK TABLE` 仍能阻止并发写入，但无法确保事务读取的内容对应于最新提交的值。

如果此类事务要更改表中的数据，就应使用 `SHARE ROW EXCLUSIVE` 锁模式，而非 `SHARE`。这样可确保同一时间只有一个此类事务运行。否则，可能发生死锁：两个事务可能都获取 `SHARE` 模式，之后却无法再获取 `ROW EXCLUSIVE` 模式来实际执行更新。请注意，事务自身的锁永不冲突，因此持有 `SHARE` 模式的事务可以获取 `ROW EXCLUSIVE` 模式，但其他事务也持有 `SHARE` 模式时则不行。为避免死锁，应确保所有事务以相同顺序获取同一组对象的锁；如果单个对象涉及多种锁模式，事务应始终先获取限制最严格的模式。

## 参数 {#parameters}

**`name`**

要锁定的现有表的名称（可以用模式名限定）。如果指定 `ONLY`，则只锁定该表。如果未指定 `ONLY`，则锁定该表及其所有后代表（如果有）。也可以在表名后指定 `*`，明确表示包含后代表。

如果给出多个表，将按 `LOCK TABLE` 命令中指定的顺序逐一锁定。

**`lockmode`**

锁模式指定该锁与哪些锁冲突。如果未指定锁模式，则使用限制最严格的 `ACCESS EXCLUSIVE`。锁模式如下：

- ACCESS SHARE — 仅与 `ACCESS EXCLUSIVE` 锁模式冲突。`SELECT` 命令会对引用的表获取此模式的锁。通常，任何只读取表而不修改表的查询都会获取此锁模式。
- ROW SHARE — 与 `EXCLUSIVE` 和 `ACCESS EXCLUSIVE` 锁模式冲突。`SELECT FOR SHARE` 命令自动对目标表获取此模式的锁（并对其他被引用但未以 `FOR SHARE` 选取的表获取 `ACCESS SHARE` 锁）。
- ROW EXCLUSIVE — 与 `SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 和 `ACCESS EXCLUSIVE` 锁模式冲突。`INSERT` 和 `COPY` 命令自动对目标表获取此锁模式（并对其他被引用的表获取 `ACCESS SHARE` 锁）。参见[注意事项](#notes)。
- SHARE UPDATE EXCLUSIVE — 与 `SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 和 `ACCESS EXCLUSIVE` 锁模式冲突。此模式保护表免受并发模式更改和 `VACUUM` 执行的影响。对堆表执行 `VACUUM`（不带 `FULL`）和执行 `ANALYZE` 时获取。
- SHARE — 与 `ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE ROW EXCLUSIVE, EXCLUSIVE` 和 `ACCESS EXCLUSIVE` 锁模式冲突。此模式保护表免受并发数据更改的影响，由 `CREATE INDEX` 自动获取。
- SHARE ROW EXCLUSIVE — 与 `ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 和 `ACCESS EXCLUSIVE` 锁模式冲突。此模式保护表免受并发数据更改的影响，并且与自身排斥，因此同一时间只能有一个会话持有它。Apache Cloudberry 的任何命令都不会自动获取此锁模式。
- EXCLUSIVE — 与 `ROW SHARE`、`ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 和 `ACCESS EXCLUSIVE` 锁模式冲突。此模式只允许并发的 `ACCESS SHARE` 锁，即只有对表的读取可以与持有此锁模式的事务并行进行。Apache Cloudberry 为 `UPDATE`、`SELECT FOR UPDATE` 和 `DELETE` 自动获取此锁模式（比普通 PostgreSQL 的锁定更严格）。参见[注意事项](#notes)。
- ACCESS EXCLUSIVE — 与所有模式的锁（`ACCESS SHARE`、`ROW SHARE`、`ROW EXCLUSIVE`、`SHARE UPDATE EXCLUSIVE`、`SHARE`、`SHARE ROW EXCLUSIVE`、`EXCLUSIVE` 和 `ACCESS EXCLUSIVE`）冲突。此模式确保持有者是唯一以任何方式访问该表的事务。`ALTER TABLE`、`DROP TABLE`、`TRUNCATE`、`REINDEX`、`CLUSTER` 和 `VACUUM FULL` 命令会自动获取它。这也是未显式指定模式的 `LOCK TABLE` 语句的默认锁模式。对 AO 表执行 `VACUUM`（不带 `FULL`）时，处理过程中也会短暂获取此锁。

> **注意：** 默认情况下，对堆表执行 `DELETE`、`UPDATE` 和 `SELECT FOR UPDATE` 操作时，Apache Cloudberry 会对表获取 `EXCLUSIVE` 锁。启用全局死锁检测器后，这些堆表操作的锁模式为 `ROW EXCLUSIVE`。

**`NOWAIT`**

指定 `LOCK TABLE` 不应等待任何冲突锁释放：如果无法不经等待立即获取指定锁，则取消事务。

**`COORDINATOR ONLY`**

指定发出 `LOCK TABLE` 命令时，Apache Cloudberry 只在 Coordinator 上锁定表，而不是在 Coordinator 和所有 Segment 上锁定。这对只操作元数据的操作特别有用。

**注意** 此选项仅支持 `ACCESS SHARE MODE`。

## 注意事项 {#notes}

`LOCK TABLE ... IN ACCESS SHARE MODE` 要求对目标表具有 `SELECT` 权限。其他所有 `LOCK` 形式都要求表级 `UPDATE`、`DELETE` 或 `TRUNCATE` 权限。

`LOCK TABLE` 在事务块外没有用处：锁只会持有到 `LOCK` 语句完成。因此，在事务块外使用 `LOCK` 时，Apache Cloudberry 会报错。使用 `BEGIN` 和 `END` 定义事务块。

`LOCK TABLE` 只处理表级锁，因此包含 `ROW` 的模式名称都名不副实。通常应将这些名称理解为用户打算在已锁定表内获取行级锁。另外，`ROW EXCLUSIVE` 模式是可共享的表锁。请记住，对 `LOCK TABLE` 而言，所有锁模式的语义相同，区别只在于哪些模式相互冲突的规则。有关如何获取真正的行级锁，参见 [SELECT](/cloudberry/reference/sql-stmts/select/) 参考文档中的 `FOR UPDATE/FOR SHARE` 子句。

## 示例 {#examples}

准备向 `films_user_comments` 表插入数据时，对 `films` 表获取 `SHARE` 锁：

```sql
BEGIN WORK;
LOCK TABLE films IN SHARE MODE;
SELECT id FROM films
    WHERE name = 'Star Wars: Episode I - The Phantom Menace';
-- Do ROLLBACK if record was not returned
INSERT INTO films_user_comments VALUES
    (_id_, 'GREAT! I was waiting for it for so long!');
COMMIT WORK;
```

执行删除操作时，对表获取 `SHARE ROW EXCLUSIVE` 锁：

```sql
BEGIN WORK;
LOCK TABLE films IN SHARE ROW EXCLUSIVE MODE;
DELETE FROM films_user_comments WHERE id IN
    (SELECT id FROM films WHERE rating < 5);
DELETE FROM films WHERE rating < 5;
COMMIT WORK;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `LOCK TABLE`，而是使用 `SET TRANSACTION` 指定事务的并发级别。Apache Cloudberry 也支持这一方式；详情参见 [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)。

除 `ACCESS SHARE`、`ACCESS EXCLUSIVE` 和 `SHARE UPDATE EXCLUSIVE` 锁模式外，Apache Cloudberry 的锁模式和 `LOCK TABLE` 语法与 Oracle 兼容。

## 另请参阅 {#see-also}

[BEGIN](/cloudberry/reference/sql-stmts/begin/), [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/), [SELECT](/cloudberry/reference/sql-stmts/select/)
