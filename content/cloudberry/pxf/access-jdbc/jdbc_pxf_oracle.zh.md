---
title: "示例：读写 Oracle 表"
description: "在 Oracle 中使用 PXF JDBC。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-jdbc/jdbc_pxf_oracle.md"
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

- 创建 Oracle 用户，并授予该用户对该表的所有权限
- 创建 Oracle 表，并向表中插入数据
- 配置 PXF JDBC 连接器以访问 Oracle 数据库
- 创建引用该 Oracle 表的 PXF 可读外部表
- 使用 PXF 读取 Oracle 表中的数据
- 创建引用该 Oracle 表的 PXF 可写外部表
- 使用 PXF 向 Oracle 表写入数据
- 再次读取 Oracle 表中的数据

有关在 Oracle 中控制并行执行的信息，请参阅本主题末尾的[关于设置 Oracle 并行查询会话参数](#about-setting-oracle-parallel-query-session-parameters)。

## 创建 Oracle 表 {#create-an-oracle-table}

执行以下步骤，在模式 `oracleuser` 中创建名为 `countries` 的 Oracle 表，并授予名为 `oracleuser` 的用户所有必要的权限：

1. 确定 Oracle 服务器的主机名和端口。

2. 以 `system` 用户身份连接到 Oracle 数据库：

    ```shell
    $ sqlplus system
    ```

3. 创建名为 `oracleuser` 的用户，并为其设置密码 `mypassword`：

    ```sql
    > CREATE USER oracleuser IDENTIFIED BY mypassword;
    ```

4. 授予用户 `oracleuser` 足够的权限，使其能够登录、创建和修改表：

    ```sql
    > GRANT CREATE SESSION TO oracleuser; 
    > GRANT CREATE TABLE TO oracleuser;
    > GRANT UNLIMITED TABLESPACE TO oracleuser;
    > exit
    ```

4. 以用户 `oracleuser` 身份登录：

    ```shell
    $ sqlplus oracleuser
    ```

4. 创建名为 `countries` 的表，向表中插入一些数据，然后提交事务：

    ```sql
    > CREATE TABLE countries (country_id int, country_name varchar(40), population float);
    > INSERT INTO countries (country_id, country_name, population) values (3, 'Portugal', 10.28);
    > INSERT INTO countries (country_id, country_name, population) values (24, 'Zambia', 17.86);
    > COMMIT;
    ```

## 配置 Oracle 连接器 {#configure-the-oracle-connector}

您必须为 Oracle 创建 JDBC 服务器配置，将 Oracle 驱动程序 JAR 文件下载到您的系统，将该 JAR 文件复制到 PXF 用户配置目录，同步 PXF 配置，然后重启 PXF。

此过程通常由 Apache Cloudberry 管理员执行。

1. 下载 Oracle JDBC 驱动程序，并将其放置在 Apache Cloudberry Coordinator 主机的 `$PXF_BASE/lib` 下。如果您[迁移了 $PXF_BASE](/cloudberry/pxf/administering/configuring/about_pxf_dir/#relocating-pxf_base)，请确保使用更新后的位置。您可以从自己偏好的下载位置获取 Oracle JDBC 驱动程序。下面的示例将从 Oracle 网站下载的驱动程序放置在 Apache Cloudberry Coordinator 的 `$PXF_BASE/lib` 下：

    1. 如果您没有迁移 `$PXF_BASE`，请在 Cloudberry Coordinator 上运行以下命令：

        ```shell
        gpadmin@coordinator$ scp ojdbc11.jar gpadmin@coordinator:/usr/local/cloudberry-pxf-<version>/lib/
        ```

    2. 如果您迁移了 `$PXF_BASE`，请在 Cloudberry Coordinator 上运行以下命令：

        ```shell
        gpadmin@coordinator$ scp ojdbc11.jar gpadmin@coordinator:$PXF_BASE/lib/
        ```

1. 同步 PXF 配置，然后重启 PXF： 

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    gpadmin@coordinator$ pxf cluster restart
    ```

2. 按照[示例配置过程](/cloudberry/pxf/administering/configuring/jdbc-connector/#example-configuration-procedure)中的说明为 Oracle 创建 JDBC 服务器配置，并将服务器目录命名为 `oracle`。`jdbc-site.xml` 文件的内容应与下面类似（请将 `oracleserverhost` 替换为您的 Oracle 主机系统，并将 `orcl` 替换为您的 Oracle 服务名称）：

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <property>
            <name>jdbc.driver</name>
            <value>oracle.jdbc.driver.OracleDriver</value>
            <description>Class name of the JDBC driver</description>
        </property>
        <property>
            <name>jdbc.url</name>
            <value>jdbc:oracle:thin:@oracleserverhost:1521/orcl</value>
            <description>The URL that the JDBC driver can use to connect to the database</description>
        </property>
        <property>
            <name>jdbc.user</name>
            <value>oracleuser</value>
            <description>User name for connecting to the database</description>
        </property>
        <property>
            <name>jdbc.password</name>
            <value>mypassword</value>
            <description>Password for connecting to the database</description>
        </property>
    </configuration>  
    ```

3. 将 PXF 服务器配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

## 读取 Oracle 表 {#read-from-the-oracle-table}

执行以下步骤，创建引用您在上一节中创建的 `countries` Oracle 表的 PXF 外部表，并读取该表中的数据：

1. 指定 `jdbc` Profile 创建 PXF 外部表。例如：

    ```sql
    gpadmin=# CREATE EXTERNAL TABLE oracle_countries (country_id int, country_name varchar, population float)
              LOCATION('pxf://oracleuser.countries?PROFILE=jdbc&SERVER=oracle')
              FORMAT 'CUSTOM' (formatter='pxfwritable_import');
    ```

	或者指定 `jdbc_pxf_fdw` 外部数据包装器创建 PXF 外表。例如：

	```sql
	gpadmin=# CREATE SERVER "oracle" FOREIGN DATA WRAPPER jdbc_pxf_fdw;
	gpadmin=# CREATE USER MAPPING FOR CURRENT_USER SERVER "oracle";
	gpadmin=# CREATE FOREIGN TABLE oracle_countries (country_id int, country_name varchar, population float)
				  SERVER "oracle"
				  OPTIONS (
					resource 'oracleuser.countries'
				  );
	```

2. 显示 `oracle_countries` 表的所有行：

    ```sql
    gpadmin=# SELECT * FROM oracle_countries ;
    country_id | country_name | population 
    -----------+--------------+------------
             3 | Portugal     |      10.28
            24 | Zambia       |      17.86
    (2 rows)
    ```

## 写入 Oracle 表 {#write-to-the-oracle-table}

执行以下步骤，向 `countries` Oracle 表中插入一些数据，然后从该表读取。您必须为写操作创建新的外部表。

1. 指定 `jdbc` Profile 创建 PXF 可写外部表。例如：

    ```sql
    gpadmin=# CREATE WRITABLE EXTERNAL TABLE oracle_countries_write (country_id int, country_name varchar, population float)
              LOCATION('pxf://oracleuser.countries?PROFILE=jdbc&SERVER=oracle')
              FORMAT 'CUSTOM' (formatter='pxfwritable_export');
    ```

	或者复用在[读取 Oracle 表](#read-from-the-oracle-table)中创建的 PXF 外表 `oracle_countries`。

4. 向 `oracle_countries_write` 表中插入一些数据。例如：

    ```sql
    gpadmin=# INSERT INTO oracle_countries_write VALUES (66, 'Colombia', 50.34);
    ```

5. 使用您在上一节中创建的 `oracle_countries` 可读外部表，查看 `countries` Oracle 表中的新数据：

    ```sql
    gpadmin=#  SELECT * FROM oracle_countries;
    country_id | country_name | population
    ------------+--------------+------------
             3 | Portugal     |      10.28
            24 | Zambia       |      17.86
            66 | Colombia     |      50.34
    (3 rows)
    ```


## 关于设置 Oracle 并行查询会话参数 {#about-setting-oracle-parallel-query-session-parameters}

PXF 能够识别某些控制并行查询执行的 Oracle 会话参数，并在运行查询之前设置这些参数。您可以通过在 Oracle PXF 服务器的 `jdbc-site.xml` 配置文件中设置属性来指定这些会话参数。

有关 Oracle 数据库中并行查询执行的更多信息，请参阅 [Oracle 文档](https://docs.oracle.com/database/121/VLDBG/GUID-3E2AE088-2505-465E-A8B2-AC38813EA355.htm#VLDBG010)。

PXF 按如下方式命名 Oracle 并行查询会话属性：

```
jdbc.session.property.alter_session_parallel.<n>
```

`<n>` 是标识某个会话参数设置的序号；例如 `jdbc.session.property.alter_session_parallel.1`。您可以指定多个属性设置，其中每个设置的 `<n>` 必须唯一。

您为 Oracle 并行查询执行属性指定的值必须符合以下格式：

```
<action>.<statement_type>[.<degree_of_parallelism>]
```

其中：

| 关键字 | 取值/说明 |
|--------------|-----------------|
| `<action>`  | `enable`<br/>`disable`<br/>`force` |
| `<statement_type>`  | `query`<br/>`ddl`<br/>`dml`<br/> |
| `<degree_of_parallelism>`  | 当 `<action>` 指定为 `force` 时，可以强制的并行会话数量（整数）。对于其他 `<action>` 设置，PXF 会忽略此值。 |

下面是 Oracle PXF 服务器的 `jdbc-site.xml` 配置文件中并行查询执行属性的设置示例：

```xml
<property>
    <name>jdbc.session.property.alter_session_parallel.1</name>
    <value>force.query.4</value>
</property>
<property>
    <name>jdbc.session.property.alter_session_parallel.2</name>
    <value>disable.ddl</value>
</property>
<property>
    <name>jdbc.session.property.alter_session_parallel.3</name>
    <value>enable.dml</value>
</property>
```

使用此配置时，PXF 在向 Oracle 数据库提交查询之前会运行以下命令：

```sql
ALTER SESSION FORCE PARALLEL QUERY PARALLEL 4;
ALTER SESSION DISABLE PARALLEL DDL;
ALTER SESSION ENABLE PARALLEL DML;
```
