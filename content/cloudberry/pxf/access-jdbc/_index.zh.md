---
title: "访问 SQL 数据库（JDBC）"
linkTitle: "使用 PXF 访问 SQL 数据库（JDBC）"
description: "使用 PXF JDBC 连接器访问 SQL 数据库。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-jdbc/jdbc_pxf.md"
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

您的部分数据可能已经存放在外部 SQL 数据库中。PXF 通过 PXF JDBC 连接器提供对这些数据的访问。JDBC 连接器是一个 JDBC 客户端，可以从 MySQL、ORACLE、Microsoft SQL Server、DB2、PostgreSQL、Hive 和 Apache Ignite 等 SQL 数据库读取数据，也可以向这些数据库写入数据。

本节介绍如何使用 PXF JDBC 连接器访问外部 SQL 数据库中的数据，包括如何创建引用外部数据库中某个表的 PXF 外部表，并对其进行查询或向其插入数据。

> <b>注意：</b>向外部 SQL 数据库写入数据时，JDBC 连接器不保证一致性。请注意，如果 `INSERT` 操作失败，部分数据可能已经写入外部数据库表。如果写入需要保证一致性，请考虑先写入外部数据库中的暂存表，待验证写入操作无误后，再加载到目标表。

## 前提条件 {#prerequisites}

在使用 PXF JDBC 连接器访问外部 SQL 数据库之前，请确保：

- 您能够确定 PXF 运行时配置目录（`$PXF_BASE`）。
- 您已经配置了 PXF，并且 PXF 正在每台 Apache Cloudberry 主机上运行。更多信息请参见[配置 PXF](/cloudberry/pxf/administering/configuring/)。
- 所有 Apache Cloudberry 主机与外部 SQL 数据库之间网络互通。
- 您已经将外部 SQL 数据库配置为允许来自所有 Apache Cloudberry 主机的用户访问。
- 您已经注册了所需的 JDBC 驱动程序 JAR 依赖。
- （推荐）您已经按照[配置 PXF JDBC 连接器](/cloudberry/pxf/administering/configuring/jdbc-connector/)中的说明，创建了一个或多个具名的 PXF JDBC 连接器服务器配置。

## 支持的数据类型 {#data-types-supported}

PXF JDBC 连接器支持以下数据类型：

- INTEGER、BIGINT、SMALLINT
- REAL、FLOAT8
- NUMERIC
- BOOLEAN
- VARCHAR、BPCHAR、TEXT
- DATE
- TIMESTAMP
- TIMESTAMPTZ
- BYTEA
- UUID

PXF JDBC 连接器不支持上面未列出的任何数据类型。

### 关于通过 JDBC 访问 Hive {#about-accessing-hive-via-jdbc}

PXF 内置 1.1.0 版本的 Hive JDBC 驱动程序。使用 PXF JDBC 连接器操作 Hive 表时，该版本**不**支持以下数据类型：

