---
title: "REVOKE"
description: "移除访问权限。"
weight: 1630
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/revoke.md"
---

## 语法概要 {#synopsis}

```sql
REVOKE [GRANT OPTION FOR]
       { {SELECT | INSERT | UPDATE | DELETE | REFERENCES | TRIGGER | TRUNCATE }
       [, ...] | ALL [PRIVILEGES] }
       ON { { [TABLE] [[[ONLY] <table_name> [, ...]] [, ...]] }
          | ALL TABLES IN SCHEMA schema_name [, ...] }
       FROM <role_specification> [, ...]
       [CASCADE | RESTRICT]

REVOKE [ GRANT OPTION FOR ]
       { { SELECT | INSERT | UPDATE | REFERENCES } ( <column_name> [, ...] )
       [, ...] | ALL [ PRIVILEGES ] ( <column_name> [, ...] ) }
       ON { [ [TABLE] [[[ONLY] <table_name> [, ...]] [, ...]] }
       FROM <role_specification> [, ...]
       [ CASCADE | RESTRICT ]

REVOKE [GRANT OPTION FOR] { {USAGE | SELECT | UPDATE} [,...] 
       | ALL [PRIVILEGES] }
       ON { SEQUENCE <sequence_name> [, ...]
            | ALL SEQUENCES IN SCHEMA schema_name [, ...] }
       FROM <role_specification> [, ...]
       [CASCADE | RESTRICT]

REVOKE [GRANT OPTION FOR]
       { {CREATE | CONNECT | TEMPORARY | TEMP} [, ...] | ALL [PRIVILEGES] }
       ON DATABASE <database_name> [, ...]
       FROM <role_specification> [, ...]
       [CASCADE | RESTRICT]

REVOKE [ GRANT OPTION FOR ]
       { USAGE | ALL [ PRIVILEGES ] }
       ON DOMAIN <domain_name> [, ...]
       FROM <role_specification> [, ...]
       [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
       { USAGE | ALL [ PRIVILEGES ] }
       ON FOREIGN DATA WRAPPER <fdw_name> [, ...]
       FROM <role_specification> [, ...]
       [ CASCADE | RESTRICT ]

REVOKE [ GRANT OPTION FOR ]
       { USAGE | ALL [ PRIVILEGES ] }
       ON FOREIGN SERVER <server_name> [, ...]
       FROM <role_specification> [, ...]
       [ CASCADE | RESTRICT ]

REVOKE [GRANT OPTION FOR] {EXECUTE | ALL [PRIVILEGES]}
       ON { { FUNCTION | PROCEDURE | ROUTINE }  <funcname> [( [[<argmode>] [<argname>] <argtype> [, ...]] )] [, ...]
            | ALL { FUNCTIONS | PROCEDURES | ROUTINES } IN SCHEMA schema_name [, ...] }
       FROM <role_specification> [, ...]
       [CASCADE | RESTRICT]

REVOKE [GRANT OPTION FOR] {USAGE | ALL [PRIVILEGES]}
       ON LANGUAGE <lang_name> [, ...]
       FROM <role_specification> [, ...]
       [ CASCADE | RESTRICT ]

REVOKE [GRANT OPTION FOR] { {CREATE | USAGE} [, ...] | ALL [PRIVILEGES] }
       ON SCHEMA <schema_name> [, ...]
       FROM <role_specification> [, ...]
       [CASCADE | RESTRICT]

REVOKE [GRANT OPTION FOR] { CREATE | ALL [PRIVILEGES] }
       ON TABLESPACE <tablespace_name> [, ...]
       FROM <role_specification> [, ...]
       [CASCADE | RESTRICT]

REVOKE [ GRANT OPTION FOR ]
       { USAGE | ALL [ PRIVILEGES ] }
       ON TYPE <type_name> [, ...]
       FROM <role_specification> [, ...]
       [ CASCADE | RESTRICT ] 

REVOKE [ADMIN OPTION FOR] <role_name> [, ...]
       FROM [ GROUP ] <role_specification> [, ...]
       [GRANTED BY <role_specification> ]
       [CASCADE | RESTRICT]

-- where <role_specification> can be:

    [ GROUP ] <role_name>
  | PUBLIC
  | CURRENT_USER
  | SESSION_USER
```

## 说明 {#description}

`REVOKE` 命令从一个或多个角色撤销此前授予的权限。关键字 `PUBLIC` 指隐式定义的、包含所有角色的组。

各种权限类型的含义请参阅 [GRANT](/cloudberry/reference/sql-stmts/grant/) 命令的说明。

注意，任何特定角色拥有的权限，都是直接授予它的权限、授予它当前所属角色的权限，以及授予 `PUBLIC` 的权限之和。因此，从 `PUBLIC` 撤销 `SELECT` 权限，并不一定意味着所有角色都失去了该对象上的 `SELECT` 权限：直接或通过其他角色获得该权限的角色仍然拥有它。同样，从某用户撤销 `SELECT`，也不一定能阻止该用户使用 `SELECT`，因为 `PUBLIC` 或该用户所属的其他角色可能仍具有 `SELECT` 权限。

