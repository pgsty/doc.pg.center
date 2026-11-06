---
title: "读取 Hive 表数据"
description: "使用 PXF 读取 Hive 表数据。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hive_pxf.md"
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

Apache Hive 是一种分布式数据仓库基础设施。Hive 便于管理支持多种数据格式的大型数据集，这些格式包括逗号分隔值（.csv）TextFile、RCFile、ORC 和 Parquet。 

PXF Hive 连接器读取存储在 Hive 表中的数据。本节介绍如何使用 PXF Hive 连接器。 

> <b>注意：</b>访问 Hive 3 时，PXF Hive 连接器仅支持使用下文所述的 `hive[:*]` Profile 访问 Hive 3 外部表。该连接器不支持使用 `hive[:*]` Profile 访问 Hive 3 托管表（CRUD 和仅插入型事务表，以及临时表）。请改用 <a href="/cloudberry/pxf/access-jdbc/">PXF JDBC Connector</a> 访问 Hive 3 托管表。

## 前提条件 {#prerequisites}

在使用 PXF 处理 Hive 表数据之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。

*如果您计划对 Hive 整数类型使用 PXF 过滤条件下推*，请确保配置参数 `hive.metastore.integral.jdo.pushdown` 存在，并且在 Hadoop 集群**和** `$PXF_BASE/servers/default/hive-site.xml` 的 `hive-site.xml` 文件中都设置为 `true`。更多信息请参见[关于更新 Hadoop 配置](/cloudberry/pxf/administering/configuring/hadoop-connectors/#about-updating-the-hadoop-configuration)。


## Hive 数据格式 {#hive-data-formats}

PXF Hive 连接器支持多种数据格式，并为访问这些格式定义了以下 Profile：

| 文件格式  | 描述 | Profile |
|-------|---------------------------|-------|
| TextFile | 平面文件，数据采用逗号、制表符或空格分隔值格式，或采用 JSON 表示法。 | hive, hive:text |
| SequenceFile | 由二进制键／值对组成的平面文件。 | hive |
| RCFile | 由二进制键／值对组成的记录列式数据；行压缩率高。 | hive, hive:rc |
| ORC | 优化行列式（Optimized Row Columnar）数据，包含 stripe、footer 和 postscript 部分；可减小数据大小。 | hive, hive:orc |
| Parquet | 压缩的列式数据表示。 | hive |
| Avro | 采用二进制数据格式的序列化系统。 | hive |

**注意**：`hive` Profile 支持所有文件存储格式。它会针对底层文件格式类型使用最优的 `hive[:*]` Profile。

## 数据类型映射 {#data-type-mapping}

PXF Hive 连接器支持基本数据类型和复杂数据类型。

### 基本数据类型 {#primitive-data-types}
要在 Apache Cloudberry 中表示 Hive 数据，请将使用基本数据类型的数据值映射到相同类型的 Apache Cloudberry 列。

下表概述了 Hive 基本类型的外部映射规则。

| Hive 数据类型  | Apache Cloudberry 数据类型 |
|-------|---------------------------|
| boolean    | bool |
| int   | int4 |
| smallint   | int2 |
| tinyint   | int2 |
| bigint   | int8 |
| float   | float4 |
| double   | float8 |
| string   | text |
| binary   | bytea |
| timestamp   | timestamp |


**注意**：当指定向量化查询执行（`VECTORIZE=true`）时，`hive:orc` Profile 不支持 timestamp 数据类型。

### 复杂数据类型 {#complex-data-types}

Hive 支持复杂数据类型，包括 array、struct、map 和 union。PXF 将这些复杂类型都映射为 `text`。您可以创建 Apache Cloudberry 函数或应用程序代码来提取这些复杂数据类型的子组件。

本主题后面提供了将复杂数据类型与 `hive` 和 `hive:orc` Profile 配合使用的示例。

**注意**：当指定向量化查询执行（`VECTORIZE=true`）时，`hive:orc` Profile 不支持复杂类型。

## 示例数据集 {#sample-data-set}

本主题中的示例基于同一个数据集进行操作。这个简单的数据集对零售销售业务建模，包含具有以下名称和数据类型的字段：

| 列名  | 数据类型 |
|-------|---------------------------|
| location | text |
| month | text |
| number\_of\_orders | integer |
| total\_sales | double |

准备使用示例数据集：

1. 首先，创建一个文本文件：

    ```
    $ vi /tmp/pxf_hive_datafile.txt
    ```

2. 将以下数据添加到 `pxf_hive_datafile.txt`；请注意，这里使用逗号（`,`）分隔四个字段值：

    ```
    Prague,Jan,101,4875.33
    Rome,Mar,87,1557.39
    Bangalore,May,317,8936.99
    Beijing,Jul,411,11600.67
    San Francisco,Sept,156,6846.34
    Paris,Nov,159,7134.56
    San Francisco,Jan,113,5397.89
    Prague,Dec,333,9894.77
    Bangalore,Jul,271,8320.55
    Beijing,Dec,100,4248.41
    ```

请记下 `pxf_hive_datafile.txt` 的路径；后面的练习中会用到它。


## Hive 命令行 {#hive-command-line}

Hive 命令行是一个类似于 `psql` 的子系统。启动 Hive 命令行的方法如下：

```shell
$ HADOOP_USER_NAME=hdfs hive
```

默认的 Hive 数据库名为 `default`。 

### 示例：创建 Hive 表 {#example-creating-a-hive-table}

创建一个 Hive 表来公开示例数据集。

1. 在 `default` 数据库中创建名为 `sales_info` 的 Hive 表：

    ```sql
    hive> CREATE TABLE sales_info (location string, month string,
            number_of_orders int, total_sales double)
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
            STORED AS textfile;
    ```

    请注意：

    - `STORED AS textfile` 子句指示 Hive 以 Textfile（默认）格式创建该表。Hive Textfile 格式支持逗号、制表符和空格分隔的值，以及以 JSON 表示法指定的数据。
    - `DELIMITED FIELDS TERMINATED BY` 子句标识数据记录（行）内的字段分隔符。`sales_info` 表的字段分隔符是逗号（`,`）。

2. 将 `pxf_hive_datafile.txt` 示例数据文件加载到您刚创建的 `sales_info` 表中：

    ```sql
    hive> LOAD DATA LOCAL INPATH '/tmp/pxf_hive_datafile.txt'
            INTO TABLE sales_info;
    ```
    
    在本节后面的示例中，您将通过 PXF 直接访问 `sales_info` Hive 表。您还将把 `sales_info` 的数据插入到其他 Hive 文件格式类型的表中，并同样使用 PXF 直接访问这些表。

3. 对 `sales_info` 执行查询，以验证数据是否已成功加载：

    ```sql
    hive> SELECT * FROM sales_info;
    ```

### 确定 Hive 表的 HDFS 位置 {#determining-the-hdfs-location-of-a-hive-table}

如果需要确定 Hive 托管表的 HDFS 文件位置，请使用其 HDFS 文件路径来引用它。可以使用 `DESCRIBE` 命令确定 Hive 表在 HDFS 中的位置。例如：

```sql
hive> DESCRIBE EXTENDED sales_info;
Detailed Table Information
...
location:hdfs://<namenode>:<port>/apps/hive/warehouse/sales_info
...
```


## 查询外部 Hive 数据 {#querying-external-hive-data}

您可以创建 Apache Cloudberry 外部表来访问 Hive 表数据。如前所述，PXF Hive 连接器定义了特定的 Profile 来支持不同的文件格式。这些 Profile 名为 `hive`、`hive:text`、`hive:rc` 和 `hive:orc`。 


`hive:text` 和 `hive:rc` Profile 分别针对文本格式和 RCFile 格式进行了专门优化。`hive:orc` Profile 针对 ORC 文件格式进行了优化。`hive` Profile 针对所有文件存储类型进行了优化；当底层 Hive 表由多个文件格式不同的分区组成时，可以使用 `hive` Profile。

使用 `hive`、`hive:rc` 或 `hive:orc` Profile 访问 Hive 表时，PXF 使用列投影来提高查询性能。

使用以下语法创建引用 Hive 表的 Apache Cloudberry 外部表：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<hive-db-name>.<hive-table-name>
    ?PROFILE=<profile_name>[&SERVER=<server_name>][&PPD=<boolean>][&VECTORIZE=<boolean>]')
FORMAT 'CUSTOM|TEXT' (FORMATTER='pxfwritable_import' | delimiter='<delim>')
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 调用中使用的 Hive 连接器专用关键字及取值说明如下。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<hive&#8209;db&#8209;name\>    | Hive 数据库的名称。如果省略，则默认为名为 `default` 的 Hive 数据库。 |
| \<hive&#8209;table&#8209;name\>    | Hive 表的名称。 |
| PROFILE=\<profile_name\>    | `<profile_name>` 必须指定为 `hive`、`hive:text`、`hive:rc` 或 `hive:orc` 之一。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| PPD=\<boolean\>    | 对此表上的所有查询启用或停用谓词下推；此选项仅适用于 `hive`、`hive:orc` 和 `hive:rc` Profile，并会覆盖 \<server_name\> 配置中的 `pxf.ppd.hive` 属性设置。 |
| VECTORIZE=\<boolean\>    | 当 `PROFILE=hive:orc` 时，此布尔值指定 PXF 访问底层 ORC 文件时是否使用向量化查询执行。默认值为 `false`，即不使用向量化查询执行。 |
| FORMAT（`hive` 和 `hive:orc` Profile）   | `FORMAT` 子句必须指定为 `'CUSTOM'`。`CUSTOM` 格式需要内置的 `pxfwritable_import` `formatter`。   |
| FORMAT（`hive:text` 和 `hive:rc` Profile） | `FORMAT` 子句必须指定为 `TEXT`。在 `delimiter='<delim>'` 格式化选项中指定单个 ASCII 字符的字段分隔符。 |

> <b>注意：</b>由于 Hive 表可以由一个或多个文件支撑，且每个文件可能具有独特的布局或模式，PXF 要求您在创建外部表时指定的列名与 Hive 表定义的列名一致。这样您就可以：<ul>
<li>创建列顺序与 Hive 表不同的 PXF 外部表。</li>
<li>创建只读取 Hive 表中部分列的 PXF 外部表。</li>
<li>读取支撑文件的列数各不相同的 Hive 表。</li></ul>


## 访问 TextFile 格式的 Hive 表 {#accessing-textfile-format-hive-tables}

您可以使用 `hive` 和 `hive:text` Profile 访问以 TextFile 格式存储的 Hive 表数据。

### 示例：使用 hive Profile {#example-using-the-hive-profile}

使用 `hive` Profile 创建可读的 Apache Cloudberry 外部表，该表引用您之前创建的 textfile 格式的 Hive 表 `sales_info`。

1. 创建外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE salesinfo_hiveprofile(location text, month text, number_of_orders int, total_sales float8)
                LOCATION ('pxf://default.sales_info?PROFILE=hive')
              FORMAT 'custom' (FORMATTER='pxfwritable_import');
    ```

2. 查询该表：

    ```sql
    postgres=# SELECT * FROM salesinfo_hiveprofile;
    ```

    ```shell
       location    | month | number_of_orders | total_sales
    ---------------+-------+------------------+-------------
     Prague        | Jan   |              101 |     4875.33
     Rome          | Mar   |               87 |     1557.39
     Bangalore     | May   |              317 |     8936.99
     ...
    ```

### 示例：使用 hive:text Profile {#example-using-the-hivetext-profile}

使用 PXF `hive:text` Profile，基于您之前创建的 textfile 格式的 Hive 表 `sales_info` 创建可读的 Apache Cloudberry 外部表。

1. 创建外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE salesinfo_hivetextprofile(location text, month text, number_of_orders int, total_sales float8)
                 LOCATION ('pxf://default.sales_info?PROFILE=hive:text')
               FORMAT 'TEXT' (delimiter=E',');
    ```

    请注意，`FORMAT` 子句的 `delimiter` 值被指定为单个 ASCII 逗号字符 `','`。`E` 用于转义该字符。

2. 查询外部表：

    ```sql
    postgres=# SELECT * FROM salesinfo_hivetextprofile WHERE location='Beijing';
    ```

    ```shell
     location | month | number_of_orders | total_sales
    ----------+-------+------------------+-------------
     Beijing  | Jul   |              411 |    11600.67
     Beijing  | Dec   |              100 |     4248.41
    (2 rows)
    ```


## 访问 RCFile 格式的 Hive 表 {#accessing-rcfile-format-hive-tables}

RCFile Hive 表格式用于行列式格式的数据。PXF `hive:rc` Profile 提供对 RCFile 数据的访问。


### 示例：使用 hive:rc Profile {#example-using-the-hiverc-profile}

使用 `hive:rc` Profile 查询 Hive 表中 RCFile 格式的数据。

1. 启动 `hive` 命令行并创建以 RCFile 格式存储的 Hive 表：

    ```shell
    $ HADOOP_USER_NAME=hdfs hive
    ```

    ```sql
    hive> CREATE TABLE sales_info_rcfile (location string, month string,
            number_of_orders int, total_sales double)
          ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
          STORED AS rcfile;
    ```

2. 将 `sales_info` 表中的数据插入 `sales_info_rcfile`：

    ```sql
    hive> INSERT INTO TABLE sales_info_rcfile SELECT * FROM sales_info;
    ```

    示例数据集的一份副本现在以 RCFile 格式存储在 Hive 的 `sales_info_rcfile` 表中。 
    
3. 查询 Hive 表 `sales_info_rcfile`，以验证数据是否已正确加载：

    ```sql
    hive> SELECT * FROM sales_info_rcfile;
    ```

4. 使用 PXF `hive:rc` Profile 创建可读的 Apache Cloudberry 外部表，该表引用您在前面步骤中创建的 Hive 表 `sales_info_rcfile`。例如：

    ```sql
    postgres=# CREATE EXTERNAL TABLE salesinfo_hivercprofile(location text, month text, number_of_orders int, total_sales float8)
                 LOCATION ('pxf://default.sales_info_rcfile?PROFILE=hive:rc')
               FORMAT 'TEXT' (delimiter=E',');
    ```

5. 查询外部表：

    ```sql
    postgres=# SELECT location, total_sales FROM salesinfo_hivercprofile;
    ```

    ```shell
       location    | total_sales
    ---------------+-------------
     Prague        |     4875.33
     Rome          |     1557.39
     Bangalore     |     8936.99
     Beijing       |    11600.67
     ...
    ```

## 访问 ORC 格式的 Hive 表 {#accessing-orc-format-hive-tables}

优化行列式（Optimized Row Columnar，ORC）文件格式是一种列式文件格式，为存储和访问 HDFS 数据提供了高效的方式。在压缩和性能两方面，ORC 格式都较文本格式和 RCFile 格式有所改进。

ORC 具有类型感知能力，专为 Hadoop 工作负载设计。ORC 文件同时存储文件中数据的类型和编码信息。在 ORC 格式文件中，同一组行数据（也称为 stripe）内的所有列在磁盘上存储在一起。ORC 格式类型的列式特性支持读投影，有助于避免在查询期间访问不必要的列。

ORC 还通过文件、stripe 和行级别的内置索引支持谓词下推，将过滤操作移至数据加载阶段。

有关 ORC 文件格式的详细信息，请参阅 [Apache orc](https://orc.apache.org/docs/) 和 Apache Hive [LanguageManual ORC](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+ORC) 网站。

### 支持 ORC 文件格式的 Profile {#profiles-supporting-the-orc-file-format}

选择支持 ORC 的 Profile 时，请考虑以下几点：

- `hive:orc` Profile：
    - 一次读取一行数据。
    - 支持列投影。 
    - 支持复杂类型。您可以访问由 array、map、struct 和 union 数据类型组成的 Hive 表。PXF 将这些复杂类型都序列化为 `text`。  

- 带 `VECTORIZE=true` 的 `hive:orc` Profile：
    - 一次最多读取 1024 行数据。
    - 支持列投影。 
    - 不支持复杂类型或 timestamp 数据类型。

### 示例：使用 hive:orc Profile {#example-using-the-hiveorc-profile}

在以下示例中，您将创建一个以 ORC 格式存储的 Hive 表，并使用 `hive:orc` Profile 查询该 Hive 表。

1. 创建 ORC 文件格式的 Hive 表：

    ```shell
    $ HADOOP_USER_NAME=hdfs hive
    ```

    ```sql
    hive> CREATE TABLE sales_info_ORC (location string, month string,
            number_of_orders int, total_sales double)
          STORED AS ORC;
    ```

2. 将 `sales_info` 表中的数据插入 `sales_info_ORC`：

    ```sql
    hive> INSERT INTO TABLE sales_info_ORC SELECT * FROM sales_info;
    ```

    示例数据集的一份副本现在以 ORC 格式存储在 `sales_info_ORC` 中。

3. 对 `sales_info_ORC` 执行 Hive 查询，以验证数据是否已成功加载：

    ```sql
    hive> SELECT * FROM sales_info_ORC;
    ```

4. 启动 `psql` 子系统并打开计时：

    ```shell
    $ psql -d postgres
    ```

    ```sql
    postgres=> \timing
    Timing is on.
    ```

4. 使用 PXF `hive:orc` Profile 创建 Apache Cloudberry 外部表，该表引用您在步骤 1 中创建的名为 `sales_info_ORC` 的 Hive 表。`FORMAT` 子句必须指定为 `'CUSTOM'`。`hive:orc` 的 `CUSTOM` 格式仅支持内置的 `'pxfwritable_import'` `formatter`。

    ```sql
    postgres=> CREATE EXTERNAL TABLE salesinfo_hiveORCprofile(location text, month text, number_of_orders int, total_sales float8)
                 LOCATION ('pxf://default.sales_info_ORC?PROFILE=hive:orc')
                 FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

5. 查询外部表：

    ```sql
    postgres=> SELECT * FROM salesinfo_hiveORCprofile;
    ```

    ```text
       location    | month | number_of_orders | total_sales 
    ---------------+-------+------------------+-------------
     Prague        | Jan   |              101 |     4875.33
     Rome          | Mar   |               87 |     1557.39
     Bangalore     | May   |              317 |     8936.99
     ...

    Time: 425.416 ms
    ```


### 示例：使用向量化 hive:orc Profile {#example-using-the-vectorized-hiveorc-profile}

在以下示例中，您将使用向量化 `hive:orc` Profile 查询在上一个示例中创建的 `sales_info_ORC` Hive 表。

1. 启动 `psql` 子系统：

    ```shell
    $ psql -d postgres
    ```

2. 使用 PXF `hive:orc` Profile 创建可读的 Apache Cloudberry 外部表，该表引用您在上一个示例的步骤 1 中创建的名为 `sales_info_ORC` 的 Hive 表。`FORMAT` 子句必须指定为 `'CUSTOM'`。`hive:orc` 的 `CUSTOM` 格式仅支持内置的 `'pxfwritable_import'` `formatter`。

    ```sql
    postgres=> CREATE EXTERNAL TABLE salesinfo_hiveVectORC(location text, month text, number_of_orders int, total_sales float8)
                 LOCATION ('pxf://default.sales_info_ORC?PROFILE=hive:orc&VECTORIZE=true')
                 FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

3. 查询外部表：

    ```sql
    postgres=> SELECT * FROM salesinfo_hiveVectORC;
    ```

    ```text
       location    | month | number_of_orders | total_sales 
    ---------------+-------+------------------+-------------
     Prague        | Jan   |              101 |     4875.33
     Rome          | Mar   |               87 |     1557.39
     Bangalore     | May   |              317 |     8936.99
     ...

    Time: 425.416 ms
    ```


## 访问 Parquet 格式的 Hive 表 {#accessing-parquet-format-hive-tables}

PXF `hive` Profile 支持使用 Parquet 存储格式的非分区和分区 Hive 表。请使用等价的 Apache Cloudberry 数据类型映射表的列。例如，如果在 `default` 模式中使用以下语句创建了 Hive 表：

```sql
hive> CREATE TABLE hive_parquet_table (location string, month string,
            number_of_orders int, total_sales double)
        STORED AS parquet;
```

定义 Apache Cloudberry 外部表：

```sql
postgres=# CREATE EXTERNAL TABLE pxf_parquet_table (location text, month text, number_of_orders int, total_sales double precision)
    LOCATION ('pxf://default.hive_parquet_table?profile=hive')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

然后查询该表：

```sql
postgres=# SELECT month, number_of_orders FROM pxf_parquet_table;
```
## 访问 Avro 格式的 Hive 表 {#accessing-avro-format-hive-tables}

PXF `hive` Profile 支持访问使用 Avro 存储格式的 Hive 表。请使用等价的 Apache Cloudberry 数据类型映射表的列。例如，如果在 `default` 模式中使用以下语句创建了 Hive 表：

```sql
hive> CREATE TABLE hive_avro_data_table (id int, name string, user_id string)
	ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
	STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
	OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat';
```

定义 Apache Cloudberry 外部表：

```sql
postgres=# CREATE EXTERNAL TABLE userinfo_hiveavro(id int, name text, user_id text)
	LOCATION ('pxf://default.hive_avro_data_table?profile=hive')
	FORMAT 'custom' (FORMATTER='pxfwritable_import');
```

然后查询该表：

```sql
postgres=# SELECT * FROM userinfo_hiveavro;
```

## 处理复杂数据类型 {#working-with-complex-data-types}

### 示例：将 hive Profile 与复杂数据类型配合使用 {#example-using-the-hive-profile-with-complex-data-types}

此示例使用 `hive` Profile 以及 array 和 map 复杂类型，具体为整数数组和字符串键／值对映射。

此示例的数据模式包含具有以下名称和数据类型的字段：

| 列名  | 数据类型 |
|-------|---------------------------|
| index | int |
| name | string
| intarray | 整数数组 |
| propmap | 字符串键值对映射 |

在 Hive 表中指定数组字段时，必须标识集合中每个元素的终止符。同样，还必须指定映射键的终止字符。

1. 创建用于加载数据集的文本文件：

    ```
    $ vi /tmp/pxf_hive_complex.txt
    ```

2. 将以下文本添加到 `pxf_hive_complex.txt`。这些数据使用逗号（`,`）分隔字段值，使用百分号 `%` 分隔集合元素，并使用 `:` 终止映射键值：

    ```
    3,Prague,1%2%3,zone:euro%status:up
    89,Rome,4%5%6,zone:euro
    400,Bangalore,7%8%9,zone:apac%status:pending
    183,Beijing,0%1%2,zone:apac
    94,Sacramento,3%4%5,zone:noam%status:down
    101,Paris,6%7%8,zone:euro%status:up
    56,Frankfurt,9%0%1,zone:euro
    202,Jakarta,2%3%4,zone:apac%status:up
    313,Sydney,5%6%7,zone:apac%status:pending
    76,Atlanta,8%9%0,zone:noam%status:down
    ```

3. 创建一个 Hive 表来表示这些数据：

    ```shell
    $ HADOOP_USER_NAME=hdfs hive
    ```

    ```sql
    hive> CREATE TABLE table_complextypes( index int, name string, intarray ARRAY<int>, propmap MAP<string, string>)
             ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
             COLLECTION ITEMS TERMINATED BY '%'
             MAP KEYS TERMINATED BY ':'
             STORED AS TEXTFILE;
    ```

    请注意：

    - `FIELDS TERMINATED BY` 将逗号标识为字段终止符。
    - `COLLECTION ITEMS TERMINATED BY` 子句将百分号指定为集合元素（数组元素、映射键／值对）的终止符。
    - `MAP KEYS TERMINATED BY` 将冒号标识为映射键的终止符。

4. 将 `pxf_hive_complex.txt` 示例数据文件加载到您刚创建的 `table_complextypes` 表中：

    ```sql
    hive> LOAD DATA LOCAL INPATH '/tmp/pxf_hive_complex.txt' INTO TABLE table_complextypes;
    ```

5. 对 Hive 表 `table_complextypes` 执行查询，以验证数据是否已成功加载：

    ```sql
    hive> SELECT * FROM table_complextypes;
    ```

    ```shell
    3	Prague	[1,2,3]	{"zone":"euro","status":"up"}
    89	Rome	[4,5,6]	{"zone":"euro"}
    400	Bangalore	[7,8,9]	{"zone":"apac","status":"pending"}
    ...
    ```

6. 使用 PXF `hive` Profile 创建可读的 Apache Cloudberry 外部表，该表引用名为 `table_complextypes` 的 Hive 表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE complextypes_hiveprofile(index int, name text, intarray text, propmap text)
                 LOCATION ('pxf://table_complextypes?PROFILE=hive')
               FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

    请注意，整数数组和 map 复杂类型被映射为 Apache Cloudberry 数据类型 text。

7. 查询外部表：

    ```sql
    postgres=# SELECT * FROM complextypes_hiveprofile;
    ```

    ```shell
     index |    name    | intarray |              propmap
    -------+------------+----------+------------------------------------
         3 | Prague     | [1,2,3]  | {"zone":"euro","status":"up"}
        89 | Rome       | [4,5,6]  | {"zone":"euro"}
       400 | Bangalore  | [7,8,9]  | {"zone":"apac","status":"pending"}
       183 | Beijing    | [0,1,2]  | {"zone":"apac"}
        94 | Sacramento | [3,4,5]  | {"zone":"noam","status":"down"}
       101 | Paris      | [6,7,8]  | {"zone":"euro","status":"up"}
        56 | Frankfurt  | [9,0,1]  | {"zone":"euro"}
       202 | Jakarta    | [2,3,4]  | {"zone":"apac","status":"up"}
       313 | Sydney     | [5,6,7]  | {"zone":"apac","status":"pending"}
        76 | Atlanta    | [8,9,0]  | {"zone":"noam","status":"down"}
    (10 rows)
    ```

    `intarray` 和 `propmap` 都被序列化为文本字符串。

### 示例：将 hive:orc Profile 与复杂数据类型配合使用 {#example-using-the-hiveorc-profile-with-complex-data-types}

在以下示例中，您将创建并填充一个以 ORC 格式存储的 Hive 表。您将使用 `hive:orc` Profile 查询此 Hive 表中的复杂类型。

1. 创建 ORC 存储格式的 Hive 表：

    ```shell
    $ HADOOP_USER_NAME=hdfs hive
    ```

    ```sql
    hive> CREATE TABLE table_complextypes_ORC( index int, name string, intarray ARRAY<int>, propmap MAP<string, string>)
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
            COLLECTION ITEMS TERMINATED BY '%'
            MAP KEYS TERMINATED BY ':'
          STORED AS ORC;
    ```

2. 将您在上一个示例中创建的 `table_complextypes` 表中的数据插入 `table_complextypes_ORC`：

    ```sql
    hive> INSERT INTO TABLE table_complextypes_ORC SELECT * FROM table_complextypes;
    ```

    示例数据集的一份副本现在以 ORC 格式存储在 `table_complextypes_ORC` 中。

3. 对 `table_complextypes_ORC` 执行 Hive 查询，以验证数据是否已成功加载：

    ```sql
    hive> SELECT * FROM table_complextypes_ORC;
    ```

    ```text
    OK
    3       Prague       [1,2,3]    {"zone":"euro","status":"up"}
    89      Rome         [4,5,6]    {"zone":"euro"}
    400     Bangalore    [7,8,9]    {"zone":"apac","status":"pending"}
    ...
    ```

4. 启动 `psql` 子系统：

    ```shell
    $ psql -d postgres
    ```

4. 使用 PXF `hive:orc` Profile，基于您在步骤 1 中创建的名为 `table_complextypes_ORC` 的 Hive 表创建可读的 Apache Cloudberry 外部表。`FORMAT` 子句必须指定为 `'CUSTOM'`。`hive:orc` 的 `CUSTOM` 格式仅支持内置的 `'pxfwritable_import'` `formatter`。

    ```sql
    postgres=> CREATE EXTERNAL TABLE complextypes_hiveorc(index int, name text, intarray text, propmap text)
               LOCATION ('pxf://default.table_complextypes_ORC?PROFILE=hive:orc')
                 FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

    请注意，整数数组和 map 复杂类型同样被映射为 Apache Cloudberry 数据类型 text。

5. 查询外部表：

    ```sql
    postgres=> SELECT * FROM complextypes_hiveorc;
    ```

    ```text
     index |    name    | intarray |              propmap               
    -------+------------+----------+------------------------------------
         3 | Prague     | [1,2,3]  | {"zone":"euro","status":"up"}
        89 | Rome       | [4,5,6]  | {"zone":"euro"}
       400 | Bangalore  | [7,8,9]  | {"zone":"apac","status":"pending"}
     ...

    ```

    `intarray` 和 `propmap` 同样被序列化为文本字符串。

## 分区裁剪 {#partition-pruning}

PXF Hive 连接器支持 Hive 分区裁剪和 Hive 分区目录结构。这使得可以对构成 Hive 表的选定 HDFS 文件进行分区排除。要使用分区过滤功能来减少网络流量和 I/O，请在 PXF 外部表上运行查询，并在 `WHERE` 子句中引用分区 Hive 表的特定分区列。

PXF Hive 连接器对 Hive 字符串类型和整数类型的分区过滤支持情况如下：

- 字符串类型支持关系运算符 `=`、`<`、`<=`、`>`、`>=` 和 `<>`。
- 整数类型支持关系运算符 `=` 和 `<>`（要对 Hive 整数类型使用分区过滤，必须按[前提条件](#prerequisites)中所述更新 Hive 配置）。
- 与上述关系运算符配合使用时，支持逻辑运算符 `AND` 和 `OR`。
- 不支持 `LIKE` 字符串运算符。

要利用 PXF 分区过滤下推，Hive 和 PXF 的分区字段名必须相同。否则，PXF 会忽略分区过滤，过滤将在 Apache Cloudberry 端执行，从而影响性能。

> <b>注意：</b>PXF Hive 连接器仅对分区列进行过滤，而不对其他表属性进行过滤。此外，仅对上面指明的数据类型和运算符支持过滤条件下推。

PXF 过滤条件下推默认启用。可按照[关于过滤条件下推](/cloudberry/pxf/intro/filter_push/)中的说明配置 PXF 过滤条件下推。


### 示例：使用 hive Profile 访问分区的同构数据 {#example-using-the-hive-profile-to-access-partitioned-homogenous-data}

在此示例中，您将使用 `hive` Profile 查询名为 `sales_part` 的 Hive 表，该表按 `delivery_state` 和 `delivery_city` 字段分区。然后，您将创建 Apache Cloudberry 外部表来查询 `sales_part`。该步骤包含说明过滤条件下推的具体示例。

1. 创建名为 `sales_part` 的 Hive 表，包含两个分区列 `delivery_state` 和 `delivery_city:`

    ```sql
    hive> CREATE TABLE sales_part (cname string, itype string, supplier_key int, price double)
            PARTITIONED BY (delivery_state string, delivery_city string)
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
    ```

2. 向该 Hive 表加载数据并添加一些分区：

    ```sql
    hive> INSERT INTO TABLE sales_part
            PARTITION(delivery_state = 'CALIFORNIA', delivery_city = 'Fresno')
            VALUES ('block', 'widget', 33, 15.17);
    hive> INSERT INTO TABLE sales_part
            PARTITION(delivery_state = 'CALIFORNIA', delivery_city = 'Sacramento')
            VALUES ('cube', 'widget', 11, 1.17);
    hive> INSERT INTO TABLE sales_part
            PARTITION(delivery_state = 'NEVADA', delivery_city = 'Reno')
            VALUES ('dowel', 'widget', 51, 31.82);
    hive> INSERT INTO TABLE sales_part
            PARTITION(delivery_state = 'NEVADA', delivery_city = 'Las Vegas')
            VALUES ('px49', 'pipe', 52, 99.82);
    ```

3. 查询 `sales_part` 表：

    ```sql
    hive> SELECT * FROM sales_part;
    ```

    对 Hive 分区表执行 `SELECT *` 语句时，分区字段显示在记录末尾。

3. 查看 `sales_part` 表的 Hive/HDFS 目录结构：

    ```shell
    $ sudo -u hdfs hdfs dfs -ls -R /apps/hive/warehouse/sales_part
    /apps/hive/warehouse/sales_part/delivery_state=CALIFORNIA/delivery_city=Fresno/
    /apps/hive/warehouse/sales_part/delivery_state=CALIFORNIA/delivery_city=Sacramento/
    /apps/hive/warehouse/sales_part/delivery_state=NEVADA/delivery_city=Reno/
    /apps/hive/warehouse/sales_part/delivery_state=NEVADA/delivery_city=Las Vegas/
    ```

4. 创建 PXF 外部表来读取分区的 `sales_part` Hive 表。为利用分区过滤下推，请在 `CREATE EXTERNAL TABLE` 属性列表末尾定义与 Hive 分区字段对应的字段。

    ```shell
    $ psql -d postgres
    ```

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_sales_part(
                 cname TEXT, itype TEXT,
                 supplier_key INTEGER, price DOUBLE PRECISION,
                 delivery_state TEXT, delivery_city TEXT)
               LOCATION ('pxf://sales_part?PROFILE=hive')
               FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

5. 查询该表：

    ```sql
    postgres=# SELECT * FROM pxf_sales_part;
    ```

6.  对 `pxf_sales_part` 执行另一个查询（无下推），返回 `delivery_city` 为 `Sacramento` 且 `cname` 为 `cube` 的记录：

    ```sql
    postgres=# SELECT * FROM pxf_sales_part WHERE delivery_city = 'Sacramento' AND cname = 'cube';
    ```

    该查询过滤 `delivery_city` 分区 `Sacramento`。对 `cname` 的过滤不会下推，因为它不是分区列。该过滤在 `Sacramento` 分区中的所有数据传输完毕后，在 Apache Cloudberry 端执行。

7. 查询（带下推）`delivery_state` 为 `CALIFORNIA` 的所有记录：

    ```sql
    postgres=# SET gp_external_enable_filter_pushdown=on;
    postgres=# SELECT * FROM pxf_sales_part WHERE delivery_state = 'CALIFORNIA';
    ```

    此查询读取 `CALIFORNIA` `delivery_state` 分区中的所有数据，而不考虑城市。


### 示例：使用 hive Profile 访问分区的异构数据 {#example-using-the-hive-profile-to-access-partitioned-heterogeneous-data}

您可以将 PXF `hive` Profile 用于任何 Hive 文件存储类型。使用 `hive` Profile，可以访问单个 Hive 表中格式各异的数据，其中各分区可能以不同的文件格式存储。

在此示例中，您将创建一个分区的 Hive 外部表。该表由与您在之前练习中创建的 `sales_info`（文本格式）和 `sales_info_rcfile`（RC 格式）Hive 表关联的 HDFS 数据文件组成。您将按年份对数据分区，把 `sales_info` 的数据分配给 2013 年，把 `sales_info_rcfile` 的数据分配给 2016 年。（暂时不必理会这两个表包含相同数据这一事实。）然后，您将使用 PXF `hive` Profile 查询这个分区的 Hive 外部表。

1. 创建名为 `hive_multiformpart` 的 Hive 外部表，按名为 `year` 的字符串字段分区：

    ```shell
    $ HADOOP_USER_NAME=hdfs hive
    ```

    ```sql
    hive> CREATE EXTERNAL TABLE hive_multiformpart( location string, month string, number_of_orders int, total_sales double)
            PARTITIONED BY( year string )
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
    ```

2. 描述 `sales_info` 和 `sales_info_rcfile` 表，记下每个表的 HDFS 文件 `location`：

    ```sql
    hive> DESCRIBE EXTENDED sales_info;
    hive> DESCRIBE EXTENDED sales_info_rcfile;
    ```
    
3. 在 `hive_multiformpart` 表中，为 `sales_info` 和 `sales_info_rcfile` 表各自关联的 HDFS 文件位置创建分区：

    ```sql
    hive> ALTER TABLE hive_multiformpart ADD PARTITION (year = '2013') LOCATION 'hdfs://namenode:8020/apps/hive/warehouse/sales_info';
    hive> ALTER TABLE hive_multiformpart ADD PARTITION (year = '2016') LOCATION 'hdfs://namenode:8020/apps/hive/warehouse/sales_info_rcfile';
    ```

4. 显式标识与 `sales_info_rcfile` 表关联的分区的文件格式：

    ```sql
    hive> ALTER TABLE hive_multiformpart PARTITION (year='2016') SET FILEFORMAT RCFILE;
    ```
    
    无需指定与 `sales_info` 表关联的分区的文件格式，因为 `TEXTFILE` 格式是默认格式。

5. 查询 `hive_multiformpart` 表：

    ```sql
    hive> SELECT * from hive_multiformpart;
    ...
    Bangalore	Jul	271	8320.55	2016
    Beijing	Dec	100	4248.41	2016
    Prague	Jan	101	4875.33	2013
    Rome	Mar	87	1557.39	2013
    ...
    hive> SELECT * from hive_multiformpart WHERE year='2013';
    hive> SELECT * from hive_multiformpart WHERE year='2016';
    ```

6. 显示为 `hive_multiformpart` 表定义的分区并退出 `hive`：

    ```sql
    hive> SHOW PARTITIONS hive_multiformpart;
    year=2013
    year=2016
    hive> quit;
    ```

7. 启动 `psql` 子系统：

    ```shell
    $ psql -d postgres
    ```

8. 使用 PXF `hive` Profile 创建可读的 Apache Cloudberry 外部表，该表引用您在前面步骤中创建的 Hive 外部表 `hive_multiformpart`：

    ```sql
    postgres=# CREATE EXTERNAL TABLE pxf_multiformpart(location text, month text, number_of_orders int, total_sales float8, year text)
                 LOCATION ('pxf://default.hive_multiformpart?PROFILE=hive')
               FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

9. 查询 PXF 外部表：

    ```sql
    postgres=# SELECT * FROM pxf_multiformpart;
    ```

    ```shell
       location    | month | number_of_orders | total_sales | year 
    ---------------+-------+------------------+-------------+--------
     ....
     Prague        | Dec   |              333 |     9894.77 | 2013
     Bangalore     | Jul   |              271 |     8320.55 | 2013
     Beijing       | Dec   |              100 |     4248.41 | 2013
     Prague        | Jan   |              101 |     4875.33 | 2016
     Rome          | Mar   |               87 |     1557.39 | 2016
     Bangalore     | May   |              317 |     8936.99 | 2016
     ....
    ```

10. 执行第二个查询，计算 2013 年的订单总数：

    ```sql
    postgres=# SELECT sum(number_of_orders) FROM pxf_multiformpart WHERE month='Dec' AND year='2013';
     sum 
    -----
     433
    ```

## 将 PXF 与 Hive 默认分区配合使用 {#using-pxf-with-hive-default-partitions}

本主题介绍当 Hive 表使用默认分区时，Hive 查询与 PXF 查询在结果上的差异。在 Hive 中启用动态分区时，分区表可能会将数据存储在默认分区中。当分区列的值与该列定义的类型不匹配时（例如，对任何分区列使用了 NULL 值），Hive 会创建默认分区。在 Hive 中，任何对分区列包含过滤条件的查询都会*排除*存储在该表默认分区中的任何数据。

与 Hive 类似，PXF 将表的分区列表示为追加到表末尾的列。但是，PXF 会将默认分区中的任何列值转换为 NULL 值。这意味着，对分区列包含 `IS NULL` 过滤条件的 Apache Cloudberry 查询，其返回结果可能与相同的 Hive 查询不同。

考虑使用如下语句创建的 Hive 分区表：

```sql
hive> CREATE TABLE sales (order_id bigint, order_amount float) PARTITIONED BY (xdate date);
```

该表加载了包含以下数据的五行：

```text
1.0    1900-01-01
2.2    1994-04-14
3.3    2011-03-31
4.5    NULL
5.0    2013-12-06
```

插入第 4 行会创建一个 Hive 默认分区，因为分区列 `xdate` 包含空值。

在 Hive 中，任何对分区列进行过滤的查询都会忽略默认分区中的数据。例如，以下查询不返回任何行：

```sql
hive> SELECT * FROM sales WHERE xdate IS null;
```

但是，如果将此 Hive 表映射到 Apache Cloudberry 中的 PXF 外部表，则所有默认分区值都会被转换为实际的 NULL 值。在 Apache Cloudberry 中，对该 PXF 外部表运行相同的查询会返回第 4 行作为结果，因为过滤条件匹配该 NULL 值。

对 Hive 分区表运行 `IS NULL` 查询时，请牢记这一行为。
