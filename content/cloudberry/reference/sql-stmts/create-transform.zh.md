---
title: "CREATE TRANSFORM"
description: "定义新的转换。"
weight: 890
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-transform.md"
---

## 概要 {#synopsis}

```sql
CREATE [ OR REPLACE ] TRANSFORM FOR <type_name> LANGUAGE <lang_name> (
  FROM SQL WITH FUNCTION <from_sql_function_name> [ (<argument_type> [, ...]) ],
  TO SQL WITH FUNCTION <to_sql_function_name> [ (<argument_type> [, ...]) ]
);
```

## 描述 {#description}

`CREATE TRANSFORM` 定义新的转换。`CREATE OR REPLACE TRANSFORM` 会创建新转换，或替换现有定义。

转换指定如何将数据类型适配到过程语言。例如，在 PL/Python 函数中使用 `hstore` 类型时，PL/Python 事先不知道如何在 Python 环境中表示 `hstore` 值。语言实现通常默认使用文本表示，但如果关联数组或列表更合适，这种方式就不方便。

转换指定两个函数：

- “from SQL” 函数，将该类型从 SQL 环境转换到过程语言。对于用该语言编写的函数，会对其参数调用此转换函数。

- “to SQL” 函数，将该类型从过程语言转换到 SQL 环境。对于用该语言编写的函数，会对其返回值调用此转换函数。

不必同时提供两个函数。如果其中一个未指定，必要时会使用该语言的默认行为。（如果要完全禁止某个方向的转换，也可以编写一个始终报错的转换函数。）

要创建转换，必须拥有该类型并对其具有 `USAGE` 权限，对该语言具有 `USAGE` 权限；如果指定了 from-SQL 和 to-SQL 函数，还必须拥有这些函数并具有其 `EXECUTE` 权限。

## 参数 {#parameters}

**`type_name`**

转换所对应的数据类型名称。

**`lang_name`**

转换所对应的语言名称。

**`from_sql_function_name[(argument_type [, ...])]`**

将该类型从 SQL 环境转换到过程语言的函数名称。它必须接受一个 `internal` 类型参数，并返回 `internal` 类型。实际参数将是此转换对应的类型，函数代码也应按该类型处理。（SQL 层面返回 `internal` 的函数必须声明至少一个 `internal` 类型参数。）实际返回值取决于语言实现。如果未指定参数列表，函数名在其模式中必须唯一。

**`to_sql_function_name[(argument_type [, ...])]`**

将该类型从过程语言转换到 SQL 环境的函数名称。它必须接受一个 `internal` 类型参数，返回此转换对应的类型。实际参数值取决于语言实现。如果未指定参数列表，函数名在其模式中必须唯一。

## 注意事项 {#notes}

使用 [DROP TRANSFORM](/cloudberry/reference/sql-stmts/drop-transform/) 删除转换。

## 示例 {#examples}

要为类型 `hstore` 和语言 `plpython3u` 创建转换，首先设置类型和语言：

``` sql
CREATE EXTENSION IF NOT EXISTS hstore;

CREATE EXTENSION plpython3u;
```

然后创建所需函数：

``` sql
CREATE FUNCTION hstore_to_plpython(val internal) RETURNS internal
LANGUAGE C STRICT IMMUTABLE
AS ...;

CREATE FUNCTION plpython_to_hstore(val internal) RETURNS hstore
LANGUAGE C STRICT IMMUTABLE
AS ...;
```

最后创建转换，将它们连接起来：

``` sql
CREATE TRANSFORM FOR hstore LANGUAGE plpython3u (
    FROM SQL WITH FUNCTION hstore_to_plpython(internal),
    TO SQL WITH FUNCTION plpython_to_hstore(internal)
);
```

实际使用中，这些命令通常会封装在扩展中。

## 兼容性 {#compatibility}

这种形式的 `CREATE TRANSFORM` 是 Apache Cloudberry 的扩展。SQL 标准中也有 `CREATE TRANSFORM` 命令，但用于将数据类型适配到客户端语言。Apache Cloudberry 不支持这种用法。

## 另见 {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/), [CREATE TYPE](/cloudberry/reference/sql-stmts/create-type/), [DROP TRANSFORM](/cloudberry/reference/sql-stmts/drop-transform/)
