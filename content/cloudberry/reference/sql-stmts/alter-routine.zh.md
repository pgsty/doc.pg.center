---
title: "ALTER ROUTINE"
description: "修改例程的定义。"
weight: 260
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-routine.md"
---

## 概要 {#synopsis}

```sql
ALTER ROUTINE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ] 
   <action> [, ... ] [RESTRICT]

ALTER ROUTINE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   RENAME TO <new_name>

ALTER ROUTINE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER ROUTINE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   SET SCHEMA <new_schema>

ALTER ROUTINE <name> [ ( [ [<argmode>] [<argname>] <argtype> [, ...] ] ) ]
   DEPENDS ON EXTENSION <extension_name>

-- where <action> is one of (depending on the type of routine):

    { IMMUTABLE | STABLE | VOLATILE }
    [ NOT ] LEAKPROOF
    { [EXTERNAL] SECURITY INVOKER | [EXTERNAL] SECURITY DEFINER }
    PARALLEL { UNSAFE | RESTRICTED | SAFE }
    EXECUTE ON { ANY | COORDINATOR | ALL SEGMENTS | INITPLAN }
    COST <execution_cost>
    ROWS <result_rows>
    SET <configuration_parameter> { TO | = } { <value> | DEFAULT }
    SET <configuration_parameter> FROM CURRENT
    RESET <configuration_parameter>
    RESET ALL
```

## 说明 {#description}

`ALTER ROUTINE` 用于修改例程的定义，例程可以是聚合函数、普通函数或过程。有关参数的说明、更多示例和进一步细节，请参阅 [ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/)、[ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/) 和 [ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/)。

## 示例 {#examples}

将针对类型 `integer` 的例程 `foo` 重命名为 `foobar`：

```sql
ALTER ROUTINE foo(integer) RENAME TO foobar;
```

无论 `foo` 是聚合函数、函数还是过程，此命令都可以正常工作。

## 兼容性 {#compatibility}

此语句与 SQL 标准中的 `ALTER ROUTINE` 语句部分兼容。更多细节请参阅 [ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/) 和 [ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/)。允许例程名称引用聚合函数是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/)、[ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/)、[ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/)、[DROP ROUTINE](/cloudberry/reference/sql-stmts/drop-routine/)
