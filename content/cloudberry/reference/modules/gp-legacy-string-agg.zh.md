---
title: gp_legacy_string_agg
description: gp_legacy_string_agg 提供单参数 string_agg(text) 聚合函数。
weight: 100
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/gp-legacy-string-agg.md
---

`gp_legacy_string_agg` 模块提供单参数 `string_agg(text)` 聚合函数。与 PostgreSQL 一样，Apache Cloudberry 内置的 `string_agg()` 仅有双参数形式。

> [!NOTE]
> 单参数函数已弃用。此模块仅应用于在将旧 SQL 迁移到内置的双参数 `string_agg()` 函数期间维持其运行。

## 安装 {#installation}

`gp_legacy_string_agg` 始终随 Apache Cloudberry 构建和安装。它属于默认的 `gpcontrib` 构建目标，不依赖任何 `configure` 选项。

此模块是一个扩展（版本为 `1.0.0`，可迁移到其他模式）。使用函数前，在每个需要使用它的数据库中创建扩展：

```sql
CREATE EXTENSION gp_legacy_string_agg;
```

此模块不需要 `shared_preload_libraries`，也不需要重启。

## 用法 {#usage}

此模块添加一个聚合函数 `string_agg(text)`。它将非空输入值连接为字符串，不使用分隔符。每个聚合结果（每个分组）都会触发弃用警告。没有非空输入值时，结果为 `NULL`。例如：

```sql
SELECT string_agg(a) FROM (VALUES('aaaa'),('bbbb'),('cccc'),(NULL)) g(a);
```

```
WARNING:  Deprecated call to string_agg(text), use string_agg(text, text) instead
  string_agg
--------------
 aaaabbbbcccc
(1 row)
```

结果取决于输入行的顺序，默认顺序未定义。要控制顺序，在聚合调用内使用 `ORDER BY` 子句。例如：

```sql
CREATE TABLE foo(a int, b text);
INSERT INTO foo VALUES(1, 'aaaa'),(2, 'bbbb'),(3, 'cccc'), (4, NULL);
SELECT string_agg(b ORDER BY a) FROM foo;
```

```
WARNING:  Deprecated call to string_agg(text), use string_agg(text, text) instead
  string_agg
--------------
 aaaabbbbcccc
(1 row)
```

## 迁移到双参数 string_agg() 函数 {#migrate-to-the-two-argument-string_agg-function}

内置的 `string_agg(text, text)` 聚合函数以第二个参数指定分隔符。使用空分隔符的调用与本模块的单参数函数等价，因此可将每处 `string_agg(a)` 调用替换为 `string_agg(a, '')`。例如，下面的查询使用本模块的函数：

```sql
SELECT string_agg(a) FROM (VALUES('aaaa'),('bbbb'),('cccc'),(NULL)) g(a);
```

可改写为：

```sql
SELECT string_agg(a, '') FROM (VALUES('aaaa'),('bbbb'),('cccc'),(NULL)) g(a);
```

两条查询均返回 `aaaabbbbcccc`。第二条查询使用内置函数，因此不会触发弃用警告。

转换所有调用后，可以删除扩展：

```sql
DROP EXTENSION gp_legacy_string_agg;
```

内置函数的更多信息，参见 PostgreSQL 文档中的[聚合函数](https://www.postgresql.org/docs/14/functions-aggregate.html)。
