---
title: "示例：读写 ClickHouse 表"
description: "在 ClickHouse 中使用 PXF JDBC。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-jdbc/jdbc_pxf_clickhouse.md"
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

- 在 Apache Cloudberry Coordinator 上安装 ClickHouse JDBC 驱动程序（参见 [JDBC 驱动程序](#jdbc-driver)）
- 创建 ClickHouse 表，并向表中插入数据
- 在 `LOCATION` 子句中使用 `JDBC_DRIVER` 和 `DB_URL`，创建引用该 ClickHouse 表的 PXF 可读外部表（无需单独的 PXF 服务器配置目录）
- 使用 PXF 读取 ClickHouse 表中的数据
- 创建引用该 ClickHouse 表的 PXF 可写外部表
- 使用 PXF 向 ClickHouse 表写入数据
- 再次读取 ClickHouse 表中的数据

## 创建 ClickHouse 表 {#create-a-clickhouse-table}

执行以下步骤，在 `default` 数据库中创建名为 `pxf_ch_types` 的 ClickHouse 表：

```sql
CREATE TABLE default.pxf_ch_types (
  i_int Int32,
  s_small Int16,
  b_big Int64,
  f_float32 Float32,
  d_float64 Float64,
  b_bool Bool,
  dec Decimal(38,10),
  t_text String,
  bin String,
  d_date Date,
  d_ts DateTime64(3,'UTC'),
  d_tstz DateTime64(3,'UTC'),
  d_uuid UUID
) ENGINE = MergeTree ORDER BY (i_int);

INSERT INTO default.pxf_ch_types
  (i_int, s_small, b_big, f_float32, d_float64, b_bool, dec, t_text, bin, d_date, d_ts, d_tstz, d_uuid)
VALUES
  (1, 2, 3, 1.25, 3.1415926, true, toDecimal64('12345.6789012345', 10), 'hello', 'ABCD',
   toDate('2020-01-02'), toDateTime64('2020-01-02 03:04:05.006', 3, 'UTC'),
   toDateTime64('2020-01-02 03:04:05.006', 3, 'UTC'), toUUID('550e8400-e29b-41d4-a716-446655440000'));
```

## JDBC 驱动程序 {#jdbc-driver}

将 ClickHouse JDBC 驱动程序 JAR 放置在每台 Coordinator 和 Segment 主机的 `$PXF_BASE/lib` 下，同步 PXF，然后重启 PXF。Cloudberry 构建可以打包 `server/pxf-jdbc-drivers` 中的 JDBC 驱动程序；请遵循您所在部署的流程（例如，用于暂存 PXF 并链接驱动程序的自动化 `Makefile` 目标）。

如果像下文所示在外部表定义中传入连接选项，则**不**需要 `servers/clickhouse/jdbc-site.xml`。

自动化测试针对 ClickHouse 服务器 **24** 和 **26** 版本，配合 ClickHouse JDBC 驱动程序进行。

对于 ClickHouse，建议使用最新的 clickhouse-jdbc-all:0.9.7 或更高版本（带有重定位依赖的 fat jar 版本）。如果遇到 HTTP 可靠性问题，可以使用 Apache HttpClient：添加 JDBC URL 参数 `http_connection_provider=APACHE_HTTP_CLIENT`（例如 `jdbc:clickhouse://clickhousehost:8123/default?http_connection_provider=APACHE_HTTP_CLIENT`）。


## 读取 ClickHouse 表 {#read-from-the-clickhouse-table}

执行以下步骤，创建引用 `pxf_ch_types` ClickHouse 表的 PXF 外部表，并读取该表中的数据：

1. 使用 `jdbc` Profile 创建 PXF 可读外部表。请按实际情况替换 ClickHouse 主机、端口和驱动程序类：

   ```sql
   CREATE EXTERNAL TABLE pxf_ch_read(
     i_int int, s_small smallint, b_big bigint,
     f_float32 real, d_float64 double precision, b_bool boolean,
     dec numeric, t_text text, bin bytea, d_date date,
     d_ts timestamp, d_tstz timestamp with time zone, d_uuid uuid)
     LOCATION ('pxf://default.pxf_ch_types?PROFILE=jdbc&JDBC_DRIVER=com.clickhouse.jdbc.ClickHouseDriver&DB_URL=jdbc:clickhouse://clickhousehost:8123/default')
     FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
   ```

2. 读取数据：

   ```sql
   SELECT * FROM pxf_ch_read ORDER BY i_int;
   ```

## 写入 ClickHouse 表 {#write-to-the-clickhouse-table}

执行以下步骤，创建引用 `pxf_ch_types` ClickHouse 表的 PXF 可写外部表，并向该表写入数据：

1. 创建 PXF 可写外部表：

   ```sql
   CREATE WRITABLE EXTERNAL TABLE pxf_ch_write(
     i_int int, s_small smallint, b_big bigint,
     f_float32 real, d_float64 double precision, b_bool boolean,
     dec numeric, t_text text, bin bytea, d_date date,
     d_ts timestamp, d_tstz timestamp with time zone, d_uuid uuid)
     LOCATION ('pxf://default.pxf_ch_types?PROFILE=jdbc&JDBC_DRIVER=com.clickhouse.jdbc.ClickHouseDriver&DB_URL=jdbc:clickhouse://clickhousehost:8123/default')
     FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
   ```

2. 写入数据：

   ```sql
   INSERT INTO pxf_ch_write VALUES
     (2, 3, 4, 2.25, 4.1415926, true, CAST('12345.6789012345' AS numeric),
      'hello2', decode('41424344','hex'), DATE '2020-01-02',
      TIMESTAMP '2020-01-02 03:04:05.006',
      TIMESTAMPTZ '2020-01-02 03:04:05.006+00',
      '550e8400-e29b-41d4-a716-446655440000'::uuid);
   ```

3. 读回数据：

   ```sql
   SELECT * FROM pxf_ch_read ORDER BY i_int;
   ```

## 数据类型映射与限制 {#data-type-mapping-and-limitations}

PXF 支持以下 JDBC 数据类型（参见[支持的 JDBC 数据类型](/cloudberry/pxf/access-jdbc/#data-types-supported)）。
对于 ClickHouse，JDBC 侧的典型映射如下：

- `INTEGER`、`SMALLINT`、`BIGINT` → `Int32`、`Int16`、`Int64`
- `REAL`、`FLOAT8` → `Float32`、`Float64`
- `NUMERIC` → `Decimal(precision, scale)`
- `BOOLEAN` → `Bool`
- `VARCHAR`、`BPCHAR`、`TEXT` → `String`
- `DATE` → `Date`
- `TIMESTAMP` → `DateTime64(precision, 'UTC')`
- `TIMESTAMPTZ` → `DateTime64(precision, 'UTC')`
- `BYTEA` → `String`
- `UUID` → `UUID`
