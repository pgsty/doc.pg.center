---
title: "ALTER EXTENSION"
description: "更改一个扩展的定义。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-extension.md"
---

## 概要 {#synopsis}

```sql
ALTER EXTENSION <name> UPDATE [ TO <new_version> ]
ALTER EXTENSION <name> SET SCHEMA <new_schema>
ALTER EXTENSION <name> ADD <member_object>
ALTER EXTENSION <name> DROP <member_object>

-- where <member_object> is:

  ACCESS METHOD <object_name> |
  AGGREGATE <aggregate_name> ( <aggregate_signature> ) |
  CAST (<source_type> AS <target_type>) |
  COLLATION <object_name> |
  CONVERSION <object_name> |
  DOMAIN <object_name> |
  EVENT TRIGGER <object_name> |
  FOREIGN DATA WRAPPER <object_name> |
  FOREIGN TABLE <object_name> |
  FUNCTION <function_name> ( [ [ <argmode> ] [ <argname> ] <argtype> [, ...] ] ) |
  MATERIALIZED VIEW <object_name> |
  OPERATOR <operator_name> (<left_type>, <right_type>) |
  OPERATOR CLASS <object_name> USING <index_method> |
  OPERATOR FAMILY <object_name> USING <index_method> |
  [ PROCEDURAL ] LANGUAGE <object_name> |
  PROCEDURE <procedure_name> [ ( [ [ <argmode> ] [ <argname> ] <argtype> [, ...] ] ) ] |
  ROUTINE <routine_name> [ ( [ [ <argmode> ] [ <argname> ] <argtype> [, ...] ] ) ] |
  SCHEMA <object_name> |
  SEQUENCE <object_name> |
  SERVER <object_name> |
  TABLE <object_name> |
  TEXT SEARCH CONFIGURATION <object_name> |
  TEXT SEARCH DICTIONARY <object_name> |
  TEXT SEARCH PARSER <object_name> |
  TEXT SEARCH TEMPLATE <object_name> |
  TRANSFORM FOR <type_name> LANGUAGE <lang_name> |
  TYPE <object_name> |
  VIEW <object_name>

and <aggregate_signature> is:

* |
[ <argmode> ] [ <argname> ] <argtype> [ , ... ] |
[ [ <argmode> ] [ <argname> ] <argtype> [ , ... ] ] ORDER BY [ <argmode> ] [ <argname> ] <argtype> [ , ... ]
```

## 描述 {#description}

`ALTER EXTENSION` 更改一个已安装扩展的定义。它有若干子形式：

**`UPDATE`**

此形式把扩展更新到较新的版本。该扩展必须提供合适的更新脚本（或一系列脚本），能够把当前已安装的版本修改为所请求的版本。

**`SET SCHEMA`**

此形式把扩展的成员对象移入另一个模式。扩展必须是*可重定位的*（relocatable），此命令才能成功。

**`ADD member_object`**

此形式把一个现有对象添加到扩展中。这主要用于扩展更新脚本。此后该对象将被视为扩展的成员；值得注意的是，它只能通过删除扩展来删除。

**`DROP member_object`**

此形式从扩展中移除一个成员对象。这主要用于扩展更新脚本。该对象不会被删除，只是与扩展解除关联。

有关这些操作的更多信息，请参见[将相关对象打包成扩展](https://www.postgresql.org/docs/12/extend-extensions.html)。

要使用 `ALTER EXTENSION`，你必须拥有该扩展。`ADD` 和 `DROP` 形式还要求你拥有被添加或被移除的对象。

## 参数 {#parameters}

**`name`**

一个已安装扩展的名称。

**`new_version`**

扩展的新版本。new_version 可以是标识符，也可以是字符串字面量。如果未指定，`ALTER EXTENSION UPDATE` 会尝试更新到扩展控制文件中显示为默认版本的版本。

**`new_schema`**

扩展的新模式。

**`object_name`**<br />
**`aggregate_name`**<br />
**`function_name`**<br />
**`operator_name`**<br />
**`procedure_name`**<br />
**`routine_name`**

要添加到扩展或从扩展中移除的对象的名称。表、聚合函数、域、外表、函数、操作符、操作符类、操作符族、存储过程、例程、序列、文本检索对象、类型和视图的名称可以是模式限定的。

**`source_type`**

类型转换的源数据类型的名称。

**`target_type`**

类型转换的目标数据类型的名称。

**`argmode`**

函数或聚合函数参数的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。如果省略，默认值为 `IN`。请注意，`ALTER EXTENSION` 实际上不会理会 `OUT` 参数，因为确定函数的标识只需要输入参数。因此只列出 `IN`、`INOUT` 和 `VARIADIC` 参数就足够了。

**`argname`**

函数或聚合函数参数的名称。请注意，`ALTER EXTENSION` 实际上不会理会参数名称，因为确定函数的标识只需要参数的数据类型。

**`argtype`**

函数、存储过程或聚合函数参数的数据类型。

**`left_type`**<br />
**`right_type`**

操作符参数的数据类型（可以是模式限定的）。对于前缀或后缀操作符中缺失的参数，请指定 `NONE`。

**`PROCEDURAL`**

这是一个噪声词。

**`type_name`**

转换（transform）所针对的数据类型的名称。

**`lang_name`**

转换（transform）所针对的语言的名称。

## 示例 {#examples}

将 hstore 扩展更新到 2.0 版本：

```sql
ALTER EXTENSION hstore UPDATE TO '2.0';
```

将 `hstore` 扩展的模式更改为 `utils`：

```sql
ALTER EXTENSION hstore SET SCHEMA utils;
```

将一个现有函数添加到 `hstore` 扩展中：

```sql
ALTER EXTENSION hstore ADD FUNCTION populate_record(anyelement, hstore);
```

## 兼容性 {#compatibility}

`ALTER EXTENSION` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE EXTENSION](/cloudberry/reference/sql-stmts/create-extension/)、[DROP EXTENSION](/cloudberry/reference/sql-stmts/drop-extension/)
