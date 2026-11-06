---
title: "示例：读写 PostgreSQL 表"
description: "在 PostgreSQL 中使用 PXF JDBC。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-jdbc/jdbc_pxf_postgresql.md"
---

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

在本示例中，您将：

- 创建 PostgreSQL 数据库和表，并向表中插入数据
- 创建 PostgreSQL 用户，并授予该用户对该表的所有权限
- 配置 PXF JDBC 连接器以访问 PostgreSQL 数据库
- 创建引用该 PostgreSQL 表的 PXF 可读外部表
- 使用 PXF 读取 PostgreSQL 表中的数据
- 创建引用该 PostgreSQL 表的 PXF 可写外部表
- 使用 PXF 向 PostgreSQL 表写入数据
- 再次读取 PostgreSQL 表中的数据

## 创建 PostgreSQL 表 {#create-a-postgresql-table}

执行以下步骤，在名为 `pgtestdb` 的数据库的 `public` 模式中创建名为 `forpxf_table1` 的 PostgreSQL 表，并授予名为 `pxfuser1` 的用户对该表的所有权限：

1. 确定 PostgreSQL 服务器的主机名和端口。

2. 以 `postgres` 用户身份连接到默认的 PostgreSQL 数据库。例如，如果您的 PostgreSQL 服务器在名为 `pserver` 的主机上以默认端口运行：

    ```shell
    $ psql -U postgres -h pserver
    ```

3. 创建名为 `pgtestdb` 的 PostgreSQL 数据库并连接到该数据库：

    ```sql
    =# CREATE DATABASE pgtestdb;
    =# \connect pgtestdb;
    ```

4. 创建名为 `forpxf_table1` 的表，并向表中插入一些数据：

    ```sql
    =# CREATE TABLE forpxf_table1(id int);
    =# INSERT INTO forpxf_table1 VALUES (1);
    =# INSERT INTO forpxf_table1 VALUES (2);
    =# INSERT INTO forpxf_table1 VALUES (3);
    ```

5. 创建名为 `pxfuser1` 的 PostgreSQL 用户：

    ```sql
    =# CREATE USER pxfuser1 WITH PASSWORD 'changeme';
    ```

6. 授予用户 `pxfuser1` 对表 `forpxf_table1` 的所有权限，然后退出 `psql` 子系统：

    ```sql
    =# GRANT ALL ON forpxf_table1 TO pxfuser1;
    =# \q
    ```

    拥有这些权限后，`pxfuser1` 可以读取和写入 `forpxf_table1` 表。

7. 更新 PostgreSQL 配置，允许用户 `pxfuser1` 从每台 Apache Cloudberry 主机访问 `pgtestdb`。此配置取决于您的 PostgreSQL 环境。您需要更新 `/var/lib/pgsql/pg_hba.conf` 文件，然后重启 PostgreSQL 服务器。


## 配置 JDBC 连接器 {#configure-the-jdbc-connector}

您必须为 PostgreSQL 创建 JDBC 服务器配置并同步 PXF 配置。PostgreSQL JAR 文件已随 PXF 一并打包，因此无需手动下载。

此过程通常由 Apache Cloudberry 管理员执行。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 按照[示例配置过程](/cloudberry/pxf/administering/configuring/jdbc-connector/#example-configuration-procedure)中的说明为 PostgreSQL 创建 JDBC 服务器配置，并将服务器目录命名为 `pgsrvcfg`。`jdbc-site.xml` 文件的内容应与下面类似（请将 `pgserverhost` 替换为您的 PostgreSQL 主机系统）：

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <property>
            <name>jdbc.driver</name>
            <value>org.postgresql.Driver</value>
        </property>
        <property>
            <name>jdbc.url</name>
            <value>jdbc:postgresql://pgserverhost:5432/pgtestdb</value>
        </property>
        <property>
            <name>jdbc.user</name>
            <value>pxfuser1</value>
        </property>
        <property>
            <name>jdbc.password</name>
            <value>changeme</value>
        </property>
    </configuration>
    ```

3. 将 PXF 服务器配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

## 读取 PostgreSQL 表 {#read-from-the-postgresql-table}

执行以下步骤，创建引用您在上一节中创建的 `forpxf_table1` PostgreSQL 表的 PXF 外部表，并读取该表中的数据：

1. 指定 `jdbc` Profile 创建 PXF 外部表。例如：

    ```sql
    gpadmin=# CREATE EXTERNAL TABLE pxf_tblfrompg(id int)
                LOCATION ('pxf://public.forpxf_table1?PROFILE=jdbc&SERVER=pgsrvcfg')
                FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

    或者创建外表
    ```sql
    gpadmin=# CREATE SERVER "pgsrvcfg" FOREIGN DATA WRAPPER jdbc_pxf_fdw;
    gpadmin=# CREATE USER MAPPING FOR CURRENT_USER SERVER "pgsrvcfg";
    gpadmin=# CREATE FOREIGN TABLE pxf_tblfrompg (name text, city text, total int, month int)
    	  SERVER "pgsrvcfg"
    	  OPTIONS ( resource 'public.forpxf_table1' );
    ```

2. 显示 `pxf_tblfrompg` 表的所有行：

    ```sql
    gpadmin=# SELECT * FROM pxf_tblfrompg;
     id
    ----
      1
      2
      3
    (3 rows)
    ```

## 写入 PostgreSQL 表 {#write-to-the-postgresql-table}

执行以下步骤，向 `forpxf_table1` Postgres 表中插入一些数据，然后从该表读取。您必须为写操作创建新的外部表。

1. 指定 `jdbc` Profile 创建 PXF 可写外部表。例如：

    ```sql
    gpadmin=# CREATE WRITABLE EXTERNAL TABLE pxf_writeto_postgres(id int)
                LOCATION ('pxf://public.forpxf_table1?PROFILE=jdbc&SERVER=pgsrvcfg')
              FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
    ```
    或者复用前面步骤中创建的外表

4. 向 `pxf_writeto_postgres` 表中插入一些数据。例如：

    ```sql
    =# INSERT INTO pxf_writeto_postgres VALUES (111);
    =# INSERT INTO pxf_writeto_postgres VALUES (222);
    =# INSERT INTO pxf_writeto_postgres VALUES (333);
    ```

5. 使用您在上一节中创建的 `pxf_tblfrompg` 可读外部表，查看 `forpxf_table1` PostgreSQL 表中的新数据：

    ```sql
    gpadmin=# SELECT * FROM pxf_tblfrompg ORDER BY id DESC;
     id
    -----
     333
     222
     111
       3
       2
       1
    (6 rows)
    ```
