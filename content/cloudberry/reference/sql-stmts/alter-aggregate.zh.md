---
title: "ALTER AGGREGATE"
description: "更改一个聚合函数的定义。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-aggregate.md"
---

## 概要 {#synopsis}

```sql
ALTER AGGREGATE <name> ( <aggregate_signature> )  RENAME TO <new_name>

ALTER AGGREGATE <name> ( <aggregate_signature> )
                 OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER AGGREGATE <name> ( <aggregate_signature> ) SET SCHEMA <new_schema>

-- where <aggregate_signature> is:

* |
[ <argmode> ] [ <argname> ] <argtype> [ , ... ] |
[ [ <argmode> ] [ <argname> ] <argtype> [ , ... ] ] ORDER BY [ <argmode> ] [ <argname> ] <argtype> [ , ... ]
```

## 描述 {#description}

`ALTER AGGREGATE` 更改一个聚合函数的定义。

要使用 `ALTER AGGREGATE`，你必须拥有该聚合函数。要更改聚合函数的模式，你还必须在新模式上具有 `CREATE` 权限。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该聚合函数所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该聚合函数无法做到的事情。不过，超级用户无论如何都可以更改任何聚合函数的所有权。）

## 参数 {#parameters}

**`name`**

一个现有聚合函数的名称（可以是模式限定的）。

**`argmode`**

参数的模式：`IN` 或 `VARIADIC`。如果省略，默认值为 `IN`。

**`argname`**

参数的名称。请注意，`ALTER AGGREGATE` 实际上不会理会参数名称，因为确定聚合函数的标识只需要参数的数据类型。

**`argtype`**

该聚合函数所处理的输入数据类型。要引用一个零参数的聚合函数，请用 `*` 代替参数说明列表。要引用一个有序集聚合函数，请在直接参数说明与被聚集参数说明之间写上 `ORDER BY`。

**`new_name`**

聚合函数的新名称。

**`new_owner`**

聚合函数的新所有者。

**`new_schema`**

聚合函数的新模式。

## 注解 {#notes}

引用有序集聚合函数时，推荐的语法是在直接参数说明与被聚集参数说明之间写上 `ORDER BY`，其风格与 [CREATE AGGREGATE](/cloudberry/reference/sql-stmts/create-aggregate/) 中相同。不过，省略 `ORDER BY`、直接把直接参数说明与被聚集参数说明连成一个列表也同样可行。在这种简写形式中，如果直接参数列表和被聚集参数列表中都使用了 `VARIADIC "any"`，则只需写一次 `VARIADIC "any"`。

## 示例 {#examples}

将类型为 `integer` 的聚合函数 `myavg` 重命名为 `my_average`：

```sql
ALTER AGGREGATE myavg(integer) RENAME TO my_average;
```

将类型为 `integer` 的聚合函数 `myavg` 的所有者更改为 `joe`：

```sql
ALTER AGGREGATE myavg(integer) OWNER TO joe;
```

将直接参数类型为 `float8`、被聚集参数类型为 `integer` 的有序集聚合函数 `mypercentile` 移入模式 `myschema`：

```sql
ALTER AGGREGATE mypercentile(float8 ORDER BY integer) SET SCHEMA myschema;
```

下面的写法同样可行：

```sql
ALTER AGGREGATE mypercentile(float8, integer) SET SCHEMA myschema;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER AGGREGATE` 语句。

## 另见 {#see-also}

[CREATE AGGREGATE](/cloudberry/reference/sql-stmts/create-aggregate/)、[DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/)
