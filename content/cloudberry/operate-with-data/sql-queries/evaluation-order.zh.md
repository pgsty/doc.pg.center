---
title: "表达式求值规则"
description: "子表达式的求值顺序未定义。操作符或函数的输入不一定按从左到右或任何其他固定顺序求值。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/evaluation-order.md"
---

如果只对表达式的某些部分求值就能确定表达式结果，那么其他子表达式可能根本不会求值。例如，在以下表达式中：

```sql
SELECT true OR somefunc();
```

`somefunc()` 很可能完全不会被调用。以下表达式也同样如此：

```sql
SELECT somefunc() OR true;
```

这不同于某些编程语言中由布尔操作符强制执行的从左到右求值顺序。

不要在复杂表达式中使用有副作用的函数，尤其不要在 `WHERE` 和 `HAVING` 子句中使用，因为在生成执行计划时会反复处理这些子句。这些子句中的布尔表达式（`AND`/`OR`/`NOT` 组合）可以按照布尔代数定律允许的任何方式重新组织。

使用 `CASE` 结构强制求值顺序。以下示例是在 `WHERE` 子句中避免除零的不可靠方式：

```sql
SELECT ... WHERE x <> 0 AND y/x > 1.5;
```

以下示例展示了可靠的求值顺序：

```sql
SELECT ... WHERE CASE WHEN x <> 0 THEN y/x > 1.5 ELSE false 
END;
```

这种 `CASE` 结构的用法会破坏优化尝试；只有必要时才使用它。