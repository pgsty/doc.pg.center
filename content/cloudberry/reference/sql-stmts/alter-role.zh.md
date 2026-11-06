---
title: "ALTER ROLE"
description: "修改数据库角色（用户或组）。"
weight: 250
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-role.md"
---

## 概要 {#synopsis}

```sql
ALTER ROLE <role_specification> [ WITH ] <option> [ ... ]
```

其中 `<option>` 可以是：

```sql
    SUPERUSER | NOSUPERUSER
  | CREATEDB | NOCREATEDB
  | CREATEROLE | NOCREATEROLE
  | CREATEEXTTABLE | NOCREATEEXTTABLE  [ ( attribute='value' [, ...] )
     where attributes and values are:
       type='readable'|'writable'
       protocol='gpfdist'|'http'
  | INHERIT | NOINHERIT
  | LOGIN | NOLOGIN
  | REPLICATION | NOREPLICATION
  | BYPASSRLS | NOBYPASSRLS
  | CONNECTION LIMIT <connlimit>
  | [ ENCRYPTED ] PASSWORD '<password>' | PASSWORD NULL
  | VALID UNTIL '<timestamp>'
  | [ DENY <deny_point> ]
  | [ DENY BETWEEN <deny_point> AND <deny_point>]
  | [ DROP DENY FOR <deny_point> ]

ALTER ROLE <name> RENAME TO <new_name>

ALTER ROLE { <role_specification> | ALL } [ IN DATABASE <database_name> ] SET <configuration_parameter> { TO | = } { <value> | DEFAULT }
ALTER ROLE { <role_specification> | ALL } [ IN DATABASE <database_name> ] SET <configuration_parameter> FROM CURRENT
ALTER ROLE { <role_specification> | ALL } [ IN DATABASE <database_name> ] RESET <configuration_parameter>
ALTER ROLE { <role_specification> | ALL } [ IN DATABASE <database_name> ] RESET ALL

ALTER ROLE <role_specification> RESOURCE QUEUE {<queue_name> | NONE}
ALTER ROLE <role_specification> RESOURCE GROUP {<group_name> | NONE}
```

其中 `<role_specification>` 可以是：

```sql
    <role_name>
  | CURRENT_USER
  | SESSION_USER
```

## 说明 {#description}

`ALTER ROLE` 用于修改 Apache Cloudberry 角色的属性。该命令有几种变体。

**`WITH option`**

修改 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 中可以指定的多种角色属性。（涵盖所有可能的属性，但没有用于添加或移除成员关系的选项；请使用 [GRANT](/cloudberry/reference/sql-stmts/grant/) 和 [REVOKE](/cloudberry/reference/sql-stmts/revoke/) 来完成。）命令中未提及的属性保持其先前的设置。数据库超级用户可以为任何角色修改这些设置中的任何一项。具有 `CREATEROLE` 权限的角色可以修改除 `SUPERUSER`、`REPLICATION` 和 `BYPASSRLS` 之外的任何这些设置，但仅限于非超级用户且非复制角色。普通角色只能修改自己的密码。

**`RENAME`**

修改角色的名称。数据库超级用户可以重命名任何角色。具有 `CREATEROLE` 权限的角色可以重命名非超级用户角色。当前会话用户不能被重命名（请以其他用户身份连接后再重命名该角色）。由于 MD5 加密的密码使用角色名称作为加密盐，因此如果角色的密码是 MD5 加密的，重命名角色会清除其密码。

**`SET | RESET`**

修改角色针对指定配置参数的会话默认值，该默认值可以对所有数据库生效；如果指定了 `IN DATABASE` 子句，则仅对指定数据库中的会话生效。如果指定 `ALL` 而不是角色名称，则会修改所有角色的设置。将 `ALL` 与 `IN DATABASE` 一起使用，其效果等同于使用命令 `ALTER DATABASE ... SET ...`。

此后，每当该角色启动新会话时，指定的值就会成为会话默认值，覆盖服务器配置文件（`postgresql.conf`）中存在的设置或从 `postgres` 命令行接收到的设置。这只在登录时发生；运行 [SET ROLE](/cloudberry/reference/sql-stmts/set-role/) 或 [SET SESSION AUTHORIZATION](/cloudberry/reference/sql-stmts/set-session-authorization/) 不会导致设置新的配置值。针对所有数据库设置的设置会被附加到角色上的特定数据库设置所覆盖。针对特定数据库或特定角色的设置会覆盖针对所有角色的设置。

超级用户可以修改任何人的会话默认值。具有 `CREATEROLE` 权限的角色可以修改非超级用户角色的默认值。普通角色只能为自己设置默认值。某些配置变量不能以这种方式设置，或者只有在由超级用户发出命令时才能设置。只有超级用户才能修改所有数据库中所有角色的某项设置。

**`RESOURCE QUEUE`**

将角色分配到资源队列。此后，该角色在发出查询时将受分配给该资源队列的限制约束。指定 `NONE` 可将角色分配到默认资源队列。一个角色只能属于一个资源队列。对于没有 `LOGIN` 权限的角色，资源队列不起作用。更多信息请参阅 [CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/)。

**`RESOURCE GROUP`**

为角色分配资源组。此后，该角色将受为该资源组配置的并发事务、内存和 CPU 限制约束。你可以将单个资源组分配给一个或多个角色。不能将为外部组件创建的资源组分配给角色。更多信息请参阅 [CREATE RESOURCE GROUP](/cloudberry/reference/sql-stmts/create-resource-group/)。

## 参数 {#parameters}

**`name`**

要修改其属性的角色的名称。

**`CURRENT_USER`**

修改当前用户，而不是明确指定的角色。

**`SESSION_USER`**

