---
title: "使用 S3 Select 从 S3 读取 CSV 和 Parquet 数据"
description: "使用 S3 Select 从 S3 读取 CSV 和 Parquet 数据。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/read_s3_s3select.md"
---

PXF S3 连接器支持使用 Amazon S3 Select 服务从 S3 读取特定的 CSV 格式和 Parquet 格式数据。S3 Select 为存储在 Amazon S3 中的数据提供原地直接查询（query-in-place）功能。

启用后，PXF 使用 S3 Select 过滤 S3 对象的内容，以检索所请求的数据子集。这通常既能减少传输到 Apache Cloudberry 的数据量，也能缩短查询时间。

通过 PXF S3 连接器配合 S3 Select，可以读取：

- 经 `gzip` 压缩或 `bzip2` 压缩的 `CSV` 文件
- 列经 `gzip` 压缩或 `snappy` 压缩的 `Parquet` 文件

数据必须采用 `UTF-8` 编码，并且可以经过服务器端加密。

使用 S3 Select 时，PXF 支持列投影（column projection），也支持针对 `AND`、`OR` 和 `NOT` 运算符的谓词下推（predicate pushdown）。

> <b>注意：</b>使用 Amazon S3 Select 服务可能会增加数据访问和检索的成本。在启用 PXF 使用 S3 Select 服务之前，请务必考虑相关成本。

## 启用 PXF 使用 S3 Select {#enabling-pxf-to-use-s3-select}

访问 S3 对象存储时，`S3_SELECT` 外部表自定义选项控制 PXF 是否使用 S3 Select。设置 `S3_SELECT` 选项时，可以提供以下值：

| S3-SELECT 值  | 描述 |
|-------|-------------------------------------|
| OFF    | PXF 不使用 S3 Select；默认值。 |
| ON    | PXF 始终使用 S3 Select。 |
| AUTO    | PXF 在 S3 Select 有利于访问或性能时使用它。 |

默认情况下，PXF 不使用 S3 Select（`S3_SELECT=OFF`）。可以让 PXF 始终使用 S3 Select，或者仅在 PXF 判定 S3 Select 可能有利于性能时才使用。例如，当 `S3_SELECT=AUTO` 时，如果对外部表的查询使用了列投影或谓词下推，或者所引用的 CSV 文件包含标题行，PXF 会自动使用 S3 Select。

**注意**：使用 PXF 外部表通过 S3 Select 从 S3 读取 CSV 文本和 Parquet 数据时，`IGNORE_MISSING_PATH` 自定义选项不可用。


## 使用 S3 Select 读取 Parquet 数据 {#reading-parquet-data-with-s3-select}

PXF 支持按照[读写对象存储中的 Parquet 数据](/cloudberry/pxf/access-objectstores/objstore_parquet/)中的说明从 S3 读取 Parquet 数据。如果希望 PXF 在读取 Parquet 数据时使用 S3 Select，请将 `S3_SELECT` 自定义选项及其值添加到 `CREATE EXTERNAL TABLE` 的 `LOCATION` URI 中。

### 指定 Parquet 列压缩类型 {#specifying-the-parquet-column-compression-type}

如果 Parquet 文件中的列经 `gzip` 压缩或 `snappy` 压缩，请在 `LOCATION` URI 中使用 `COMPRESSION_CODEC` 自定义选项标明压缩编解码器别名。例如：

```text
&COMPRESSION_CODEC=gzip
```

或者：

```text
&COMPRESSION_CODEC=snappy
```

### 创建外部表 {#creating-the-external-table}

使用以下语法创建 Apache Cloudberry 外部表，引用 S3 上希望 PXF 通过 S3 Select 服务访问的 Parquet 文件：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
  LOCATION ('pxf://<path-to-file>?PROFILE=s3:parquet&SERVER=<server_name>&S3_SELECT=ON|AUTO[&<other-custom-option>=<value>[...]]')
FORMAT 'CSV';
```

> <b>注意：</b>在为访问 S3 上 Parquet 文件的外部表启用 PXF 使用 S3 Select 时，<i>必须</i>指定 `FORMAT 'CSV'`。

例如，使用以下命令让 PXF 在最优时使用 S3 Select 访问 S3 上的 Parquet 文件：

```sql
CREATE EXTERNAL TABLE parquet_on_s3 ( LIKE table1 )
  LOCATION ('pxf://bucket/file.parquet?PROFILE=s3:parquet&SERVER=s3srvcfg&S3_SELECT=AUTO')
