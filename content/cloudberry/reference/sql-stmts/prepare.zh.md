---
title: "PREPARE"
description: "准备要执行的语句。"
weight: 1560
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/prepare.md"
---

## 语法概要 {#synopsis}

```sql
PREPARE <name> [ (<data_type> [, ...] ) ] AS <statement>
```

## 说明 {#description}

`PREPARE` 创建预备语句。预备语句是可用于优化性能的服务器端对象。运行 `PREPARE` 语句时，会对指定语句进行解析、分析和重写。随后发出 `EXECUTE` 命令时，系统会为预备语句生成计划并执行。这种分工避免了重复的解析分析工作，同时允许执行计划取决于所提供的具体参数值。

预备语句可以接受参数，运行时会将参数值代入语句。创建预备语句时，使用 `$1`、`$2` 等按位置引用参数。可以选择指定对应的参数数据类型列表。如果某个参数的数据类型未指定或声明为 `unknown`，则根据首次引用该参数的上下文推断类型（如果可能）。运行语句时，在 [EXECUTE](/cloudberry/reference/sql-stmts/execute/) 语句中指定这些参数的实际值。

预备语句只在当前数据库会话期间存在。会话结束时，预备语句会被遗忘，因此再次使用前必须重新创建。这也意味着多个并发数据库客户端不能使用同一个预备语句；不过，每个客户端都可以创建自己的预备语句。可以使用 [DEALLOCATE](/cloudberry/reference/sql-stmts/deallocate/) 命令手动清理预备语句。

当单个会话用于运行大量相似语句时，预备语句的性能优势最大。如果语句的计划或重写很复杂，例如查询连接许多表或需要应用多条规则，性能差异尤其明显。如果语句的计划和重写相对简单，但执行成本较高，预备语句的性能优势则不太明显。

## 参数 {#parameters}

**`name`**

为此预备语句指定的任意名称。它必须在单个会话内唯一，之后用于执行或释放先前准备的语句。

**`data_type`**

预备语句参数的数据类型。如果某个参数的数据类型未指定或指定为 `unknown`，则会根据首次引用它的上下文推断。要在预备语句本身中引用参数，使用 `$1`、`$2` 等。

**`statement`**

任意 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 或 `VALUES` 语句。

## 注意事项 {#notes}

预备语句可以使用*通用计划*或*定制计划*执行。通用计划在所有执行中相同，而定制计划针对某次具体执行，使用该次调用给出的参数值生成。使用通用计划可以避免规划开销，但在某些情况下，由于规划器能够利用参数值信息，定制计划的执行效率会高得多。如果预备语句没有参数，则始终使用通用计划。

默认情况下（服务器配置参数 `plan_cache_mode` 使用默认值 `auto`），服务器会自动为带参数的预备语句选择通用计划或定制计划。目前的规则是前五次执行使用定制计划，随后 Apache Cloudberry 计算这些计划的平均估算代价。接着创建通用计划，并将其估算代价与定制计划的平均代价比较。如果通用计划的代价没有高出平均定制计划代价太多，以至于值得反复重新规划，则后续执行使用通用计划。

可以分别将 `plan_cache_mode` 设为 `force_generic_plan` 或 `force_custom_plan`，覆盖这一启发式规则，强制服务器使用通用计划或定制计划。这主要适用于通用计划的代价估算因某种原因严重失准，导致其实际代价远高于定制计划却仍被选中的情况。

要查看 Apache Cloudberry 为预备语句使用的查询计划，请使用 [EXPLAIN](/cloudberry/reference/sql-stmts/explain/)，例如：

```sql
EXPLAIN EXECUTE <name>(<parameter_values>);
```

如果使用通用计划，计划中将包含参数符号 `$n`；定制计划则会代入提供的参数值。

有关查询规划及 Apache Cloudberry 为此收集的统计信息，参见 [ANALYZE](/cloudberry/reference/sql-stmts/analyze/) 文档。

虽然预备语句的主要目的是避免重复解析分析和规划，但如果语句中使用的数据库对象自上次使用预备语句以来发生了定义（DDL）变化，Apache Cloudberry 就会在使用之前强制重新分析和规划。此外，如果两次使用之间 `search_path` 的值发生变化，语句会使用新的 `search_path` 重新解析。这些规则使预备语句在语义上几乎等价于反复提交相同的查询文本，同时在对象定义未改变时带来性能收益，尤其是在多次使用时最佳计划保持相同的情况下。语义不完全等价的一个例子是：语句以非限定名称引用表，之后在 `search_path` 更靠前的模式中创建了同名新表；由于语句使用的对象没有变化，不会自动重新解析。不过，如果其他变化强制重新解析，后续使用就会引用新表。

可以查询 pg_prepared_statements 系统视图，查看当前会话可用的所有预备语句。

## 示例 {#examples}

为 `INSERT` 语句创建预备语句，然后运行：

```sql
PREPARE fooplan (int, text, bool, numeric) AS
    INSERT INTO foo VALUES($1, $2, $3, $4);
EXECUTE fooplan(1, 'Hunter Valley', 't', 200.00);
```

为 `SELECT` 语句创建预备语句，然后运行。请注意，第二个参数未指定数据类型，因此会从 `$2` 的使用上下文中推断：

```sql
PREPARE usrrptplan (int) AS
    SELECT * FROM users u, logs l WHERE u.usrid=$1 AND u.usrid=l.usrid
    AND l.date = $2;
EXECUTE usrrptplan(1, current_date);
```

## 兼容性 {#compatibility}

SQL 标准包含 `PREPARE` 语句，但它只能用于嵌入式 SQL，并使用不同的语法。

## 另请参阅 {#see-also}

[EXECUTE](/cloudberry/reference/sql-stmts/execute/), [DEALLOCATE](/cloudberry/reference/sql-stmts/deallocate/)