修改当前会话用户，而不是明确指定的角色。

**`SUPERUSER`**<br />
**`NOSUPERUSER`**<br />
**`CREATEDB`**<br />
**`NOCREATEDB`**<br />
**`CREATEROLE`**<br />
**`NOCREATEROLE`**<br />
**`INHERIT`**<br />
**`NOINHERIT`**<br />
**`LOGIN`**<br />
**`NOLOGIN`**<br />
**`REPLICATION`**<br />
**`NOREPLICATION`**<br />
**`BYPASSRLS`**<br />
**`NOBYPASSRLS`**<br />
**`CONNECTION LIMIT connlimit`**<br />
**`[ ENCRYPTED ] PASSWORD 'password'`**<br />
**`PASSWORD NULL`**<br />
**`VALID UNTIL 'timestamp'`**

这些子句用于修改最初由 `CREATE ROLE` 设置的属性。更多信息请参阅 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 参考页。

**`new_name`**

角色的新名称。

**`database_name`**

要在其中设置配置参数的数据库的名称。

**`configuration_parameter`**<br />
**`value`**

将该角色针对指定配置参数的会话默认值设置为给定值。如果值为 `DEFAULT`，或者等效地使用了 `RESET`，则会移除该角色特定的参数设置，因此该角色在新会话中将继承系统范围的默认设置。使用 `RESET ALL` 可清除所有角色特定的设置。`SET FROM CURRENT` 会将会话中该参数的当前值保存为角色特定的值。如果指定了 `IN DATABASE`，则仅为给定的角色和数据库设置或移除该配置参数。

角色特定的变量设置仅在登录时生效；[SET ROLE](/cloudberry/reference/sql-stmts/set-role/) 和 [SET SESSION AUTHORIZATION](/cloudberry/reference/sql-stmts/set-session-authorization/) 不会处理角色特定的变量设置。

有关允许的参数名称和取值的更多信息，请参阅 [SET](/cloudberry/reference/sql-stmts/set/) 和服务器配置参数。

**`group_name`**

要分配给该角色的资源组的名称。指定 group_name 为 `NONE` 会移除角色当前的资源组分配，并根据角色的能力分配一个默认资源组。`SUPERUSER` 角色被分配到 `admin_group` 资源组，而非管理员角色被分配到 `default_group` 资源组。

不能将为外部组件创建的资源组分配给角色。

**`queue_name`**

要将用户级角色分配到的资源队列的名称。只有具有 `LOGIN` 权限的角色才能被分配到资源队列。要将角色从资源队列中取消分配并放入默认资源队列，请指定 `NONE`。一个角色只能属于一个资源队列。

## 注解 {#notes}

使用 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 添加新角色，使用 [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/) 删除角色。

`ALTER ROLE` 不能修改角色的成员关系；请使用 [GRANT](/cloudberry/reference/sql-stmts/grant/) 和 [REVOKE](/cloudberry/reference/sql-stmts/revoke/) 来完成。

使用此命令指定未加密的密码时必须谨慎。密码将以明文形式传输到服务器，并且还可能被记录在客户端的命令历史或服务器日志中。psql 命令行客户端包含元命令 `\password`，可用于修改角色的密码而不暴露明文密码。

也可以将会话默认值绑定到特定数据库而不是角色；请参阅 [ALTER DATABASE](/cloudberry/reference/sql-stmts/alter-database/)。如果存在冲突，数据库-角色特定的设置会覆盖角色特定的设置，而角色特定的设置又会覆盖数据库特定的设置。

## 示例 {#examples}

修改角色的密码：

```sql
ALTER ROLE daria WITH PASSWORD 'passwd123';
```

移除角色的密码：

```sql
ALTER ROLE daria WITH PASSWORD NULL;
```

修改密码到期日期，指定密码在 2022 年 5 月 4 日正午到期，使用比 UTC 早一小时的时区：

```sql
ALTER ROLE scott VALID UNTIL 'May 4 12:00:00 2022 +1';
```

使密码永久有效：

```sql
ALTER ROLE luke VALID UNTIL 'infinity';
```

赋予角色创建其他角色和新数据库的能力：

```sql
ALTER ROLE joelle CREATEROLE CREATEDB;
```

为角色设置 `maintenance_work_mem` 参数的非默认值：

```sql
ALTER ROLE admin SET maintenance_work_mem = 100000;
```

为角色设置 `client_min_messages` 参数的非默认、特定于数据库的值：

```sql
ALTER ROLE fred IN DATABASE devel SET client_min_messages = DEBUG;
```

将角色分配到资源队列：

```sql
ALTER ROLE sammy RESOURCE QUEUE poweruser;
```

授予角色创建可写外部表的权限：

```sql
ALTER ROLE load CREATEEXTTABLE (type='writable');
```

修改角色，使其在星期日不允许登录访问：

```sql
ALTER ROLE user3 DENY DAY 'Sunday';
```

修改角色，移除不允许其在星期日登录访问的约束：

```sql
ALTER ROLE user3 DROP DENY FOR DAY 'Sunday';
```

为角色分配新的资源组：

```sql
ALTER ROLE parttime_user RESOURCE GROUP rg_light;
```

## 兼容性 {#compatibility}

`ALTER ROLE` 语句是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/)、[DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/)、[ALTER DATABASE](/cloudberry/reference/sql-stmts/alter-database/)、[SET](/cloudberry/reference/sql-stmts/set/)、[CREATE RESOURCE GROUP](/cloudberry/reference/sql-stmts/create-resource-group/)、[CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/)、[GRANT](/cloudberry/reference/sql-stmts/grant/)、[REVOKE](/cloudberry/reference/sql-stmts/revoke/)
