---
title: "CREATE SEQUENCE"
description: "定义新的序列生成器。"
weight: 790
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-sequence.md"
---

## 语法概要 {#synopsis}

```sql
CREATE [TEMPORARY | TEMP] SEQUENCE [IF NOT EXISTS] <name>
       [ AS data_type ]
       [INCREMENT [BY] <increment>] 
       [MINVALUE <minvalue> | NO MINVALUE] 
       [MAXVALUE <maxvalue> | NO MAXVALUE] 
       [START [ WITH ] <start>] 
       [CACHE <cache>] 
       [[NO] CYCLE] 
       [OWNED BY { <table_name>.<column_name> | NONE }]
```

## 说明 {#description}

`CREATE SEQUENCE` 创建新的序列号生成器。这包括创建并初始化一个同名的特殊单行表。生成器归执行命令的用户所有。

如果给出模式名，序列就在指定模式中创建；否则在当前模式中创建。临时序列存在于特殊模式中，因此创建临时序列时不能提供模式名。序列名称必须与同一模式中任何其他序列、表、索引、视图或外表的名称不同。

创建序列后，可以使用 `nextval()` 函数操作该序列。例如，向表中插入一行并取得序列的下一个值：

```sql
INSERT INTO distributors VALUES (nextval('myserial'), 'acme');
```

也可以使用 `setval()` 函数操作序列，但只能用于不操作分布式数据的查询。下面的查询之所以允许执行，是因为它会为 Coordinator 上的序列生成器进程重置序列计数值：

```sql
SELECT setval('myserial', 201);
```

但下面的查询会在 Apache Cloudberry 中被拒绝，因为它操作分布式数据：

```sql
INSERT INTO product VALUES (setval('myserial', 201), 'gizmo');
```

在普通（非分布式）数据库中，操作序列的函数会在需要时访问本地序列表以获取值。但在 Apache Cloudberry 中，请注意每个 Segment 都是独立的数据库进程。因此，所有 Segment 都需要一个统一的序列值来源，以便正确递增并按正确顺序推进序列。序列服务器进程运行在 Coordinator 上，是 Apache Cloudberry 分布式数据库中序列的唯一真实来源。Segment 在运行时从 Coordinator 获取序列值。

由于这种分布式序列设计，Apache Cloudberry 中操作序列的函数存在一些限制：

- 不支持 `lastval()` 和 `currval()` 函数。
- `setval()` 只能用于设置 Coordinator 上序列生成器的值，不能在子查询中用于更新分布式表数据。
- `nextval()` 有时会根据查询从 Coordinator 获取一组值供某个 Segment 使用。因此，如果 Segment 端最终不需要整组值，序列中可能会跳过一些值。请注意，普通 PostgreSQL 数据库也会这样做，因此这不是 Apache Cloudberry 独有的行为。

> **注意**
> Apache Cloudberry 中序列缓存大小的默认值为 `20`。

虽然不能直接更新序列，但可以使用如下查询：

```sql
SELECT * FROM <sequence_name>;
```

以查看序列的参数和当前状态。特别是，序列的 last_value 字段显示任何会话分配的最后一个值。（请注意，如果其他会话正在积极调用 `nextval()`，该值在打印时可能已经过时。）

## 参数 {#parameters}

**`TEMPORARY | TEMP`**

如果指定，则序列对象只对当前会话创建，并在会话退出时自动删除。临时序列存在期间，同名的永久序列不可见（在当前会话中），除非使用模式限定名称引用它们。

**`IF NOT EXISTS`**

如果同名关系已存在，则不抛出错误。Apache Cloudberry 会在这种情况下发出提示。请注意，无法保证现有关系与要创建的序列相似；它甚至可能不是序列。

**`name`**

要创建的序列名称（可以用模式名限定）。

**`data_type`**

可选子句 `AS data_type` 指定序列的数据类型。有效类型为 `smallint`、`integer` 和 `bigint`。默认值为 `bigint`。数据类型决定序列的默认最小值和最大值。

**`increment`**

指定将加到当前序列值上以生成新值的数值。正值生成递增序列，负值生成递减序列。默认值为 `1`。

