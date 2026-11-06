---
title: "WITH 查询（公用表表达式）"
linkTitle: "公用表表达式"
description: "`WITH` 子句提供了一种编写辅助语句、供更大查询使用的方式。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/cte-queries.md"
---

这些语句通常称为公用表表达式（Common Table Expressions，CTE），可以理解为定义了仅在一次查询中存在的临时表。

> [!NOTE]
> 在 Apache Cloudberry 中使用 `WITH` 子句时存在以下限制：
>
> - 对于包含 `WITH` 子句的 `SELECT` 命令，该子句最多只能包含一个修改表数据的子句（`INSERT`、`UPDATE` 或 `DELETE` 命令）。
> - 对于包含 `WITH` 子句的数据修改命令（`INSERT`、`UPDATE` 或 `DELETE`），该子句只能包含 `SELECT` 命令，不能包含数据修改命令。

默认情况下，Apache Cloudberry 为 `WITH` 子句启用 `RECURSIVE` 关键字。可以通过将服务器配置参数 `gp_recursive_cte` 设置为 `false` 来停用 `RECURSIVE`。

## WITH 子句中的 SELECT {#select-in-a-with-clause}

CTE 的一种用途是将复杂查询拆分为更简单的部分。本节中的示例展示了如何将 `WITH` 子句与 `SELECT` 命令结合使用。这些示例中的 `WITH` 子句同样可以与 `INSERT`、`UPDATE` 或 `DELETE` 一起使用。

`WITH` 子句中的 `SELECT` 命令在主查询的每次执行中只计算一次，即使主查询或同级 `WITH` 子句多次引用它。因此，可以将多个位置需要的昂贵计算放在 `WITH` 子句中，从而避免重复工作。另一个可能的用途是避免带副作用的函数被意外多次计算。但这也有另一面：与普通子查询相比，优化器不太能够将主查询中的限制条件下推到 `WITH` 查询中。`WITH` 查询通常会按照书写方式执行，不会抑制主查询之后可能丢弃的行。不过，如果对该查询的引用只需要有限数量的行，执行可能会提前停止。

下面的示例查询仅显示销量最高区域中的每种产品的销售总额：

```sql
WITH regional_sales AS (
     SELECT region, SUM(amount) AS total_sales
     FROM orders
     GROUP BY region
  ), top_regions AS (
     SELECT region
     FROM regional_sales
     WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
  )
SELECT region,
    product,
    SUM(quantity) AS product_units,
    SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;
```

`WITH` 子句定义了两个名为 `regional_sales` 和 `top_regions` 的辅助语句，其中 `regional_sales` 的输出用于 `top_regions`，而 `top_regions` 的输出用于主 `SELECT` 查询。也可以不使用 `WITH` 子句来编写该查询，但那样需要两层嵌套的子 `SELECT`。

指定可选的 `RECURSIVE` 关键字后，`WITH` 子句可以执行标准 SQL 中通常无法执行的操作。使用 `RECURSIVE` 时，`WITH` 查询可以引用自身的输出。下面这个简单示例计算从 1 到 100 的整数之和：

