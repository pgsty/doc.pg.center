---
title: "在 Apache Cloudberry 中管理角色与权限"
linkTitle: "管理角色与权限"
description: "Apache Cloudberry 的授权机制将角色及其访问数据库对象的权限存储在数据库中，并通过 SQL 语句或命令行工具进行管理。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/manage-roles-and-privileges.md"
---

Apache Cloudberry 使用*角色*管理数据库访问权限。角色的概念涵盖了*用户*和*组*。角色可以是数据库用户、组，也可以同时兼具两者身份。角色可以拥有数据库对象（例如表），并将这些对象的权限授予其他角色，以控制对象访问。角色也可以是其他角色的成员，因此成员角色可以继承其父角色的对象权限。

每个 Apache Cloudberry 系统都包含一组数据库角色（用户和组）。这些角色独立于服务器所在操作系统管理的用户和组。不过，为方便使用，可以让操作系统用户名与 Apache Cloudberry 角色名保持对应关系，因为许多客户端应用程序默认使用当前操作系统的用户名。

在 Apache Cloudberry 中，用户通过 Coordinator 实例登录并连接，Coordinator 随后验证其角色和访问权限。然后，Coordinator 在后台以当前登录角色的身份向 Segment 实例发送命令。

角色在系统级别定义，因此对系统中的所有数据库都有效。

为引导 Apache Cloudberry 系统，刚完成初始化的系统始终包含一个预定义的*超级用户*角色（也称为系统用户）。该角色与初始化 Apache Cloudberry 系统的操作系统用户同名。按照惯例，此角色名为 `gpadmin`。要创建更多角色，必须先以这个初始角色连接。

## 角色与权限的安全最佳实践 {#security-best-practices-for-roles-and-privileges}