| 数据类型 | 修复该问题的 Hive JDBC 驱动程序版本 | 上游问题 | 不支持的操作 |
|-----------|---------------------------|----------------| ---------- |
| NUMERIC   | 2.3.0                     | [HIVE-13614](https://issues.apache.org/jira/browse/HIVE-13614) | 写 |
| TIMESTAMP | 2.0.0                     | [HIVE-11748](https://issues.apache.org/jira/browse/HIVE-11748) | 写 |
| DATE      | 1.3.0, 2.0.0              | [HIVE-11024](https://issues.apache.org/jira/browse/HIVE-11024) | 写 |
| TIMESTAMPTZ | N/A              | [HIVE-576](https://issues.apache.org/jira/browse/HIVE-576) | 读、写 |
| BYTEA     | N/A                       | N/A | 读、写 |

## 访问外部 SQL 数据库 {#accessing-an-external-sql-database}
PXF JDBC 连接器对外部表支持名为 `jdbc` 的单一 Profile，对 FDW 支持 `jdbc_pxf_fdw` 外部数据包装器。您可以使用该 Profile 读取外部 SQL 数据库表中的数据，也可以向其写入数据。您还可以使用该连接器在外部 SQL 数据库中运行静态的具名查询并读取其结果。

要访问远程 SQL 数据库中的数据，请创建引用远程数据库表的可读或可写 Apache Cloudberry 外部表。Apache Cloudberry 外部表与远程数据库表或查询结果元组必须具有相同的定义：列名和列类型必须一致。

使用以下语法创建引用远程 SQL 数据库表或远程数据库查询结果的 Apache Cloudberry 外表：

<pre>
CREATE SERVER "my_server" FOREIGN DATA WRAPPER jdbc_pxf_fdw;
CREATE USER MAPPING FOR CURRENT_USER SERVER "my_server";
CREATE FOREIGN TABLE &lt;table_name>
    ( &lt;column_name> &lt;data_type> [, ...] | LIKE &lt;other_table> )
    SERVER "my_server"
    OPTIONS (
     	resource '&lt;external-table-name>|query:&lt;query_name>'
     	[,&&lt;custom-option>=&lt;value>[...]]
	)
</pre>

或者创建 Apache Cloudberry 外部表：

<pre>
CREATE [READABLE | WRITABLE] EXTERNAL TABLE &lt;table_name>
    ( &lt;column_name> &lt;data_type> [, ...] | LIKE &lt;other_table> )
LOCATION ('pxf://&lt;external-table-name>|query:&lt;query_name>?<b>PROFILE=jdbc[&SERVER=&lt;server_name>]</b>[&&lt;custom-option>=&lt;value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export');
</pre>


下表说明 Apache Cloudberry [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) / [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的关键字和取值。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<external&#8209;table&#8209;name\>    | 外部表的完整名称。取决于外部 SQL 数据库，可以包含模式名和表名。 |
| query:\<query_name\>    | 要在远程 SQL 数据库中运行的查询的名称。 |
| PROFILE    | `PROFILE` 关键字的值必须指定为 `jdbc`。 |
| SERVER=\<server_name\>   | PXF 用于访问数据的具名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>=\<value\>  | \<custom-option\> 取决于具体 Profile。`jdbc` Profile 专用的选项在下一节中讨论。|
| FORMAT 'CUSTOM' | JDBC 的 `CUSTOM` `FORMAT` 在读操作中支持内置的 `'pxfwritable_import'` `FORMATTER` 函数，在写操作中支持内置的 `'pxfwritable_export'` 函数。 |

**注意**：创建 PXF 外部表时，不能在 `FORMAT` 规范中使用 `HEADER` 选项。

### JDBC 自定义选项 {#jdbc-custom-options}

您可以在 `OPTIONS` 或 `LOCATION` URI 中包含 JDBC 连接器的自定义选项（每个选项前加一个与号 `&`）。`jdbc` Profile 支持的 `CREATE FOREIGN TABLE` / `CREATE EXTERNAL TABLE` \<custom-option\> 包括：

| 选项名称   | 操作 | 说明
|---------------|------------|--------|
| BATCH_SIZE | 写 | 整数，指定向外部 SQL 数据库批量提交的 `INSERT` 操作数量。写批处理默认启用，默认值为 100。 |
| FETCH_SIZE | 读 | 整数，指定从外部 SQL 数据库读取时缓冲的行数。读行批处理默认启用。MySQL 的默认读取获取大小为 `-2147483648`（`Integer.MIN_VALUE`）。所有其他数据库的默认读取获取大小为 1000。 |
| QUERY_TIMEOUT | 读/写 | 整数，指定 JDBC 驱动程序等待语句运行的时间（单位为秒）。默认等待时间为无限。 |
| DATE_WIDE_RANGE | 读/写 | 布尔值，启用对指定 `BC` 或 `AD` 的 `date` 和 `timestamp` 数据类型的支持。将此值设置为 `true` 可确保纪元数据不丢失，并在年份超过 4 位数字的情况下提高性能。默认值为 `false`。 |
| POOL_SIZE | 写 | 在 `INSERT` 操作上启用线程池，并指定线程池中的线程数。线程池默认关闭。 |
| PARTITION_BY | 读 | 启用读分区。分区列的格式为 \<column-name\>:\<column-type\>。只能指定一个分区列。JDBC 连接器支持 `date`、`int` 和 `enum` 三种 \<column-type\> 取值，其中 `int` 代表任何 JDBC 整数类型。如果没有指定 `PARTITION_BY` 列，则由单个 PXF 实例处理读请求。 |
| RANGE | 读 | 指定 `PARTITION_BY` 时必需。查询范围，用作帮助创建分区的提示。`RANGE` 的格式取决于分区列的数据类型。当分区列为 `enum` 类型时，`RANGE` 必须指定值列表 \<value\>:\<value\>[:\<value\>[...]]，其中每个值各自构成一个分片。如果分区列为 `int` 或 `date` 类型，`RANGE` 必须指定 \<start-value\>:\<end-value\>，表示从 \<start-value\> 到 \<end-value\> 的区间（包含两端）。`int` 分区列的 `RANGE` 可以跨越任意 64 位有符号整数值。如果分区列为 `date` 类型，请使用 `yyyy-MM-dd` 日期格式。 |
| INTERVAL | 读 | 指定了 `PARTITION_BY` 且分区列为 `int`、`bigint` 或 `date` 类型时必需。单个分片的间隔，格式为 \<interval-value\>[:\<interval-unit\>]。与 `RANGE` 配合使用，作为帮助创建分区的提示。在 \<interval-value\> 中指定分片的大小。如果分区列为 `date` 类型，请使用 \<interval-unit\> 指定 `year`、`month` 或 `day`。当 `PARTITION_BY` 列为 `enum` 类型时，PXF 忽略 `INTERVAL`。 |
| QUOTE_COLUMNS | 读 | 控制 PXF 在构造发往外部数据库的 SQL 查询时是否对列名加引号。指定 `true` 会强制 PXF 对所有列名加引号；如果提供任何其他值，PXF 不会对列名加引号。如果未指定 `QUOTE_COLUMNS`（默认情况），则当*任一*列名出现以下情况时，PXF 会自动对查询中的*所有*列名加引号：<br/>- 包含特殊字符，或 <br/>- 为大小写混合，且外部数据库不支持不加引号的大小写混合标识符。 |

#### 批量插入操作（写）{#batching-insert-operations-write}

*当外部 SQL 数据库的 JDBC 驱动程序支持时*，对 `INSERT` 操作进行批处理可以显著提高性能。

写批处理默认启用，默认批大小为 100。要关闭批处理或修改默认批大小，请在创建 PXF 外部表时设置 `BATCH_SIZE`：

- `BATCH_SIZE=0` 或 `BATCH_SIZE=1` - 关闭批处理
- `BATCH_SIZE=(n>1)` - 将 `BATCH_SIZE` 设置为 `n`

当外部数据库的 JDBC 驱动程序不支持批处理时，PXF JDBC 连接器的行为取决于 `BATCH_SIZE` 设置，具体如下：

- 省略 `BATCH_SIZE` - JDBC 连接器不使用批处理进行插入。
- `BATCH_SIZE=(n>1)` - `INSERT` 操作失败，连接器返回错误。

#### 读操作的批处理 {#batching-on-read-operations}

默认情况下，PXF JDBC 连接器会自动对从外部数据库表获取的行进行批处理。默认的行获取大小为 1000。要修改默认获取大小，请在创建 PXF 外部表时指定 `FETCH_SIZE`。例如：

```text
FETCH_SIZE=5000
```

如果外部数据库的 JDBC 驱动程序不支持读批处理，则必须通过设置 `FETCH_SIZE=0` 显式关闭读行批处理。

#### 线程池（写）{#thread-pooling-write}

当外部 SQL 数据库的 JDBC 驱动程序支持多线程时，PXF JDBC 连接器可以通过在多个线程中处理 `INSERT` 操作进一步提高写性能。

可以考虑将批处理与线程池配合使用。二者同时使用时，每个线程接收并处理一个完整的数据批。如果使用线程池而不使用批处理，则池中每个线程恰好接收一个元组。

线程池中任何线程失败时，JDBC 连接器都会返回错误。请注意，如果 `INSERT` 操作失败，部分数据可能已经写入外部数据库表。

要关闭或启用线程池并设置线程池大小，请在创建 PXF 外部表时按如下方式设置 `POOL_SIZE`：

- `POOL_SIZE=(n<1)` - 线程池大小为系统中的 CPU 数量
- `POOL_SIZE=1` - 关闭线程池
- `POOL_SIZE=(n>1)`- 将 `POOL_SIZE` 设置为 `n`

#### 分区（读）{#partitioning-read}

PXF JDBC 连接器支持运行在多台 Apache Cloudberry 主机上的 PXF 实例同时读取外部 SQL 表。此功能称为分区。读分区默认不启用。要启用读分区，请在创建 PXF 外部表时设置 `PARTITION_BY`、`RANGE` 和 `INTERVAL` 自定义选项。

PXF 使用您指定的 `RANGE` 和 `INTERVAL` 值以及 `PARTITON_BY` 列，将外部表中的特定数据行分配给运行在 Apache Cloudberry Segment 主机上的 PXF 实例。该列的选择只用于 PXF 处理，与您可能为外部 SQL 数据库中的表指定的分区列没有任何关系。


标识分区参数的 JDBC \<custom-option\> 子串示例：

```text
&PARTITION_BY=id:int&RANGE=1:100&INTERVAL=5
&PARTITION_BY=year:int&RANGE=2011:2013&INTERVAL=1
&PARTITION_BY=createdate:date&RANGE=2013-01-01:2016-01-01&INTERVAL=1:month
&PARTITION_BY=color:enum&RANGE=red:yellow:blue
```

启用分区后，PXF JDBC 连接器会将 `SELECT` 查询拆分为多个子查询，每个子查询检索数据的一个子集，称为一个分片。JDBC 连接器会自动为每个分片添加额外的查询约束（`WHERE` 表达式），以保证每个数据元组都恰好从外部数据库检索一次。

例如，当用户查询的 PXF 外部表是用指定 `&PARTITION_BY=id:int&RANGE=1:5&INTERVAL=2` 的 `LOCATION` 子句创建时，PXF 会生成 5 个分片：两个由分区设置决定，另外最多三个为隐式生成。与各分片关联的约束如下：

- 分片 1：WHERE (id < 1) - 为 RANGE 起始边界之前的区间隐式生成的分片
- 分片 2：WHERE (id >= 1) AND (id < 3) - 由分区设置指定的分片
- 分片 3：WHERE (id >= 3) AND (id < 5) - 由分区设置指定的分片
- 分片 4：WHERE (id >= 5) - 为 RANGE 结束边界之后的区间隐式生成的分片
- 分片 5：WHERE (id IS NULL) - 隐式生成的分片

PXF 将分片分配给各个 Apache Cloudberry Segment。运行在 Segment 主机上的 PXF 实例会为该主机上处理分片的每个 Segment 派生一个线程。如果分片数量小于或等于 Segment 主机上配置的 Cloudberry Segment 数量，则单个 PXF 实例可以处理全部分片。每个 PXF 实例将其结果发送回 Apache Cloudberry，由 Apache Cloudberry 汇总后返回给用户。

指定 `PARTITION_BY` 选项时，请根据到目标数据库的最优 JDBC 连接数，以及外部数据在 Apache Cloudberry Segment 之间的最优分布，调整 `INTERVAL` 的值和单位。`INTERVAL` 的下界由 Apache Cloudberry Segment 的数量决定，上界则由目标数据库可接受的 JDBC 连接数决定。`INTERVAL` 设置会影响分片数量，理想情况下既不应设置得过大，也不应设置得过小。使用多个值进行测试有助于选出最优设置。

## 示例 {#examples}

有关如何使用 PXF 从特定 SQL 数据库读取数据和向其写入数据的示例，请参阅以下主题：

- [读写 PostgreSQL 表](/cloudberry/pxf/access-jdbc/jdbc_pxf_postgresql/)
- [读写 MySQL 表](/cloudberry/pxf/access-jdbc/jdbc_pxf_mysql/)
- [读写 Oracle 表](/cloudberry/pxf/access-jdbc/jdbc_pxf_oracle/)
- [读写 ClickHouse 表](/cloudberry/pxf/access-jdbc/jdbc_pxf_clickhouse/)
- [读写 Trino 表](/cloudberry/pxf/access-jdbc/jdbc_pxf_trino/)

## 关于使用具名查询 {#about-using-named-queries}

PXF JDBC 连接器允许您指定一个静态定义的查询，在远程 SQL 数据库上运行。在以下情况下，请考虑使用*具名查询*：

- 需要连接位于同一外部数据库中的多个表。
- 希望在更靠近数据源的位置执行复杂的聚合。
- 本来想使用 `VIEW`，但不允许在外部数据库中创建。
- 希望消耗外部系统的计算资源，以尽量减少对 Apache Cloudberry 资源的占用。
- 希望运行 HIVE 查询，并通过 YARN 控制资源使用。

Apache Cloudberry 管理员定义查询，并向您提供创建外部表时要使用的查询名称。在 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句中，您指定 `query:<query_name>` 而不是表名，以指示 PXF JDBC 连接器在远程 SQL 数据库中运行名为 `<query_name>` 的静态查询。

PXF 仅在可读外部表中支持具名查询。对于要运行的每个查询，您必须创建一个唯一的 Apache Cloudberry 可读外部表。

外部表列的名称和类型必须与查询结果返回的列的名称、类型和顺序完全匹配。如果查询返回的是聚合或其他函数的结果，请务必使用 `AS` 限定符指定具体的列名。

例如，假设您使用的 PostgreSQL 表具有以下定义：

```sql
CREATE TABLE customers(id int, name text, city text, state text);
CREATE TABLE orders(customer_id int, amount int, month int, year int);
```

以及管理员命名为 `order_rpt` 的如下 PostgreSQL 查询：

```sql
SELECT c.name, sum(o.amount) AS total, o.month
  FROM customers c JOIN orders o ON c.id = o.customer_id
  WHERE c.state = 'CO'
GROUP BY c.name, o.month
```

此查询返回类型为 `(name text, total int, month int)` 的元组。如果 `order_rpt` 查询是为名为 `pgserver` 的 PXF JDBC 服务器定义的，则可以按如下方式创建 Apache Cloudberry 外部表/外表来读取这些查询结果：

```sql
CREATE FOREIGN TABLE orderrpt_frompg(name text, total int, month int)
  SERVER pgserver
   OPTIONS ( resource 'query:order_rpt', PARTITION_BY 'month:int', RANGE '1:13', INTERVAL '3')
```
或者
```sql
CREATE EXTERNAL TABLE orderrpt_frompg(name text, total int, month int)
  LOCATION ('pxf://query:order_rpt?PROFILE=jdbc&SERVER=pgserver&PARTITION_BY=month:int&RANGE=1:13&INTERVAL=3')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

此命令引用了在 `pgserver` 服务器配置中定义的名为 `order_rpt` 的查询。它还指定了 JDBC 读分区选项，为 PXF 提供将查询结果数据拆分/分区到各服务器/Segment 所需的信息。

更详细的示例请参见[示例：在 PostgreSQL 中使用命名查询](/cloudberry/pxf/access-jdbc/jdbc_pxf_named/)。

PXF JDBC 连接器会自动对引用具名查询的外部表应用列投影和过滤条件下推。

## 使用 DDL 覆盖 JDBC 服务器配置 {#overriding-the-jdbc-server-configuration-with-ddl}

对于特定的外部数据库表，您可以在 `CREATE SERVER` 的 `OPTIONS` 部分或 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句中直接指定自定义选项，从而覆盖 JDBC 服务器配置中的某些属性：

| 自定义选项名称   | jdbc-site.xml 属性名称 |
|----------------------|-----------------------------|
| JDBC_DRIVER | jdbc.driver |
| DB_URL | jdbc.url |
| USER | jdbc.user |
| PASS | jdbc.password |
| BATCH_SIZE | jdbc.statement.batchSize |
| FETCH_SIZE | jdbc.statement.fetchSize |
| QUERY_TIMEOUT | jdbc.statement.queryTimeout |
| DATE_WIDE_RANGE | jdbc.date.wideRange |

对于外表：
```sql
CREATE SERVER "pgserver" FOREIGN DATA WRAPPER jdbc_pxf_fdw
	OPTIONS (
		jdbc_driver 'org.postgresql.Driver',
		db_url 'jdbc:postgresql://pgserverhost:5432/pgtestdb',
		user 'pxfuser1',
		pass 'changeme'
	);
CREATE USER MAPPING FOR CURRENT_USER SERVER "pgserver";
CREATE FOREIGN TABLE pxf_pgtbl(name varchar, age int)
  SERVER "pgserver"
  OPTIONS (resource 'public.forpxf_table1');
```

对于外部表：
```sql
CREATE EXTERNAL TABLE pxf_pgtbl(name text, orders int)
  LOCATION ('pxf://public.forpxf_table1?PROFILE=jdbc&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://pgserverhost:5432/pgtestdb&USER=pxfuser1&PASS=changeme')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
```
> <b>警告：</b>以这种方式提供的凭据会作为外部表定义的一部分而可见。请勿在生产环境中使用这种传递凭据的方式。

有关 PXF 为 Apache Cloudberry 用户获取配置属性设置时所遵循的优先级规则，详见[配置属性优先级](/cloudberry/pxf/administering/configuring/cfg_server/#about-configuration-property-precedence)。
