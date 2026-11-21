---
title: dblink
description: dblink 支持在数据库会话中连接其他数据库。
weight: 40
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/dblink.md
---

`dblink` 模块支持在数据库会话中连接其他数据库。目标数据库可以位于同一个 Apache Cloudberry 集群、另一个 Apache Cloudberry 集群或 PostgreSQL 服务器上。

> [!NOTE]
> `dblink` 用于对其他数据库执行简短的临时查询，不能替代外部表、外表或数据迁移工具。

Apache Cloudberry 的 `dblink` 模块是 PostgreSQL `dblink` 模块的修改版。适用限制见 [MPP 注意事项](#mpp-considerations)。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `dblink`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION dblink;
```

## MPP 注意事项 {#mpp-considerations}

- 命名或隐式（未命名）的 `dblink` 连接仅存在于服务当前会话的 Coordinator 进程中。`INSERT INTO ... SELECT ... FROM dblink(...)` 等修改表数据的语句会在另一个进程中运行 `dblink()` 调用，该进程看不到此连接。对于这类语句，应直接将连接字符串传给 `dblink()`。以下示例读取[使用 dblink](#use-dblink) 第 1 步中创建的 `testdblink` 表：

    ```sql
    CREATE TABLE testdbllocal (a int, b text) DISTRIBUTED BY (a);
    INSERT INTO testdbllocal
      SELECT * FROM dblink('dbname=postgres', 'SELECT * FROM testdblink') AS dbltab(id int, product text);
    ```

    如果改用连接名称，语句会失败，报错为 `could not establish connection`，详情为 `missing "=" after "<connection name>" in connection info string`。

- 不支持异步查询。扩展不会创建 `dblink_send_query()`、`dblink_is_busy()` 和 `dblink_get_result()` 函数。

- 非超级用户必须在 `dblink_connect()` 和 `dblink()` 的连接字符串中同时指定 `host` 和 `password`，即使连接本地数据库也是如此。否则，调用会报错 `host is required` 或 `password is required`。非超级用户未指定 `user` 时，使用当前数据库用户名。

## 使用 dblink {#use-dblink}

以下步骤展示 `dblink` 的基本用法。示例使用 `dblink_connect()` 创建数据库连接，使用 `dblink()` 运行 SQL 查询。

1. 在 `postgres` 数据库中创建示例表：

    ```sql
    CREATE TABLE testdblink (a int, b text) DISTRIBUTED BY (a);
    INSERT INTO testdblink VALUES (1, 'Cheese'), (2, 'Fish');
    ```

2. 以超级用户身份登录另一个数据库（例如 `testdb`），如果尚未注册扩展，先注册它：

    ```sql
    CREATE EXTENSION dblink;
    ```

3. 使用 `dblink_connect()` 创建到另一个数据库的隐式连接或命名连接。连接字符串采用 `libpq` 风格的关键字/值字符串。此示例创建名为 `mylocalconn` 的连接，连接本地集群上的 `postgres` 数据库：

    ```sql
    SELECT dblink_connect('mylocalconn', 'dbname=postgres user=gpadmin');
    ```

    ```text
     dblink_connect
    ----------------
     OK
    (1 row)
    ```

4. 使用 `dblink()` 通过该连接运行查询。函数返回 `record`，因此必须指定返回列的名称和类型：

    ```sql
    SELECT * FROM dblink('mylocalconn', 'SELECT * FROM testdblink') AS dbltab(id int, product text);
    ```

    ```text
     id | product
    ----+---------
      1 | Cheese
      2 | Fish
    (2 rows)
    ```

5. 不再需要连接时，关闭它：

    ```sql
    SELECT dblink_disconnect('mylocalconn');
    ```

连接远程系统时，在连接字符串中包含主机和密码信息。例如，创建隐式连接：

```sql
SELECT dblink_connect('host=remotehost port=5432 dbname=postgres user=gpadmin password=secret');
```

### 以非超级用户身份使用 dblink {#use-dblink-as-a-non-superuser}

非超级用户必须在 `dblink_connect()` 的连接字符串中包含主机和密码。例如，用户 `test_user` 可以使用以下命令创建到本地 Coordinator 主机 `cdw` 的连接：

```sql
SELECT dblink_connect('host=cdw port=5432 dbname=postgres user=test_user password=secret');
```

远程服务器还必须实际要求该连接提供密码。如果未要求（例如使用 `trust` 身份验证），调用会报错 `password is required`。

要允许非超级用户创建不要求密码的连接，使用 `dblink_connect_u()` 函数。除跳过这些检查外，它与 `dblink_connect()` 相同。安装 `dblink_connect_u()` 时，`PUBLIC` 对它的所有权限均被撤销，因此在你授予其 `EXECUTE` 权限之前，只有超级用户可以调用。

> [!CAUTION]
> 只向可信用户授予 `dblink_connect_u()` 的 `EXECUTE` 权限。如果目标系统中有用户采用不涉及密码的身份验证方式，能够调用 `dblink_connect_u()` 的非超级用户就可以冒充该用户并提升权限。此外，密码还可能由服务器环境提供，例如由运行服务器的操作系统用户所有的 `~/.pgpass` 文件提供。

1. 以超级用户身份，授予 `dblink_connect_u()` 函数的 `EXECUTE` 权限：

    ```sql
    GRANT EXECUTE ON FUNCTION dblink_connect_u(text) TO test_user;
    GRANT EXECUTE ON FUNCTION dblink_connect_u(text, text) TO test_user;
    ```

2. 以 `test_user` 身份创建不带密码的连接并使用它：

    ```sql
    SELECT dblink_connect_u('testconn', 'dbname=postgres user=test_user');
    SELECT * FROM dblink('testconn', 'SELECT * FROM testdblink') AS dbltab(id int, product text);
    ```

### 通过 SSL 加密连接使用 dblink {#use-dblink-with-ssl-encrypted-connections}

要使用加密连接，在连接字符串中指定 `sslmode` 关键字。将 `sslmode` 设为至少 `require`，以禁止未加密连接。例如：

```sql
SELECT dblink_connect('con_sales', 'dbname=sales host=cdw user=gpadmin sslmode=require');
```

## 模块文档 {#module-documentation}

此模块各个函数的详细信息，参见 PostgreSQL 文档中的 [dblink](https://www.postgresql.org/docs/14/dblink.html)。
