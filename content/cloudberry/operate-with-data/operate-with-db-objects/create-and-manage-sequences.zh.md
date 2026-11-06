---
title: "创建和管理序列"
description: "Apache Cloudberry 序列对象是一种特殊的单行表，充当数字生成器。"
weight: 130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-sequences.md"
---

可以使用序列为添加到表中的行生成唯一的整数标识符。声明列的类型为 `SERIAL` 会隐式创建一个序列计数器，供该表列使用。

Apache Cloudberry 提供创建、修改和删除序列的命令。Apache Cloudberry 还提供内置函数，用于返回序列的下一个值（`nextval()`），或将序列设置为特定的起始值（`setval()`）。

> [!NOTE]
> Apache Cloudberry 不支持 PostgreSQL 的 `currval()` 和 `lastval()` 序列函数。

序列对象的属性包括序列名称、增量值，以及序列计数器的最后值、最小值和最大值。序列还有一个名为 `is_called` 的特殊布尔属性，它控制序列计数器上 `nextval()` 操作的自动递增行为。当序列的 `is_called` 属性为 `true` 时，`nextval()` 会在返回值之前递增序列计数器。当序列的 `is_called` 属性值为 `false` 时，`nextval()` 不会在返回值之前递增计数器。

## 创建序列 {#create-a-sequence}

[`CREATE SEQUENCE`](/cloudberry/reference/sql-stmts/create-sequence/) 命令使用给定的序列名称和可选的起始值创建并初始化序列。序列名称必须与同一模式中任何其他序列、表、索引或视图的名称不同。例如：

```sql
CREATE SEQUENCE myserial START 101;
```

创建新序列时，Apache Cloudberry 将序列的 `is_called` 属性设置为 `false`。对新创建的序列调用 `nextval()` 不会递增序列计数器，而是返回序列起始值，并将 `is_called` 设置为 `true`。

## 使用序列 {#use-a-sequence}

使用 `CREATE SEQUENCE` 命令创建序列后，可以检查序列并使用序列内置函数。

### 检查序列属性 {#examine-sequence-attributes}

要检查序列的当前属性，请直接查询序列。例如，要检查名为 `myserial` 的序列：

```sql
SELECT * FROM myserial;
```

### 返回下一个序列计数器值 {#return-the-next-sequence-counter-value}

可以调用 `nextval()` 内置函数来返回并使用序列中的下一个值。以下命令将名为 `myserial` 的序列的下一个值插入名为 `vendors` 的表的第一列：

```sql
INSERT INTO vendors VALUES (nextval('myserial'), 'acme');
```

`nextval()` 使用序列的 `is_called` 属性值来决定在返回序列计数器值之前是否递增计数器。当 `is_called` 为 `true` 时，`nextval()` 会推进计数器。`nextval()` 会在返回值之前将序列的 `is_called` 属性设置为 `true`。

`nextval()` 操作永远不会回滚。获取的值即使执行 `nextval()` 的事务失败，也会被视为已使用。这意味着失败的事务可能会在已分配的值序列中留下未使用的空洞。

> [!NOTE]
> 如果 Apache Cloudberry 启用了镜像，则不能在 `UPDATE` 或 `DELETE` 语句中使用 `nextval()` 函数。

### 设置序列计数器值 {#set-the-sequence-counter-value}

可以使用 Apache Cloudberry 的 `setval()` 内置函数设置序列的计数器值。例如，以下命令将名为 `myserial` 的序列的计数器值设置为 `201`：

```sql
SELECT setval('myserial', 201);
```

`setval()` 有两种函数签名：`setval(sequence, start_val)` 和 `setval(sequence, start_val, is_called)`。`setval(sequence, start_val)` 的默认行为是将序列的 `is_called` 属性值设置为 `true`。

如果不希望序列计数器在下一次调用 `nextval()` 时推进，请使用 `setval(sequence, start_val, is_called)` 函数签名，并传入 `false` 参数：

