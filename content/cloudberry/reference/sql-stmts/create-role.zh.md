---
title: "CREATE ROLE"
description: "定义新的数据库角色（用户或组）。"
weight: 760
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-role.md"
---

## 语法概要 {#synopsis}

```sql
CREATE ROLE <name> [[WITH] <option> [ ... ]]
```

其中 option 可以为：

```sql
      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | CREATEEXTTABLE | NOCREATEEXTTABLE 
      [ ( <attribute>='<value>'[, ...] ) ]
           where <attributes> and <value> are:
           type='readable'|'writable'
           protocol='gpfdist'|'http'
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT <connlimit>
    | [ ENCRYPTED ] PASSWORD '<password>' | PASSWORD NULL
    | VALID UNTIL '<timestamp>' 
    | IN ROLE <role_name> [, ...]
    | IN GROUP <role_name> [, ...]
    | ROLE <role_name> [, ...]
    | ADMIN <role_name> [, ...]
    | USER <role_name> [, ...]
    | SYSID <uid> [, ...]
    | RESOURCE QUEUE <queue_name>
    | RESOURCE GROUP <group_name>
    | [ DENY <deny_point> ]
    | [ DENY BETWEEN <deny_point> AND <deny_point>]
```

## 说明 {#description}

`CREATE ROLE` 向 Apache Cloudberry 系统添加新角色。角色是可以拥有数据库对象并具有数据库权限的实体。根据使用方式，角色可以视为用户、组，或兼具两者身份。必须具有 `CREATEROLE` 权限或是数据库超级用户，才能使用此命令。

注意，角色在系统级定义，对 Apache Cloudberry 系统中的所有数据库均有效。

## 参数 {#parameters}

**`name`**

新角色的名称。

**`SUPERUSER`**<br />
**`NOSUPERUSER`**

这些子句决定新角色是否为“超级用户”。如果指定 `SUPERUSER`，所定义的角色就是超级用户，可以绕过数据库内的所有访问限制。超级用户身份具有风险，只应在确实需要时使用。只有超级用户才能创建新的超级用户。默认值为 `NOSUPERUSER`。

**`CREATEDB`**<br />
**`NOCREATEDB`**

这些子句定义角色创建数据库的能力。如果指定 `CREATEDB`，所定义的角色将被允许创建新数据库。指定 `NOCREATEDB`（默认值）则禁止该角色创建数据库。

**`CREATEROLE`**<br />
**`NOCREATEROLE`**

这些子句决定角色是否可以创建新角色（即执行 `CREATE ROLE`）。如果指定 `CREATEROLE`，所定义的角色可以创建新角色、修改其他角色以及删除其他角色。`NOCREATEROLE`（默认值）则禁止角色创建角色，或修改自身以外的角色。

**`CREATEEXTTABLE`**<br />
**`NOCREATEEXTTABLE`**

如果指定 `CREATEEXTTABLE`，所定义的角色可以创建外部表。如果未指定，默认 `type` 为 `readable`，默认 `protocol` 为 `gpfdist`。有效类型为 `gpfdist`、`gpfdists`、`http` 和 `https`。`NOCREATEEXTTABLE`（默认类型）禁止该角色创建外部表。注意，使用 `file` 或 `execute` 协议的外部表只能由超级用户创建。

使用 `GRANT...ON PROTOCOL` 命令，可允许用户创建和使用采用自定义协议类型的外部表，包括 Apache Cloudberry 自带的 `s3` 和 `pxf` 协议。

**`INHERIT`**<br />
**`NOINHERIT`**

这些子句决定角色是否“继承”其所属角色的权限。`INHERIT`（默认值）允许角色使用授予其直接或间接所属角色的所有数据库权限。使用 `NOINHERIT` 时，其他角色的成员身份只赋予通过 `SET ROLE` 切换到该角色的能力；只有切换之后，才能使用该角色的权限。

**`LOGIN`**<br />
**`NOLOGIN`**

这些子句决定角色能否登录，即能否在客户端连接时将该角色用作初始会话授权名。指定 `LOGIN` 允许角色登录数据库。具有 `LOGIN` 属性的角色可视为用户。具有 `NOLOGIN` 的角色适合管理数据库权限，但不是通常意义上的用户。如果未指定，默认为 `NOLOGIN`，除非通过另一种写法 [CREATE USER](/cloudberry/reference/sql-stmts/create-user/) 调用 `CREATE ROLE`。

**`REPLICATION`**<br />
**`NOREPLICATION`**

这些子句决定角色是否为复制角色。角色必须具有此属性（或是超级用户），才能以复制模式（物理复制或逻辑复制）连接服务器，以及创建或删除复制槽。具有 `REPLICATION` 属性的角色权限很高，只应为实际用于复制的角色设置此属性。如果未指定，默认为 `NOREPLICATION`。只有超级用户才能创建具有 `REPLICATION` 属性的新角色。

