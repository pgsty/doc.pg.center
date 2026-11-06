---
title: "示例：在 PostgreSQL 中使用命名查询"
description: "将 PXF JDBC 与命名查询配合使用。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-jdbc/jdbc_pxf_named.md"
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

- 使用您在[示例：读写 PostgreSQL 数据库](/cloudberry/pxf/access-jdbc/jdbc_pxf_postgresql/)中创建的 PostgreSQL 数据库 `pgtestdb`、用户 `pxfuser1` 以及 PXF JDBC 连接器服务器配置 `pgsrvcfg`。
- 创建两个 PostgreSQL 表，并向表中插入数据。
- 授予 `pxfuser1` 对这两个表的所有权限。
- 定义一个对这两个 PostgreSQL 表执行复杂 SQL 语句的命名查询，并将该查询添加到 `pgsrvcfg` JDBC 服务器配置中。
- 创建与查询结果元组相匹配、并同时指定读分区选项的 PXF 可读外部表定义。
- 读取查询结果，并利用 PXF 的列投影和过滤条件下推。

## 创建 PostgreSQL 表并分配权限 {#create-the-postgresql-tables-and-assign-permissions}

执行以下步骤，在名为 `pgtestdb` 的数据库的 `public` 模式中创建名为 `customers` 和 `orders` 的 PostgreSQL 表，并授予名为 `pxfuser1` 的用户对这些表的所有权限：

1. 确定 PostgreSQL 服务器的主机名和端口。

2. 以 `postgres` 用户身份连接到 `pgtestdb` PostgreSQL 数据库。例如，如果您的 PostgreSQL 服务器在名为 `pserver` 的主机上以默认端口运行：

    ```shell
    $ psql -U postgres -h pserver -d pgtestdb
    ```

3. 创建名为 `customers` 的表，并向表中插入一些数据：

    ```sql
    CREATE TABLE customers(id int, name text, city text, state text);
    INSERT INTO customers VALUES (111, 'Bill', 'Helena', 'MT');
    INSERT INTO customers VALUES (222, 'Mary', 'Athens', 'OH');
    INSERT INTO customers VALUES (333, 'Tom', 'Denver', 'CO');
    INSERT INTO customers VALUES (444, 'Kate', 'Helena', 'MT');
    INSERT INTO customers VALUES (555, 'Harry', 'Columbus', 'OH');
    INSERT INTO customers VALUES (666, 'Kim', 'Denver', 'CO');
    INSERT INTO customers VALUES (777, 'Erik', 'Missoula', 'MT');
    INSERT INTO customers VALUES (888, 'Laura', 'Athens', 'OH');
    INSERT INTO customers VALUES (999, 'Matt', 'Aurora', 'CO');
    ```

4. 创建名为 `orders` 的表，并向表中插入一些数据：

    ```sql
    CREATE TABLE orders(customer_id int, amount int, month int, year int);
    INSERT INTO orders VALUES (111, 12, 12, 2018);
    INSERT INTO orders VALUES (222, 234, 11, 2018);
    INSERT INTO orders VALUES (333, 34, 7, 2018);
    INSERT INTO orders VALUES (444, 456, 111, 2018);
    INSERT INTO orders VALUES (555, 56, 11, 2018);
    INSERT INTO orders VALUES (666, 678, 12, 2018);
    INSERT INTO orders VALUES (777, 12, 9, 2018);
    INSERT INTO orders VALUES (888, 120, 10, 2018);
    INSERT INTO orders VALUES (999, 120, 11, 2018);
    ```

5. 授予用户 `pxfuser1` 对表 `customers` 和 `orders` 的所有权限，然后退出 `psql` 子系统：

    ```sql
    GRANT ALL ON customers TO pxfuser1;
    GRANT ALL ON orders TO pxfuser1;
    \q
    ```

## 配置命名查询 {#configure-the-named-query}

在此过程中，您将创建命名查询文本文件，将其添加到 `pgsrvcfg` JDBC 服务器配置中，并将 PXF 配置同步到 Apache Cloudberry 集群。

此过程通常由 Apache Cloudberry 管理员执行。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 进入 JDBC 服务器配置目录 `pgsrvcfg`。例如：

    ```shell
    gpadmin@coordinator$ cd $PXF_BASE/servers/pgsrvcfg
    ```

3. 在文本编辑器中打开名为 `pg_order_report.sql` 的查询文本文件，并将以下查询复制粘贴到该文件中：

    ```sql
    SELECT c.name, c.city, sum(o.amount) AS total, o.month
      FROM customers c JOIN orders o ON c.id = o.customer_id
      WHERE c.state = 'CO'
    GROUP BY c.name, c.city, o.month
    ```

4. 保存文件并退出编辑器。

5. 将对 PXF 配置所做的这些更改同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

## 读取查询结果 {#read-the-query-results}

在 Apache Cloudberry 集群上执行以下步骤，创建引用您在上一节中创建的查询文件的 PXF 外部表，然后读取查询结果数据：

1. 指定 `jdbc` Profile 创建 PXF 外部表。例如：

    ```sql
    CREATE EXTERNAL TABLE pxf_queryres_frompg(name text, city text, total int, month int)
      LOCATION ('pxf://query:pg_order_report?PROFILE=jdbc&SERVER=pgsrvcfg&PARTITION_BY=month:int&RANGE=1:13&INTERVAL=3')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

    或者创建外表
    ```sql
	CREATE SERVER "pgsrvcfg" FOREIGN DATA WRAPPER jdbc_pxf_fdw;
	CREATE USER MAPPING FOR CURRENT_USER SERVER "pgsrvcfg";
	CREATE FOREIGN TABLE pxf_queryres_frompg (name text, city text, total int, month int)
	  SERVER "pgsrvcfg"
	  OPTIONS (
		resource 'query:pg_order_report',
		PARTITION_BY 'month:int'
		RANGE '1:13'
		INTERVAL '3'
	);
    ```

    使用此分区方案时，PXF 会向远程 SQL 数据库发出 4 个查询，每个季度一个查询。每个查询会返回客户名称，以及他们在目标季度每个月份的订单总金额（按客户、按月聚合）。当您查询该外部表时，Apache Cloudberry 会将这些数据合并为单个结果集返回给您。

2. 显示查询结果的所有行：

    ```sql
    SELECT * FROM pxf_queryres_frompg ORDER BY city, total;

     name |  city  | total | month
    ------+--------+-------+-------
     Matt | Aurora |   120 |    11
     Tom  | Denver |    34 |     7
     Kim  | Denver |   678 |    12
    (3 rows)
    ```

3. 使用列投影显示每个城市的订单总额：

    ```sql
    SELECT city, sum(total) FROM pxf_queryres_frompg GROUP BY city;

      city  | sum
    --------+-----
     Aurora | 120
     Denver | 712
    (2 rows)
    ```

    运行此查询时，PXF 仅请求并检索 `city` 和 `total` 两列的查询结果，从而减少发回 Apache Cloudberry 的数据量。

4. 提供额外的过滤条件和聚合，在 PostgreSQL 中对 `total` 进行过滤：

    ```sql
    SELECT city, sum(total) FROM pxf_queryres_frompg
                WHERE total > 100
                GROUP BY city;

      city  | sum
    --------+-----
     Denver | 678
     Aurora | 120
    (2 rows)
    ```

    在此示例中，PXF 会将 `WHERE` 过滤条件添加到子查询中。该过滤条件被下推到远程数据库系统并在其上运行，从而减少 PXF 发回 Apache Cloudberry 的数据量。但是，`GROUP BY` 聚合不会下推到远程，而是由 Cloudberry 执行。
