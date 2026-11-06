---
title: "ALTER FUNCTION"
description: "更改函数的定义。"
weight: 120
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-function.md"
---

## 概要 {#synopsis}

```sql
ALTER FUNCTION <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ] 
   <action> [, ... ] [RESTRICT]

ALTER FUNCTION <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   RENAME TO <new_name>

ALTER FUNCTION <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER FUNCTION <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   SET SCHEMA <new_schema>

ALTER FUNCTION <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   DEPENDS ON EXTENSION <extension_name>

-- where <action> is one of:

    { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT }
    { IMMUTABLE | STABLE | VOLATILE }
    [ NOT ] LEAKPROOF
    { [EXTERNAL] SECURITY INVOKER | [EXTERNAL] SECURITY DEFINER }
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    EXECUTE ON { ANY | COORDINATOR | ALL SEGMENTS | INITPLAN }
    COST <execution_cost>
    ROWS <result_rows>
    SUPPORT <support_function>
    SET <configuration_parameter> { TO | = } { <value> | DEFAULT }
    SET <configuration_parameter> FROM CURRENT
    RESET <configuration_parameter>
    RESET ALL
```

## 描述 {#description}

`ALTER FUNCTION` 更改函数的定义。

要使用 `ALTER FUNCTION`，你必须拥有该函数。要更改函数所在的模式，你还必须在新模式上具有 `CREATE` 权限。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该函数所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该函数无法做到的事情。不过，超级用户无论如何都可以更改任何函数的所有权。）

## 参数 {#parameters}

**`name`**

一个现有函数的名称（可以是模式限定的）。如果未指定参数列表，则该名称在其模式中必须是唯一的。

**`argmode`**

参数的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。如果省略，默认为 `IN`。请注意，`ALTER FUNCTION` 实际上并不关注 `OUT` 参数，因为确定函数的标识只需要输入参数。因此，只列出 `IN`、`INOUT` 和 `VARIADIC` 参数就足够了。

**`argname`**

参数的名称。请注意，[ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/) 实际上并不关注参数名称，因为确定函数的标识只需要参数的数据类型。

**`argtype`**

函数参数的数据类型（可以是模式限定的），如果有的话。

**`new_name`**

函数的新名称。

**`new_owner`**

函数的新所有者。请注意，如果该函数被标记为 `SECURITY DEFINER`，它此后将以新所有者的身份运行。

**`new_schema`**

函数的新模式。

**`extension_name`**

该函数要依赖的扩展的名称。

**`CALLED ON NULL INPUT`**<br />
**`RETURNS NULL ON NULL INPUT`**<br />
**`STRICT`**

`CALLED ON NULL INPUT` 将函数更改为在其部分或全部参数为空值时仍会被调用。`RETURNS NULL ON NULL INPUT` 或 `STRICT` 将函数更改为只要任一参数为空值就不会被调用；而是自动假定结果为空值。更多信息请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

IMMUTABLE
STABLE
**`VOLATILE`**

将函数的易变性更改为指定的设置。详情请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

**`[ EXTERNAL ] SECURITY INVOKER`**<br />
**`[ EXTERNAL ] SECURITY DEFINER`**

更改函数是否为安全定义者（security definer）。出于 SQL 一致性考虑，关键字 `EXTERNAL` 会被忽略。关于此功能的更多信息，请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

**`PARALLEL`**

更改该函数是否被认为可以安全地并行执行。详情请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

**`LEAKPROOF`**

更改该函数是否被视为防泄漏（leakproof）。关于此功能的更多信息，请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

**`EXECUTE ON ANY`**<br />
**`EXECUTE ON COORDINATOR`**<br />
**`EXECUTE ON ALL SEGMENTS`**<br />
**`EXECUTE ON INITPLAN`**

`EXECUTE ON` 属性指定函数在查询执行过程中被调用时在何处（Coordinator 还是 Segment 实例）运行。

`EXECUTE ON ANY`（默认值）表示该函数可以在 Coordinator 或任意 Segment 实例上运行，并且无论在何处运行都返回相同的结果。Apache Cloudberry 决定该函数在何处运行。

`EXECUTE ON COORDINATOR` 表示该函数必须只在 Coordinator 实例上运行。

`EXECUTE ON ALL SEGMENTS` 表示每次调用时，该函数必须在所有主 Segment 实例上运行，但不在 Coordinator 上运行。该函数的总体结果是所有 Segment 实例结果的 `UNION ALL`。

`EXECUTE ON INITPLAN` 表示该函数包含一条向 Segment 实例派发查询的 SQL 命令，并且在可能的情况下，需要 Apache Cloudberry 在 Coordinator 实例上进行特殊处理。

关于 `EXECUTE ON` 属性的更多信息，请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

**`COST execution_cost`**

更改函数的估计执行代价。更多信息请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

**`ROWS result_rows`**

更改返回集合的函数所返回的估计行数。更多信息请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

**`SUPPORT support_function`**

设置或更改用于该函数的规划器支持函数。要使用此选项，你必须是超级用户。

此选项不能用于彻底移除支持函数，因为它必须指定一个新的支持函数。如果需要移除，请使用 `CREATE OR REPLACE FUNCTION`。

**`configuration_parameter`**<br />
**`value`**

设置或更改函数被调用时某个配置参数的值。如果 value 为 `DEFAULT`，或者等效地使用了 `RESET`，则函数本地的设置会被移除，函数将以其环境中已有的值运行。使用 `RESET ALL` 可清除所有函数本地的设置。`SET FROM CURRENT` 会把运行 `ALTER FUNCTION` 时该参数的当前值保存下来，作为进入函数时要应用的值。
关于允许的参数名称和值的更多信息，请参见 [SET](/cloudberry/reference/sql-stmts/set/)。

**`RESTRICT`**

为符合 SQL 标准而被忽略。

## 注解 {#notes}

Apache Cloudberry 对定义为 `STABLE` 或 `VOLATILE` 的函数的使用有一些限制。更多信息请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

## 示例 {#examples}

将类型为 `integer` 的函数 `sqrt` 重命名为 `square_root`：

```sql
ALTER FUNCTION sqrt(integer) RENAME TO square_root;
```

将类型为 `integer` 的函数 `sqrt` 的所有者更改为 `joe`：

```sql
ALTER FUNCTION sqrt(integer) OWNER TO joe;
```

将类型为 `integer` 的函数 `sqrt` 的模式更改为 `maths`：

```sql
ALTER FUNCTION sqrt(integer) SET SCHEMA maths;
```

将类型为 `integer` 的函数 `sqrt` 标记为依赖于扩展 `mathlib`：

```sql
ALTER FUNCTION sqrt(integer) DEPENDS ON EXTENSION mathlib;
```

调整为函数自动设置的搜索路径：

```sql
ALTER FUNCTION check_password(text) search_path = admin, pg_temp;
```

禁用为函数自动设置 `search_path`：

```sql
ALTER FUNCTION check_password(text) RESET search_path;
```

该函数此后将使用其调用者所用的任何搜索路径来执行。

## 兼容性 {#compatibility}

此语句与 SQL 标准中的 `ALTER FUNCTION` 语句部分兼容。标准允许修改函数的更多属性，但不提供重命名函数、将函数设为安全定义者、为函数附加配置参数值，或者更改函数的所有者、模式或易变性的能力。标准还要求使用 `RESTRICT` 关键字，而在 Apache Cloudberry 中它是可选的。

## 另见 {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)、[DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/)、[ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/)、[ALTER ROUTINE](/cloudberry/reference/sql-stmts/alter-routine/)