**`BYPASSRLS`**<br />
**`NOBYPASSRLS`**

这些子句决定角色是否绕过所有行级安全（RLS）策略。默认值为 `NOBYPASSRLS`。只有超级用户才能创建具有 `BYPASSRLS` 属性的新角色。

注意，`pg_dump` 默认会将 row_security 设为 `OFF`，以确保转储表的全部内容。如果运行 `pg_dump` 的用户没有适当权限，就会报错。不过，超级用户和被转储表的所有者始终绕过 RLS。

**`CONNECTION LIMIT connlimit`**

如果角色可以登录，此选项指定该角色允许建立的并发连接数。默认值 `-1` 表示不限制。注意，此限制只统计普通连接，不计入预备事务或后台工作进程的连接。

**`[ ENCRYPTED ] PASSWORD 'password'`**<br />
**`PASSWORD NULL`**

设置角色的密码。（密码只对具有 `LOGIN` 属性的角色有用，但仍可为不具有该属性的角色定义密码。）如果不打算使用密码认证，可以省略此选项。如果没有指定密码，密码将被设为空值，该用户的密码认证始终会失败。也可以显式写 `PASSWORD NULL` 来指定空密码。

> **注意：** 指定空字符串也会将密码设为空值，但在 Apache Cloudberry 7 之前并非如此。在较早版本中，能否使用空字符串取决于认证方法和具体版本，而 `libpq` 无论如何都会拒绝使用它。为避免歧义，不应指定空字符串。

密码始终以加密形式保存在系统目录中。`ENCRYPTED` 关键字不起作用，但为向后兼容仍被接受。加密方法由配置参数 `password_encryption` 决定。如果提供的密码字符串已经是 MD5 或 SCRAM 加密格式，则无论 `password_encryption` 如何设置，都按原样存储（因为系统无法解密所指定的加密密码字符串，再以另一种格式加密）。这使得转储/恢复过程中可以重新载入加密密码。

**`VALID UNTIL 'timestamp'`**

VALID UNTIL 子句设置角色密码失效的日期和时间。如果省略此子句，密码永不过期。

**`IN ROLE role_name`**

将新角色添加为所列角色的成员。（注意，没有将新角色添加为管理员的选项；需要使用单独的 `GRANT` 命令。）

**`IN GROUP role_name`**

`IN GROUP` 是 `IN ROLE` 的过时写法。

**`ROLE role_name`**

将所列角色添加为此角色的成员。（这实际上使新角色成为一个“组”。）

**`ADMIN rolename`**

`ADMIN` 子句类似于 `ROLE`，但会以 `WITH ADMIN OPTION` 将所列角色添加到新角色中，使它们有权将该角色的成员资格授予其他角色。

**`USER role_name`**

`USER` 子句是 `ROLE` 子句的过时写法。

**`SYSID uid`**

`SYSID` 子句会被忽略，但为向后兼容仍被接受。

**`RESOURCE GROUP group_name`**

要分配给新角色的资源组名称。该角色受资源组配置的并发事务数、内存和 CPU 限制。一个资源组可以分配给一个或多个角色。

如果没有为新角色指定资源组，系统会按角色能力自动分配默认资源组：`SUPERUSER` 角色使用 `admin_group`，非管理角色使用 `default_group`。

可以将 `admin_group` 资源组分配给任何具有 `SUPERUSER` 属性的角色。

可以将 `default_group` 资源组分配给任何角色。

不能将为外部组件创建的资源组分配给角色。

**`RESOURCE QUEUE queue_name`**

要为新的用户级角色分配的资源队列名称。只有具有 `LOGIN` 权限的角色才能分配到资源队列。特殊关键字 `NONE` 表示将角色分配到默认资源队列。一个角色只能属于一个资源队列。

具有 `SUPERUSER` 属性的角色不受资源队列限制。超级用户角色的查询始终立即运行，不受所分配资源队列限制的影响。

**`DENY deny_point`**<br />
**`DENY BETWEEN deny_point AND deny_point`**

`DENY` 和 `DENY BETWEEN` 关键字设置在登录时实施的时间约束。`DENY` 设置拒绝访问的某一天，或某一天的某个时间。`DENY BETWEEN` 设置拒绝访问的时间区间。两者都使用以下格式的 deny_point 参数：

```sql
DAY day [ TIME 'time' ]
```

`deny_point` 参数的两部分采用以下格式：

`day` 的格式：

```sql
{'Sunday' | 'Monday' | 'Tuesday' |'Wednesday' | 'Thursday' | 'Friday' | 
'Saturday' | 0-6 }
```

`time` 的格式：

```sql
{ 00-23 : 00-59 | 01-12 : 00-59 { AM | PM }}
```

`DENY BETWEEN` 子句使用两个 deny_point 参数：

```sql
DENY BETWEEN <deny_point> AND <deny_point>
```

## 注意事项 {#notes}

