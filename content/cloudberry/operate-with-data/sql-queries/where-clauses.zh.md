---
title: "WHERE 子句"
description: "使用 WHERE 搜索条件筛选查询行，包括谓词、连接和相关子查询。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/where-clauses.md"
---

`WHERE` 子句的语法如下：

```sql
WHERE search_condition
```

其中，`search_condition` 是返回 boolean 类型值的任意值表达式。

完成 `FROM` 子句的处理后，会根据搜索条件检查派生虚拟表中的每一行。如果条件结果为 `true`，则该行保留在输出表中；否则（也就是说，如果结果为 false 或 null），该行会被丢弃。搜索条件通常至少引用 `FROM` 子句生成的表中的一列；这不是必需的，但除此之外，`WHERE` 子句将几乎没有用处。

> [!NOTE]
> 内连接的连接条件既可以写在 `WHERE` 子句中，也可以写在 `JOIN` 子句中。例如，以下表表达式是等价的：
>
> ```sql
> FROM a, b WHERE a.id = b.id AND b.val > 5
> ```
>
> 以及：
>
> ```sql
> FROM a INNER JOIN b ON (a.id = b.id) WHERE b.val > 5
> ```
>
> 甚至可以是：
>
> ```sql
> FROM a NATURAL JOIN b WHERE b.val > 5
> ```
>
> 你选择其中哪一种主要是风格问题。`FROM` 子句中的 `JOIN` 语法可能不如其他 SQL 数据库管理系统中的语法具有可移植性，尽管它属于 SQL 标准。对于外连接则没有选择：必须在 `FROM` 子句中完成。外连接的 `ON` 或 `USING` 子句不等价于 `WHERE` 条件，因为它既会添加行（对于不匹配的输入行），也会删除最终结果中的行。

以下是 WHERE 子句的一些示例：

```sql
SELECT ... FROM fdt WHERE c1 > 5

SELECT ... FROM fdt WHERE c1 IN (1, 2, 3)

SELECT ... FROM fdt WHERE c1 IN (SELECT c1 FROM t2)

SELECT ... FROM fdt WHERE c1 IN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10)

SELECT ... FROM fdt WHERE c1 BETWEEN (SELECT c3 FROM t2 WHERE c2 = fdt.c1 + 10) AND 100

SELECT ... FROM fdt WHERE EXISTS (SELECT c1 FROM t2 WHERE c2 > fdt.c1)
```

`fdt` 是 `FROM` 子句中派生的表。不满足 `WHERE` 子句搜索条件的行会从 `fdt` 中删除。请注意值表达式中标量子查询的使用。与任何其他查询一样，子查询可以使用复杂的表表达式。还要注意 `fdt` 在子查询中的引用方式。只有当 `c1` 同时也是子查询派生输入表中的列名时，才有必要将 `c1` 限定为 `fdt.c1`。不过，即使不需要，限定列名也会增加清晰度。此示例展示了外层查询的列命名作用域如何延伸到内层查询。