```sql
SELECT setval('myserial', 201, false);
```

`setval()` 操作永远不会回滚。

### nextval() 和 setval() 注意事项 {#nextval-and-setval-caution}

为了避免阻塞从同一序列获取数字的并发事务，如果调用 `nextval()` 的事务随后中止，所获取的值也不会被回收以供重新使用。因此，事务中止或数据库崩溃可能导致已分配值的序列出现空洞。即使事务没有中止，也可能出现这种情况。例如，带有 `ON CONFLICT` 子句的 `INSERT` 会在检测到冲突并决定遵循 `ON CONFLICT` 规则之前，先计算待插入元组，包括调用任何所需的 `nextval()`。因此，不能使用 Apache Cloudberry 序列对象获取“无空洞”的序列。

同样，`setval()` 所作的序列状态更改会立即对其他事务可见；如果调用事务回滚，这些更改也不会被撤销。

如果数据库集群在包含 `nextval()` 或 `setval()` 调用的事务提交之前崩溃，序列状态更改可能尚未传播到持久存储，因此集群重启后序列是原始状态还是更新后的状态并不确定。这对在数据库中使用序列没有影响，因为未提交事务的其他效果也同样可见。但是，如果希望将序列值用于数据库外的持久用途，请确保在此之前已经提交 `nextval()` 调用。

## 修改序列 {#alter-a-sequence}

[`ALTER SEQUENCE`](/cloudberry/reference/sql-stmts/alter-sequence/) 命令修改现有序列的属性。可以修改序列的起始值、最小值、最大值和增量值。还可以将序列重新启动为起始值或指定的值。

`ALTER SEQUENCE` 命令中未设置的参数会保留之前的设置。

`ALTER SEQUENCE sequence START WITH start_value` 将序列的 `start_value` 属性设置为新的起始值。它不会影响 `last_value` 属性，也不会影响 `nextval(sequence)` 函数返回的值。

`ALTER SEQUENCE sequence RESTART` 将序列的 `last_value` 属性重置为当前 `start_value` 属性的值，并将 `is_called` 属性设置为 `false`。下一次调用 `nextval(sequence)` 时会返回 `start_value`。

`ALTER SEQUENCE sequence RESTART WITH restart_value` 将序列的 `last_value` 设置为新值，并将 `is_called` 属性设置为 `false`。下一次调用 `nextval(sequence)` 时会返回 `restart_value`。这等价于调用 `setval(sequence, restart_value, false)`。

以下命令将名为 `myserial` 的序列重新启动为值 `105`：

```sql
ALTER SEQUENCE myserial RESTART WITH 105;
```

## 删除序列 {#drop-a-sequence}

[`DROP SEQUENCE`](/cloudberry/reference/sql-stmts/drop-sequence/) 命令删除序列。例如，以下命令删除名为 `myserial` 的序列：

```sql
DROP SEQUENCE myserial;
```

## 将序列指定为列的默认值 {#specify-a-sequence-as-the-default-value-for-a-column}

除了使用 `SERIAL` 或 `BIGSERIAL` 类型外，还可以在 [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/) 命令中直接引用序列。例如：

```sql
CREATE TABLE tablename ( id INT4 DEFAULT nextval('myserial'), name text );
```

还可以修改表列，将其默认值设置为序列计数器：

```sql
ALTER TABLE tablename ALTER COLUMN id SET DEFAULT nextval('myserial');
```

## 序列回绕 {#sequence-wraparound}

默认情况下，序列不会回绕。也就是说，当序列达到最大值（`SMALLSERIAL` 为 `+32767`，`SERIAL` 为 `+2147483647`，`BIGSERIAL` 为 `+9223372036854775807`）时，之后的每次 `nextval()` 调用都会产生错误。可以修改序列，使其循环并重新从 `1` 开始：

```sql
ALTER SEQUENCE myserial CYCLE;
```

也可以在创建序列时指定回绕行为：

```sql
CREATE SEQUENCE myserial CYCLE;
```