FORMAT 'CSV';
```

## 使用 S3 Select 读取 CSV 文件 {#reading-csv-files-with-s3-select}

PXF 支持按照[读写对象存储中的文本数据](/cloudberry/pxf/access-objectstores/objstore_text/)中的说明从 S3 读取 CSV 数据。如果希望 PXF 在读取 CSV 数据时使用 S3 Select，请将 `S3_SELECT` 自定义选项及其值添加到 `CREATE EXTERNAL TABLE` 的 `LOCATION` URI 中。还可以指定分隔符格式化器选项，以及文件标题和压缩自定义选项。

### 处理 CSV 文件标题 {#handling-the-csv-file-header}

> <b>注意：</b>只有当 S3 连接器使用 Amazon S3 Select 服务访问 S3 上的文件时，PXF 才能读取带有标题行的 CSV 文件。PXF 不支持从任何其他外部数据存储读取包含标题行的 CSV 文件。

CSV 文件可以包含标题行。启用 PXF 使用 S3 Select 访问 CSV 格式文件时，使用 `LOCATION` URI 中的 `FILE_HEADER` 自定义选项标明 CSV 文件是否有标题行，以及有标题行时希望 PXF 如何处理。PXF 从不返回标题行。

**注意**：当 CSV 文件包含标题行时，*必须*指定 `S3_SELECT=ON` 或 `S3_SELECT=AUTO`。此时不要指定 `S3_SELECT=OFF`。

`FILE_HEADER` 选项取以下值：

| FILE_HEADER 值  | 描述 |
|-------|-------------------------------------|
| NONE    | 文件没有标题行；默认值。 |
| IGNORE  | 文件有标题行；忽略该标题。在外部表和 CSV 文件的列顺序相同时使用。（列顺序相同时，列名与 CSV 标题名可以不同。）|
| USE    | 文件有标题行；读取该标题。在外部表列名与 CSV 标题名相同但顺序不同时使用。 |

如果外部表列与 CSV 标题的顺序和名称都相同，可以指定 `FILE_HEADER=IGNORE` 或 `FILE_HEADER=USE`。

> <b>注意：</b>当外部表列的顺序和名称都与 CSV 标题列不同时，PXF 无法将 CSV 数据与外部表定义相匹配。对满足这些条件的外部表执行的任何查询都会失败，并报错 `Some headers in the query are missing from the file`。

例如，如果 CSV 文件标题与外部表中的列顺序相同，请将以下内容添加到 `CREATE EXTERNAL TABLE` 的 `LOCATION` URI 中，让 PXF 忽略 CSV 标题：

```text
&FILE_HEADER=IGNORE
```

### 指定 CSV 文件压缩类型 {#specifying-the-csv-file-compression-type}

如果 CSV 文件经 `gzip` 或 `bzip2` 压缩，请在 `LOCATION` URI 中使用 `COMPRESSION_CODEC` 自定义选项标明压缩编解码器别名。例如：

```text
&COMPRESSION_CODEC=gzip
```

或者：

```text
&COMPRESSION_CODEC=bzip2
```

### 创建外部表 {#creating-the-external-table-1}

使用以下语法创建 Apache Cloudberry 外部表，引用 S3 上希望 PXF 通过 S3 Select 服务访问的 CSV 文件：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-file>
    ?PROFILE=s3:text&SERVER=<server_name>&S3_SELECT=ON|AUTO[&FILE_HEADER=IGNORE|USE][&COMPRESSION_CODEC=gzip|bzip2][&<other-custom-option>=<value>[...]]')
FORMAT 'CSV' [(delimiter '<delim_char>')];
```

**注意**：不要在 `CREATE EXTERNAL TABLE` 命令中使用 `(HEADER)` 格式化器选项。

**注意**：使用 S3 Select 服务读取 S3 上的 CSV 文件时，PXF 不支持 `SKIP_HEADER_COUNT` 自定义选项。

例如，使用以下命令让 PXF 始终使用 S3 Select 访问 S3 上经 `gzip` 压缩的文件，其中字段分隔符为竖线（'|'）字符，且外部表与 CSV 标题的列顺序相同。

```sql
CREATE EXTERNAL TABLE gzippedcsv_on_s3 ( LIKE table2 )
  LOCATION ('pxf://bucket/file.csv.gz?PROFILE=s3:text&SERVER=s3srvcfg&S3_SELECT=ON&FILE_HEADER=USE')
FORMAT 'CSV' (delimiter '|');
```
