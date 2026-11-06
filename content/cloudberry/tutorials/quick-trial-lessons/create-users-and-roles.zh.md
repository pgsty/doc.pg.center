---
title: "第 1 课：创建用户和角色"
description: "通过本简介学习如何在 Apache Cloudberry 中创建用户和角色。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/quick-trial-lessons/create-users-and-roles.md"
---

Apache Cloudberry 使用角色管理数据库访问。最初只有一个超级用户角色，即初始化数据库实例的操作系统用户所关联的角色，通常是 `gpadmin`。该用户拥有 Apache Cloudberry 的所有文件和操作系统进程，因此应当只将 `gpadmin` 角色保留给系统任务使用。

角色可以是用户，也可以是组。用户角色可以登录数据库，也就是说，它具有 `LOGIN` 属性。用户角色或组角色可以成为某个组的成员。

可以向用户或组授予权限。最初只有 `gpadmin` 角色能够创建角色。你可以使用 `createuser` 工具命令、`CREATE ROLE` SQL 命令或 `CREATE USER` SQL 命令添加角色。`CREATE USER` 命令与 `CREATE ROLE` 命令相同，只是它会自动为角色分配 `LOGIN` 属性。

## 快速开始操作 {#quick-start-operations}

你可以按照下面的示例创建用户和角色。

