---
title: "pg_class"
description: "系统目录表 `pg_class` 记录表，以及几乎所有其他具有列或在其他方面与表类似的对象。"
weight: 210
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-class.md"
---

这些对象包括索引（另见 `pg_index`）、序列、视图、物化视图、复合类型和 TOAST 表。下文统称这些对象为“关系”。并非所有列对每种关系类型都有意义。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符。|
|`relname`|name| |表、索引或视图的名称。|
|`relnamespace`|oid| `pg_namespace.oid` |包含此关系的名字空间（模式）的对象标识符。|
|`reltype`|oid| `pg_type.oid` |此表行类型所对应的数据类型的对象标识符（如果有；索引没有 `pg_type` 条目，因此为零）。|
|`reloftype`|oid| `pg_type.oid` |对于类型化表，为其底层复合类型的对象标识符；所有其他关系均为零。|
|`relowner`|oid|`pg_authid.oid`|关系的所有者。|
|`relam`|oid|`pg_am.oid`|如果是表或索引，则为所用的访问方法（堆、B-树、哈希等）。|
|`relfilenode`|bigint| |此关系在磁盘上的文件名；零表示这是一个“映射”关系，其磁盘文件名由底层状态决定。|
|`reltablespace`|oid|`pg_tablespace.oid`|存储此关系的表空间。零表示使用数据库的默认表空间。（如果关系没有磁盘文件，则无意义。）|
|`relpages`|int4| |此表磁盘表示的大小，以页为单位（每页大小为 `BLCKSZ`）。它只是规划器使用的估算值，由 `VACUUM`、`ANALYZE` 以及 `CREATE INDEX` 等少数 DDL 命令更新。|
|`reltuples`|real| |表中的行数。它只是规划器使用的估算值，由 `VACUUM`、`ANALYZE` 以及 `CREATE INDEX` 等少数 DDL 命令更新。|
|`relallvisible`|int4| |表的可见性映射中标记为全部可见的页数。它只是规划器使用的估算值，由 `VACUUM`、`ANALYZE` 以及 `CREATE INDEX` 等少数 DDL 命令更新。|
|`reltoastrelid`|oid| `pg_class.oid` |与此表关联的 TOAST 表的对象标识符；没有则为 `0`。TOAST 表将较大的属性“行外”存储在辅助表中。|
|`relhasindex`|boolean| |如果这是表且有索引（或最近曾有索引），则为真。|
|`relisshared`|boolean| |如果此表由系统中的所有数据库共享，则为真。只有某些系统目录表（例如 `pg_database`）是共享的。|
|`relpersistence`|char| |对象的持久性类型：`p` = 堆或 AO 永久表，`u` = 不记录日志的临时表，`t` = 临时表。|
|`relkind`|char| |对象类型：<br/><br/>`r` = 堆或 AO 普通表，`i` = 索引，`S` = 序列，`t` = TOAST 表，`v` = 视图，`m` = 物化视图，`c` = 复合类型，`f` = 外表，`p` = 分区表，`I` = 分区索引，`u` = 未登记到目录中的临时堆表，`o` = 内部 AO 段文件及 EOF，`b` = 仅追加块目录，`M` = 仅追加可见性映射。|
|`relnatts`|int2| |关系中用户列的数量（不计系统列）。`pg_attribute` 中必须有相同数量的对应条目。另见 `pg_attribute.attnum`。|
|`relchecks`|int2| |表上 `CHECK` 约束的数量；参见 `pg_constraint` 目录。|
|`relhasrules`|boolean| |如果表有规则（或曾经有过规则），则为真；参见 `pg_rewrite` 目录。|
|`relhastriggers`|boolean| |如果表有触发器（或曾经有过触发器），则为真。|
|`relhassubclass`|boolean| |如果表有继承子表（或曾经有过继承子表），则为真。|
|`relrowsecurity`|boolean| |如果表启用了行级安全性，则为真；参见 `pg_policy` 目录。|
|`relforcerowsecurity`|boolean| |如果行级安全性（启用时）也适用于表所有者，则为真；参见 `pg_policy` 目录。|
|`relispopulated`|boolean| |如果关系已填充数据，则为真（除部分物化视图之外，所有关系均为真）。|
|`relreplident`|char| |构成行的“复制标识”的列：`d` = 默认值（主键，如果有），`n` = 无，`f` = 所有列，`i` = 设置了 `indisreplident` 的索引（如果所用索引已删除，则等同于无）。|
|`relispartition`|boolean| |如果表或索引是分区，则为真。|
|`relrewrite`|oid|`pg_class.oid` |对于需要重写表的 DDL 操作正在写入的新关系，此列包含原关系的对象标识符；否则为 0。该状态只在内部可见；对于用户可见的关系，此字段的值始终应为 0。|
|`relfrozenxid`|xid| |此表中早于该值的所有事务 ID 都已替换为永久（冻结）的事务 ID。此值用于跟踪表是否需要执行清理，以防止事务 ID 回卷或允许收缩 `pg_xact`。<br/><br/>如果关系不是表，或此表不需要通过清理来防止事务 ID 回卷，则为 `0`（`InvalidTransactionId`）。表仍可能需要通过清理来回收磁盘空间。|
|`relminmxid`|xid| |此表中早于该值的所有多事务 ID 都已替换为事务 ID。此值用于跟踪表是否需要执行清理，以防止多事务 ID 回卷或允许收缩 `pg_multixact`。如果关系不是表，则为零（`InvalidMultiXactId`）。|
|`relacl`|aclitem[]| |由 `GRANT` 和 `REVOKE` 分配的访问权限。|
|`reloptions`|text[]| |访问方法相关选项，以“keyword=value”字符串表示。|
|`relpartbound`|`pg_node_tree`| |如果表是分区（见 `relispartition`），则为分区边界的内部表示。|

`pg_class` 中的若干布尔标志采用延迟维护：当条件成立时，保证其值为真；当条件不再成立时，却可能不会立即重置为假。例如，`CREATE INDEX` 会设置 `relhasindex`，但 `DROP INDEX` 从不会清除此标志。相反，`VACUUM` 在发现表没有索引时会清除 `relhasindex`。这种安排避免了竞争条件，并提高了并发性。
