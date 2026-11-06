---
title: "ALTER PROCEDURE"
description: "更改存储过程的定义。"
weight: 210
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-procedure.md"
---

## 概要 {#synopsis}

```sql
ALTER PROCEDURE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ] 
   <action> [, ... ] [RESTRICT]

ALTER PROCEDURE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   RENAME TO <new_name>

ALTER PROCEDURE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER PROCEDURE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   SET SCHEMA <new_schema>

ALTER PROCEDURE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   DEPENDS ON EXTENSION <extension_name>

-- where <action> is one of:

    { [EXTERNAL] SECURITY INVOKER | [EXTERNAL] SECURITY DEFINER }
    SET <configuration_parameter> { TO | = } { <value> | DEFAULT }
    SET <configuration_parameter> FROM CURRENT
    RESET <configuration_parameter>
    RESET ALL
```

## 描述 {#description}

`ALTER PROCEDURE` 更改存储过程的定义。

要使用 `ALTER PROCEDURE`，你必须拥有该存储过程。要更改存储过程所在的模式，你还必须在新模式上具有 `CREATE` 权限。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该存储过程所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该存储过程无法做到的事情。不过，超级用户无论如何都可以更改任何存储过程的所有权。）

## 参数 {#parameters}

**`name`**

一个现有存储过程的名称（可以是模式限定的）。如果未指定参数列表，则该名称在其模式中必须是唯一的。

**`argmode`**

参数的模式：`IN` 或 `VARIADIC`。如果省略，默认为 `IN`。

**`argname`**

参数的名称。请注意，`ALTER PROCEDURE` 实际上并不关注参数名称，因为确定函数的标识只需要参数的数据类型。

**`argtype`**

存储过程参数的数据类型（可以是模式限定的），如果有的话。

**`new_name`**

存储过程的新名称。

**`new_owner`**

存储过程的新所有者。请注意，如果该存储过程被标记为 `SECURITY DEFINER`，它此后将以新所有者的身份运行。

**`new_schema`**

存储过程的新模式。

**`extension_name`**

该存储过程要依赖的扩展的名称。

**`[ EXTERNAL ] SECURITY INVOKER`**<br />
**`[ EXTERNAL ] SECURITY DEFINER`**

更改存储过程是否为安全定义者（security definer）。出于 SQL 一致性考虑，关键字 `EXTERNAL` 会被忽略。关于此功能的更多信息，请参见 [CREATE PROCEDURE](/cloudberry/reference/sql-stmts/create-procedure/)。

**`configuration_parameter`**<br />
**`value`**

设置或更改存储过程被调用时某个配置参数的值。如果 value 为 `DEFAULT`，或者等效地使用了 `RESET`，则存储过程本地的设置会被移除，存储过程将以其环境中已有的值运行。使用 `RESET ALL` 可清除所有存储过程本地的设置。`SET FROM CURRENT` 会把运行 `ALTER PROCEDURE` 时该参数的当前值保存下来，作为进入存储过程时要应用的值。

关于允许的参数名称和值的更多信息，请参见 [SET](/cloudberry/reference/sql-stmts/set/)。

**`RESTRICT`**

为符合 SQL 标准而被忽略。

## 注解 {#notes}

Apache Cloudberry 对定义为 `STABLE` 或 `VOLATILE` 的函数的使用有一些限制。更多信息请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

## 示例 {#examples}

将带有两个 `integer` 类型参数的存储过程 `insert_data` 重命名为 `insert_record`：

```sql
ALTER PROCEDURE insert_data(integer, integer) RENAME TO insert_record;
```

将带有两个 `integer` 类型参数的存储过程 `insert_data` 的所有者更改为 `joe`：

```sql
ALTER PROCEDURE insert_data(integer, integer) OWNER TO joe;
```

将带有两个 `integer` 类型参数的存储过程 `insert_data` 的模式更改为 `accounting`：

```sql
ALTER PROCEDURE insert_data(integer, integer) SET SCHEMA accounting;
```

将存储过程 `insert_data(integer, integer)` 标记为依赖于扩展 `myext`：

```sql
ALTER PROCEDURE insert_data(integer, integer) DEPENDS ON EXTENSION myext;
```

调整为存储过程自动设置的搜索路径：

```sql
ALTER PROCEDURE check_password(text) SET search_path = admin, pg_temp;
```

禁用为存储过程自动设置 `search_path`：

```sql
ALTER PROCEDURE check_password(text) RESET search_path;
```

该存储过程此后将使用其调用者所用的任何搜索路径来执行。

## 兼容性 {#compatibility}

此语句与 SQL 标准中的 `ALTER PROCEDURE` 语句部分兼容。标准允许修改存储过程的更多属性，但不提供重命名存储过程、将存储过程设为安全定义者、为存储过程附加配置参数值，或者更改存储过程的所有者、模式或易变性的能力。标准还要求使用 `RESTRICT` 关键字，而在 Apache Cloudberry 中它是可选的。

## 另见 {#see-also}

[CREATE PROCEDURE](/cloudberry/reference/sql-stmts/create-procedure/)、[DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/)