继续操作前，请按照[安装 Apache Cloudberry](https://github.com/apache/cloudberry-bootcamp/tree/main/000-cbdb-sandbox)完成 Apache Cloudberry 的安装。

### 使用 CREATE USER 命令创建用户 {#create-a-user-using-the-create-user-command}

1. 在 Docker 中登录 Apache Cloudberry。以 `gpadmin` 用户连接数据库。

    ```shell
    [gpadmin@cdw ~]$ psql

    psql (14.4, server 14.4)
    Type "help" for help.
    ```

    ```shell
    gpadmin=#
    ```

2. 创建名为 `lily` 的用户，使用 `CREATE USER` 命令将密码设为 `changeme`。创建完成后，以用户 `lily` 登录时需要输入该密码。

    ```sql
    gpadmin=# CREATE USER lily WITH PASSWORD 'changeme';
    ```

    输出：

    ```sql
    NOTICE:  resource queue required -- using default resource queue "pg_default"
    CREATE ROLE
    ```

3. 验证用户 `lily` 已创建。

    ```sql
    gpadmin=# \du
                                 List of roles
     Role name |                   Attributes                   | Member of
    -----------+------------------------------------------------+-----------
     gpadmin   | Superuser, Create role, Create DB, Replication | {}
     lily      |                                                | {}
    ```

### 使用 createuser 工具命令创建用户 {#create-a-user-using-the-createuser-utility-command}

1. 创建名为 `lucy` 的用户，使用 `createuser` 工具命令。

    ```sql
    gpadmin=# \q  -- exit psql
    ```

    ```shell
    [gpadmin@cdw ~]$ createuser --interactive lucy
    ```

    系统会询问新角色是否应当成为超级用户。输入 `y` 创建超级用户。

    ```shell
    Shall the new role be a superuser? (y/n)
    ```

2. 以 `gpadmin` 用户连接数据库。

    ```shell
    [gpadmin@cdw ~]$ psql

    psql (14.4, server 14.4)
    Type "help" for help.
    ```

3. 验证用户 `lucy` 已创建。

    ```sql
    gpadmin=# \du
                                 List of roles
     Role name |                   Attributes                   | Member of
    -----------+------------------------------------------------+-----------
     gpadmin   | Superuser, Create role, Create DB, Replication | {}
     lily      |                                                | {}
     lucy      | Superuser, Create role, Create DB              | {}
    ```

    ```sql
    gpadmin=# \q  -- exit psql
    ```

### 创建用户组并将用户加入其中 {#create-a-users-group-and-add-the-users-to-it}

1. 以 `gpadmin` 用户连接数据库。

    ```shell
    [gpadmin@cdw ~]$ psql

    psql (14.4, server 14.4)
    Type "help" for help.
    ```

    输出：

    ```shell
    gpadmin=#
    ```

2. 创建名为 `users` 的组，使用 `CREATE ROLE` 命令。

    ```sql
    gpadmin=# CREATE ROLE users;
    ```

    输出：

    ```sql
    NOTICE:  resource queue required -- using default resource queue "pg_default"
    CREATE ROLE
    ```

3. 将用户 `lily` 和 `lucy` 加入 `users` 组。

    ```sql
    gpadmin=# GRANT users TO lily, lucy;
    ```

    输出：

    ```sql
    GRANT ROLE
    ```

4. 验证两个用户已加入 `users` 组。

    ```sql
    gpadmin=# \du
                                 List of roles
     Role name |                   Attributes                   | Member of
    -----------+------------------------------------------------+-----------
     gpadmin   | Superuser, Create role, Create DB, Replication | {}
     lily      |                                                | {users}
     lucy      | Superuser, Create role, Create DB              | {users}
     users     | Cannot login                                   | {}
    ```

不过，创建 `users` 组后，`lily` 和 `lucy` 仍然无法登录 Apache Cloudberry。下面是相应的错误消息。

```shell
[gpadmin@cdw ~]$ psql -U lily -d gpadmin

psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL:  no pg_hba.conf entry for host "[local]", user "lily", database "gpadmin", no encryption
```

```shell
[gpadmin@cdw ~]$ psql -U lucy -d gpadmin

psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL:  no pg_hba.conf entry for host "[local]", user "lucy", database "gpadmin", no encryption
```

要让用户（`lily` 和 `lucy`）能够登录数据库，需要调整 Coordinator 节点上的 `pg_hba.conf` 配置文件，并使用 `gpstop` 使修改生效。

1. 在 Coordinator 节点上，将 `local gpadmin lily md5` 和 `local gpadmin lucy trust` 追加到 `pg_hba.conf` 文件中。

    ```sql
    gpadmin=# \q  -- exit psql
    ```

    ```shell
    [gpadmin@cdw ~]$ echo "local gpadmin lily md5" >> /data0/database/coordinator/gpseg-1/pg_hba.conf
    [gpadmin@cdw ~]$ echo "local gpadmin lucy trust" >> /data0/database/coordinator/gpseg-1/pg_hba.conf
    ```

    > **说明：**
    >
    > - `pg_hba.conf` 是 Apache Cloudberry 中用于控制访问权限的配置文件。
    > - `md5` 和 `trust` 是身份验证方法。`md5` 表示用户需要输入密码才能登录；`trust` 表示用户无需输入密码即可登录。

2. 使用 `gpstop` 使修改生效。

    ```shell
    [gpadmin@cdw ~]$ gpstop -u
    ```

    ```shell
    20230818:14:16:05:003653 gpstop:cdw:gpadmin-[INFO]:-Starting gpstop with args: -u
    20230818:14:16:05:003653 gpstop:cdw:gpadmin-[INFO]:-Gathering information and validating the environment...
    20230818:14:16:05:003653 gpstop:cdw:gpadmin-[INFO]:-Obtaining Cloudberry Coordinator catalog information
    20230818:14:16:05:003653 gpstop:cdw:gpadmin-[INFO]:-Obtaining Segment details from coordinator...
    20230818:14:16:05:003653 gpstop:cdw:gpadmin-[INFO]:-Cloudberry Version: 'postgres (Apache Cloudberry) 1.0.0 build dev'
    20230818:14:16:05:003653 gpstop:cdw:gpadmin-[INFO]:-Signalling all postmaster processes to reload
    ```

3. 验证两个用户可以登录数据库。

    ```shell
    [gpadmin@cdw ~]$ psql -U lily -d gpadmin
    Password for user lily:  # changeme

    psql (14.4, server 14.4)
    Type "help" for help.
    ```

    ```shell
    [gpadmin@cdw ~]$ psql -U lucy -d gpadmin

    psql (14.4, server 14.4)
    Type "help" for help.
    ```

    用户 `lily` 和用户 `lucy` 拥有不同的权限。用户 lily 登录时需要提供密码“changeme”。
