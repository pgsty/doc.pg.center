---
title: "ALTER DEFAULT PRIVILEGES"
description: "更改默认访问权限。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-default-privileges.md"
---

## 概要 {#synopsis}

```sql

ALTER DEFAULT PRIVILEGES
    [ FOR { ROLE | USER } <target_role> [, ...] ]
    [ IN SCHEMA <schema_name> [, ...] ]
    <abbreviated_grant_or_revoke>

-- where <abbreviated_grant_or_revoke> is one of:

GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON TABLES
    TO { [ GROUP ] <role_name> | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SEQUENCES
    TO { [ GROUP ] <role_name> | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { EXECUTE | ALL [ PRIVILEGES ] }
    ON { FUNCTIONS | ROUTINES }
    TO { [ GROUP ] <role_name> | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPES
    TO { [ GROUP ] <role_name> | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | CREATE | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    TO { [ GROUP ] <role_name> | PUBLIC } [, ...] [ WITH GRANT OPTION ]

REVOKE [ GRANT OPTION FOR ]
    { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON TABLES
    FROM { [ GROUP ] <role_name> | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SEQUENCES
    FROM { [ GROUP ] <role_name> | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { EXECUTE | ALL [ PRIVILEGES ] }
    ON { FUNCTIONS | ROUTINES }
    FROM { [ GROUP ] <role_name> | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | ALL [ PRIVILEGES ] }
    ON TYPES
    FROM { [ GROUP ] <role_name> | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
    { USAGE | CREATE | ALL [ PRIVILEGES ] }
    ON SCHEMAS
    FROM { [ GROUP ] <role_name> | PUBLIC } [, ...]
    [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`ALTER DEFAULT PRIVILEGES` 允许你设置将应用于未来所创建对象的权限。（它不会影响已赋予现有对象的权限。）目前，只能更改模式、表（包括视图和外表）、序列、函数以及类型（包括域）的权限。对于此命令，函数包括聚合函数和存储过程。在此命令中，`FUNCTIONS` 和 `ROUTINES` 这两个词是等价的。（今后推荐使用 `ROUTINES`，它是对函数和存储过程的统称的标准术语。在 Apache Cloudberry 的早期版本中，只允许使用 `FUNCTIONS` 一词。无法分别为函数和存储过程设置默认权限。）

你只能为由你自己或你所属角色创建的对象更改默认权限。权限可以全局设置（即针对当前数据库中创建的所有对象），也可以只针对在指定模式中创建的对象设置。

如 [GRANT](/cloudberry/reference/sql-stmts/grant/) 中所述，任何对象类型的默认权限通常会把所有可授予的权限授予对象所有者，并且也可能把某些权限授予 `PUBLIC`。不过，可以通过 `ALTER DEFAULT PRIVILEGES` 更改全局默认权限来改变这种行为。

按模式指定的默认权限会叠加到该特定对象类型的全局默认权限之上。这意味着，如果权限已被全局授予（无论是默认如此，还是依据先前某条未指定模式的 `ALTER DEFAULT PRIVILEGES` 命令），你就不能按模式撤销它们。按模式的 `REVOKE` 只适用于撤销先前按模式的 `GRANT` 所产生的效果。

## 参数 {#parameters}

**`target_role`**

一个现有角色的名称，当前角色是该角色的成员。如果省略 `FOR ROLE`，则假定为当前角色。

**`schema_name`**

一个现有模式的名称。如果指定，则会更改此后在该模式中创建的对象的默认权限。如果省略 `IN SCHEMA`，则更改全局默认权限。为模式设置权限时不允许使用 `IN SCHEMA`，因为模式不能嵌套。

**`role_name`**

要为其授予或撤销权限的现有角色的名称。此参数以及 abbreviated_grant_or_revoke 中的所有其他参数，其作用均如 [GRANT](/cloudberry/reference/sql-stmts/grant/) 或 [REVOKE](/cloudberry/reference/sql-stmts/revoke/) 中所述，区别在于这里设置的是针对整类对象的权限，而不是针对特定命名对象的权限。

## 注解 {#notes}

使用 psql 的 `\ddp` 命令可获得关于现有默认权限分配的信息。权限值的含义与 [GRANT](/cloudberry/reference/sql-stmts/grant/) 中对 `\dp` 的说明相同。

如果你希望删除一个已更改过默认权限的角色，就必须撤销其默认权限的变更，或者使用 `DROP OWNED BY` 来清除该角色的默认权限条目。

## 示例 {#examples}

把 SELECT 权限授予所有人，适用于你此后在模式 `myschema` 中创建的所有表（和视图），并且同时允许角色 `webuser` 对它们执行 INSERT：

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT SELECT ON TABLES TO PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema GRANT INSERT ON TABLES TO webuser;
```

撤销上面的设置，使此后创建的表不会比通常情况拥有更多权限：

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE SELECT ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA myschema REVOKE INSERT ON TABLES FROM webuser;
```

对于角色 `admin` 此后创建的所有函数，移除通常授予函数的公共 EXECUTE 权限：

```sql
ALTER DEFAULT PRIVILEGES FOR ROLE admin REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

不过请注意，你*不能*通过只限于单个模式的命令达到该效果。下面这条命令不会产生任何效果，除非它是在撤销一条与之匹配的 `GRANT`：

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

这是因为按模式的默认权限只能在全局设置的基础上增加权限，而不能移除全局设置所授予的权限。

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER DEFAULT PRIVILEGES` 语句。

## 另见 {#see-also}

[GRANT](/cloudberry/reference/sql-stmts/grant/)、[REVOKE](/cloudberry/reference/sql-stmts/revoke/)
