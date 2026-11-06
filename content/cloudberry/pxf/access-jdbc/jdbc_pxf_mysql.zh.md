---
title: "示例：读写 MySQL 表"
description: "在 MySQL 中使用 PXF JDBC。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-jdbc/jdbc_pxf_mysql.md"
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

- 创建 MySQL 数据库和表，并向表中插入数据
- 创建 MySQL 用户，并授予该用户对该表的所有权限
- 配置 PXF JDBC 连接器以访问 MySQL 数据库
- 创建引用该 MySQL 表的 PXF 可读外部表
- 使用 PXF 读取 MySQL 表中的数据
- 创建引用该 MySQL 表的 PXF 可写外部表
- 使用 PXF 向 MySQL 表写入数据
- 再次读取 MySQL 表中的数据

## 创建 MySQL 表 {#create-a-mysql-table}

执行以下步骤，在名为 `mysqltestdb` 的数据库中创建名为 `names` 的 MySQL 表，并授予名为 `mysql-user` 的用户对该表的所有权限：

1. 确定 MySQL 服务器的主机名和端口。

2. 以 `root` 用户身份连接到默认的 MySQL 数据库：

    ```shell
    $ mysql -u root -p
    ```

3. 创建名为 `mysqltestdb` 的 MySQL 数据库并连接到该数据库：

    ```sql
    > CREATE DATABASE mysqltestdb;
    > USE mysqltestdb;
    ```

4. 创建名为 `names` 的表，并向表中插入一些数据：

    ```sql
    > CREATE TABLE names (id int, name varchar(64), last varchar(64));
    > INSERT INTO names values (1, 'John', 'Smith'), (2, 'Mary', 'Blake');
    ```

5. 创建名为 `mysql-user` 的 MySQL 用户，并为其设置密码 `my-secret-pw`：

    ```sql
    > CREATE USER 'mysql-user' IDENTIFIED BY 'my-secret-pw';
    ```

6. 授予用户 `mysql-user` 对表 `names` 的所有权限，然后退出 `mysql` 子系统：

    ```sql
    > GRANT ALL PRIVILEGES ON mysqltestdb.names TO 'mysql-user';
    > exit
    ```

    拥有这些权限后，`mysql-user` 可以读取和写入 `names` 表。

## 配置 MySQL 连接器 {#configure-the-mysql-connector}

您必须为 MySQL 创建 JDBC 服务器配置，将 MySQL 驱动程序 JAR 文件下载到您的系统，将该 JAR 文件复制到 PXF 用户配置目录，同步 PXF 配置，然后重启 PXF。

此过程通常由 Apache Cloudberry 管理员执行。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```
1. 下载 MySQL JDBC 驱动程序，并将其放置在 `$PXF_BASE/lib` 下。如果您[迁移了 $PXF_BASE](/cloudberry/pxf/administering/configuring/about_pxf_dir/#relocating-pxf_base)，请确保使用更新后的位置。您可以从自己偏好的下载位置获取 MySQL JDBC 驱动程序。下面的示例从 Maven Central 下载驱动程序，并将其放置在 `$PXF_BASE/lib` 下：

    1. 如果您没有迁移 `$PXF_BASE`，请在 Cloudberry Coordinator 上运行以下命令：

        ```shell
        gpadmin@coordinator$ cd /usr/local/cloudberry-pxf-<version>/lib
        gpadmin@coordinator$ wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.26/mysql-connector-java-8.0.26.jar
        ```

    2. 如果您迁移了 `$PXF_BASE`，请在 Cloudberry Coordinator 上运行以下命令：

        ```shell
        gpadmin@coordinator$ cd $PXF_BASE/lib
        gpadmin@coordinator$ wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.26/mysql-connector-java-8.0.26.jar
        ```

1. 同步 PXF 配置，然后重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    gpadmin@coordinator$ pxf cluster restart
    ```

2. 按照[示例配置过程](/cloudberry/pxf/administering/configuring/jdbc-connector/#example-configuration-procedure)中的说明为 MySQL 创建 JDBC 服务器配置，并将服务器目录命名为 `mysql`。`jdbc-site.xml` 文件的内容应与下面类似（请将 `mysqlserverhost` 替换为您的 MySQL 主机系统）：

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <property>
            <name>jdbc.driver</name>
            <value>com.mysql.jdbc.Driver</value>
            <description>Class name of the JDBC driver</description>
        </property>
        <property>
            <name>jdbc.url</name>
            <value>jdbc:mysql://mysqlserverhost:3306/mysqltestdb</value>
            <description>The URL that the JDBC driver can use to connect to the database</description>
        </property>
        <property>
            <name>jdbc.user</name>
            <value>mysql-user</value>
            <description>User name for connecting to the database</description>
        </property>
        <property>
            <name>jdbc.password</name>
            <value>my-secret-pw</value>
            <description>Password for connecting to the database</description>
        </property>
    </configuration> 
    ```

3. 将 PXF 服务器配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

## 读取 MySQL 表 {#read-from-the-mysql-table}

执行以下步骤，创建引用您在上一节中创建的 `names` MySQL 表的 PXF 外部表，并读取该表中的数据：

1. 指定 `jdbc` Profile 创建 PXF 外部表。例如：

    ```sql
    gpadmin=# CREATE EXTERNAL TABLE names_in_mysql (id int, name text, last text)
              LOCATION('pxf://names?PROFILE=jdbc&SERVER=mysql')
              FORMAT 'CUSTOM' (formatter='pxfwritable_import');
    ```

	或者创建外表
	```sql
	gpadmin=# CREATE SERVER "mysql" FOREIGN DATA WRAPPER jdbc_pxf_fdw;
	gpadmin=# CREATE USER MAPPING FOR CURRENT_USER SERVER "mysql";
    gpadmin=# CREATE FOREIGN TABLE names_in_mysql (id int, name text, last text)
                SERVER "mysql"
                OPTIONS ( resource 'names' );
	```

2. 显示 `names_in_mysql` 表的所有行：

    ```sql
    gpadmin=# SELECT * FROM names_in_mysql;
     id |   name    |   last  
    ----+-----------+----------
      1 |   John    |   Smith
      2 |   Mary    |   Blake
    (2 rows)   
    ```

## 写入 MySQL 表 {#write-to-the-mysql-table}

执行以下步骤，向 `names` MySQL 表中插入一些数据，然后从该表读取。您必须为写操作创建新的外部表。

1. 指定 `jdbc` Profile 创建 PXF 可写外部表。例如：

    ```sql
    gpadmin=# CREATE WRITABLE EXTERNAL TABLE names_in_mysql_w (id int, name text, last text)
              LOCATION('pxf://names?PROFILE=jdbc&SERVER=mysql')
              FORMAT 'CUSTOM' (formatter='pxfwritable_export');
    ```
    或者复用前面步骤中创建的外表

4. 向 `names_in_mysql_w` 表中插入一些数据。例如：

    ```sql
    =# INSERT INTO names_in_mysql_w VALUES (3, 'Muhammad', 'Ali');
    ```

5. 使用您在上一节中创建的 `names_in_mysql` 可读外部表，查看 `names` MySQL 表中的新数据：

    ```sql
    gpadmin=#  SELECT * FROM names_in_mysql;
     id |   name     |   last  
    ----+------------+--------
      1 |   John     |   Smith
      2 |   Mary     |   Blake
      3 |   Muhammad |   Ali
    (3 rows)
  
