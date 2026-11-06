---
title: "第 2 课：创建和准备数据库"
description: "创建一个新的 Apache Cloudberry 数据库。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/quick-trial-lessons/create-and-prepare-database.md"
---

在 Apache Cloudberry 中创建新数据库时，可以在 `psql` 客户端中使用 `CREATE DATABASE` SQL 命令，也可以使用 `createdb` 工具。`createdb` 工具是 `CREATE DATABASE` 命令的封装。

## 快速开始操作 {#quick-start-operations}

下面的操作将引导你使用 `createdb` 工具创建新数据库、创建模式并设置模式搜索路径。你还将学习如何创建用户并向用户授予权限。

继续操作前，请确保已经完成上一教程 `Lesson 1: Create Users and Roles`。你将以在上一教程中设置好密码的用户 `lily` 连接 tutorial 数据库。

### 创建数据库 {#create-database}

1. 在 Docker 中登录 Apache Cloudberry。创建 `tutorial` 数据库前，请确保该数据库不存在。

    ```shell
    [gpadmin@cdw ~]$ dropdb tutorial
    ```

    输出：

    ```shell
    dropdb: error: database removal failed: ERROR:  database "tutorial" does not exist
    ```

2. 使用 `createdb` 工具创建 `tutorial` 数据库。

    ```shell
    [gpadmin@cdw ~]$ createdb tutorial
    ```

    ```shell
    [gpadmin@cdw ~]$ psql -l  # Verifies that this database has been created.
                                    List of databases
       Name    |  Owner  | Encoding |   Collate   |    Ctype    |  Access privileges
    -----------+---------+----------+-------------+-------------+---------------------
     gpadmin   | gpadmin | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
     postgres  | gpadmin | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
     template0 | gpadmin | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/gpadmin         +
               |         |          |             |             | gpadmin=CTc/gpadmin
     template1 | gpadmin | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/gpadmin         +
               |         |          |             |             | gpadmin=CTc/gpadmin
     tutorial  | gpadmin | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
    (5 rows)
    ```

    > **说明：**
    >
    > 除非指定其他数据库，否则新创建的数据库是 `template1` 数据库的副本。

3. 向 `/data0/database/coordinator/gpseg-1/pg_hba.conf` 追加 `local tutorial lily md5`，在 `pg_hba.conf` 配置文件中创建条目。

    ```shell
    [gpadmin@cdw ~]$ echo "local tutorial lily md5" >> /data0/database/coordinator/gpseg-1/pg_hba.conf
    ```

    > **说明：**
    >
    > - `pg_hba.conf` 是 Apache Cloudberry 中用于控制客户端访问的配置文件。
    > - `md5` 是身份验证方法，表示用户需要输入密码才能登录。

4. 重新加载配置文件，使修改生效。

    ```shell
    [gpadmin@cdw ~]$ gpstop -u
    ```

    ```shell
    20230818:14:18:45:003733 gpstop:cdw:gpadmin-[INFO]:-Starting gpstop with args: -u
    20230818:14:18:45:003733 gpstop:cdw:gpadmin-[INFO]:-Gathering information and validating the environment...
    20230818:14:18:45:003733 gpstop:cdw:gpadmin-[INFO]:-Obtaining Cloudberry Coordinator catalog information
    20230818:14:18:45:003733 gpstop:cdw:gpadmin-[INFO]:-Obtaining Segment details from coordinator...
    20230818:14:18:45:003733 gpstop:cdw:gpadmin-[INFO]:-Cloudberry Version: 'postgres (Apache Cloudberry) 1.0.0 build dev'
    20230818:14:18:45:003733 gpstop:cdw:gpadmin-[INFO]:-Signalling all postmaster processes to reload
    ```

