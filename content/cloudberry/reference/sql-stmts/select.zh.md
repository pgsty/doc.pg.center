---
title: "SELECT"
description: "从表或视图中获取行。"
weight: 1680
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/select.md"
---

## 语法概要 {#synopsis}

```sql
[ WITH [ RECURSIVE ] <with_query> [, ...] ]
SELECT [ALL | DISTINCT [ON (<expression> [, ...])]]
  [* | <expression> [[AS] <output_name>] [, ...]]
  [FROM <from_item> [, ...]]
  [WHERE <condition>]
  [GROUP BY <grouping_element> [, ...]]
  [HAVING <condition> [, ...]]
  [WINDOW <window_name> AS (<window_definition>) [, ...] ]
  [{UNION | INTERSECT | EXCEPT} [ALL | DISTINCT] <select>]
  [ORDER BY <expression> [ASC | DESC | USING <operator>] [NULLS {FIRST | LAST}] [, ...]]
  [LIMIT {<count> | ALL}]
  [OFFSET <start> [ ROW | ROWS ] ]
  [FETCH { FIRST | NEXT } [ <count> ] { ROW | ROWS } ONLY]
  [FOR {UPDATE | NO KEY UPDATE | SHARE | KEY SHARE} [OF <table_name> [, ...]] [NOWAIT | SKIP LOCKED ] [...]]

-- where <from_item> can be one of:

  [ONLY] <table_name> [ * ] [ [ AS ] <alias> [ ( <column_alias> [, ...] ) ] ]
      [ TABLESAMPLE <sampling_method> ( <argument> [, ...] ) [ REPEATABLE ( <seed> ) ] ]
  [LATERAL] ( <select> ) [ AS ] <alias> [( <column_alias> [, ...] ) ]
  <with_query_name> [ [ AS ] <alias> [ ( <column_alias> [, ...] ) ] ]
  [LATERAL] <function_name> ( [ <argument> [, ...] ] )
      [ WITH ORDINALITY ] [ [ AS ] <alias> [ ( <column_alias> [, ...] ) ] ]
  [LATERAL] <function_name> ( [ <argument> [, ...] ] ) [ AS ] <alias> ( <column_definition> [, ...] )
  [LATERAL] <function_name> ( [ <argument> [, ...] ] ) AS ( <column_definition> [, ...] )
  [LATERAL] ROWS FROM( <function_name> ( [ <argument> [, ...] ] ) [ AS ( <column_definition> [, ...] ) ] [, ...] )
      [ WITH ORDINALITY ] [ [ AS ] <alias> [ ( <column_alias> [, ...] ) ] ]
  <from_item> <join_type> <from_item> { ON <join_condition> | USING ( <join_column> [, ...] ) }
  <from_item> NATURAL <join_type> <from_item>
  <from_item> CROSS JOIN <from_item>

-- where <grouping_element> can be one of:

  ()
  <expression>
  ROLLUP (<expression> [,...])
  CUBE (<expression> [,...])
  GROUPING SETS (<grouping_element> [, ...])

-- where <with_query> is:

  <with_query_name> [( <column_name> [, ...] )] AS ( [ NOT ] MATERIALIZED ] ( <select> | <values> | <insert> | <update> | delete )

TABLE [ ONLY ] <table_name> [ * ]
```

## 说明 {#description}

`SELECT` 从零个或多个表中获取行。`SELECT` 的一般处理过程如下：