- **保护 gpadmin 系统用户。** 安装和初始化 Apache Cloudberry 系统需要一个 UNIX 用户 ID。Apache Cloudberry 文档将此系统用户称为 `gpadmin`。`gpadmin` 用户既是 Apache Cloudberry 中默认的数据库超级用户，也是 Apache Cloudberry 安装文件及其底层数据文件的文件系统所有者。这个默认管理员账户是 Apache Cloudberry 设计的基础。没有它，系统就无法运行，而且无法限制 gpadmin 用户 ID 的访问权限。应使用角色管理哪些人可以出于特定目的访问数据库。`gpadmin` 账户应仅用于扩容、升级等系统维护任务。任何以此用户 ID 登录 Apache Cloudberry 主机的人，都能读取、修改或删除任何数据，包括系统目录数据和数据库访问权限。因此，保护 gpadmin 用户 ID 非常重要，只有必需的系统管理员才应获得其访问权。管理员只有在执行某些系统维护任务（如升级或扩容）时，才应以 `gpadmin` 身份登录 Apache Cloudberry。数据库用户绝不应以 `gpadmin` 身份登录，ETL 或生产工作负载也绝不应以 `gpadmin` 身份运行。
- **为每个登录用户分配独立的角色。** 为满足日志记录和审计的需要，每个获准登录 Apache Cloudberry 的用户都应拥有自己的数据库角色。对于应用程序或 Web 服务，可考虑为每个应用程序或服务创建独立的角色。请参阅[创建新角色（用户）](#create-new-roles-users)。
- **使用组管理访问权限。** 请参阅[角色成员关系](#role-membership)。
- **限制具有 SUPERUSER 角色属性的用户。** 超级用户角色会绕过 Apache Cloudberry 中的所有访问权限检查，也会绕过资源排队。只有系统管理员才应获得超级用户权限。请参阅[修改角色属性](#alter-role-attributes)。

## 创建新角色（用户） {#create-new-roles-users}

用户级角色是指能够登录数据库并发起数据库会话的数据库角色。因此，使用 `CREATE ROLE` 命令创建新的用户级角色时，必须指定 `LOGIN` 权限。例如：

```sql
=# CREATE ROLE jsmith WITH LOGIN;
```

数据库角色可以具有多个属性，用于定义该角色能够在数据库中执行哪些任务。可以在创建角色时设置这些属性，也可以稍后使用 `ALTER ROLE` 命令设置。

### 修改角色属性 {#alter-role-attributes}

数据库角色可以具有多个属性，用于定义该角色能够在数据库中执行哪些任务。

|属性|说明|
|----------|-----------|
|`SUPERUSER` 或 `NOSUPERUSER`|决定角色是否为超级用户。创建新的超级用户时，自己也必须是超级用户。默认为 `NOSUPERUSER`。|
|`CREATEDB` 或 `NOCREATEDB`|决定角色是否允许创建数据库。默认为 `NOCREATEDB`。|
|`CREATEROLE` 或 `NOCREATEROLE`|决定角色是否允许创建和管理其他角色。默认为 `NOCREATEROLE`。|
|`INHERIT` 或 `NOINHERIT`|决定角色是否继承其所属角色的权限。具有 `INHERIT` 属性的角色，可以自动使用其直接或间接所属的所有角色获得的数据库权限。默认为 `INHERIT`。 |
|`LOGIN` 或 `NOLOGIN`|决定角色是否允许登录。具有 `LOGIN` 属性的角色可以视为用户。不具有此属性的角色适合用于管理数据库权限（组）。默认为 `NOLOGIN`。|
|`CONNECTION LIMIT *connlimit*`|如果角色可以登录，此属性指定该角色可建立的并发连接数。-1（默认值）表示不限制。|
|`CREATEEXTTABLE` 或 `NOCREATEEXTTABLE`|决定角色是否允许创建外部表。默认为 `NOCREATEEXTTABLE`。对于具有 `CREATEEXTTABLE` 属性的角色，默认外部表 `type` 为 `readable`，默认 `protocol` 为 `gpfdist`。请注意，只有超级用户才能创建使用 `file` 协议的外部表。|
|`PASSWORD '*password*'`|设置角色的密码。如果不打算使用密码认证，可以省略此选项。如果未指定密码，密码将设为 null，该用户的密码认证将始终失败。也可以显式写为 `PASSWORD NULL`，将密码设为 NULL。|
|`DENY deny_interval` 或 `DENY deny_point` | 在指定时段内限制访问，时段可以按星期几，或按星期几和时间指定。有关详细信息，请参阅[按时间限制访问](/cloudberry/security/configure-db-auth/#restrict-access-by-time)。|

可以在创建角色时设置这些属性，也可以稍后使用 `ALTER ROLE` 命令设置。例如：

```sql
=# ALTER ROLE jsmith WITH PASSWORD 'passwd123';
=# ALTER ROLE jsmith LOGIN;
=# ALTER ROLE jsmith DENY DAY 'Sunday';
```

角色还可以为许多服务器配置项设置专属的默认值。例如，为某个角色设置默认模式搜索路径：

```sql
=# ALTER ROLE admin SET search_path TO myschema, public;
```

## 角色成员关系 {#role-membership}

将用户归为一组通常有助于简化对象权限管理：这样就可以对整个组授予或撤销权限。在 Apache Cloudberry 中，做法是创建一个代表该组的角色，再将组角色的成员身份授予各个用户角色。

使用 `CREATE ROLE` SQL 命令创建新的组角色。例如：

```sql
=# CREATE ROLE admin CREATEROLE CREATEDB;
```

组角色创建后，可以使用 `GRANT` 和 `REVOKE` 命令添加和移除成员（用户角色）。例如：

```sql
=# GRANT admin TO john, sally;
=# REVOKE admin FROM bob;
```

管理对象权限时，只需将适当的权限授予组级角色（请参阅[管理对象权限](#manage-object-privileges)）。成员用户角色随后便会继承组角色的对象权限。例如：

```sql
=# GRANT ALL ON TABLE mytable TO admin;
=# GRANT ALL ON SCHEMA myschema TO admin;
=# GRANT ALL ON DATABASE mydb TO admin;
```

`LOGIN`、`SUPERUSER`、`CREATEDB`、`CREATEROLE`、`CREATEEXTTABLE` 和 `RESOURCE QUEUE` 这些角色属性，绝不会像数据库对象的普通权限那样被继承。用户成员必须通过 `SET ROLE` 切换到具有某个属性的特定角色，才能使用该属性。在上例中，我们为 `admin` 角色赋予了 `CREATEDB` 和 `CREATEROLE`。如果 `sally` 是 `admin` 的成员，那么 `sally` 可以执行以下命令，取得父角色的角色属性：

```sql
=> SET ROLE admin;
```

## 管理对象权限 {#manage-object-privileges}

创建对象（表、视图、序列、数据库、函数、语言、模式或表空间）时，会为其指定一个所有者。所有者通常是执行创建语句的角色。对于大多数类型的对象，初始状态下只有所有者（或超级用户）能够对其执行操作。要允许其他角色使用对象，必须授予相应权限。Apache Cloudberry 为各类对象支持以下权限：

| 对象类型                      | 权限                                                                                   |
| :-----------------------------| :--------------------------------------------------------------------------------------|
| 表、外部表、视图               | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REFERENCES`, `TRIGGER`, `TRUNCATE`, `ALL`   |
| 列                            | `SELECT`, `INSERT`, `UPDATE`, `REFERENCES`, `ALL`                                    |
| 序列                          | `USAGE`, `SELECT`, `UPDATE`, `ALL`                                                   |
| 数据库                        | `CREATE`, `CONNECT`, `TEMPORARY`, `TEMP`, `ALL`                                      |
| 域                            | `USAGE`, `ALL`                                                                       |
| 外部数据包装器                 | `USAGE`, `ALL`                                                                       |
| 外部服务器                    | `USAGE`, `ALL`                                                                       |
| 函数                          | `EXECUTE`, `ALL`                                                                     |
| 过程语言                      | `USAGE`, `ALL`                                                                       |
| 模式                          | `CREATE`, `USAGE`, `ALL`                                                             |
| 表空间                        | `CREATE`, `ALL`                                                                      |
| 类型                          | `USAGE`, `ALL`                                                                       |
| 协议                          | `SELECT`, `INSERT`, `ALL`                                                            |

> [!NOTE] 注意
> 必须为每个对象单独授予权限。例如，在数据库上授予 `ALL` 并不意味着可以完全访问该数据库中的对象。它只是在数据库本身上授予所有数据库级权限（`CONNECT`、`CREATE`、`TEMPORARY`）。

使用 `GRANT` SQL 命令将对象的权限授予指定角色。例如，将表 `mytable` 的插入权限授予角色 `jsmith`：

```sql
=# GRANT INSERT ON mytable TO jsmith;
```

类似地，要仅将表 `table2` 中 `col1` 列的查询权限授予 `jsmith`：

```sql
=# GRANT SELECT (col1) on TABLE table2 TO jsmith;
```

要撤销权限，请使用 `REVOKE` 命令。例如：

```sql
=# REVOKE ALL PRIVILEGES ON mytable FROM jsmith;
```

还可以使用 `DROP OWNED` 和 `REASSIGN OWNED` 命令，管理已停用角色拥有的对象（注意：只有对象的所有者或超级用户才能删除对象或重新指定其所有者）。例如：

```sql
=# REASSIGN OWNED BY sally TO bob;
=# DROP OWNED BY visitor;
```

## 加密数据 {#encrypt-data}

Apache Cloudberry 安装时附带一个名为 `pgcrypto` 的可选加密/解密函数模块。`pgcrypto` 函数允许数据库管理员以加密形式存储某些列的数据。这为敏感数据增加了一层保护，因为存储在 Apache Cloudberry 中的加密数据既不能被没有加密密钥的人读取，也无法直接从磁盘读取。

> [!NOTE] 注意
> `pgcrypto` 函数在数据库服务器内部运行，这意味着所有数据和密码都以明文形式在 `pgcrypto` 与客户端应用程序之间传输。

要使用 `pgcrypto` 函数，请在每个需要使用这些函数的数据库中注册 `pgcrypto` 扩展。例如：

```shell
psql -d testdb -c "CREATE EXTENSION pgcrypto"
```

有关各个函数的更多信息，请参阅 PostgreSQL 文档中的 [pgcrypto](https://www.postgresql.org/docs/12/pgcrypto.html)。