使用 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 更改角色属性，使用 [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/) 删除角色。`CREATE ROLE` 指定的所有属性均可通过后续的 `ALTER ROLE` 命令修改。

添加和移除角色成员的推荐方法是使用 [GRANT](/cloudberry/reference/sql-stmts/grant/) 和 [REVOKE](/cloudberry/reference/sql-stmts/revoke/)。

`VALID UNTIL` 子句只定义密码的过期时间，不定义角色*本身*的过期时间。使用非密码认证方法登录时，不检查此过期时间。

`INHERIT` 属性控制可授予权限（数据库对象访问权限和角色成员资格）的继承，不适用于 `CREATE ROLE` 和 `ALTER ROLE` 设置的特殊角色属性。例如，成为具有 `CREATEDB` 权限的角色的成员，并不会立即获得创建数据库的能力，即使已设置 `INHERIT` 也是如此；必须先通过 [SET ROLE](/cloudberry/reference/sql-stmts/set-role/) 切换到该角色，才能创建数据库。

出于向后兼容的考虑，默认启用 `INHERIT` 属性。在早期 Apache Cloudberry 版本中，用户始终可以使用其所属组的所有权限。不过，`NOINHERIT` 更接近 SQL 标准规定的语义。

请谨慎使用 `CREATEROLE` 权限。具有 `CREATEROLE` 的角色所拥有的权限不受继承概念约束。这意味着，即使某个角色没有某项权限，只要允许它创建其他角色，它就可以轻易创建权限与自身不同的角色（但不能创建具有超级用户权限的角色）。例如，某个角色具有 `CREATEROLE` 权限但没有 `CREATEDB` 权限，它仍可以创建具有 `CREATEDB` 权限的新角色。因此，应将具有 `CREATEROLE` 权限的角色视为接近超级用户的角色。

Apache Cloudberry 提供 createuser 程序，功能与 `CREATE ROLE` 相同（实际上就是调用此命令），但可以从命令行 shell 运行。

`CONNECTION LIMIT` 选项只能近似实施；如果角色只剩一个连接“名额”，而两个新会话几乎同时启动，两者可能都会失败。此外，此限制从不对超级用户实施。

用此命令指定未加密密码时必须谨慎。密码会以明文传送给服务器，也可能被记录在客户端命令历史或服务器日志中。不过，客户端程序 createuser 会以加密形式传送密码。此外，psql 提供 `\password` 命令，可用于之后安全地修改密码。

## 示例 {#examples}

创建可以登录但没有密码的角色：

```sql
CREATE ROLE jonathan LOGIN;
```

创建具有密码的角色：

```sql
CREATE USER davide WITH PASSWORD 'jw8s0F4';
```

（`CREATE USER` 与 `CREATE ROLE` 相同，只是前者隐含 `LOGIN`。）

创建密码有效期截至 2022 年年底的角色：

```sql
CREATE USER joelle WITH LOGIN PASSWORD 'jw8s0F4' VALID UNTIL '2023-01-01';
```

创建可以创建数据库并管理其他角色的角色：

```sql
CREATE ROLE admin WITH CREATEDB CREATEROLE;
```

创建不允许在星期日登录的角色：

```sql
CREATE ROLE user3 DENY DAY 'Sunday';
```

创建可以创建 'gpfdist' 类型的可读和可写外部表的角色：

```sql
CREATE ROLE jan WITH CREATEEXTTABLE(type='readable', protocol='gpfdist')
   CREATEEXTTABLE(type='writable', protocol='gpfdist'); 
```

创建角色并分配资源组：

```sql
CREATE ROLE bill RESOURCE GROUP rg_light;
```

创建属于某个资源队列的角色：

```sql
CREATE ROLE jonathan LOGIN RESOURCE QUEUE poweruser;
```

## 兼容性 {#compatibility}

SQL 标准包含 `CREATE ROLE`，但标准只要求以下语法：

```sql
CREATE ROLE <name> [WITH ADMIN <rolename>]
```

允许指定多个初始管理员，以及 `CREATE ROLE` 的所有其他选项，都是 Apache Cloudberry 的扩展。

SQL 标准定义了用户和角色的概念，但将其视为不同概念，并将所有定义用户的命令交由数据库实现规定。在 Apache Cloudberry 中，用户和角色统一为一种对象。因此，角色具有比标准中多得多的可选属性。

为用户设置 `NOINHERIT` 属性、为角色设置 `INHERIT` 属性，最接近 SQL 标准规定的行为。

## 另请参阅 {#see-also}

[SET ROLE](/cloudberry/reference/sql-stmts/set-role/), [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/), [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/), [GRANT](/cloudberry/reference/sql-stmts/grant/), [REVOKE](/cloudberry/reference/sql-stmts/revoke/), [CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/) [CREATE RESOURCE GROUP](/cloudberry/reference/sql-stmts/create-resource-group/), createuser