```sql
WITH RECURSIVE t(n) AS (
    VALUES (1)
  UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

递归 `WITH` 查询的一般形式总是遵循以下模式：先是一个*非递归项*，然后是 `UNION`（或 `UNION ALL`），再后是一个*递归项*；其中只有*递归项*可以包含对查询输出的引用。

```sql
<non_recursive_term> UNION [ ALL ] <recursive_term>
```

包含 `UNION [ ALL ]` 的递归 `WITH` 查询的执行方式如下：

- 计算非递归项。对于 `UNION`（而不是 `UNION ALL`），丢弃重复行。将所有剩余行加入递归查询的结果，并将这些行放入临时*工作表*中。
- 只要工作表不为空，就重复执行以下步骤：
    1. 计算递归项，将工作表的当前内容代入递归自引用。对于 `UNION`（而不是 `UNION ALL`），丢弃重复行以及与此前任何结果行重复的行。将所有剩余行加入递归查询的结果，并将这些行放入临时*中间表*中。
    2. 用中间表的内容替换*工作表*的内容，然后清空*中间表*。

    > [!NOTE]
    > `RECURSIVE` 允许递归地指定查询，但 Apache Cloudberry 在内部会迭代执行此类查询。

在上面的示例中，工作表在每一步都只有一行，其值依次为 1 到 100。第 100 步中，由于 `WHERE` 子句没有输出，查询终止。

递归 `WITH` 查询通常用于处理层级数据或树形结构数据。例如，已知一个只展示直接包含关系的表时，下面的查询可以定位产品的所有直接和间接子部件：

```sql
WITH RECURSIVE included_parts(sub_part, part, quantity) AS (
    SELECT sub_part, part, quantity FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part, p.quantity * pr.quantity
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
)
SELECT sub_part, SUM(quantity) as total_quantity
FROM included_parts
GROUP BY sub_part;
```

使用递归 `WITH` 查询时，必须确保查询的递归部分最终不再返回元组，否则查询会无限循环。

对于某些查询，使用 `UNION` 而不是 `UNION ALL` 可以通过丢弃与此前输出行重复的行，确保查询的递归部分最终不再返回元组。然而，循环通常并不涉及完全重复的输出行：只检查一个或几个字段，往往就足以判断是否再次到达同一个节点。处理此类情况的标准方法是计算一个包含已访问值的数组。例如，考虑下面使用 `graph` 表和 `link` 字段的查询：

```sql
WITH RECURSIVE search_graph(id, link, data, depth) AS (
    SELECT g.id, g.link, g.data, 1
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1
    FROM graph g, search_graph sg
    WHERE g.id = sg.link
)
SELECT * FROM search_graph;
```

如果 `link` 关系包含循环，这个查询就会循环执行。由于该查询需要输出 `depth`，将 `UNION ALL` 改为 `UNION` 并不能消除循环。相反，需要在沿着特定链接路径前进时识别是否再次到达同一行。下面这个修改后的查询向容易循环的查询添加了 `path` 和 `cycle` 两列：

```sql
WITH RECURSIVE search_graph(id, link, data, depth, path, cycle) AS (
    SELECT g.id, g.link, g.data, 1,
      ARRAY[g.id],
      false
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1,
      path || g.id,
      g.id = ANY(path)
    FROM graph g, search_graph sg
    WHERE g.id = sg.link AND NOT cycle
)
SELECT * FROM search_graph;
```

除了检测循环之外，数组值本身也很有用，因为它表示到达任意特定行所经过的“路径”。

在通常需要检查多个字段来识别循环的情况下，请使用行数组。例如，如果需要比较字段 `f1` 和 `f2`：

```sql
WITH RECURSIVE search_graph(id, link, data, depth, path, cycle) AS (
    SELECT g.id, g.link, g.data, 1,
      ARRAY[ROW(g.f1, g.f2)],
      false
    FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1,
      path || ROW(g.f1, g.f2),
      ROW(g.f1, g.f2) = ANY(path)
    FROM graph g, search_graph sg
    WHERE g.id = sg.link AND NOT cycle
)
SELECT * FROM search_graph;
```

**提示：** 如果只需检查一个字段来识别循环，可以省略 `ROW()` 语法。这样会使用简单数组，而不是复合类型数组，从而提高效率。

**提示：** 递归查询求值算法按广度优先搜索顺序生成输出。可以将外层查询的 `ORDER BY` 设置为按这种方式构造的“路径”列，从而按深度优先搜索顺序显示结果。

如果不确定查询是否可能无限循环，一个有用的测试方法是在主查询中加入 `LIMIT`。例如，下面的查询如果没有 `LIMIT` 子句将永远循环：

```sql
WITH RECURSIVE t(n) AS (
    SELECT 1
  UNION ALL
    SELECT n+1 FROM t
)
SELECT n FROM t LIMIT 100;
```

这种方法有效，是因为 Apache Cloudberry 只会计算主查询实际获取的 `WITH` 查询行数。*不建议在生产环境中使用此方法*，因为其他系统的行为可能不同。此外，如果外层查询对递归 `WITH` 的结果排序，或者将结果与另一个表连接，这种方法可能无效，因为在这些情况下，外层查询通常会尝试获取 `WITH` 查询的全部输出。

`WITH` 查询的一个有用特性是，即使主查询或同级 `WITH` 查询多次引用它，通常也只会在主查询的每次执行中计算一次。因此，可以将多个位置需要的昂贵计算放在 `WITH` 查询中，从而避免重复工作。另一个可能的用途是避免带副作用的函数被意外多次计算。但这也有另一面：优化器无法将主查询中的限制条件下推到被多次引用的 `WITH` 查询中，因为这可能会影响 `WITH` 查询输出的所有使用位置，而本应只影响其中一个位置。Apache Cloudberry 会按照书写方式执行被多次引用的 `WITH` 查询，不会抑制主查询之后可能丢弃的行。（不过，如上所述，如果对该查询的引用只需要有限数量的行，执行可能会提前停止。）

如果 `WITH` 查询是非递归且无副作用的（也就是说，它是一个不含易变函数的 `SELECT`），则可以将其折叠到主查询中，从而对两个查询层级进行联合优化。默认情况下，当主查询只引用该 `WITH` 查询一次时会这样做；当主查询多次引用 `WITH` 查询时则不会。可以通过指定 `MATERIALIZED` 强制单独计算 `WITH` 查询，也可以通过指定 `NOT MATERIALIZED` 强制将其合并到主查询中。后一种选择可能导致重复计算 `WITH` 查询，但如果每次使用只需要 `WITH` 查询输出的一小部分，即完整 `WITH` 查询输出的一小部分，最终仍可能节省开销。

下面是这些规则的一个简单示例：

```sql
WITH w AS (
    SELECT * FROM big_table
)
SELECT * FROM w WHERE key = 123;
```

这个 `WITH` 查询会被折叠，生成与下面查询相同的执行计划：

```sql
SELECT * FROM big_table WHERE key = 123;
```

具体来说，如果 `key` 上存在索引，Apache Cloudberry 会使用它只获取 `key = 123` 的行。另一方面，在下面的查询中：

```sql
WITH w AS (
    SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

`WITH` 查询会被物化，生成一个 `big_table` 的临时副本，然后将该副本与自身连接，而无法利用索引。将查询写成下面这样，执行效率会高得多：

```sql
WITH w AS NOT MATERIALIZED (
    SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

这样，主查询的限制条件就可以直接应用于对 `big_table` 的扫描。

下面是一个不适合使用 `NOT MATERIALIZED` 的示例：

```sql
WITH w AS (
    SELECT key, very_expensive_function(val) as f FROM some_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.f = w2.f;
```

在这里，将 `WITH` 查询物化可以确保 Apache Cloudberry 对每一行表数据只计算一次 `very_expensive_function`，而不是两次。

## WITH 子句中的数据修改语句 {#data-modifying-statements-in-a-with-clause}

对于 `SELECT` 命令，可以在 `WITH` 子句中使用 `INSERT`、`UPDATE` 或 `DELETE` 数据修改命令。这样可以在同一个查询中执行多个不同的操作。

`WITH` 子句中的数据修改语句只运行一次，并且总会执行完毕，不受主查询是否读取了全部输出（甚至是否读取任何输出）的影响。这与在 `WITH` 子句中使用 `SELECT` 时的规则不同：后者只要主查询需要其输出，`SELECT` 就会继续执行。

下面这个简单的 CTE 查询从 `products` 中删除行。`WITH` 子句中的 `DELETE` 通过其 `RETURNING` 子句返回被指定行的内容。

```sql
WITH deleted_rows AS (
    DELETE FROM products
    WHERE
        "date" >= '2010-10-01' AND
        "date" < '2010-11-01'
    RETURNING *
)
SELECT * FROM deleted_rows;
```

如前面的示例所示，`WITH` 子句中的数据修改语句必须有 `RETURNING` 子句。形成临时表的是 `RETURNING` 子句的输出，而不是数据修改语句的目标表；其余查询可以引用这个临时表。如果 `WITH` 中的数据修改语句缺少 `RETURNING` 子句，则不会形成临时表，后续查询也不能引用它。Apache Cloudberry 仍会运行该语句。

如果启用了可选的 `RECURSIVE` 关键字，数据修改语句中不允许递归自引用。在某些情况下，可以通过引用递归 `WITH` 的输出来绕过此限制。例如，下面的查询会删除产品的所有直接和间接子部件：

```sql
WITH RECURSIVE included_parts(sub_part, part) AS (
    SELECT sub_part, part FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
  )
DELETE FROM parts
  WHERE part IN (SELECT part FROM included_parts);
```

`WITH` 子句中的子语句会彼此并发运行，并与主查询并发运行。因此，在包含数据修改语句的 `WITH` 中，指定的更新实际发生的顺序是不可预测的。所有语句都使用同一个*快照*。语句的效果对目标表不可见。这减轻了行更新实际顺序不可预测的影响，也意味着 `RETURNING` 数据是不同 `WITH` 子语句与主查询之间传递变更的唯一方式。

在这个示例中，外层 `SELECT` 返回 `WITH` 子句中的 `UPDATE` 执行之前的原始价格：

```sql
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM products;
```

在这个示例中，外层 `SELECT` 返回更新后的数据：

```sql
WITH t AS (
    UPDATE products SET price = price * 1.05
    RETURNING *
)
SELECT * FROM t;
```

不支持在一条语句中两次更新同一行。这类语句的效果不可预测。只有一次修改会生效，但很难（有时甚至不可能）预测究竟是哪一次修改发生。

`WITH` 子句中数据修改语句的任何目标表都不能有条件规则、`ALSO` 规则，也不能有会展开为多个语句的 `INSTEAD` 规则。

## 注意事项 {#considerations}

构造 `WITH` 查询时，请注意以下事项：

- `SELECT FOR UPDATE` 不能内联。
- Apache Cloudberry 只有在请求时（通过指定 `NOT MATERIALIZED`）才会内联多次引用的 CTE。
- 如果多次引用的 CTE 包含外部自引用，则不能内联。
- 如果 CTE 包含易变函数，Apache Cloudberry 不会内联。
- 子查询或 CTE 中的 `ORDER BY` 不会强制整个查询排序。
- Apache Cloudberry 始终会物化查询中的 CTE 项。由于这些原因：
    - 本应只访问少量数据的查询可能会改为读取整张表，并可能溢出到临时文件。
    - CTE 项中不允许使用 `UPDATE` 或 `DELETE FROM` 语句，因为 CTE 项更像只读临时表，而不是动态视图。
- 尽管内联通常能带来很大收益，但也存在某些边界情况，内联反而不利；例如，一个复杂表达式会在多个位置被内联时。
- GPORCA 查询优化器不支持 `[NOT] MATERIALIZED`。