如果指定 `GRANT OPTION FOR`，只撤销该权限的授权选项，不撤销权限本身。否则，同时撤销权限和授权选项。

如果某个角色持有带授权选项的权限，并已将其授予其他角色，那么这些其他角色持有的权限称为依赖权限。撤销第一个角色的权限或授权选项时，如果存在依赖权限，指定 `CASCADE` 就会一并撤销这些依赖权限，否则撤销操作会失败。这种递归撤销只影响通过角色授权链授予、且能追溯到本次 `REVOKE` 命令目标角色的权限。因此，如果受影响的角色还通过其他角色获得了该权限，实际上仍可能保留该权限。

撤销表上的权限时，Apache Cloudberry 也会撤销该表各列上的对应列权限（如果存在）。另一方面，如果某角色已经获得表上的权限，那么撤销单个列上的相同权限不会产生作用。

默认情况下，撤销分区表上的权限时，Apache Cloudberry 会将操作递归应用到其子表。要让 Apache Cloudberry 只对分区表执行 `REVOKE`，请指定 `ONLY <table_name>` 子句。

撤销角色成员资格时，`GRANT OPTION` 改称为 `ADMIN OPTION`，但行为类似。此命令形式也允许 `GRANTED BY` 选项，不过目前会忽略该选项（只检查所指定角色是否存在）。还应注意，此命令形式不允许在 role_specification 中使用无实际作用的关键字 `GROUP`。

## 参数 {#parameters}

请参阅 [GRANT](/cloudberry/reference/sql-stmts/grant/)。

## 注意事项 {#notes}

用户只能撤销自己直接授予的权限。例如，用户 A 将某权限连同授权选项授予用户 B，而 B 又将其授予用户 C，则 A 不能直接从 C 撤销权限。A 可以改为从 B 撤销授权选项，并使用 `CASCADE` 选项，使 C 的权限也随之撤销。再如，如果 A 和 B 都向 C 授予了同一权限，A 可以撤销自己的授权，却不能撤销 B 的授权，因此 C 实际上仍拥有该权限。

非所有者尝试对对象执行 `REVOKE` 时，如果用户对该对象没有任何权限，命令会直接失败。只要具有某些权限，命令就会继续，但只撤销该用户具有授权选项的那些权限。对于 `REVOKE ALL PRIVILEGES` 形式，如果用户没有任何授权选项，会发出警告；对于其他形式，如果缺少命令明确列出的任何权限的授权选项，就会发出警告。（原则上这些规则也适用于对象所有者，但由于 Apache Cloudberry 始终将所有者视为持有全部授权选项，这些情况不会发生。）

如果超级用户执行 `GRANT` 或 `REVOKE` 命令，Apache Cloudberry 会将其视为由受影响对象的所有者执行。由于所有权限最终都来自对象所有者（可能通过授权选项链间接授予），超级用户可以撤销所有权限，但可能需要按上文所述使用 `CASCADE`。

`REVOKE` 也可以由不是受影响对象所有者的角色调用，只要它是拥有该对象的角色的成员，或是对该对象持有 `WITH GRANT OPTION` 权限的角色的成员。此时，Apache Cloudberry 会将命令视为由实际拥有对象或持有 `WITH GRANT OPTION` 权限的所属角色执行。例如，表 `t1` 由角色 `g1` 拥有，而角色 `u1` 是其成员，则 `u1` 可以撤销 `t1` 上记录为由 `g1` 授予的权限。这既包括 `u1` 作出的授权，也包括角色 `g1` 的其他成员作出的授权。

如果运行 `REVOKE` 的角色通过多条角色成员关系路径间接持有权限，系统不保证使用哪个所属角色来执行命令。此时，最佳做法是先用 `SET ROLE` 切换到希望用来执行 `REVOKE` 的具体角色。否则，可能撤销非预期的权限，或完全没有撤销任何权限。

使用 `psql` 的 `\dp` 元命令可以查看表和列的现有权限。其他 `\d` 元命令可用于显示非表对象的权限。

## 示例 {#examples}

撤销所有角色对表 `films` 的插入权限：

```sql
REVOKE INSERT ON films FROM PUBLIC;
```

撤销用户 `manuel` 对视图 `kinds` 的所有权限。注意，如果当前角色不是超级用户，这实际上表示撤销当前角色此前授予的所有权限。

```sql
REVOKE ALL PRIVILEGES ON kinds FROM manuel;
```

从用户 `joe` 撤销角色 `admins` 的成员资格：

```sql
REVOKE admins FROM joe;
```

## 兼容性 {#compatibility}

[GRANT](/cloudberry/reference/sql-stmts/grant/) 命令的兼容性说明也适用于 `REVOKE`。

标准要求显式指定 `RESTRICT` 或 `CASCADE`，而 Apache Cloudberry 默认采用 `RESTRICT`。

## 另请参阅 {#see-also}

[ALTER DEFAULT PRIVILEGES](/cloudberry/reference/sql-stmts/alter-default-privileges/), [GRANT](/cloudberry/reference/sql-stmts/grant/)
