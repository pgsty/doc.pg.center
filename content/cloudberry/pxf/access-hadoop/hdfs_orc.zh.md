---
title: "读写 HDFS ORC 数据"
description: "通过 PXF 读写 HDFS 中的 ORC 数据。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_orc.md"
---

使用 PXF HDFS 连接器的 `hdfs:orc` Profile 读写 ORC 格式的数据。本节介绍如何读写以 ORC 格式存储的 HDFS 文件，包括如何创建引用 HDFS 数据存储中文件的外部表，以及如何查询这些外部表并向其中插入数据。

使用 `hdfs:orc` Profile 读取 ORC 格式的数据时，连接器：

- 每次读取 1024 行数据。
- 支持列投影。
- 支持基于文件级、条带（stripe）级和行级 ORC 统计信息的过滤条件下推。
- 对 ORC 标量类型的一个子集，支持复合类型 list。
- 不支持 map、union 或 struct 复合类型。

使用 `hdfs:orc` Profile 写入 ORC 格式的数据时，连接器：

- 支持写入与读取 ORC 格式数据时相同的基本类型子集。
- 仅支持为一维数组写入复合 list 类型。不支持用户提供的模式。
- 不支持 map、union 或 struct 复合类型。

`hdfs:orc` Profile 目前支持从 ORC 文件中读写标量数据类型以及部分标量类型的 list。如果数据位于 Hive 表中，并且您要读取复杂类型，或者该 Hive 表是分区表，请使用 [`hive:orc`](/cloudberry/pxf/access-hadoop/hive_pxf/#accessing-orc-format-hive-tables) Profile。


## 前提条件 {#prerequisites}

在尝试从 HDFS 读取数据或向 HDFS 写入数据之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。


## 关于 ORC 数据格式 {#about-the-orc-data-format}

优化行列式（Optimized Row Columnar，ORC）文件格式是一种列式文件格式，为存储和访问 HDFS 数据提供了一种高效的方式。与文本格式和 RCFile 格式相比，ORC 格式在压缩和性能两方面都有改进。PXF 支持 ORC 文件版本 v0 和 v1。

ORC 具有类型感知能力，并专为 Hadoop 工作负载设计。ORC 文件同时存储文件中数据的类型信息和编码信息。在 ORC 格式文件中，同一组行数据（也称为条带，stripe）内的所有列在磁盘上存储在一起。ORC 格式的列式特性支持读取投影，有助于避免在查询期间访问不必要的列。

ORC 还支持谓词下推，其内置的文件级、条带级和行级索引将过滤操作移到数据加载阶段。

有关 ORC 文件格式的详细信息，请参阅 [Apache ORC](https://orc.apache.org/docs/) 文档。


## 数据类型映射 {#data-type-mapping}

要在 Apache Cloudberry 中读写 ORC 基本数据类型，请将 ORC 数据值映射到类型相同的 Apache Cloudberry 列。

### 读取映射 {#read-mapping}

要在 Apache Cloudberry 中读取 ORC 标量数据类型，请将 ORC 数据值映射到类型相同的 Apache Cloudberry 列。

PXF 读取 ORC 数据时使用以下数据类型映射：

| ORC 物理类型 | ORC 逻辑类型 | PXF/Apache Cloudberry 数据类型 |
|-------------------|---------------|--------------------------|
| binary | decimal | Numeric |
| binary | timestamp | Timestamp |
| byte[] | string | Text |
| byte[] | char | Bpchar |
| byte[] | varchar | Varchar |
| byte[] | binary | Bytea |
| Double | float | Real |
| Double | double | Float8 |
| Integer | boolean (1 bit) | Boolean |
| Integer | tinyint (8 bit) | Smallint |
| Integer | smallint (16 bit) | Smallint |
| Integer | int (32 bit) | Integer |
| Integer | bigint (64 bit) | Bigint |
| Integer | date | Date |

PXF 仅支持 ORC 复合类型中的 list，并且仅支持部分 ORC 标量类型。支持的映射如下：

| ORC 复合类型 | PXF/Apache Cloudberry 数据类型 |
|-------------------|-------------------------|
| array\&lt;string&gt; | Text[] |
| array\&lt;char&gt; | Bpchar[] |
| array\&lt;varchar&gt; | Varchar[] |
| array\&lt;binary&gt; | Bytea[] |
| array\&lt;float&gt; | Real[] |
| array\&lt;double&gt; | Float8[] |
| array\&lt;boolean&gt; | Boolean[] |
| array\&lt;tinyint&gt; | Smallint[] |
| array\&lt;smallint&gt; | Smallint[] |
| array\&lt;int&gt; | Integer[] |
| array\&lt;bigint&gt; | Bigint[] |

### 写入映射 {#write-mapping}

PXF 写入 ORC 数据时使用以下数据类型映射：

| PXF/Apache Cloudberry 数据类型 | ORC 逻辑类型 | ORC 物理类型 |
|-------------------------|------------------|-------------------|
| Numeric | decimal | binary |
| Timestamp | timestamp | binary |
| Timestamp with Timezone | timestamp with local time zone | timestamp |
| Text | string | byte[] |
| Bpchar | char | byte[] |
| Varchar | varchar | byte[] |
| Bytea | binary | byte[] |
| Real | float | Double |
| Float8 | double | Double |
| Boolean | boolean (1 bit) | Integer |
| Smallint | tinyint (8 bit) | Integer |
| Smallint | smallint (16 bit) | Integer |
| Integer | int (32 bit) | Integer |
| Bigint | bigint (64 bit) | Integer |
| Date | date | Integer |
| UUID | string | byte[] |

PXF 支持为一维数组写入 ORC 复合类型 list，适用于上述所有 ORC 基本类型。支持的映射如下：

| ORC 复合类型 | PXF/Apache Cloudberry 数据类型 |
|-------------------|-------------------------|
| array\&lt;decimal&gt; | Numeric[] |
| array\&lt;timestamp&gt; | Timestamp[] |
| array\&lt;string&gt; | Text[] |
| array\&lt;char&gt; | Bpchar[] |
| array\&lt;varchar&gt; | Varchar[] |
| array\&lt;binary&gt; | Bytea[] |
| array\&lt;float&gt; | Real[] |
| array\&lt;double&gt; | Float8[] |
| array\&lt;boolean&gt; | Boolean[] |
| array\&lt;tinyint&gt; | Smallint[] |
| array\&lt;smallint&gt; | Smallint[] |
| array\&lt;int&gt; | Integer[] |
| array\&lt;bigint&gt; | Bigint[] |
| array\&lt;date&gt; | Date[] |

## 创建外部表 {#creating-the-external-table}

PXF HDFS 连接器的 `hdfs:orc` Profile 支持读写 ORC 格式的 HDFS 文件。向可写外部表插入记录时，您插入的数据块会写入所指定目录中的文件，每个 Segment 写入一个文件。

使用以下语法创建引用 HDFS 文件或目录的 Apache Cloudberry 外部表：

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-file>
    ?PROFILE=hdfs:orc[&SERVER=<server_name>][&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export')
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的关键字和取值说明如下。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中文件或目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hdfs:orc`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom-option\>    | \<custom-option\> 的说明见下文。 |
| FORMAT 'CUSTOM' | 将 `FORMAT 'CUSTOM'` 与 `(FORMATTER='pxfwritable_export')`（写入）或 `(FORMATTER='pxfwritable_import')`（读取）配合使用。   |
| DISTRIBUTED BY | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间额外的数据移动。  |

## 创建外表 {#creating-the-foreign-table}

PXF HDFS 的 `hdfs_pxf_fdw` 外部数据包装器支持读写 ORC 格式的 HDFS 文件。向外表插入记录时，您插入的数据块会写入 `resource` 子句所指定目录中的文件，每个 Segment 写入一个文件。

使用以下语法创建引用 HDFS 文件或目录的 Apache Cloudberry 外表：

```sql
CREATE SERVER <foreign_server> FOREIGN DATA WRAPPER hdfs_pxf_fdw;
CREATE USER MAPPING FOR <user_name> SERVER <foreign_server>;

CREATE FOREIGN TABLE [ IF NOT EXISTS ] <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
  SERVER <foreign_server>
  OPTIONS ( resource '<path-to-file>', format 'orc' [, <custom-option> '<value>'[...]]);
```

Apache Cloudberry [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) 命令中使用的关键字和取值说明如下。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<foreign_server\>    | PXF 用于访问数据的命名服务器配置。您可以在 `CREATE SERVER` 语句中覆盖凭据，方法见[为外表覆盖 S3 服务器配置](/cloudberry/pxf/access-objectstores/access_s3/#overriding-the-s3-server-configuration-for-foreign-tables) |
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中文件或目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| format    | 文件格式；对于 ORC 格式的数据，请指定 `'orc'`。 |
| \<custom-option\>    | \<custom-option\> 的说明见下文。 |

### 自定义选项 {#custom-options}

PXF `hdfs:orc` Profile 支持以下*读取*选项。您在 `LOCATION` 子句中指定该选项：

| 读取选项  | 取值说明 |
|-------|-------------------------------------|
| IGNORE_MISSING_PATH | 布尔值，指定当 \<path-to-hdfs-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。当取值为 `true` 时，PXF 忽略路径缺失错误并返回空分片。 |
| MAP_BY_POSITION | 布尔值，设置为 `true` 时，指定 PXF 按位置将 ORC 列映射到 Apache Cloudberry 列。默认值为 `false`，此时 PXF 按名称将 ORC 列映射到 Apache Cloudberry 列。 |

PXF `hdfs:orc` Profile 支持一个与压缩相关的写入选项；您在 `CREATE WRITABLE EXTERNAL TABLE` 的 `LOCATION` 子句中指定该选项：

| 写入选项  | 取值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。写入 ORC 数据时支持的压缩编解码器包括：`lz4`、`lzo`、`zstd`、`snappy`、`zlib` 和 `none`。如果未指定此选项，PXF 使用 `zlib` 压缩数据。 |

## 关于写入 ORC 数据 {#about-writing-orc-data}

向可写外部表插入记录时，您插入的数据块会写入 `LOCATION` 或 `resource` 子句所指定目录中的一个或多个文件。

插入 ORC 数据记录时，`pxf-site.xml` 文件中的 `pxf.orc.write.timezone.utc` 属性决定 PXF 如何将时间戳值写入外部数据存储。默认情况下，PXF 使用 UTC 时区写入时间戳类型。如果需要 PXF 使用 PXF JVM 的本地时区写入时间戳类型，请为该服务器将 `pxf.orc.write.timezone.utc` 属性设置为 `false`，并同步 PXF 配置。

## 示例：读取 HDFS 上的 ORC 文件 {#example-reading-an-orc-file-on-hdfs}

本示例使用一个模拟零售销售业务的简单数据集。数据包含以下名称和类型的字段：

| 列名  | 数据类型 |
|--------------|---------------|
| location | text |
| month | text |
| num\_orders | integer |
| total\_sales | numeric(10,2) |
| items\_sold | text[] |

在本示例中，您将：

- 创建 JSON 格式的示例数据集，使用 `orc-tools` JAR 实用工具将该 JSON 文件转换为 ORC 格式的文件，然后将该 ORC 文件复制到 HDFS。
- 创建引用该 ORC 文件并指定 `hdfs:orc` Profile 的 Apache Cloudberry 可读外部表。
- 查询该外部表。

要运行本示例，您必须同时拥有 Hadoop 集群和 Apache Cloudberry 集群的管理权限。您还必须已配置用于访问 Hadoop 的 PXF 服务器。


步骤：

1. 在 `/tmp` 目录中创建名为 `sampledata.json` 的 JSON 文件：

    ```shell
    $ echo '{"location": "Prague", "month": "Jan","num_orders": 101, "total_sales": 4875.33, "items_sold": ["boots", "hats"]}
    {"location": "Rome", "month": "Mar","num_orders": 87, "total_sales": 1557.39, "items_sold": ["coats"]}
    {"location": "Bangalore", "month": "May","num_orders": 317, "total_sales": 8936.99, "items_sold": ["winter socks", "long-sleeved shirts", "boots"]}
    {"location": "Beijing", "month": "Jul","num_orders": 411, "total_sales": 11600.67, "items_sold": ["hoodies/sweaters", "pants"]}
    {"location": "Los Angeles", "month": "Dec","num_orders": 0, "total_sales": 0.00, "items_sold": null}' > /tmp/sampledata.json
    ```

1. [下载](https://repo1.maven.org/maven2/org/apache/orc/orc-tools)最新版本的 `orc-tools` JAR 到当前工作目录。

1. 运行 `orc-tools` 的 `convert` 命令，将 `sampledata.json` 转换为 ORC 文件 `/tmp/sampledata.orc`；需向该命令提供模式：

    ```shell
    $ java -jar orc-tools-1.7.3-uber.jar convert /tmp/sampledata.json \
      --schema 'struct<location:string,month:string,num_orders:int,total_sales:decimal(10,2),items_sold:array<string>>' \
      -o /tmp/sampledata.orc
    ```

1. 将 ORC 文件复制到 HDFS。以下命令将该文件复制到 `/data/pxf_examples/orc_example` 目录：

    ```shell
    $ hdfs dfs -put /tmp/sampledata.orc /data/pxf_examples/orc_example/
    ```

1. 登录 Apache Cloudberry Coordinator 主机并连接到数据库。以下命令以 `gpadmin` 用户身份连接到名为 `testdb` 的数据库：

    ```shell
    gpadmin@coordinator$ psql -d testdb
    ```

1. 创建名为 `sample_orc` 的外部表，使其引用 HDFS 上的 `/data/pxf_examples/orc_example/sampledata.orc` 文件。以下命令使用 ORC 模式中指定的列名创建该表，并使用 `default` PXF 服务器：

    ```sql
    testdb=# CREATE EXTERNAL TABLE sample_orc(location text, month text, num_orders int, total_sales numeric(10,2), items_sold text[])
               LOCATION ('pxf://data/pxf_examples/orc_example?PROFILE=hdfs:orc')
             FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```

    或者

    ```sql
    testdb=# CREATE SERVER example_orc FOREIGN DATA WRAPPER hdfs_pxf_fdw;
    testdb=# CREATE USER MAPPING FOR CURRENT_USER SERVER example_orc;
    testdb=# CREATE FOREIGN TABLE sample_orc(location text, month text, num_orders int, total_sales numeric(10,2), items_sold text[])
               SERVER example_orc
               OPTIONS (
               	resource 'data/pxf_examples/orc_example',
               	format 'orc'
               );
    ```

1. 通过查询 `sample_orc` 表读取文件中的数据：

    ```sql
    testdb=# SELECT * FROM sample_orc;
    ```

    ```shell
      location   | month | num_orders | total_sales |                  items_sold
    -------------+-------+------------+-------------+----------------------------------------------
     Prague      | Jan   |        101 |     4875.33 | {boots,hats}
     Rome        | Mar   |         87 |     1557.39 | {coats}
     Bangalore   | May   |        317 |     8936.99 | {"winter socks","long-sleeved shirts",boots}
     Beijing     | Jul   |        411 |    11600.67 | {hoodies/sweaters,pants}
     Los Angeles | Dec   |          0 |        0.00 |
    (5 rows)
    ```

1. 您可以对任意列执行查询，包括数组列 `items_sold`。例如，以下查询返回售出商品包含 `boots` 和/或 `pants` 的行：

    ```sql
    testdb=# SELECT * FROM sample_orc WHERE items_sold && '{"boots", "pants"}';
    ```

    ```shell
     location  | month | num_orders | total_sales |                  items_sold
    -----------+-------+------------+-------------+----------------------------------------------
     Prague    | Jan   |        101 |     4875.33 | {boots,hats}
     Bangalore | May   |        317 |     8936.99 | {"winter socks","long-sleeved shirts",boots}
     Beijing   | Jul   |        411 |    11600.67 | {hoodies/sweaters,pants}
    (3 rows)
    ```

1. 以下查询返回第一件售出商品为 `boots` 的行：

    ```sql
    testdb=# SELECT * FROM sample_orc WHERE items_sold[0] = 'boots';
    ```

    ```shell
     location  | month | num_orders | total_sales |                  items_sold
    -----------+-------+------------+-------------+----------------------------------------------
     Prague    | Jan   |        101 |     4875.33 | {boots,hats}
    (1 row)
    ```

## 示例：写入 HDFS 上的 ORC 文件 {#example-writing-to-an-orc-file-on-hdfs}

在本示例中，您将创建一个可写外部表，向 `sample_orc` 表所引用的目录写入一些数据。

1. 创建一个外部表，在 `LOCATION` URL 中指定 `hdfs:orc` Profile 和 HDFS 目录 `/data/pxf_examples/orc_example`：

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE write_to_sample_orc (location text, month text, num_orders int, total_sales numeric(10,2), items_sold text[] )
        LOCATION ('pxf://data/pxf_examples/orc_example?PROFILE=hdfs:orc')
      FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
    ```

    或者

    ```
        testdb=# CREATE SERVER example_orc FOREIGN DATA WRAPPER hdfs_pxf_fdw;
        testdb=# CREATE USER MAPPING FOR CURRENT_USER SERVER example_orc;
        testdb=# CREATE FOREIGN TABLE sample_orc(location text, month text, num_orders int, total_sales numeric(10,2), items_sold text[])
                   SERVER example_orc
                   OPTIONS (
                   	resource 'data/pxf_examples/orc_example',
                   	format 'orc'
                   );
    ```

1. 通过向 `write_to_sample_orc` 表插入数据，将几条记录写入 `orc_example` 目录中的 Segment 文件：
   
    ```sql
    postgres=# INSERT INTO write_to_sample_orc VALUES ( 'Frankfurt', 'Mar', 777, 3956.98, '{"winter socks","pants",boots}' );
    postgres=# INSERT INTO write_to_sample_orc VALUES ( 'Cleveland', 'Oct', 3218, 96645.37, '{"long-sleeved shirts",hats}' );
    ```

1. 请注意，Apache Cloudberry 不支持直接查询可写外部表。请查询您在上一个示例中创建的 `sample_orc` 表，以读取您新增的数据：

    ```sql
    postgres=# SELECT * FROM sample_orc ORDER BY num_orders;
    ```

## 了解写入数值数据时的溢出情况 {#understanding-overflow-conditions-when-writing-numeric-data}

PXF 使用 `HiveDecimal` 类写入 ORC 数值数据。在 6.7.0 之前的版本中，PXF 仅将数值类型的精度限制为最大 38。在 6.7.0 及更高版本中，PXF 在写入 ORC 数值数据之前必须同时满足精度和标度的要求。

在外部表中定义 `NUMERIC` 列而不指定精度或标度时，PXF 在内部将该列映射为 `DECIMAL(38, 10)`。

PXF 处理以下精度溢出情况：

- 您在外部表中定义了 `NUMERIC` 列，且某个值的整数位数超过所支持的最大精度 38。例如 `1234567890123456789012345678901234567890.12345`，其整数位数为 45。
- 您定义了 `NUMERIC(<precision>)` 列，且 `<precision>` 大于 38。例如 `NUMERIC(55)`。
- 您在外部表中定义了 `NUMERIC` 列，且某个值的整数位数大于 28（38-10）。例如 `123456789012345678901234567890.12345`，其整数位数为 30。

如果您定义了 `NUMERIC(<precision>, <scale>)` 列，并且某个值的整数位数大于 `<precision> - <scale>`，PXF 将返回错误。例如，您定义了 `NUMERIC(20,4)` 列，而值为 `12345678901234567.12`，其整数位数为 19，大于 20-4=16。

在向 ORC 文件写入数值数据时检测到溢出，PXF 可以采取三种操作之一：对该值进行舍入（默认）、返回错误，或忽略溢出。`pxf-site.xml` 服务器配置中的 `pxf.orc.write.decimal.overflow` 属性决定 PXF 在这种情况下采取的操作；该属性的有效取值如下：

| 取值  | PXF 操作 |
|-------|-------------------------------------|
| `round` | 当 PXF 遇到溢出时，会尝试对该值进行舍入，使其在写入之前同时满足精度和标度的要求。如果舍入失败，PXF 报告错误。这可能会在外部系统中留下不完整的数据集。`round` 为默认值。 |
| `error` | PXF 遇到溢出时报告错误，事务失败。 |
| `ignore` | PXF 尝试对该值进行舍入，使其仅满足精度要求，并忽略对精度和标度的验证；否则 PXF 写入 NULL 值。（这是 PXF 在 6.7.0 版本之前的行为。） |

当 PXF 检测到溢出且 `pxf.orc.write.decimal.overflow` 属性设置为 `ignore` 时，PXF 会记录一条警告。
