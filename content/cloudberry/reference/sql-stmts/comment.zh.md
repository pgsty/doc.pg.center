---
title: "COMMENT"
description: "定义或更改对象的注释。"
weight: 490
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/comment.md"
---

## 概要 {#synopsis}

```sql
COMMENT ON
{ ACCESS METHOD <object_name> |
  AGGREGATE <aggregate_name> (<aggregate_signature>) |
  CAST (<source_type> AS <target_type>) |
  COLLATION <object_name>
  COLUMN <relation_name>.<column_name> |
  CONSTRAINT <constraint_name> ON <table_name> |
  CONSTRAINT <constraint_name> ON DOMAIN <domain_name> |
  CONVERSION <object_name> |
  DATABASE <object_name> |
  DOMAIN <object_name> |
  EVENT TRIGGER <object_name> |
  EXTENSION <object_name> |
  FOREIGN DATA WRAPPER <object_name> |
  FOREIGN TABLE <object_name> |
  FUNCTION <function_name> [([[<argmode>] [<argname>] <argtype> [, ...]])] |
  INDEX <object_name> |
  MATERIALIZED VIEW <object_name> |
  OPERATOR <operator_name> (<left_type>, <right_type>) |
  OPERATOR CLASS <object_name> USING <index_method> |
  OPERATOR FAMILY <object_name> USING <index_method> |
  POLICY <policy_name> ON <table_name> |
  [PROCEDURAL] LANGUAGE <object_name> |
  PROCEDURE <procedure_name> [([[<argmode>] [<argname>] <argtype> [, ...]])] |
  RESOURCE GROUP <object_name> |
  RESOURCE QUEUE <object_name> |
  ROLE <object_name |
  ROUTINE <routine_name> [([[<argmode>] [<argname>] <argtype> [, ...]])] |
  RULE <rule_name> ON <table_name> |
  SCHEMA <object_name> |
  SEQUENCE <object_name> |
  SERVER <object_name> |
  STATISTICS <object_name> |
  TABLE <object_name> |
  TABLESPACE <object_name> |
  TEXT SEARCH CONFIGURATION <object_name> |
  TEXT SEARCH DICTIONARY <object_name> |
  TEXT SEARCH PARSER <object_name> |
  TEXT SEARCH TEMPLATE <object_name> |
  TRANSFORM FOR <type_name> LANGUAGE <lang_name> |
  TRIGGER <trigger_name> ON <table_name> |
  TYPE <object_name> |
  VIEW <object_name>
} IS { <string_literal> | NULL }

-- where <aggregate_signature> is:

* |
[ <argmode> ] [ <argname> ] <argtype> [ , ... ] |
[ [ <argmode> ] [ <argname> ] <argtype> [ , ... ] ] ORDER BY [ <argmode> ] [ <argname> ] <argtype> [ , ... ]
```

## 描述 {#description}

`COMMENT` 存储有关数据库对象的注释。每个对象只存储一个注释字符串，因此要修改注释，需要对同一对象发出新的 `COMMENT` 命令。要删除注释，请用 `NULL` 代替文本字符串。对象被删除时，其注释会自动删除。

Apache Cloudberry 会对要添加注释的对象获取 `SHARE UPDATE EXCLUSIVE` 锁。

对于大多数种类的对象，只有对象的所有者才能设置注释。角色没有所有者，因此 `COMMENT ON ROLE` 的规则是：必须是超级用户才能为超级用户角色添加注释，而为非超级用户角色添加注释则需要具有 `CREATEROLE` 权限。同样，访问方法也没有所有者；必须是超级用户才能为访问方法添加注释。当然，超级用户可以为任何对象添加注释。

可以使用 `psql` 元命令 `\dd`、`\d+` 和 `\l+` 查看注释。其他检索注释的用户界面可以基于 `psql` 所使用的同一组内置函数构建，即 `obj_description()`、`col_description()` 和 `shobj_description()`。

## 参数 {#parameters}

**`object_name`**<br />
**`relation_name.column_name`**<br />
**`aggregate_name`**<br />
**`constraint_name`**<br />
**`function_name`**<br />
**`operator_name`**<br />
**`policy_name`**<br />
**`procedure_name`**<br />
**`routine_name`**<br />
**`rule_name`**<br />
**`trigger_name`**

要添加注释的对象的名称。表、聚合、排序规则、转换、域、外表、函数、索引、操作符、操作符类、操作符族、过程、例程、序列、统计信息、文本检索对象、类型、视图和物化视图的名称可以带模式限定。为列添加注释时，relation_name 必须指向表、视图、物化视图、复合类型或外表。

> **注意** Apache Cloudberry 不支持触发器。

**`table_name`**<br />
**`domain_name`**

为约束、触发器、规则或策略创建注释时，这些参数指定定义该对象的表或域的名称。

**`source_type`**

类型转换的源数据类型的名称。

**`target_type`**

类型转换的目标数据类型的名称。

**`argmode`**

函数或聚合参数的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。如果省略，默认为 `IN`。注意，`COMMENT` 实际上并不关注 `OUT` 参数，因为确定函数的标识只需要输入参数。列出 `IN`、`INOUT` 和 `VARIADIC` 参数就足够了。