1. 计算 `WITH` 子句中的所有查询。它们实际上充当可在 `FROM` 列表中引用的临时表。在 `FROM` 中多次引用的 `WITH` 查询只计算一次，除非通过 `NOT MATERIALIZED` 另行指定。（见下文的 [WITH 子句](#the-with-clause)。）
2. 计算 `FROM` 列表中的所有元素。（`FROM` 列表中的每个元素都是实际表或虚拟表。）如果 `FROM` 列表中指定了多个元素，就将它们进行交叉连接。（见下文的 [FROM 子句](#the-from-clause)。）
3. 如果指定了 `WHERE` 子句，则从输出中删除所有不满足条件的行。（见下文的 [WHERE 子句](#the-where-clause)。）
4. 如果指定了 `GROUP BY` 子句，或存在聚合函数调用，则将输出合并为在一个或多个值上匹配的行组，并计算聚合函数的结果。如果存在 `HAVING` 子句，则删除不满足给定条件的组。（见下文的 [GROUP BY 子句](#the-group-by-clause) 和 [HAVING 子句](#the-having-clause)。）
5. 使用每个选定行或行组的 `SELECT` 输出表达式计算实际输出行。（见下文的 [SELECT 列表](#the-select-list)。）
6. `SELECT DISTINCT` 从结果中删除重复行。`SELECT DISTINCT ON` 删除在所有指定表达式上匹配的行。`SELECT ALL`（默认值）返回所有候选行，包括重复行。（见下文的 [DISTINCT 子句](#the-distinct-clause)。）
7. 如果指定了窗口表达式（以及可选的 `WINDOW` 子句），则根据位置（行）型或基于值（范围）型窗口帧组织输出。（见下文的 [WINDOW 子句](#the-window-clause)。）
9. 使用 `UNION`、`INTERSECT` 和 `EXCEPT` 操作符，可以将多个 `SELECT` 语句的输出合并为一个结果集。`UNION` 操作符返回存在于两个结果集之一或两者中的所有行。`INTERSECT` 操作符返回严格同时存在于两个结果集中的所有行。`EXCEPT` 操作符返回存在于第一个结果集但不存在于第二个结果集中的行。在这三种情况下，除非指定 `ALL`，否则都会删除重复行。可以添加无实际作用的关键字 `DISTINCT`，显式指定删除重复行。注意，这里 `DISTINCT` 是默认行为，尽管对 `SELECT` 本身而言 `ALL` 才是默认值。（见下文的 [UNION 子句](#the-union-clause)、[INTERSECT 子句](#the-intersect-clause) 和 [EXCEPT 子句](#the-except-clause)。）
10. 如果指定了 `ORDER BY` 子句，则按指定顺序对返回行排序。如果未指定 `ORDER BY`，则按系统认为生成速度最快的顺序返回行。（见下文的 [ORDER BY 子句](#the-order-by-clause)。）
11. 如果指定了 `LIMIT`（或 `FETCH FIRST`）或 `OFFSET` 子句，`SELECT` 命令只返回结果行的一个子集。（见下文的 [LIMIT 子句](#the-limit-clause)。）
12. 如果指定了 `FOR UPDATE`、`FOR NO KEY UPDATE`、`FOR SHARE` 或 `FOR KEY SHARE`，则在全局死锁检测器停用时（默认情况），`SELECT` 命令会锁定整张表，防止并发更新。启用全局死锁检测器时，它会影响包含锁定子句的某些简单 `SELECT` 语句。（见下文的[锁定子句](#the-locking-clause)。）

必须对 `SELECT` 命令使用的每一列具有 `SELECT` 权限。使用 `FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 或 `FOR KEY SHARE` 还要求具有 `UPDATE` 权限（所选每张表至少有一列需要此权限）。

## 参数 {#parameters}

### `WITH` 子句 {#the-with-clause}

`WITH` 子句允许指定一个或多个子查询，并在主查询中按名称引用它们。在主查询执行期间，子查询实际上充当临时表或视图。每个子查询可以是 `SELECT`、`TABLE`、`VALUES`、`INSERT`、`UPDATE` 或 `DELETE` 语句。在 `WITH` 中编写数据修改语句（`INSERT`、`UPDATE` 或 `DELETE`）时，通常应包含 `RETURNING` 子句。形成主查询所读取临时表的是 `RETURNING` 的输出，*而不是*该语句修改的底层表。如果省略 `RETURNING`，语句仍会运行，但不会产生输出，因此主查询不能将其作为表引用。

包含 `WITH` 子句的 `SELECT` 命令中，该子句最多只能包含一个修改表数据的子句（`INSERT`、`UPDATE` 或 `DELETE` 命令）。

必须为每个 `WITH` 查询指定一个名称（不能使用模式限定）。也可以指定列名列表；如果省略，则从子查询推导列名。

指定 `RECURSIVE` 后，`SELECT` 子查询可以按名称引用自身。此类子查询必须采用以下形式：

```sql
<non_recursive_term> UNION [ALL | DISTINCT] <recursive_term>
```

递归自引用出现在 `UNION` 的右侧。每个查询只允许有一个递归自引用。不支持递归数据修改语句，但可以在数据修改语句中使用递归 `SELECT` 查询的结果。

指定 `RECURSIVE` 关键字后，`WITH` 查询不必按依赖顺序排列：查询可以引用列表中后面的另一个查询。不过不支持循环引用或相互递归。不使用 `RECURSIVE` 关键字时，`WITH` 查询只能引用 `WITH` 列表中位于其前面的同级 `WITH` 查询。

`WITH` 子句包含多个查询时，只应写一次 `RECURSIVE`，并紧跟在 `WITH` 后面。它适用于 `WITH` 子句中的所有查询，但对不使用递归或前向引用的查询没有作用。

`WITH RECURSIVE` 的限制。以下项目不受支持：

- 包含以下内容的递归 `WITH` 子句（位于 `<recursive_term>` 中）。
    -  带自引用的子查询
    -  `DISTINCT` 子句
    -  `GROUP BY` 子句
    -  窗口函数
- `<with_query_name>` 作为集合操作一部分的递归 `WITH` 子句。

下面是集合操作限制的示例。由于集合操作 `UNION` 包含对表 `foo` 的引用，以下查询会返回错误。

```sql
WITH RECURSIVE foo(i) AS (
    SELECT 1
  UNION ALL
    SELECT i+1 FROM (SELECT * FROM foo UNION SELECT 0) bar
)
SELECT * FROM foo LIMIT 5;
```

以下递归 CTE 是允许的，因为集合操作 `UNION` 没有引用 CTE `foo`。

```sql
WITH RECURSIVE foo(i) AS (
    SELECT 1
  UNION ALL
    SELECT i+1 FROM (SELECT * FROM bar UNION SELECT 0) bar, foo
    WHERE foo.i = bar.a
)
SELECT * FROM foo LIMIT 5;
```

主查询和 `WITH` 查询（从概念上说）会同时运行。这意味着，除读取其 `RETURNING` 输出外，其他查询部分看不到 `WITH` 中数据修改语句的影响。如果两个此类数据修改语句试图修改同一行，结果未定义。

`WITH` 查询的一个重要属性是：每次执行主查询时，它只求值一次，即使主查询多次引用它。尤其是，无论主查询是否读取其全部或任何输出，都保证数据修改语句只运行一次且仅运行一次。

不过，可以将 `WITH` 查询标记为 `NOT MATERIALIZED`，以取消这一保证。此时，`WITH` 查询可以像主查询 `FROM` 子句中的简单子 `SELECT` 一样合并到主查询中。如果主查询多次引用该 `WITH` 查询，就会产生重复计算；但如果每次使用只需要 `WITH` 查询总输出中的少量行，`NOT MATERIALIZED` 可以通过允许联合优化查询而带来总体节省。如果 `NOT MATERIALIZED` 附加到递归 `WITH` 查询，或附加到并非无副作用的查询（例如不是不含易变函数的普通 `SELECT`），则会被忽略。

默认情况下，无副作用的 `WITH` 查询如果在主查询的 `FROM` 子句中恰好使用一次，就会合并到主查询中。这使两个查询层可以联合优化，而且这种变化在语义上应当不可见。不过，将 `WITH` 查询标记为 `MATERIALIZED` 可以阻止这种合并。例如，如果将 `WITH` 查询用作优化屏障，防止规划器选择错误计划，这可能很有用。Apache Cloudberry 7 之前的版本从不执行这种合并，因此为旧版本编写的查询可能依赖 `WITH` 充当优化屏障。

更多信息请参阅《Apache Cloudberry 管理员指南》中的“WITH 查询（公用表表达式）”。

### `FROM` 子句 {#the-from-clause}

`FROM` 子句为 `SELECT` 指定一个或多个源表。如果指定多个源，结果就是所有源的笛卡尔积（交叉连接）。不过，通常会通过 `WHERE` 添加限定条件，将返回结果限制为笛卡尔积的一个小子集。

`FROM` 子句可以包含以下元素：

**`table_name`**

已有表或视图的名称（可用模式限定）。如果在表名前指定 `ONLY`，则只扫描该表。如果未指定 `ONLY`，则扫描该表及其所有后代表（如果有）。也可以在表名后指定 `*`，显式表示包含后代表。

**`alias`**

包含别名的 `FROM` 项的替代名称。别名可用于简写，或消除自连接中的歧义（同一表被多次扫描时）。提供别名后，实际表名或函数名会被完全隐藏；例如，对于 `FROM foo AS f`，`SELECT` 的其余部分必须用 `f` 而不能用 `foo` 引用此 `FROM` 项。如果指定别名，还可以指定列别名列表，为表的一个或多个列提供替代名称。

**`TABLESAMPLE sampling_method ( argument [, ...] ) [ REPEATABLE ( seed ) ]`**

table_name 后的 `TABLESAMPLE` 子句表示应使用指定的 sampling_method 获取该表的一个子集。此采样先于 `WHERE` 子句等其他过滤条件执行。Apache Cloudberry 的标准发行版包含两种采样方法：`BERNOULLI` 和 `SYSTEM`。可以通过扩展在数据库中安装其他采样方法。

`BERNOULLI` 和 `SYSTEM` 采样方法都接受一个参数，即要采样的表所占比例，以 0 到 100 之间的百分比表示。该参数可以是任意实数表达式。（其他采样方法可能接受不同或更多参数。）这两种方法都会随机选择表的样本，样本大约包含指定百分比的表行。`BERNOULLI` 方法扫描整张表，并以指定概率独立选择或忽略每一行。`SYSTEM` 方法在块级别采样，每个块都有指定的选中概率；返回每个选中块中的所有行。当指定较小采样百分比时，`SYSTEM` 方法明显快于 `BERNOULLI`，但由于聚簇效应，返回的样本可能不那么随机。

可选的 `REPEATABLE` 子句指定采样方法生成随机数时使用的种子数或表达式。种子值可以是任意非空浮点值。如果表在此期间未发生变化，指定相同种子和参数值的两个查询会选择表的相同样本。不过，不同种子值通常会产生不同样本。如果未指定 `REPEATABLE`，Apache Cloudberry 会根据系统生成的种子为每个查询选择新的随机样本。注意，某些附加采样方法不接受 `REPEATABLE`，每次使用都会生成新样本。

**`select`**

子 `SELECT` 可以出现在 `FROM` 子句中。它的输出在这条 `SELECT` 命令执行期间充当临时表。注意，子 `SELECT` 必须用括号括起，并且*必须*提供别名。这里也可以使用 [VALUES](/cloudberry/reference/sql-stmts/values/) 命令。有关在 Apache Cloudberry 中使用相关子查询的限制，请参阅[兼容性](#compatibility)部分的“非标准子句”。

**`with_query_name`**

在 `FROM` 子句中指定 `WITH` 查询的名称，就像指定表名一样来引用该查询。可以像为表指定别名一样为它提供别名。

对于主查询，`WITH` 查询会隐藏同名表。如有必要，可以使用模式限定的表名引用同名表。

**`function_name`**

函数调用可以出现在 `FROM` 子句中。（这对返回结果集的函数尤其有用，但任何函数都可以使用。）在这条 `SELECT` 命令执行期间，函数的输出充当临时表。函数调用添加可选的 `WITH ORDINALITY` 子句时，Apache Cloudberry 会在函数所有输出列之后追加一列，为每行编号。

可以像为表指定别名一样为函数调用提供别名。如果指定别名，还可以指定列别名列表，为函数复合返回类型的一个或多个属性提供替代名称；如果存在 `ORDINALITY`，也包括它添加的列。

可以将多个函数调用放在 `ROWS FROM( ... )` 中，组合成一个 `FROM` 子句项。此项的输出依次连接每个函数的第一行、第二行等。如果某些函数产生的行少于其他函数，则用空值替代缺少的数据，因此返回的总行数始终与产生行数最多的函数相同。

如果函数已定义为返回 `record` 数据类型，则必须提供别名或关键字 `AS`，后面跟着形如 `( <column_name> <data_type> [, ... ] )` 的列定义列表。列定义列表必须与函数实际返回的列数和列类型匹配。

使用 `ROWS FROM( ... )` 语法时，如果其中一个函数需要列定义列表，最好将列定义列表放在 `ROWS FROM( ... )` 内部的函数调用之后。只有在其中只有一个函数且没有 `WITH ORDINALITY` 子句时，才能将列定义列表放在 `ROWS FROM( ... )` 构造之后。

要将 `ORDINALITY` 与列定义列表一起使用，必须使用 `ROWS FROM( ... )` 语法，并将列定义列表放在 `ROWS FROM( ... )` 内部。

**`join_type`**

以下之一：

- `[INNER] JOIN`
- `LEFT [OUTER] JOIN`
- `RIGHT [OUTER] JOIN`
- `FULL [OUTER] JOIN`

对于 `INNER` 和 `OUTER` 连接类型，必须指定连接条件，且必须恰好是 `NATURAL`、`ON <join_condition>` 或 `USING ( <join_column> [, ...])` 中的一种。含义见下文。

JOIN 子句组合两个 `FROM` 项；为方便起见，下面称它们为“表”，但实际上可以是任何类型的 `FROM` 项。如有必要，请使用括号确定嵌套顺序。没有括号时，`JOIN` 从左到右嵌套。`JOIN` 的绑定优先级高于分隔 `FROM` 列表项的逗号。所有 `JOIN` 选项都只是记法上的便利，并没有实现不了的功能；使用普通 `FROM` 和 `WHERE` 即可达到相同效果。

`LEFT OUTER JOIN` 返回限定笛卡尔积中的所有行（即所有满足连接条件的组合行），并额外返回左表中没有右表匹配行的每一行的一个副本。通过插入空值补齐右侧列后，这些左表行扩展到连接表的完整宽度。注意，判断哪些行匹配时只考虑 `JOIN` 子句自身的条件，外部条件之后才应用。

相应地，`RIGHT OUTER JOIN` 返回所有连接行，并为每个未匹配的右表行返回一行（左侧用空值扩展）。这只是记法上的便利，因为交换左右表即可将其转换为 `LEFT OUTER JOIN`。

`FULL OUTER JOIN` 返回所有连接行，并为每个未匹配的左表行返回一行（右侧用空值扩展），再为每个未匹配的右表行返回一行（左侧用空值扩展）。

**`ON join_condition`**

join_condition 是一个求值结果为 `boolean` 类型的表达式（类似 `WHERE` 子句），指定连接中哪些行被视为匹配。

**`USING (join_column [, ...])`**

`USING ( a, b, ... )` 形式的子句是 `ON left_table.a = right_table.a AND left_table.b = right_table.b ...` 的简写。此外，`USING` 表示连接输出中每对等价列只包含一列，而不是两列都包含。

**`NATURAL`**

`NATURAL` 是 `USING` 列表的简写，该列表包含两个表中名称相同的所有列。如果没有同名列，`NATURAL` 等价于 `ON TRUE`。

**`CROSS JOIN`**

`CROSS JOIN` 等价于 `INNER JOIN ON (TRUE)`，也就是限定条件不会删除任何行。它们产生简单的笛卡尔积，与在 `FROM` 顶层列出两个表时得到的结果相同，但会受连接条件（如果有）的限制。

**`LATERAL`**

`LATERAL` 关键字可以放在子 `SELECT FROM` 项之前，使子 `SELECT` 可以引用 `FROM` 列表中位于它之前的 `FROM` 项的列。（没有 `LATERAL` 时，Apache Cloudberry 会独立计算每个子 `SELECT`，因此不能交叉引用其他 `FROM` 项。）

`LATERAL` 也可以放在函数调用 `FROM` 项之前。此时它是无实际作用的关键字，因为函数表达式可以引用之前的 `FROM` 项。

`LATERAL` 项可以位于 `FROM` 列表顶层，也可以位于 `JOIN` 树中。后一种情况下，如果它位于某个 `JOIN` 的右侧，还可以引用该连接左侧的任何项。

当 `FROM` 项包含 `LATERAL` 交叉引用时，按以下方式求值：对于提供被引用列的 `FROM` 项中的每一行，或提供这些列的多个 `FROM` 项中的每组行，使用该行或行组的列值计算 `LATERAL` 项。然后将生成的行照常与产生它们的行连接。对列源表中的每一行或每组行重复此过程。

列源表必须与 `LATERAL` 项执行 `INNER` 或 `LEFT` 连接，否则没有定义明确的行集，无法据此计算 `LATERAL` 项的每个行集。因此，虽然 `<X> RIGHT JOIN LATERAL <Y>` 这样的构造在语法上有效，但 Apache Cloudberry 不允许 `<Y>` 引用 `<X>`。

### `WHERE` 子句 {#the-where-clause}

可选的 `WHERE` 子句一般形式如下：

```sql
WHERE <condition>
```

其中 condition 是求值结果为 `boolean` 类型的任意表达式。将实际行值代入变量引用后，凡不满足该条件的行都会从输出中删除。条件返回 true 时，行满足该条件。

### `GROUP BY` 子句 {#the-group-by-clause}

可选的 `GROUP BY` 子句一般形式如下：

```sql
GROUP BY <grouping_element> [, ...]
```

其中 `<grouping_element>` 可以是以下之一：

```sql
()
<expression>
ROLLUP (<expression> [,...])
CUBE (<expression> [,...])
GROUPING SETS ((<grouping_element> [, ...]))
```

`GROUP BY` 将所有在分组表达式上具有相同值的选定行压缩为一行。grouping_element 中使用的表达式可以是输入列名、输出列（`SELECT` 列表项）的名称或序号，也可以是由输入列值构成的任意表达式。存在歧义时，`GROUP BY` 名称会被解释为输入列名，而不是输出列名。

如果分组元素中存在 `GROUPING SETS`、`ROLLUP` 或 `CUBE` 中的任何一个，则整个 `GROUP BY` 子句定义若干独立分组集。其效果等同于在各个子查询之间构造 `UNION ALL`，每个子查询都将相应分组集作为自己的 `GROUP BY` 子句。有关分组集处理的更多详情，请参阅 PostgreSQL 文档中的 [GROUPING SETS、CUBE 和 ROLLUP](https://www.postgresql.org/docs/12/queries-table-expressions.html#QUERIES-GROUPING-SETS)。

如果使用了聚合函数，则会在组成每个组的所有行上计算这些函数，为每个组生成一个值。（如果存在聚合函数但没有 `GROUP BY` 子句，则查询被视为只有一个组，该组包含所有选定行。）还可以为聚合函数调用附加 `FILTER` 子句，进一步过滤传给每个聚合函数的行集。存在 `FILTER` 子句时，只有与该子句匹配的行才会包含在该聚合函数的输入中。

存在 `GROUP BY` 或任何聚合函数时，`SELECT` 列表表达式不能引用未分组列，除非位于聚合函数中，或未分组列对分组列具有函数依赖；否则未分组列可能有多个值可供返回。如果分组列（或其中的一个子集）是包含未分组列的表的主键，则存在函数依赖。

请记住，所有聚合函数都会在计算 `HAVING` 子句或 `SELECT` 列表中的任何“标量”表达式之前完成求值。这意味着，例如，不能使用 `CASE` 表达式跳过聚合函数的求值。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 不能与 `GROUP BY` 一起指定。

Apache Cloudberry 还提供以下 OLAP 分组扩展（通常称为*超组*）：

**`ROLLUP`**

`ROLLUP` 分组是 `GROUP BY` 子句的扩展，它按照分组列（或表达式）列表，从最详细层级逐级汇总到总计，创建聚合小计。`ROLLUP` 接受有序的分组列列表，计算 `GROUP BY` 子句指定的标准聚合值，然后从右向左遍历列表，逐步创建更高层级的小计，最后创建总计。可以将 `ROLLUP` 分组视为一系列分组集。例如：

```sql
GROUP BY ROLLUP (a,b,c) 
```

等价于：

```sql
GROUP BY GROUPING SETS( (a,b,c), (a,b), (a), () ) 
```

注意，`ROLLUP` 中的 n 个元素会转换为 n+1 个分组集。此外，在 `ROLLUP` 中指定分组表达式的顺序很重要。

**`CUBE`**

`CUBE` 分组是 `GROUP BY` 子句的扩展，它为给定分组列（或表达式）列表的所有可能组合创建小计。从多维分析角度看，`CUBE` 会生成指定维度的数据立方体可以计算出的所有小计。例如：

```sql
GROUP BY CUBE (a,b,c) 
```

等价于：

```sql
GROUP BY GROUPING SETS( (a,b,c), (a,b), (a,c), (b,c), (a), 
(b), (c), () ) 
```

注意，`CUBE` 中的 n 个元素会转换为 2n 个分组集。任何需要交叉表报告的场景都可以考虑使用 `CUBE`。`CUBE` 通常最适合使用多个维度的列，而不是表示单个维度不同层级的列。例如，常见的交叉表可能需要按月份、州和产品的所有组合生成小计。

**`GROUPING SETS`**

可以在 `GROUP BY` 子句中使用 `GROUPING SETS` 表达式，有选择地指定要创建的组集。这样可以跨多个维度进行精确指定，而无须计算完整的 `ROLLUP` 或 `CUBE`。例如：

```sql
GROUP BY GROUPING SETS( (a,c), (a,b) )
```

使用 `ROLLUP`、`CUBE` 或 `GROUPING SETS` 等分组扩展子句时，会出现两个问题。首先，如何确定哪些结果行是小计，以及给定小计的确切聚合层级；或者说，如何区分同时包含已存储 `NULL` 值和由 `ROLLUP` 或 `CUBE` 创建的“NULL”值。其次，当 `GROUP BY` 子句中指定了重复分组集时，如何确定哪些结果行是重复行？可以在 `SELECT` 列表中使用以下两个附加分组函数来帮助处理：

- **grouping(column [, ...])** — `grouping` 函数可应用于一个或多个分组属性，用于区分超级聚合行和普通分组行。这有助于区分超级聚合行中表示所有值集合的“NULL”和普通行中的 `NULL`。此函数的每个参数都会生成一位，即 `1` 或 `0`；`1` 表示结果行是超级聚合行，`0` 表示结果行来自普通分组。`grouping` 函数将这些位作为二进制数处理，再转换为十进制整数并返回。

- **group_id()** — 对于包含重复分组集的分组扩展查询，使用 `group_id` 函数识别输出中的重复行。所有*唯一*分组集输出行的 `<group_id>` 值为 0。对检测到的每个重复分组集，`group_id` 函数都会分配一个大于 0 的 `<group_id>` 值。某个重复分组集中的所有输出行都由同一个 `<group_id>` 值标识。

### `HAVING` 子句 {#the-having-clause}

可选的 `HAVING` 子句一般形式如下：

```sql
HAVING <condition>
```

其中 `<condition>` 与 `WHERE` 子句中指定的相同。

`HAVING` 会删除不满足条件的组行。`HAVING` 与 `WHERE` 不同：`WHERE` 在应用 `GROUP BY` 之前过滤单行，而 `HAVING` 过滤 `GROUP BY` 创建的组行。`<condition>` 中引用的每一列都必须明确引用分组列，除非该引用位于聚合函数中，或未分组列对分组列具有函数依赖。

存在 `HAVING` 时，即使没有 `GROUP BY` 子句，查询也会成为分组查询。这与查询包含聚合函数但没有 `GROUP BY` 子句时的情况相同。所有选定行都视为组成一个组，`SELECT` 列表和 `HAVING` 子句只能在聚合函数中引用表列。如果 `HAVING` 条件为 true，查询会输出一行；如果不为 true，则输出零行。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 不能与 `HAVING` 一起指定。

### `WINDOW` 子句 {#the-window-clause}

可选的 `WINDOW` 子句指定查询 `SELECT` 列表或 `ORDER BY` 子句中窗口函数的行为。`WINDOW` 子句的一般形式如下：

```sql
WINDOW <window_name> AS ( <window_definition> ) [, ...]
```

其中 `<window_name>` 是可以在 `OVER` 子句或后续窗口定义中引用的名称，`<window_definition>` 为：

```sql
[<existing_window_name>]
[PARTITION BY <expression> [, ...]]
[ORDER BY <expression> [ASC | DESC | USING <operator>] [NULLS {FIRST | LAST}] [, ...] ]
[<frame_clause>] 
```

`WINDOW` 子句项不必在任何地方引用；如果查询未使用它，就会被简单忽略。完全可以不使用 `WINDOW` 子句而使用窗口函数，因为窗口函数调用可以直接在其 `OVER` 子句中指定窗口定义。不过，当多个窗口函数需要相同窗口定义时，`WINDOW` 子句可以减少重复输入。

例如：

```sql
SELECT vendor, rank() OVER (mywindow) FROM sale
GROUP BY vendor
WINDOW mywindow AS (ORDER BY sum(prc*qty));
```

**`existing_window_name`**

如果指定 existing_window_name，则它必须引用 `WINDOW` 列表中的较早项；新窗口从该项复制分区子句，以及其中存在的排序子句。新窗口不能指定自己的 `PARTITION BY` 子句，只有复制的窗口没有排序子句时才能指定 `ORDER BY`。新窗口始终使用自己的帧子句；复制的窗口不能指定帧子句。

**`PARTITION BY`**

`PARTITION BY` 子句根据指定表达式的唯一值将结果集组织为逻辑组。`PARTITION BY` 子句的元素与 [GROUP BY 子句](#the-group-by-clause)的元素在很大程度上采用相同解释方式，但它们始终是简单表达式，不能是输出列的名称或编号。另一个区别是，这些表达式可以包含聚合函数调用，而普通 `GROUP BY` 子句不允许。这里之所以允许，是因为窗口化发生在分组和聚合之后。与窗口函数一起使用时，会对每个分区独立应用函数。例如，在 `PARTITION BY` 后跟列名时，结果集会按该列的不同值分区。省略时，整个结果集视为一个分区。

**`ORDER BY`**

同样，`ORDER BY` 列表的元素与 [ORDER BY 子句](#the-order-by-clause)的元素大体采用相同解释方式，但表达式始终被视为简单表达式，不能是输出列的名称或编号。

> **注意** `ORDER BY` 子句的元素决定结果集每个分区中的行如何排序。省略时，按效率最高的任意顺序返回行，顺序可能变化。

**`frame_clause`**

可选的 frame_clause 为依赖帧的窗口函数定义*窗口帧*（并非所有窗口函数都依赖帧）。窗口帧是查询中每一行的相关行集合（称为*当前行*）。frame_clause 可以是以下之一：

```sql
{ RANGE | ROWS | GROUPS } <frame_start> [ <frame_exclusion> ]
{ RANGE | ROWS | GROUPS } BETWEEN <frame_start> AND <frame_end> [ <frame_exclusion> ]
```

其中 `<frame_start>` 和 `<frame_end>` 可以是以下之一：

```sql
UNBOUNDED PRECEDING
<offset> PRECEDING
CURRENT ROW
<offset> FOLLOWING
UNBOUNDED FOLLOWING
```

`<frame_exclusion>` 可以是以下之一：

```sql
EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```

如果省略 `<frame_end>`，默认为 `CURRENT ROW`。限制条件是：`<frame_start>` 不能是 `UNBOUNDED FOLLOWING`，`<frame_end>` 不能是 `UNBOUNDED PRECEDING`，并且 `<frame_end>` 选项在上面的 `<frame_start>` 和 `<frame_end>` 选项列表中不能早于 `<frame_start>` 选项出现。例如，不允许 `RANGE BETWEEN CURRENT ROW AND <offset> PRECEDING`。

默认帧选项是 `RANGE UNBOUNDED PRECEDING`，这与 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` 相同；它将窗口帧设为从分区开始到当前行的最后一个同等行（窗口的 `ORDER BY` 子句认为与当前行等价的行；如果没有 `ORDER BY`，所有行都是同等行）的所有行。通常，`UNBOUNDED PRECEDING` 表示帧从分区第一行开始，`UNBOUNDED FOLLOWING` 表示帧在分区最后一行结束，与 `RANGE`、`ROWS` 或 `GROUPS` 模式无关。在 `ROWS` 模式中，`CURRENT ROW` 表示帧从当前行开始或在当前行结束；但在 `RANGE` 或 `GROUPS` 模式中，它表示帧从 `ORDER BY` 排序中的当前行第一个或最后一个同等行开始或结束。`<offset> PRECEDING` 和 `<offset> FOLLOWING` 选项的含义取决于帧模式。在 `ROWS` 模式中，`<offset>` 是一个整数，表示帧在当前行之前或之后多少行开始或结束。

在 `GROUPS` 模式中，`<offset>` 是一个整数，表示帧在当前行所属同等行组之前或之后多少个同等行组开始或结束；同等行组是根据窗口 `ORDER BY` 子句判断为等价的行组。在 `RANGE` 模式中，使用 `<offset>` 选项要求窗口定义中恰好有一个 `ORDER BY` 列。此时，帧包含排序列值与当前行排序列值的差在指定方向上不超过 `<offset>` 的行：`PRECEDING` 表示向前，`FOLLOWING` 表示向后。在这些情况下，`<offset>` 表达式的数据类型取决于排序列的数据类型。对于数值排序列，通常与排序列类型相同；对于日期时间排序列，则为 `interval`。在所有这些情况下，`<offset>` 的值必须非空且非负。此外，虽然 offset 不必是简单常量，但不能包含变量、聚合函数或窗口函数。

`<frame_exclusion>` 选项允许从帧中排除当前行周围的行，即使根据帧起点和终点选项它们本应被包含。`EXCLUDE CURRENT ROW` 将当前行从帧中排除。`EXCLUDE GROUP` 将当前行及其同等行从帧中排除。`EXCLUDE TIES` 将当前行的所有同等行从帧中排除，但不排除当前行本身。`EXCLUDE NO OTHERS` 只是显式指定不排除当前行或其同等行这一默认行为。

请注意，如果 `ORDER BY` 排序不能唯一确定行的顺序，`ROWS` 模式可能产生不可预测的结果。`RANGE` 和 `GROUPS` 模式旨在确保 `ORDER BY` 中属于同级的行以相同方式处理：给定同等行组中的所有行要么都在帧中，要么都从帧中排除。

使用 `ROWS`、`RANGE` 或 `GROUPS` 子句表达窗口边界。窗口边界可以是分区中的一行、多行或所有行。可以将窗口边界表示为相对于当前行值偏移的数据值范围（`RANGE`）、相对于当前行偏移的行数（`ROWS`），或同等行组的数量（`GROUPS`）。使用 `RANGE` 或 `GROUPS` 子句时，还必须使用 `ORDER BY` 子句，因为计算窗口需要先对值排序。此外，`ORDER BY` 子句不能包含多个表达式，且表达式的结果必须是日期或数值。使用 `ROWS`、`RANGE` 或 `GROUPS` 子句时，如果只指定起始行，则将当前行作为窗口的末行。

**PRECEDING** — `PRECEDING` 子句以当前行为参考点定义窗口的第一行。起始行以当前行之前的行数表示。例如，在 `ROWS` 帧中，`5 PRECEDING` 将窗口起点设为当前行之前第五行。在 `RANGE` 帧中，它将窗口起点设为排序列值按给定顺序比当前行早 5 的第一行。如果按日期升序排列，则是当前行之前 5 天内的第一行。`UNBOUNDED PRECEDING` 将窗口第一行设为分区第一行。

**BETWEEN** — `BETWEEN` 子句以当前行为参考点定义窗口的第一行和最后一行。第一行和最后一行分别用当前行之前和之后的行数表示。例如，`BETWEEN 3 PRECEDING AND 5 FOLLOWING` 将窗口起点设为当前行之前第三行，终点设为当前行之后第五行。使用 `BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` 可以将窗口起点和终点分别设为分区的第一行和最后一行。如果未指定 `ROWs`、`RANGE` 或 `GROUPS` 子句，这就是默认行为。

**FOLLOWING** — `FOLLOWING` 子句以当前行为参考点定义窗口的最后一行。最后一行以当前行之后的行数表示。例如，在 `ROWS` 帧中，`5 FOLLOWING` 将窗口终点设为当前行之后第五行。在 `RANGE` 帧中，它将窗口终点设为排序列值按给定顺序比当前行晚 5 的最后一行。如果按日期升序排列，则是当前行之后 5 天内的最后一行。使用 `UNBOUNDED FOLLOWING` 将窗口最后一行设为分区最后一行。

如果未指定 `ROWS`、`RANGE` 或 `GROUPS` 子句，则使用 `ORDER BY` 时，窗口边界从分区第一行（`UNBOUNDED PRECEDING`）开始，到当前行（`CURRENT ROW`）结束；未指定 `ORDER BY` 时，窗口从分区第一行（`UNBOUNDED PRECEDING`）开始，到分区最后一行（`UNBOUNDED FOLLOWING`）结束。

`WINDOW` 子句用于指定查询[SELECT 列表](#the-select-list)或[ORDER BY 子句](#the-order-by-clause)中窗口函数的行为。这些函数可以在其 `OVER` 子句中按名称引用 `WINDOW` 子句项。不过，`WINDOW` 子句项不必在任何地方引用；如果查询未使用它，就会被简单忽略。完全可以不使用 `WINDOW` 子句而使用窗口函数，因为窗口函数调用可以直接在其 `OVER` 子句中指定窗口定义。不过，当多个窗口函数需要相同窗口定义时，`WINDOW` 子句可以减少重复输入。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 不能与 `WINDOW` 一起指定。

### `SELECT` 列表 {#the-select-list}

`SELECT` 列表（位于关键字 `SELECT` 与 `FROM` 之间）指定构成 `SELECT` 语句输出行的表达式。这些表达式可以（通常也确实会）引用在 `FROM` 子句中计算出的列。

`SELECT` 列表中的表达式可以是常量值、列引用、操作符调用、函数调用、聚合表达式、窗口表达式、标量子查询等。有些构造可以归类为表达式，但不遵循通用语法规则；它们通常具有函数或操作符的语义。有关 SQL 值表达式和函数调用的信息，请参阅《Apache Cloudberry 管理员指南》中的“查询数据”。

与表一样，`SELECT` 的每个输出列都有名称。在简单 `SELECT` 中，这个名称只用于显示时标记列；但当 `SELECT` 是更大查询的子查询时，更大查询会将该名称视为子查询生成的虚拟表的列名。要指定输出列名称，请在列表达式后写 `AS <output_name>`。（可以省略 `AS`，但只有所需输出名称不匹配任何 SQL 关键字时才可以。为防止将来增加关键字，始终可以写 `AS` 或用双引号括起输出名称。）如果未指定列名，Apache Cloudberry 会自动选择名称。如果列的表达式是简单列引用，所选名称与列名相同；在更复杂的情况下，可能使用函数名或类型名，也可能退回到 `?column?` 或 `columnN` 这样的生成名称。

输出列的名称可以在 `ORDER BY` 和 `GROUP BY` 子句中引用列值，但不能在 `WHERE` 或 `HAVING` 子句中引用；后两者必须指定表达式本身。

可以在输出列表中使用 `*` 代替表达式，简写表示所选行的所有列。也可以使用 `<table_name>.*` 简写表示仅来自该表的列。在这些情况下不能通过 `AS` 指定新名称；输出列名称将与表列名称相同。

根据 SQL 标准，输出列表中的表达式应在应用 `DISTINCT`、`ORDER BY` 或 `LIMIT` 之前计算。使用 `DISTINCT` 时这显然是必要的，否则无法明确哪些值需要去重。不过，在许多情况下，如果输出表达式在 `ORDER BY` 和 `LIMIT` 之后计算会很方便，尤其当输出列表包含易变函数或昂贵函数时。这样，函数求值顺序更直观，也不会对最终不出现在输出中的行求值。Apache Cloudberry 实际上会在排序和限制之后计算输出表达式，只要这些表达式没有被 `DISTINCT`、`ORDER BY` 或 `GROUP BY` 引用。（反例是 `SELECT f(x) FROM tab ORDER BY 1`，此时显然必须在排序前计算 `f(x)`。）包含返回集合函数的输出表达式实际上在排序后、限制前计算，因此 `LIMIT` 会截断返回集合函数的输出。

> **注意** Apache Cloudberry 7 之前的版本不保证输出表达式相对于排序和限制的求值时机；时机取决于所选查询计划的形式。

### `DISTINCT` 子句 {#the-distinct-clause}

指定 `SELECT DISTINCT` 时，从结果集中删除所有重复行（每组重复行保留一行）。`SELECT ALL` 表示相反行为，即保留所有行，这是默认值。

`SELECT DISTINCT ON ( <expression> [, ...] )` 只保留给定表达式求值相等的每组行中的第一行。`DISTINCT ON` 表达式采用与 `ORDER BY` 相同的规则解释（见上文）。注意，除非使用 `ORDER BY` 确保目标行排在第一位，否则每组中的“第一行”不可预测。例如：

```sql
SELECT DISTINCT ON (location) location, time, report
    FROM weather_reports
    ORDER BY location, time DESC;
```

获取每个地点最近的天气报告。不过，如果没有使用 `ORDER BY` 强制每个地点按时间降序排列，就会得到每个地点某个不可预测时间的报告。

`DISTINCT ON` 表达式必须与最左侧的 `ORDER BY` 表达式匹配。`ORDER BY` 子句通常还会包含额外表达式，用于决定每个 `DISTINCT ON` 组内行的优先级。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 不能与 `DISTINCT` 一起指定。

### `UNION` 子句 {#the-union-clause}

`UNION` 子句的一般形式如下：

```sql
<select_statement> UNION [ALL | DISTINCT] <select_statement>
```

`<select_statement>` 是不带 `ORDER BY`、`LIMIT`、`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 或 `FOR KEY SHARE` 子句的任意 `SELECT` 语句。（如果用括号括起子查询表达式，可以将 `ORDER BY` 和 `LIMIT` 附加到子查询表达式；不使用括号时，这些子句会被视为应用于 `UNION` 的结果，而不是其右侧输入表达式。）

`UNION` 操作符计算所涉及 `SELECT` 语句返回行的集合并集。如果一行至少出现在一个结果集中，就属于两个结果集的集合并集。作为 `UNION` 直接操作数的两个 `SELECT` 语句必须产生相同数量的列，对应列的数据类型必须兼容。

除非指定 `ALL` 选项，否则 `UNION` 的结果不包含重复行。`ALL` 阻止删除重复项。（因此，`UNION ALL` 通常明显快于 `UNION`；可以使用 `ALL` 时应使用它。）可以指定 `DISTINCT`，显式表示删除重复行这一默认行为。

同一 `SELECT` 语句中的多个 `UNION` 操作符从左到右求值，除非括号另有指示。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 既不能在 `UNION` 结果上指定，也不能在 `UNION` 的任何输入上指定。

### `INTERSECT` 子句 {#the-intersect-clause}

`INTERSECT` 子句的一般形式如下：

```sql
<select_statement> INTERSECT [ALL | DISTINCT] <select_statement>
```

`<select_statement>` 是不带 `ORDER BY`、`LIMIT`、`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 或 `FOR KEY SHARE` 子句的任意 `SELECT` 语句。

`INTERSECT` 操作符计算所涉及 `SELECT` 语句返回行的集合交集。如果一行同时出现在两个结果集中，就属于这两个结果集的交集。

除非指定 `ALL` 选项，否则 `INTERSECT` 的结果不包含重复行。使用 `ALL` 时，如果某行在左表中重复 `<m>` 次，在右表中重复 `<n>` 次，则它会在结果集中出现 `min(<m>, <n>)` 次。可以写 `DISTINCT`，显式表示删除重复行这一默认行为。

同一 `SELECT` 语句中的多个 `INTERSECT` 操作符从左到右求值，除非括号另有规定。`INTERSECT` 的绑定优先级高于 `UNION`。也就是说，`A UNION B INTERSECT C` 会按 `A UNION (B INTERSECT C)` 解释。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 既不能在 `INTERSECT` 结果上指定，也不能在 `INTERSECT` 的任何输入上指定。

### `EXCEPT` 子句 {#the-except-clause}

`EXCEPT` 子句的一般形式如下：

```sql
<select_statement> EXCEPT [ALL | DISTINCT] <select_statement>
```

`<select_statement>` 是不带 `ORDER BY`、`LIMIT`、`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 或 `FOR KEY SHARE` 子句的任意 `SELECT` 语句。

`EXCEPT` 操作符计算存在于左侧 `SELECT` 语句结果中、但不存在于右侧结果中的行集合。

除非指定 `ALL` 选项，否则 `EXCEPT` 的结果不包含重复行。使用 `ALL` 时，如果某行在左表中重复 `<m>` 次，在右表中重复 `<n>` 次，则它会在结果集中出现 `max(<m>-<n>,0)` 次。可以写 `DISTINCT`，显式表示删除重复行这一默认行为。

同一 `SELECT` 语句中的多个 `EXCEPT` 操作符从左到右求值，除非括号另有规定。`EXCEPT` 与 `UNION` 处于同一绑定层级。

目前，`FOR NO KEY UPDATE`、`FOR UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 既不能在 `EXCEPT` 结果上指定，也不能在 `EXCEPT` 的任何输入上指定。

### `ORDER BY` 子句 {#the-order-by-clause}

可选的 `ORDER BY` 子句一般形式如下：

```sql
ORDER BY <expression> [ASC | DESC | USING <operator>] [NULLS {FIRST | LAST}] [,...]
```

`ORDER BY` 子句使结果行按指定表达式排序。如果根据最左侧表达式两个行相等，则继续根据下一个表达式比较，依此类推。如果根据所有指定表达式都相等，则按实现依赖的顺序返回。

每个 `<expression>` 可以是输出列（`SELECT` 列表项）的名称或序号，也可以是由输入列值构成的任意表达式。

序号表示输出列的序号（从左到右的位置）。此功能使得可以基于没有唯一名称的列定义排序。它从来不是绝对必要的，因为始终可以使用 `AS` 子句为输出列指定名称。

也可以在 `ORDER BY` 子句中使用任意表达式，包括未出现在 `SELECT` 输出列表中的列。因此，以下语句有效：

```sql
SELECT name FROM distributors ORDER BY code;
```

此功能的限制是：应用于 `UNION`、`INTERSECT` 或 `EXCEPT` 子句结果的 `ORDER BY` 子句只能指定输出列名称或编号，不能指定表达式。

如果 `ORDER BY` 表达式是一个简单名称，同时匹配输出列名和输入列名，则 `ORDER BY` 将其解释为输出列名。这与 `GROUP BY` 在相同情况下的选择相反。这种不一致是为了兼容 SQL 标准。

可以选择在 `ORDER BY` 子句中任意表达式后添加关键字 `ASC`（升序）或 `DESC`（降序）。如果未指定，默认假定为 `ASC`。也可以在 `USING` 子句中指定特定排序操作符名。`ASC` 通常等价于 `USING <`，`DESC` 通常等价于 `USING >`。（不过，用户定义数据类型的创建者可以精确定义默认排序顺序，且该顺序可能对应其他名称的操作符。）

如果指定 `NULLS LAST`，空值排在所有非空值之后；如果指定 `NULLS FIRST`，空值排在所有非空值之前。如果两者都未指定，则指定或隐含 `ASC` 时默认为 `NULLS LAST`，指定 `DESC` 时默认为 `NULLS FIRST`（也就是默认将空值视为大于非空值）。指定 `USING` 时，默认空值顺序取决于操作符是小于操作符还是大于操作符。

注意，排序选项只适用于它们前面的那个表达式；例如，`ORDER BY x, y DESC` 与 `ORDER BY x DESC, y DESC` 含义不同。

字符串数据按照创建数据库时确定的、特定于区域设置的排序规则顺序排序。如有需要，可以在表达式中加入 `COLLATE` 子句覆盖此顺序，例如 `ORDER BY mycolumn COLLATE "en_US"`。

字符串数据按照适用于被排序列的排序规则排序。如有需要，可以在表达式中加入 `COLLATE` 子句覆盖此规则，例如 `ORDER BY mycolumn COLLATE "en_US"`。有关定义排序规则的信息，请参阅 [CREATE COLLATION](/cloudberry/reference/sql-stmts/create-collation/)。

### `LIMIT` 子句 {#the-limit-clause}

`LIMIT` 子句由两个相互独立的子句组成：

```sql
LIMIT {<count> | ALL}
OFFSET <start>
```

`<count>` 指定要返回的最大行数，`<start>` 指定开始返回行之前要跳过的行数。如果同时指定两者，则先跳过 `<start>` 行，再开始计数要返回的 `<count>` 行。

如果 `<count>` 表达式求值为空，则按 `LIMIT ALL` 处理，即不设限制。如果 `<start>` 求值为空，则与 `OFFSET 0` 的处理相同。

SQL:2008 引入了实现相同结果的另一种语法，Apache Cloudberry 也支持该语法：

```sql
OFFSET <start> [ ROW | ROWS ]
    FETCH { FIRST | NEXT } [ <count> ] { ROW | ROWS } ONLY
```

在此语法中，标准要求 `<start>` 或 `<count>` 值必须是字面量常量、参数或变量名；作为 Apache Cloudberry 的扩展，也允许其他表达式，但通常需要用括号括起以避免歧义。如果 `FETCH` 子句省略 `<count>`，则默认为 1。`ROW` 和 `ROWS`，以及 `FIRST` 和 `NEXT` 都是无实际作用的关键字，不影响这些子句的效果。根据标准，如果同时存在，`OFFSET` 子句必须位于 `FETCH` 子句之前；但 Apache Cloudberry 允许任意顺序。

使用 `LIMIT` 时，最好使用 `ORDER BY` 子句将结果行限定为唯一顺序。否则会得到不可预测的查询行子集——你可能想要第十到第二十行，但它们是按什么顺序排列的第十到第二十行？如果不指定 `ORDER BY`，就不知道顺序是什么。

查询优化器在生成查询计划时会考虑 `LIMIT`，因此，根据使用的 `LIMIT` 和 `OFFSET`，很可能得到不同的计划（从而得到不同的行顺序）。因此，使用不同的 `LIMIT/OFFSET` 值选择查询结果的不同子集时，如果不通过 `ORDER BY` 强制可预测的结果顺序，就会得到不一致的结果。这不是缺陷，而是 SQL 的固有结果：除非使用 `ORDER BY` 限定顺序，否则 SQL 不承诺以任何特定顺序交付查询结果。

如果没有 `ORDER BY` 强制选择确定的子集，甚至多次执行同一个 `LIMIT` 查询，也可能返回表中不同的行子集。同样，这不是错误；Apache Cloudberry 不保证这种情况下结果具有确定性。

### `LOCKING` 子句 {#the-locking-clause}

`FOR UPDATE`、`FOR NO KEY UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 是*锁定子句*，会影响 `SELECT` 从表中获取行时如何加锁。全局死锁检测器会影响包含锁定子句（`FOR <lock_strength>`）的 `SELECT` 查询所使用的锁。通过将 gp_enable_global_deadlock_detector 配置参数设为 `on` 可以启用全局死锁检测器。

锁定子句的一般形式如下：

```sql
FOR <lock_strength> [OF <table_name> [ , ... ] ] [ NOWAIT | SKIP LOCKED ] 
```

`<lock_strength>` 可以是以下值之一：

- `UPDATE` - 使用 `EXCLUSIVE` 锁锁定表。
- `NO KEY UPDATE` - 使用 `EXCLUSIVE` 锁锁定表。
- `SHARE` - 使用 `ROW SHARE` 锁锁定表。
- `KEY SHARE` - 使用 `ROW SHARE` 锁锁定表。

全局死锁检测器停用时（默认情况），Apache Cloudberry 使用指定的锁。

启用全局死锁检测器时，对于包含锁定子句的简单 `SELECT` 查询，使用 `ROW SHARE` 锁锁定表，查询计划包含 `lockrows` 节点。包含锁定子句的简单 `SELECT` 查询必须满足以下所有条件：

- 锁定子句位于顶层 `SELECT` 上下文中。
- `FROM` 子句只包含一个表，且该表不是视图或 AO 表。
- `SELECT` 命令不包含 `UNION` 或 `INTERSECT` 等集合操作。
- `SELECT` 命令不包含子查询。

否则，包含锁定子句的 `SELECT` 查询的表锁行为与停用全局死锁检测器时相同。

> **注意** 全局死锁检测器也会影响 `DELETE` 和 `UPDATE` 操作所使用的锁。默认情况下，Apache Cloudberry 对堆表执行 `DELETE` 和 `UPDATE` 操作时会获取表上的 `EXCLUSIVE` 锁。启用全局死锁检测器时，堆表上 `DELETE` 和 `UPDATE` 操作的锁模式为 `ROW EXCLUSIVE`。

有关每种行级锁模式的更多信息，请参阅 PostgreSQL 文档中的[显式锁定](https://www.postgresql.org/docs/12/explicit-locking.html)。

要防止操作等待其他事务提交，请使用 `NOWAIT` 或 `SKIP LOCKED` 选项。使用 `NOWAIT` 时，如果选定行无法立即锁定，语句会报错而不是等待。使用 `SKIP LOCKED` 时，任何无法立即锁定的选定行都会被跳过。跳过已锁定的行会产生不一致的数据视图，因此不适合通用场景，但可以避免多个消费者访问类似队列表时发生锁竞争。注意，`NOWAIT` 和 `SKIP LOCKED` 只适用于行级锁；所需的 `ROW SHARE` 表级锁仍会按普通方式获取。如果需要在不等待的情况下获取表级锁，可以先对带 `NOWAIT` 选项的 [LOCK](/cloudberry/reference/sql-stmts/lock/) 执行操作。

如果锁定子句中指定了具体表，则只锁定来自这些表的行；`SELECT` 中使用的其他表仍按普通方式读取。不带表列表的锁定子句会影响语句使用的所有表。如果锁定子句应用于视图或子查询，则会影响该视图或子查询使用的所有表。不过，这些子句不适用于主查询引用的 `WITH` 查询。如果希望在 `WITH` 查询中锁定行，请在 `WITH` 查询内部指定锁定子句。

如果需要为不同表指定不同的锁定行为，可以编写多个锁定子句。如果同一表被多个锁定子句提及（或隐式影响），则按其中最强的锁定子句处理。同样，只要影响某表的任一子句指定了相应选项，就按 `NOWAIT` 处理；否则，如果任一子句要求跳过锁定行，就按 `SKIP LOCKED` 处理。

不能在无法将返回行明确对应到单个表行的上下文中使用锁定子句，例如不能与聚合一起使用。

锁定子句出现在 `SELECT` 查询顶层时，锁定的行正好是查询返回的行；对于连接查询，锁定的是对返回连接行有贡献的行。此外，按查询快照满足查询条件的行也会被锁定，即使它们在快照之后被更新、不再满足查询条件而不会返回。如果使用 `LIMIT`，返回足够满足限制的行后就停止加锁（但注意，被 `OFFSET` 跳过的行也会被锁定）。同样，如果游标的查询使用了锁定子句，则只锁定游标实际取回或经过的行。

锁定子句出现在子 `SELECT` 中时，锁定的是子查询返回给外层查询的行。由于外层查询的条件可能被用于优化子查询执行，这可能少于仅检查子查询时看起来会锁定的行数。例如：

```sql
SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss WHERE col1 = 5;
```

即使该条件在文本上不在子查询中，也只会锁定 `col1 = 5` 的行。

在 `READ COMMITTED` 事务隔离级别下运行 `SELECT`，并同时使用 `ORDER BY` 和锁定子句时，可能返回乱序行。这是因为先应用 `ORDER BY`：命令先对结果排序，但随后可能在尝试获取一行或多行的锁时阻塞。`SELECT` 解除阻塞后，某些排序列值可能已经被修改，导致这些行看起来乱序（尽管按原始列值顺序它们是有序的）。如有需要，可以将 `FOR UPDATE/SHARE` 子句放入子查询来避免这种情况，例如：

```sql
SELECT * FROM (SELECT * FROM mytable FOR UPDATE) ss ORDER BY column1;
```

注意，这会锁定 `mytable` 的所有行，而顶层的 `FOR UPDATE` 只会锁定实际返回的行。这可能造成显著的性能差异，尤其是 `ORDER BY` 与 `LIMIT` 或其他限制一起使用时。因此，只有预期排序列会被并发更新且必须严格按顺序返回结果时，才建议使用此技术。

在 `REPEATABLE READ` 或 `SERIALIZABLE` 事务隔离级别下，这会导致串行化失败（`SQLSTATE` 为 `40001`），因此在这些隔离级别下不可能收到乱序行。

## TABLE 命令 {#the-table-command}

命令

```sql
TABLE <name>
```

等价于

```sql
SELECT * FROM <name>
```

它可以作为顶层命令，也可以在复杂查询的部分位置作为更简洁的语法变体。只有 `WITH`、`UNION`、`INTERSECT`、`EXCEPT`、`ORDER BY`、`LIMIT`、`OFFSET`、`FETCH` 和 `FOR` 锁定子句可以与 `TABLE` 一起使用；不能使用 `WHERE` 子句或任何形式的聚合。

## 示例 {#examples}

将表 `films` 与表 `distributors` 连接：

```sql
SELECT f.title, f.did, d.name, f.date_prod, f.kind
  FROM distributors d, JOIN films f USING (did);
```

对所有电影的 `length` 列求和，并按 `kind` 对结果分组：

```sql
SELECT kind, sum(length) AS total FROM films GROUP BY kind;
```

对所有电影的 `length` 列求和，按 `kind` 对结果分组，并显示总时长小于 5 小时的组：

```sql
SELECT kind, sum(length) AS total FROM films GROUP BY kind 
  HAVING sum(length) < interval '5 hours';
```

按电影的 `kind` 和 `distributor` 计算所有销售额的小计与总计。

```sql
SELECT kind, distributor, sum(prc*qty) FROM sales
GROUP BY ROLLUP(kind, distributor)
ORDER BY 1,2,3;
```

根据总销售额计算电影发行商的排名：

```sql
SELECT distributor, sum(prc*qty), 
       rank() OVER (ORDER BY sum(prc*qty) DESC) 
FROM sales
GROUP BY distributor ORDER BY 2 DESC;
```

下面两个示例使用等价的方法，按第二列（`name`）的内容对各个结果排序：

```sql
SELECT * FROM distributors ORDER BY name;
SELECT * FROM distributors ORDER BY 2;
```

下一个示例展示如何求表 `distributors` 和 `actors` 的并集，并将结果限制为各表中以字母 `W` 开头的行。由于只需要不同的行，因此省略关键字 `ALL`：

```sql
SELECT distributors.name
  FROM distributors
  WHERE distributors.name LIKE 'W%'
UNION
SELECT actors.name
  FROM actors
  WHERE actors.name LIKE 'W%';
```

此例展示在 `FROM` 子句中使用函数的方法，包括带列定义列表和不带列定义列表的情况：

```sql
CREATE FUNCTION distributors(int) RETURNS SETOF distributors 
AS $$ SELECT * FROM distributors WHERE did = $1; $$ LANGUAGE 
SQL;
SELECT * FROM distributors(111);

CREATE FUNCTION distributors_2(int) RETURNS SETOF record AS 
$$ SELECT * FROM distributors WHERE did = $1; $$ LANGUAGE 
SQL;
SELECT * FROM distributors_2(111) AS (dist_id int, dist_name text);
```

此例使用添加了序号列的函数：

```sql
SELECT * FROM unnest(ARRAY['a','b','c','d','e','f']) WITH ORDINALITY;
```

此例使用简单的 `WITH` 子句：

```sql
WITH test AS (
  SELECT random() as x FROM generate_series(1, 3)
  )
SELECT * FROM test
UNION ALL
SELECT * FROM test; 
```

此例使用 `WITH` 子句，仅显示销售额最高地区中各产品的销售总额。

```sql
WITH regional_sales AS 
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
  ), top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > (SELECT SUM(total_sales) FROM
       regional_sales)
  )
SELECT region, product, SUM(quantity) AS product_units,
   SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions) 
GROUP BY region, product;
```

此例也可以不使用 `WITH` 子句，但那样需要两层嵌套的子 `SELECT` 语句。

此例使用 `WITH RECURSIVE` 子句，从只记录直接下属的表中找出员工 Mary 的所有直接或间接下属，以及他们与 Mary 之间相隔的层级：

```sql
WITH RECURSIVE employee_recursive(distance, employee_name, manager_name) AS (
    SELECT 1, employee_name, manager_name
    FROM employee
    WHERE manager_name = 'Mary'
  UNION ALL
    SELECT er.distance + 1, e.employee_name, e.manager_name
    FROM employee_recursive er, employee e
    WHERE er.employee_name = e.manager_name
  )
SELECT distance, employee_name FROM employee_recursive;
```

递归查询的典型形式是初始条件，后接 `UNION [ALL]`，再接查询的递归部分。必须确保查询的递归部分最终不再返回元组，否则查询会无限循环。

此例使用 `LATERAL`，为表 `manufacturers` 的每一行应用返回集合的函数 `get_product_names()`：

```sql
SELECT m.name AS mname, pname
  FROM manufacturers m, LATERAL get_product_names(m.id) pname;
```

由于这是内连接，当前没有任何产品的制造商不会出现在结果中。如果希望结果也包含这些制造商的名称，可以按如下方式编写查询：

```sql
SELECT m.name AS mname, pname
  FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true;
```

## 兼容性 {#compatibility}

`SELECT` 语句兼容 SQL 标准，但包含一些扩展，也缺少一些功能。

**省略 FROM 子句**

Apache Cloudberry 允许省略 `FROM` 子句。一个直接的用途是计算简单表达式的结果。例如：

```sql
SELECT 2+2;
```

某些其他 SQL 数据库无法这样做，必须引入一个虚拟单行表，再对其执行 `SELECT`。

注意，如果没有指定 `FROM` 子句，查询就不能引用任何数据库表。例如，以下查询无效：

```sql
SELECT distributors.* WHERE distributors.name = 'Westward';
```

在早期版本中，将服务器配置参数 `add_missing_from` 设为 true，可以让 Apache Cloudberry 为查询引用的每张表在查询的 `FROM` 子句中添加一个隐式条目。现在已不允许这样做。

**空 SELECT 列表**

`SELECT` 后的输出表达式列表可以为空，从而生成零列结果表。根据 SQL 标准，这不是有效语法。Apache Cloudberry 允许这样做，以便与允许零列表的行为保持一致。不过，使用 `DISTINCT` 时不允许空列表。

**省略 AS 关键字**

在 SQL 标准中，只要新列名是有效列名（即不与任何保留关键字相同），就可以省略输出列名前可选的关键字 `AS`。Apache Cloudberry 稍严格一些：如果新列名与任何关键字匹配，无论是否保留，都必须使用 `AS`。建议使用 `AS` 或用双引号括起输出列名，以防与今后新增的关键字冲突。

在 `FROM` 项中，标准和 Apache Cloudberry 都允许在非保留关键字别名前省略 `AS`。但由于语法歧义，这不适用于输出列名。

**ONLY 与继承**

SQL 标准要求使用 `ONLY` 时将表名用括号括起，例如：

```sql
SELECT * FROM ONLY (tab1), ONLY (tab2) WHERE ...
```

Apache Cloudberry 将这些括号视为可选。

Apache Cloudberry 允许在末尾写 `*`，显式指定包含子表的非 `ONLY` 行为。标准不允许这样做。

注意：上述几点同样适用于所有支持 `ONLY` 选项的 SQL 命令。

**TABLESAMPLE 子句限制**

目前只有普通表和物化视图接受 `TABLESAMPLE` 子句。根据 SQL 标准，它应当可以应用于任何 `FROM` 项。

**FROM 中的函数调用**

Apache Cloudberry 允许将函数调用直接写成 `FROM` 列表的一项。SQL 标准则要求将此类函数调用包在子 `SELECT` 中；即语法 `FROM func(...) alias` 大致等价于 `FROM LATERAL (SELECT func(...)) alias`。注意，这里隐含 `LATERAL`；这是因为标准要求 `FROM` 中的 `UNNEST()` 项具有 `LATERAL` 语义。Apache Cloudberry 对 `UNNEST()` 与其他返回集合的函数采用相同处理方式。

**GROUP BY 和 ORDER BY 可用的命名空间**

在 SQL-92 标准中，`ORDER BY` 子句只能使用输出列名或编号，而 `GROUP BY` 子句只能使用基于输入列名的表达式。Apache Cloudberry 扩展了这两个子句，使其也允许另一种选择（但存在歧义时，使用标准的解释）。Apache Cloudberry 还允许这两个子句指定任意表达式。注意，表达式中出现的名称始终被视为输入列名，而不是输出列名。

SQL:1999 及更高版本采用略有不同的定义，并非完全向上兼容 SQL-92。不过，在大多数情况下，Apache Cloudberry 对 `ORDER BY` 或 `GROUP BY` 表达式的解释与 SQL:1999 相同。

**函数依赖**

只有表的主键包含在 `GROUP BY` 列表中时，Apache Cloudberry 才识别函数依赖（从而允许在 `GROUP BY` 中省略其他列）。SQL 标准还规定了一些应当识别的其他条件。

**LIMIT 与 OFFSET**

`LIMIT` 和 `OFFSET` 子句是 Apache Cloudberry 特有的语法，MySQL 也使用这种语法。SQL:2008 标准引入了 `OFFSET .. FETCH {FIRST|NEXT} ...` 子句来实现相同功能，如上文的 [LIMIT 子句](#the-limit-clause)所示。IBM DB2 也使用这种语法。（Oracle 应用经常采用一种变通方法，通过自动生成的 `rownum` 列实现这些子句的效果；Apache Cloudberry 没有该列。）

**FOR NO KEY UPDATE、FOR UPDATE、FOR SHARE 和 FOR KEY SHARE**

虽然 SQL 标准中存在 `FOR UPDATE`，但标准只允许将它用作 `DECLARE CURSOR` 的选项。Apache Cloudberry 还允许在任何 `SELECT` 查询以及子 `SELECT` 中使用它，这属于扩展。`FOR NO KEY UPDATE`、`FOR SHARE` 和 `FOR KEY SHARE` 变体，以及 `NOWAIT` 和 `SKIP LOCKED` 选项，都不在标准中。

**WITH 中的数据修改语句**

Apache Cloudberry 允许将 `INSERT`、`UPDATE` 和 `DELETE` 用作 `WITH` 查询。SQL 标准没有这一功能。

**非标准子句**

SQL 标准没有定义 `DISTINCT ON` 子句。

`ROWS FROM( ... )` 是对 SQL 标准的扩展。

`WITH` 的 `MATERIALIZED` 和 `NOT MATERIALIZED` 选项是对 SQL 标准的扩展。

**STABLE 和 VOLATILE 函数的使用限制**

为防止 Apache Cloudberry 中各个 Segment 的数据不同步，如果归类为 `STABLE` 或 `VOLATILE` 的函数包含 SQL 或以任何方式修改数据库，就不能在 Segment 数据库级别运行该函数。更多信息请参阅 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

## 另请参阅 {#see-also}

[EXPLAIN](/cloudberry/reference/sql-stmts/explain/)
