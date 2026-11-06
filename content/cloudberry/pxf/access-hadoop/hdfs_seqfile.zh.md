---
title: "读写 HDFS SequenceFile 数据"
description: "通过 PXF 读写 HDFS 中的 SequenceFile 数据。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_seqfile.md"
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

PXF HDFS 连接器支持 SequenceFile 格式的二进制数据。本节介绍如何使用 PXF 读写 HDFS 中的 SequenceFile 数据，包括如何创建引用 HDFS 数据存储中文件的外部表、向其中插入数据以及对其进行查询。

PXF 支持读取或写入使用 `default`、`bzip2` 和 `gzip` 编解码器压缩的 SequenceFile 文件。

## 前提条件 {#prerequisites}

在尝试从 HDFS 读取数据或向 HDFS 写入数据之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。

## 创建外部表 {#creating-the-external-table}

PXF HDFS 连接器的 `hdfs:SequenceFile` Profile 支持读写 SequenceFile 二进制格式的 HDFS 数据。向可写外部表插入记录时，所插入的数据块会被写入您所指定目录中的一个或多个文件。

**注意**：使用可写 Profile 创建的外部表只能用于 INSERT 操作。如果要查询已插入的数据，必须另外创建一个引用该 HDFS 目录的可读外部表。

使用以下语法创建引用 HDFS 目录的 Apache Cloudberry 外部表： 

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name> 
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-dir>
    ?PROFILE=hdfs:SequenceFile[&SERVER=<server_name>][&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (<formatting-properties>)
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;dir\>    | HDFS 数据存储中目录的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;dir\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;dir\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hdfs:SequenceFile`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>  | 下文介绍 \<custom-option\>。|
| FORMAT | 将 `FORMAT` '`CUSTOM`' 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间的额外数据移动。 |

### 自定义选项 {#custom-options}

SequenceFile 格式的数据可以选择使用记录压缩或块压缩，以及特定的压缩编解码器。

使用 `hdfs:SequenceFile` Profile 写入 SequenceFile 格式的数据时，必须提供用于序列化／反序列化二进制数据的 Java 类的名称。该类必须为数据模式中引用的每种数据类型提供读方法和写方法。

压缩类型和编解码器，以及 Java 序列化／反序列化类，都通过 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句中的自定义选项指定。`hdfs:SequenceFile` Profile 支持以下自定义选项：

| 选项  | 取值说明 |
|-------|-------------------------------------|
| COMPRESSION_CODEC    | 压缩编解码器别名。支持的压缩编解码器包括：`default`、`bzip2`、`gzip` 和 `uncompressed`。如果未提供此选项，Apache Cloudberry 不执行数据压缩。 |
| COMPRESSION_TYPE    | 要使用的压缩类型；支持的取值为 `RECORD`（默认）或 `BLOCK`。 |
| DATA_SCHEMA    | 写入器序列化／反序列化类的名称。该类所在的 jar 文件必须位于 PXF 类路径中。`hdfs:SequenceFile` Profile 需要此选项，且没有默认值。（**注意**：与之等效的名为 `DATA-SCHEMA` 的选项已弃用，并可能在未来版本中移除。） |
| IGNORE_MISSING_PATH | 布尔值，指定当 \<path-to-hdfs-dir\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片。 |


## 读写二进制数据 {#reading-and-writing-binary-data}

当您想向 HDFS 读写 SequenceFile 格式的数据时，请使用 HDFS 连接器的 `hdfs:SequenceFile` Profile。此类文件由二进制键／值对组成。SequenceFile 格式是 MapReduce 作业之间常用的数据传输格式。 


### 示例：向 HDFS 写入二进制数据 {#example-writing-binary-data-to-hdfs}

在此示例中，您将创建一个名为 `PxfExample_CustomWritable` 的 Java 类，用于序列化／反序列化之前示例中使用的示例模式中的字段。然后，您将使用该类访问通过 `hdfs:SequenceFile` Profile 创建并使用默认 PXF 服务器的可写外部表。

按以下步骤创建该 Java 类和可写表。

1. 准备创建示例 Java 类：

    ```shell
    $ mkdir -p pxfex/com/example/pxf/hdfs/writable/dataschema
    $ cd pxfex/com/example/pxf/hdfs/writable/dataschema
    $ vi PxfExample_CustomWritable.java
    ```

2. 将以下文本复制并粘贴到 `PxfExample_CustomWritable.java` 文件中：

    ```java
    package com.example.pxf.hdfs.writable.dataschema;
    
    import org.apache.hadoop.io.*;
    import java.io.DataInput;
    import java.io.DataOutput;
    import java.io.IOException;
    import java.lang.reflect.Field;

    /**
     * PxfExample_CustomWritable class - used to serialize and deserialize data with
     * text, int, and float data types
     */
    public class PxfExample_CustomWritable implements Writable {

        public String st1, st2;
        public int int1;
        public float ft;

        public PxfExample_CustomWritable() {
            st1 = new String("");
            st2 = new String("");
            int1 = 0;
            ft = 0.f;
        }

        public PxfExample_CustomWritable(int i1, int i2, int i3) {

            st1 = new String("short_string___" + i1);
            st2 = new String("short_string___" + i1);
            int1 = i2;
            ft = i1 * 10.f * 2.3f;

        }

        String GetSt1() {
            return st1;
        }

        String GetSt2() {
            return st2;
        }

        int GetInt1() {
            return int1;
        }
    
        float GetFt() {
            return ft;
        }

        @Override
        public void write(DataOutput out) throws IOException {

            Text txt = new Text();
            txt.set(st1);
            txt.write(out);
            txt.set(st2);
            txt.write(out);

            IntWritable intw = new IntWritable();
            intw.set(int1);
            intw.write(out);

            FloatWritable fw = new FloatWritable();
            fw.set(ft);
            fw.write(out);
        }

        @Override
        public void readFields(DataInput in) throws IOException {

            Text txt = new Text();
            txt.readFields(in);
            st1 = txt.toString();
            txt.readFields(in);
            st2 = txt.toString();

            IntWritable intw = new IntWritable();
            intw.readFields(in);
            int1 = intw.get();

            FloatWritable fw = new FloatWritable();
            fw.readFields(in);
            ft = fw.get();
        }

        public void printFieldTypes() {
            Class myClass = this.getClass();
            Field[] fields = myClass.getDeclaredFields();

            for (int i = 0; i < fields.length; i++) {
                System.out.println(fields[i].getType().getName());
            }
        }
    }
    ```

3. 编译 `PxfExample_CustomWritable` 并创建 Java 类 JAR 文件。提供的类路径必须包含您的 Hadoop 发行版的 `hadoop-common.jar` 文件。例如，如果您安装了 Hortonworks Data Platform Hadoop 客户端：

    ```shell
    $ javac -classpath /usr/hdp/current/hadoop-client/hadoop-common.jar  PxfExample_CustomWritable.java
    $ cd ../../../../../../
    $ jar cf pxfex-customwritable.jar com
    $ cp pxfex-customwritable.jar /tmp/
    ```

    （您的 Hadoop 库类路径可能有所不同。）

3. 将 `pxfex-customwritable.jar` 文件复制到 Apache Cloudberry 的 Coordinator 主机。例如：

    ```shell
    $ scp pxfex-customwritable.jar gpadmin@coordinator:/home/gpadmin
    ```

4. 登录您的 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ````

5. 将 `pxfex-customwritable.jar` JAR 文件复制到用户运行时库目录，并记下其位置。例如，如果 `PXF_BASE=/usr/local/cloudberry-pxf`：

    ```shell
    gpadmin@coordinator$ cp /home/gpadmin/pxfex-customwritable.jar /usr/local/cloudberry-pxf/lib/pxfex-customwritable.jar
    ```

5. 将 PXF 配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

3. 按照[重启 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#restarting-pxf) 中的说明，在每台 Apache Cloudberry 主机上重启 PXF。

5. 使用 PXF `hdfs:SequenceFile` Profile 创建 Apache Cloudberry 可写外部表。在 `DATA_SCHEMA` \<custom-option\> 中指定您在上面创建的序列化／反序列化 Java 类。创建可写表时，使用 `bzip2` 的 `BLOCK` 模式压缩。

    ```sql
    postgres=# CREATE WRITABLE EXTERNAL TABLE pxf_tbl_seqfile (location text, month text, number_of_orders integer, total_sales real)
                LOCATION ('pxf://data/pxf_examples/pxf_seqfile?PROFILE=hdfs:SequenceFile&DATA_SCHEMA=com.example.pxf.hdfs.writable.dataschema.PxfExample_CustomWritable&COMPRESSION_TYPE=BLOCK&COMPRESSION_CODEC=bzip2')
              FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
    ```

    请注意，`'CUSTOM'` `FORMAT` 的 \<formatting-properties\> 指定的是内置的 `pxfwritable_export` 格式化器。

6. 直接向 `pxf_tbl_seqfile` 表插入数据，向 HDFS 目录 `pxf_seqfile` 写入几条记录。例如：

    ```sql
    postgres=# INSERT INTO pxf_tbl_seqfile VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    postgres=# INSERT INTO pxf_tbl_seqfile VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    ```

6. 请记住，Apache Cloudberry 不支持直接查询可写外部表。要读取 `pxf_seqfile` 中的数据，请创建引用该 HDFS 目录的 Apache Cloudberry 可读外部表：

    ```sql
    postgres=# CREATE EXTERNAL TABLE read_pxf_tbl_seqfile (location text, month text, number_of_orders integer, total_sales real)
                LOCATION ('pxf://data/pxf_examples/pxf_seqfile?PROFILE=hdfs:SequenceFile&DATA_SCHEMA=com.example.pxf.hdfs.writable.dataschema.PxfExample_CustomWritable')
              FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    ```
    通过 `hdfs:SequenceFile` Profile 读取 HDFS 数据时，必须指定 `DATA_SCHEMA` \<custom-option\>。无需提供与压缩相关的选项。
    
6. 查询可读外部表 `read_pxf_tbl_seqfile`：

    ```sql
    gpadmin=# SELECT * FROM read_pxf_tbl_seqfile ORDER BY total_sales;
    ```
    
    ```text
     location  | month | number_of_orders | total_sales 
    -----------+-------+------------------+-------------
     Frankfurt | Mar   |              777 |     3956.98
     Cleveland | Oct   |             3812 |     96645.4
    (2 rows)
    ```

## 读取记录键 {#reading-the-record-key}

当 Apache Cloudberry 外部表引用 SequenceFile 或其他以键值格式存储行的数据格式时，可以在 Apache Cloudberry 查询中使用 `recordkey` 关键字作为字段名来访问键值。

`recordkey` 的字段类型必须与键的类型相对应，这与其他字段必须匹配 HDFS 数据的要求类似。 

可以将 `recordkey` 定义为以下任一 Hadoop 类型：

-   BooleanWritable
-   ByteWritable
-   DoubleWritable
-   FloatWritable
-   IntWritable
-   LongWritable
-   Text

如果某一行未定义记录键，Apache Cloudberry 将返回处理该行的 Segment 的 id。


### 示例：使用记录键 {#example-using-record-keys}

创建一个可读外部表，用于访问您在[示例：向 HDFS 写入二进制数据](#example-writing-binary-data-to-hdfs)中创建的可写表 `pxf_tbl_seqfile` 的记录键。在此示例中，将 `recordkey` 定义为 `int8` 类型。

```sql
postgres=# CREATE EXTERNAL TABLE read_pxf_tbl_seqfile_recordkey(recordkey int8, location text, month text, number_of_orders integer, total_sales real)
                LOCATION ('pxf://data/pxf_examples/pxf_seqfile?PROFILE=hdfs:SequenceFile&DATA_SCHEMA=com.example.pxf.hdfs.writable.dataschema.PxfExample_CustomWritable')
          FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
gpadmin=# SELECT * FROM read_pxf_tbl_seqfile_recordkey;
```

```text
 recordkey |  location   | month | number_of_orders | total_sales 
-----------+-------------+-------+------------------+-------------
         2 | Frankfurt   | Mar   |              777 |     3956.98
         1 | Cleveland   | Oct   |             3812 |     96645.4
(2 rows)
```

向可写表插入行时您没有定义记录键，因此 `recordkey` 标识的是处理该行数据的 Segment。