**`argname`**

函数、过程或聚合参数的名称。注意，`COMMENT` 实际上并不关注参数名称，因为确定函数的标识只需要参数的数据类型。

**`argtype`**

函数、过程或聚合参数的数据类型。

**`left_type`**<br />
**`right_type`**

操作符参数的数据类型（可以带模式限定）。对于前缀或后缀操作符缺失的参数，请指定 `NONE`。

**`PROCEDURAL`**

Apache Cloudberry 会忽略这个噪声词。

**`type_name`**

转换（transform）所针对的数据类型的名称。

**`lang_name`**

转换（transform）所针对的语言的名称。

**`string_literal`**

新的注释内容，写作字符串字面量。

**`NULL`**

指定 `NULL` 以删除注释。

## 注解 {#notes}

目前没有查看注释的安全机制：连接到某个数据库的任何用户都可以看到该数据库中对象的所有注释。对于数据库、角色和表空间等共享对象，注释是全局存储的，因此连接到集群中任意数据库的任何用户都可以看到共享对象的所有注释。

> **警告** 不要在注释中放入安全敏感的信息。

## 示例 {#examples}

为表 `mytable` 添加注释：

```sql
COMMENT ON TABLE mytable IS 'This is my table.';
```

再次删除它：

```sql
COMMENT ON TABLE mytable IS NULL;
```

更多示例：

```sql
COMMENT ON ACCESS METHOD gin IS 'GIN index access method';
COMMENT ON AGGREGATE my_aggregate (double precision) IS 'Computes sample variance';
COMMENT ON CAST (text AS int4) IS 'Allow casts from text to int4';
COMMENT ON COLLATION "fr_CA" IS 'Canadian French';
COMMENT ON COLUMN my_table.my_column IS 'Employee ID number';
COMMENT ON CONVERSION my_conv IS 'Conversion to UTF8';
COMMENT ON CONSTRAINT bar_col_cons ON bar IS 'Constrains column col';
COMMENT ON CONSTRAINT dom_col_constr ON DOMAIN dom IS 'Constrains col of domain';
COMMENT ON DATABASE my_database IS 'Development Database';
COMMENT ON DOMAIN my_domain IS 'Email Address Domain';
COMMENT ON EVENT TRIGGER cancel_ddl IS 'Cancels all DLL commands';
COMMENT ON EXTENSION hstore IS 'implements the hstore data type';
COMMENT ON FOREIGN DATA WRAPPER mywrapper IS 'my foreign data wrapper';
COMMENT ON FOREIGN TABLE my_foreign_table IS 'Employee Information in other database';
COMMENT ON FUNCTION my_function (timestamp) IS 'Returns Roman Numeral';
COMMENT ON INDEX my_index IS 'Enforces uniqueness on employee ID';
COMMENT ON LANGUAGE plpython IS 'Python support for stored procedures';
COMMENT ON MATERIALIZED VIEW my_matview IS 'Summary of order history';
COMMENT ON OPERATOR ^ (text, text) IS 'Performs intersection of two texts';
COMMENT ON OPERATOR - (NONE, integer) IS 'Unary minus';
COMMENT ON OPERATOR CLASS int4_ops USING btree IS '4 byte integer operators for btrees';
COMMENT ON OPERATOR FAMILY integer_ops USING btree IS 'all integer operators for btrees';
COMMENT ON POLICY my_policy ON mytable IS 'Filter rows by users';
COMMENT ON PROCEDURE my_proc (integer, integer) IS 'Runs a report';
COMMENT ON ROLE my_role IS 'Administration group for finance tables';
COMMENT ON ROUTINE my_routine (integer, integer) IS 'Runs a routine (which is a function or procedure)';
COMMENT ON RULE my_rule ON my_table IS 'Logs updates of employee records';
COMMENT ON SCHEMA my_schema IS 'Departmental data';
COMMENT ON SEQUENCE my_sequence IS 'Used to generate primary keys';
COMMENT ON SERVER myserver IS 'my foreign server';
COMMENT ON STATISTICS my_statistics IS 'Improves planner row estimations';
COMMENT ON TABLE my_schema.my_table IS 'Employee Information';
COMMENT ON TABLESPACE my_tablespace IS 'Tablespace for indexes';
COMMENT ON TEXT SEARCH CONFIGURATION my_config IS 'Special word filtering';
COMMENT ON TEXT SEARCH DICTIONARY swedish IS 'Snowball stemmer for Swedish language';
COMMENT ON TEXT SEARCH PARSER my_parser IS 'Splits text into words';
COMMENT ON TEXT SEARCH TEMPLATE snowball IS 'Snowball stemmer';
COMMENT ON TRANSFORM FOR hstore LANGUAGE plpythonu IS 'Transform between hstore and Python dict';
COMMENT ON TRIGGER my_trigger ON my_table IS 'Used for RI';
COMMENT ON TYPE complex IS 'Complex number data type';
COMMENT ON VIEW my_view IS 'View of departmental costs';
```

## 兼容性 {#compatibility}

SQL 标准中没有 `COMMENT` 命令。