5. 以用户 `lily` 连接 `tutorial` 数据库。需要输入在[上一教程](/cloudberry/tutorials/quick-trial-lessons/create-users-and-roles/#create-a-user-using-the-create-user-command)中设置的密码。

    ```shell
    [gpadmin@cdw ~]$ psql -U lily tutorial

    Password for user lily:  # changeme
    psql (14.4, server 14.4)
    Type "help" for help.
    ```

    ```sql
    tutorial=> \q    -- Exits the database.
    ```

### 向用户授予数据库权限 {#grant-database-privileges-to-users}

为了让数据库用户正常完成工作，需要向他们授予所需的最低权限。例如，用户可能需要表上的 `SELECT` 权限来查看数据，也可能需要 `UPDATE`、`INSERT` 或 `DELETE` 权限来修改数据。

下面的操作将为数据库用户 `lily` 授予在 `tutorial` 数据库中创建和操作对象所需的权限。

1. 以 `gpadmin` 用户连接 `tutorial` 数据库。

    ```shell
    [gpadmin@cdw ~]$ psql -U gpadmin tutorial
    ```

    输出：

    ```shell
    psql (14.4, server 14.4)
    Type "help" for help.
    ```

2. 向 `lily` 授予 `tutorial` 数据库的所有权限。

    ```sql
    tutorial=# GRANT ALL PRIVILEGES ON DATABASE tutorial TO lily;
    ```

    输出：

    ```sql
    GRANT
    ```

    ```sql
    tutorial=# \q    -- Exits the database.
    ```

### 创建模式并设置搜索路径 {#create-schema-and-set-search-path}

本节将引导你创建 `faa` 模式，并设置搜索路径，使 `faa` 成为默认模式。

> **说明：**
>
> 数据库模式是数据库对象集合的命名容器，其中可以包含表、数据类型和函数。一个数据库可以包含多个模式。模式中的对象通过在对象名前加上模式名并以句点分隔来引用。例如，`employee schema` 中的 `person` 表写作 `employee.person`。
>
> 模式为其中包含的对象提供命名空间。如果数据库用于多个应用，且每个应用都有自己的模式，那么每个模式都可以使用相同的表名。例如，`employee.person` 与 `customer.person` 是不同的表，只要使用相应的模式名，就可以在同一个查询中访问这两个表。
>
> 数据库包含一个模式搜索路径，其中列出一组模式名。搜索路径中的第一个模式也是未指定模式时创建新对象的模式。默认搜索路径为 user,public，因此默认情况下，你创建的每个对象都属于与登录名关联的模式。

1. 以用户 `lily` 连接 `tutorial` 数据库。

    ```shell
    [gpadmin@cdw ~]$ psql -U lily tutorial
    ```

    ```shell
    Password for user lily:  # changeme

    psql (14.4, server 14.4)
    Type "help" for help.
    ```

2. 创建 `faa` 模式。

    ```sql
    tutorial=> DROP SCHEMA IF EXISTS faa CASCADE;
    tutorial=> CREATE SCHEMA faa;
    ```

3. 将搜索路径设置为 `faa`、`public`、`pg_catalog` 和 `gp_toolkit` 模式。

    ```sql
    tutorial=> SET SEARCH_PATH TO faa, public, pg_catalog, gp_toolkit;
    ```

    输出：

    ```sql
    SET
    ```

4. 验证搜索路径设置正确。

    ```sql
    tutorial=> SHOW search_path;
    ```

    输出：

    ```sql
    search_path
    -------------------------------------
    faa, public, pg_catalog, gp_toolkit
    (1 row)
    ```

5. 将搜索路径与用户角色 `lily` 关联。

    上一步设置的搜索路径不会持久保存。每次连接数据库时都需要重新设置。可以使用 `ALTER ROLE` 命令为用户角色关联搜索路径，这样每次使用该角色连接数据库时，搜索路径都会恢复。

    ```sql
    tutorial=> ALTER ROLE lily SET search_path TO faa, public, pg_catalog, gp_toolkit;
    ```

    输出：

    ```sql
    ALTER ROLE
    ```