**`minvalue`**<br />
**`NO MINVALUE`**

确定序列可以生成的最小值。如果未提供该子句或指定 `NO MINVALUE`，则使用默认值。递增序列的默认值是数据类型的最大值。递减序列的默认值是 `-1`。

**`maxvalue`**<br />
**`NO MAXVALUE`**

确定序列的最大值。如果未提供该子句或指定 `NO MAXVALUE`，则使用默认值。递增和递减序列的默认值分别为 263-1 和 -1。

**`start`**

允许序列从任意位置开始。递增序列的默认起始值为 `minvalue`，递减序列的默认起始值为 `maxvalue`。

**`cache`**

指定要预分配并存储在内存中的序列号数量，以便更快访问。默认值为 20，最小值为 1（不使用缓存）。

> **注意** 使用序列号缓存（`cache > 1`）时，Apache Cloudberry 可能丢弃某些缓存的序列值。如果需要连续值，创建或修改序列时必须明确设置 `CACHE 1`。

**`CYCLE`**<br />
**`NO CYCLE`**

允许序列在达到递增时的 `maxvalue` 或递减时的 `minvalue` 后循环。如果达到限制，下一个生成的数值将分别为递增序列的 `minvalue` 或递减序列的 `maxvalue`。如果指定 `NO CYCLE`，序列达到最大值后再调用 `nextval()` 会返回错误。如果既未指定 `CYCLE` 也未指定 `NO CYCLE`，默认使用 `NO CYCLE`。

**`OWNED BY table_name.colume_name`**<br />
**`OWNED BY NONE`**

使序列与特定表列关联；如果该列（或其所属的整个表）被删除，序列也会自动删除。指定的表必须与序列具有相同所有者，并且位于同一模式中。默认值 `OWNED BY NONE` 表示不存在这种关联。

## 注意事项 {#notes}

使用 `DROP SEQUENCE` 删除序列。

序列基于 bigint 算术，因此取值范围不能超过八字节整数的范围（-9223372036854775808 到 9223372036854775807）。

由于 `nextval()` 和 `setval()` 调用永远不会回滚，如果需要“无间隙”地分配序列号，就不能使用序列对象。可以通过对包含计数器的表使用排他锁实现无间隙分配，但这种方案比序列对象昂贵得多，尤其是在许多事务需要并发获取序列号时。

虽然可以保证多个会话分配不同的序列值，但把所有会话放在一起看时，值可能会乱序生成。例如，`cache` 设置为 `10` 时，会话 A 可能预留 1..10 并返回 `nextval=1`，随后会话 B 预留 11..20 并在会话 A 生成 nextval=2 之前返回 `nextval=11`。因此，`cache` 值为 1 时，可以安全地假定 `nextval()` 值按顺序生成；`cache` 值大于 1 时，只能假定 `nextval()` 值彼此不同，不能假定它们严格按顺序生成。

还要注意，对这种序列执行的 `setval()` 要等其他会话用完已缓存的预分配值后，才会被其他会话看到。

## 示例 {#examples}

创建名为 `myseq`、从 101 开始的递增序列：

```sql
CREATE SEQUENCE myseq START 101;
```

向表中插入一行，并取得名为 `myseq` 的序列的下一个值：

```sql
INSERT INTO distributors VALUES (nextval('myseq'), 'acme'); 
```

重置 Apache Cloudberry Coordinator 上的序列计数值：

```sql
SELECT setval('myseq', 201);
```

在 Apache Cloudberry 中非法使用 `setval()`（在分布式数据上设置序列值）：

```sql
INSERT INTO product VALUES (setval('myseq', 201), 'gizmo'); 
```

## 兼容性 {#compatibility}

`CREATE SEQUENCE` 符合 SQL 标准，但有以下例外：

- 使用 `nextval()` 函数获取下一个值，而不是 SQL 标准规定的 `NEXT VALUE FOR` 表达式。
- `OWNED BY` 子句是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[ALTER SEQUENCE](/cloudberry/reference/sql-stmts/alter-sequence/), [DROP SEQUENCE](/cloudberry/reference/sql-stmts/drop-sequence/)
