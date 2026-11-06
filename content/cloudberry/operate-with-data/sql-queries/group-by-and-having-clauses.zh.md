---
title: "GROUP BY 和 HAVING 子句"
description: "通过 `WHERE` 筛选后，派生输入表可能会使用 `GROUP BY` 子句进行分组，并使用 `HAVING` 子句消除分组行。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/group-by-and-having-clauses.md"
---

```sql
SELECT select_list
    FROM ...
    [WHERE ...]
    GROUP BY grouping_column_reference [, grouping_column_reference]...
```

`GROUP BY` 子句用于将表中在所有所列列上取值都相同的行归为一组。列的列出顺序无关紧要。其作用是将具有共同值的每组行合并为一个组行，该组行代表组中的所有行。这样做是为了消除输出中的冗余，和／或计算适用于这些组的聚合。例如：

```sql
=> SELECT * FROM test1;
 x | y
---+---
 a | 3
 c | 2
 b | 5
 a | 1
(4 rows)

=> SELECT x FROM test1 GROUP BY x;
 x
---
 a
 b
 c
(3 rows)
```

在第二个查询中，不能写成 `SELECT * FROM test1 GROUP BY x`，因为没有一个单独的 y 列值可以与每个组关联。分组列可以在选择列表中引用，因为它们在每个组中只有一个值。

一般来说，如果对表进行了分组，则除非出现在聚合表达式中，否则不能引用未列在 `GROUP BY` 中的列。包含聚合表达式的示例如下：

```sql
=> SELECT x, sum(y) FROM test1 GROUP BY x;
 x | sum
---+-----
 a |   4
 b |   5
 c |   2
(3 rows)
```

这里的 sum 是一个聚合函数，用于计算整个组的单个值。

> [!TIP]
> 不使用聚合表达式进行分组，实际上会计算某列不同值的集合。也可以使用 `DISTINCT` 子句实现这一点。

下面是另一个示例：它计算每种产品的总销售额（而不是所有产品的总销售额）：

```sql
SELECT product_id, p.name, (sum(s.units) * p.price) AS sales
    FROM products p LEFT JOIN sales s USING (product_id)
    GROUP BY product_id, p.name, p.price;
```

在此示例中，列 `product_id`、`p.name` 和 `p.price` 必须位于 `GROUP BY` 子句中，因为它们在查询选择列表中被引用（但见下文）。列 `s.units` 不必位于 `GROUP BY` 列表中，因为它只用于聚合表达式（`sum(...)`），该表达式表示某种产品的销售额。对于每种产品，查询都会返回一行汇总，描述该产品的所有销售情况。

如果 products 表的设置使 `product_id` 成为主键，那么在上述示例中只按 `product_id` 分组就足够了，因为 name 和 price 函数依赖于产品 ID，因此对于每个产品 ID 组，要返回哪个 name 和 price 值不会有歧义。

在严格 SQL 中，`GROUP BY` 只能按源表的列进行分组，但 Apache Cloudberry 扩展了这一规则，也允许 `GROUP BY` 按选择列表中的列进行分组。也允许使用值表达式而不是简单列名进行分组。

如果使用 `GROUP BY` 对表进行了分组，但只关注某些组，则可以使用 `HAVING` 子句（与 `WHERE` 子句类似）从结果中消除其他组。语法如下：

```sql
SELECT select_list FROM ... [WHERE ...] GROUP BY ... HAVING boolean_expression
```

`HAVING` 子句中的表达式既可以引用分组表达式，也可以引用未分组表达式（后者必然涉及聚合函数）。

示例：

```sql
=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING sum(y) > 3;
 x | sum
---+-----
 a |   4
 b |   5
(2 rows)

=> SELECT x, sum(y) FROM test1 GROUP BY x HAVING x < 'c';
 x | sum
---+-----
 a |   4
 b |   5
(2 rows)
```

再看一个更贴近实际的示例：

```sql
SELECT product_id, p.name, (sum(s.units) * (p.price - p.cost)) AS profit
    FROM products p LEFT JOIN sales s USING (product_id)
    WHERE s.date > CURRENT_DATE - INTERVAL '4 weeks'
    GROUP BY product_id, p.name, p.price, p.cost
    HAVING sum(p.price * s.units) > 5000;
```

在上面的示例中，`WHERE` 子句按一个未分组的列筛选行（该表达式仅对最近四周的销售为 true），而 `HAVING` 子句将输出限制为总毛销售额超过 5000 的组。请注意，查询的所有部分不一定需要使用相同的聚合表达式。

如果查询包含聚合函数调用但没有 `GROUP BY` 子句，仍然会发生分组：结果是一个组行（如果该单行随后被 `HAVING` 消除，也可能没有行）。即使查询包含 `HAVING` 子句但没有任何聚合函数调用或 `GROUP BY` 子句，情况也相同。
