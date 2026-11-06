---
title: "读写 HDFS 中的 JSON 数据"
description: "通过 PXF 读取 HDFS 中的 JSON 数据。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_json.md"
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

使用 PXF HDFS Connector 读写 JSON 格式的数据。本节介绍如何使用 PXF 和外部表访问并写入 HDFS 中的 JSON 数据。

## 前提条件 {#prerequisites}

在尝试从 HDFS 读取数据或向 HDFS 写入数据之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。

## 处理 JSON 数据 {#working-with-json-data}

JSON 是一种基于文本的数据交换格式。一个 JSON 数据文件包含一个或多个 JSON 对象。JSON 对象是无序的名称／值对的集合。值可以是字符串、数字、true、false、null、对象或数组。您可以定义嵌套的 JSON 对象和数组。

如下文各节所述，JSON 数据通常存储在后缀为 `.json` 或 `.jsonl`（JSON Lines）的文件中。

### 关于 PXF JSON 数据访问模式 {#about-the-pxf-json-data-access-modes}

PXF 为 JSON 文件支持两种数据访问模式。默认模式要求每行包含一条完整的 JSON 记录（JSONL）。PXF 还支持另一种访问模式，要求每个文件只包含一个 JSON 对象，其中的 JSON 记录可以（但不要求）跨越多行。

#### 每行一个对象 {#single-object-per-row}

JSON 文件可以在每行包含一个 JSON 对象，其中每一行代表一个数据库元组。PXF 读取的、每行包含一个对象的 JSON 文件可以使用任意后缀，也可以没有后缀。写入时，PXF 创建后缀为 `.jsonl` 的文件。

每行一个对象的 JSON 数据文件示例片段：

```text
{"id":1,"color":"red"}
{"id":2,"color":"yellow"}
{"id":3,"color":"green"}
```

有关此 JSON 语法的详细信息，请参阅 [JSON Lines](https://jsonlines.org/)。

#### 每个文件一个对象 {#single-object-per-file}

JSON 文件也可以包含单个具名的根级 JSON 对象，其值是一个 JSON 对象数组。读取时，该数组可以包含任意复杂度和嵌套层次的对象，PXF 会根据具有与 `IDENTIFIER`（下文讨论）所指定名称相同的属性的对象构成数据库元组。写入时，数组中的每个 JSON 对象代表一个数据库元组。此类 JSON 文件的后缀为 `.json`。

在下面的 JSON 数据文件示例中，根级 `records` 对象是一个包含三个对象（元组）的数组：

```text
{"records":[
{"id":1,"color":"red"}
,{"id":2,"color":"yellow"}
,{"id":3,"color":"green"}
]}
```

单个 JSON 对象中的记录也可以跨越多行：

```text
{
  "records":[
    {
      "id":1,
      "color":"red"
    },
    {
      "id":2,
      "color":"yellow"
    },
    {
      "id":3,
      "color":"green"
    }
  ]
}
```

有关此 JSON 语法的详细信息，请参阅 [Introducing JSON](http://www.json.org/)。

## 数据类型映射 {#data-type-mapping}

要在 Apache Cloudberry 中表示 JSON 数据，请将使用基本数据类型的数据值映射到相同类型的 Apache Cloudberry 列。JSON 支持复杂数据类型，包括投影和数组。

### 读映射 {#read-mapping}

读取 JSON 数据时，PXF 使用以下数据类型映射：

| JSON 数据类型    | PXF/Apache Cloudberry 数据类型 |
|-------------------|-------------------------------------------|
| boolean | boolean |
| number  | `{ bigint &#124; float8 &#124; integer &#124; numeric &#124; real &#124; smallint }` |
| string | text |
| string（base64 编码的值） | bytea |
| string（Apache Cloudberry 可识别的文本格式的 date、time、timestamp、timestamptz）<sup>1</sup> | `{ date &#124; time &#124; timestamp &#124; timestamptz }` |
| boolean[] 类型的数组（一维） | boolean[] |
| number[] 类型的数组（一维） | `{ bigint[] &#124; float8[] &#124; integer[] &#124; numeric[] &#124; real[] &#124; smallint[] }` |
| string[] 类型的数组（一维）（base64 编码的值） | bytea[] |
| string[] 类型的数组（一维）（Apache Cloudberry 可识别的文本格式的 date、time、timestamp）<sup>1</sup> | `{ date[] &#124; time[] &#124; timestamp[] &#124; timestamptz[] }` |
| string[] 类型的数组（一维） | text[] |
| 其他类型的数组 | text[] |
| Object                | 使用点 `.` 表示法指定到基本类型或数组类型成员的每一级投影（嵌套）。                                                                                         |
<sup>1</sup> 如果 Apache Cloudberry 无法将日期或时间字符串转换为目标类型，PXF 会返回错误。

读取时，可以使用 N 级投影将嵌套对象和数组的成员映射到基本数据类型。

### 写映射 {#write-mapping}

PXF 支持写入基本类型以及基本类型的一维数组。PXF 支持将其他复杂类型以字符串形式写入 JSON。

写入 JSON 数据时，PXF 使用以下数据类型映射：

| PXF/Apache Cloudberry 数据类型 | JSON 数据类型 |
|-------------------|----------------------|
| bigint, float8, integer, numeric, real, smallint | number |
| boolean | boolean |
| bpchar, text, varchar | string |
| bytea | string（base64 编码的值） |
| date, time, timestamp, timestamptz | string |
| boolean[] | boolean[] |
| bigint[], float8[], int[], numeric[], real[], smallint[] | number[] |
| bytea[] | string[]（base64 编码的值）  |
| date[], time[], timestamp[], timestamptz[] | string[] |

## 关于使用投影（读） {#about-using-projection-read}

在下面的 JSON 数据文件示例片段中，`user` 是由名为 `id` 和 `location` 的字段组成的对象：


```json
  {
    "created_at":"MonSep3004:04:53+00002013",
    "id_str":"384529256681725952",
    "user": {
      "id":31424214,
      "location":"COLUMBUS"
    },
    "coordinates":{
      "type":"Point",
      "values":[
         13,
         99
      ]
    }
  }
```

要将 `user` 对象中的嵌套字段直接指定为 Apache Cloudberry 外部表的列，请使用 `.` 投影：

```text
user.id
user.location
```

`coordinates` 是一个对象，由名为 `type` 的文本字段和名为 `values` 的整数数组组成。 

要将 `values` 数组的所有元素读入单个列，请将对应的 Apache Cloudberry 外部表列定义为 `int[]` 类型。

```text
"coordinates.values" int[]
```

## 创建外部表 {#creating-the-external-table}

使用 `hdfs:json` Profile 读写 HDFS 中 JSON 格式的数据。以下语法创建引用此类文件的 Apache Cloudberry 外部表：

```sql
CREATE [WRITABLE] EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<path-to-hdfs-file>?PROFILE=hdfs:json[&SERVER=<server_name>][&<custom-option>=<value>[...]]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import'|'pxfwritable_export')
[DISTRIBUTED BY (<column_name> [, ... ] ) | DISTRIBUTED RANDOMLY];
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的具体关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;hdfs&#8209;file\>    | HDFS 数据存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;file\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;hdfs&#8209;file\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hdfs:json`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>  | 读写操作的 \<custom-option\> 见下文。|
| FORMAT 'CUSTOM' | 将 `FORMAT` '`CUSTOM`' 与 `(FORMATTER='pxfwritable_export')`（写）或 `(FORMATTER='pxfwritable_import')`（读）配合使用。 |

### 自定义选项 {#custom-options}

PXF 支持读取和写入每行包含一个对象（默认）或包含单个 JSON 对象的 JSON 文件。当您要读取或写入的 JSON 文件包含单个对象时，必须提供 `IDENTIFIER` \<custom-option\> 及其取值。使用此选项标识某个字段的名称，PXF 将返回或写入该字段所属的父 JSON 对象，作为一个单独的元组。

`hdfs:json` Profile 支持以下自定义**读**选项：

| 选项关键字  | 描述 |
|-------|-----------------------|
| IDENTIFIER=\<value\> | 当您读取的 JSON 数据由单个 JSON 对象组成时，必须指定 `IDENTIFIER` 来标识某个字段的名称，PXF 将把该字段所属的父 JSON 对象作为单独的元组返回。 | 
| SPLIT_BY_FILE=\<boolean\> | 指定 PXF 如何拆分 \<path-to-hdfs-file\> 中的数据。默认值为 `false`，此时 PXF 为每个要处理的文件创建多个分片并行处理。设置为 `true` 时，PXF 为每个文件创建并处理单个分片。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-hdfs-file\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片。 |

> <b>注意：</b>当单对象 JSON 文件中的嵌套对象包含与父对象字段同名的字段，<i>并且</i>该字段名同时被指定为 `IDENTIFIER` 时，PXF 可能返回不正确的结果。如有需要，可以通过压缩该 JSON 文件并使用 PXF 读取压缩文件来规避这一边缘情况。

`hdfs:json` Profile 支持以下自定义**写**选项：

| 选项  | 取值说明 |
|-------|-------------------------------------|
| ROOT=\<value\>    | 写入单个 JSON 对象时，标识根级对象属性的名称。 |
| COMPRESSION_CODEC    | 压缩编解码器别名。写入 json 数据时支持的压缩编解码器包括：`default`、`bzip2`、`gzip` 和 `uncompressed`。如果未提供此选项，Apache Cloudberry 不执行数据压缩。 |
| DISTRIBUTED BY    | 如果要将现有 Apache Cloudberry 表中的数据加载到可写外部表中，请考虑在两个表上指定相同的分布策略或 `<column_name>`。这样做可以避免加载操作期间 Segment 之间的额外数据移动。 |

为 JSON 写操作指定压缩时，PXF 将其写入的文件命名为 `<basename>.<json_file_type>.<compression_extension>`。例如：`jan_sales.jsonl.gz`。

## 读示例 {#read-examples}

### 示例数据集 {#example-data-sets}

在后面的读示例中，您将使用两种 JSON 访问模式对一个示例数据集进行操作。该示例数据集的模式定义了具有以下成员名称和值数据类型的对象：

- "created_at" - text
- "id_str" - text
- "user" - object
    - "id" - integer
    - "location" - text
- "coordinates" - object（可选）
    - "type" - text
    - "values" - array
        - [0] - integer
        - [1] - integer

每行一个对象（JSONL）访问模式的数据集如下：

```text
{"created_at":"FriJun0722:45:03+00002013","id_str":"343136551322136576","user":{"id":395504494,"location":"NearCornwall"},"coordinates":{"type":"Point","values": [ 6, 50 ]}},
{"created_at":"FriJun0722:45:02+00002013","id_str":"343136547115253761","user":{"id":26643566,"location":"Austin,Texas"}, "coordinates": null},
{"created_at":"FriJun0722:45:02+00002013","id_str":"343136547136233472","user":{"id":287819058,"location":""}, "coordinates": null}
```

每个文件一个对象的 JSON 访问模式的数据集如下：

```json
{
  "root":[
    {
      "record_obj":{
        "created_at":"MonSep3004:04:53+00002013",
        "id_str":"384529256681725952",
        "user":{
          "id":31424214,
          "location":"COLUMBUS"
        },
        "coordinates":null
      },
      "record_obj":{
        "created_at":"MonSep3004:04:54+00002013",
        "id_str":"384529260872228864",
        "user":{
          "id":67600981,
          "location":"KryberWorld"
        },
        "coordinates":{
          "type":"Point",
          "values":[
             8,
             52
          ]
        }
      }
    }
  ]
}
```

您将在下一节中为这些示例数据集创建 JSON 文件并将其添加到 HDFS。

### 将示例 JSON 数据加载到 HDFS {#loading-the-sample-json-data-to-hdfs}

PXF HDFS 连接器可以读写存储在 HDFS 中的原生 JSON。

将上面每行一个对象的 JSON 示例数据集复制并粘贴到名为 `objperrow.jsonl` 的文件中。同样，将每个文件一个对象的 JSON 记录数据集复制并粘贴到名为 `singleobj.json` 的文件中。

> **注意** 请确保 JSON 文件中**没有**空行。

将刚创建的 JSON 数据文件复制到您的 HDFS 数据存储。如果您在之前的练习中尚未创建 `/data/pxf_examples` 目录，请先创建。例如：

```shell
$ hdfs dfs -mkdir /data/pxf_examples
$ hdfs dfs -put objperrow.jsonl /data/pxf_examples/
$ hdfs dfs -put singleobj.json /data/pxf_examples/
```

数据加载到 HDFS 之后，就可以使用 Apache Cloudberry 和 PXF 查询 JSON 数据并向其中添加数据。

### 示例：每行一个对象（读） {#example-single-object-per-row-read}

使用以下 [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) SQL 命令创建可读外部表，该表引用每行一个对象的 JSON 数据文件并使用 PXF 默认服务器。

```sql
CREATE EXTERNAL TABLE objperrow_json_tbl(
  created_at TEXT,
  id_str TEXT,
  "user.id" INTEGER,
  "user.location" TEXT,
  "coordinates.values" INTEGER[]
)
LOCATION('pxf://data/pxf_examples/objperrow.jsonl?PROFILE=hdfs:json')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

此表读取 JSON 文件中选定的字段。请注意，这里使用了 `.` 投影来访问 `user` 和 `coordinates` 对象中的嵌套字段。

要查看文件中的 JSON 数据，请查询该外部表：

```sql
SELECT * FROM objperrow_json_tbl;
```

要访问 `coordinates.values` 数组的特定元素，可以在方括号中指定数组下标：

```sql
SELECT "coordinates.values"[1], "coordinates.values"[2] FROM objperrow_json_tbl;
```

### 示例：每个文件一个对象（读） {#example-single-object-per-file-read}

为单对象 JSON 文件创建可读外部表的 SQL 命令与上面每行一个对象的数据集非常相似。此外还必须指定 `LOCATION` 子句的 `IDENTIFIER` 关键字及其关联值。例如：

```sql
CREATE EXTERNAL TABLE singleobj_json_tbl(
  created_at TEXT,
  id_str TEXT,
  "user.id" INTEGER,
  "user.location" TEXT,
  "coordinates.values" INTEGER[]
)
LOCATION('pxf://data/pxf_examples/singleobj.json?PROFILE=hdfs:json&IDENTIFIER=created_at')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

`created_at` 标识示例数据模式中 JSON 记录 `record_obj` 的第一个字段的成员名称。

要查看文件中的 JSON 数据，请查询该外部表：

```sql
SELECT * FROM singleobj_json_tbl;
```

### 读取 JSON 数组的其他方法 {#other-methods-to-read-a-json-array}

从 6.2.0 版本开始，PXF 支持将 JSON 数组读入 `TEXT[]` 列。PXF 仍然支持使用数组元素投影或单个文本类型列读取 JSON 数组的旧方法。这些访问方法介绍如下。

#### 使用数组元素投影 {#using-array-element-projection}

PXF 支持在表定义中使用 `[n]` 语法标识具体元素，从而访问 JSON 数组的特定元素。

```sql
CREATE EXTERNAL TABLE objperrow_json_tbl_aep(
  created_at TEXT,
  id_str TEXT,
  "user.id" INTEGER,
  "user.location" TEXT,
  "coordinates.values[0]" INTEGER,
  "coordinates.values[1]" INTEGER
)
LOCATION('pxf://data/pxf_examples/objperrow.jsonl?PROFILE=hdfs:json')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

**注意**：使用此方法标识特定数组元素时，PXF _仅_向 Apache Cloudberry 提供这些值，而不是整个 JSON 数组。

如果现有外部表定义使用数组元素投影，而您希望将数组读入 `TEXT[]` 列，可以使用 `ALTER EXTERNAL TABLE` 命令更新表定义。例如：

```sql
ALTER EXTERNAL TABLE objperrow_json_tbl_aep DROP COLUMN "coordinates.values[0]", DROP COLUMN "coordinates.values[1]", ADD COLUMN "coordinates.values" TEXT[];
```

如果选择以这种方式修改外部表定义，请务必更新外部表上所有现有的查询，以适应列名和列类型的变化。

#### 指定单个文本类型列 {#specifying-a-single-text-type-column}

通过将对应的 Apache Cloudberry 表列定义为以下数据类型之一：`TEXT`、`VARCHAR` 或 `BPCHAR`，PXF 支持以包含序列化 JSON 数组的单个字符串的形式访问数组中的所有元素。

```sql
CREATE EXTERNAL TABLE objperrow_json_tbl_stc(
  created_at TEXT,
  id_str TEXT,
  "user.id" INTEGER,
  "user.location" TEXT,
  "coordinates.values" TEXT
)
LOCATION('pxf://data/pxf_examples/objperrow.jsonl?PROFILE=hdfs:json')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

如果将 JSON 数组检索到单个文本类型列中，并希望将序列化为 `TEXT` 的 JSON 数组转换回原生 Apache Cloudberry 数组类型，可以使用下面的示例查询：

```sql
SELECT user.id,
       ARRAY(SELECT json_array_elements_text(coordinates.values::json))::int[] AS coords
FROM objperrow_json_tbl_stc;
```

如果外部表定义对 JSON 数组使用单个文本类型列，而您希望将数组读入 `TEXT[]` 列，可以使用 `ALTER EXTERNAL TABLE` 命令更新表定义。例如：

```sql
ALTER EXTERNAL TABLE objperrow_json_tbl_stc ALTER COLUMN "coordinates.values" TYPE TEXT[];
```

如果选择以这种方式修改外部表定义，请务必更新外部表上所有现有的查询，以适应列类型的变化。

## 写入 JSON 数据 {#writing-json-data}

要写入 JSON 数据，请创建引用 HDFS 上某个目录名称的可写外部表。向可写外部表插入记录时，PXF 会将所插入的数据块写入您所指定目录中的一个或多个文件。在默认情况下（每行一个对象），PXF 将数据写入 `.jsonl` 文件。指定 `ROOT` 属性（每个文件一个对象）时，PXF 写入 `.json` 文件。

> **注意** 写入 JSON 数据时，PXF 仅支持 Apache Cloudberry 数据类型的标量或一维数组。写入 JSON 数据时，PXF 不支持列投影。

可写外部表只能用于 `INSERT` 操作。如果要查询已插入的数据，必须另外创建一个引用该 HDFS 目录的可读外部表，并从该表中读取。

写示例使用与读示例类似的数据模式。

### 示例：每行一个对象（写） {#example-single-object-per-row-write}

在此示例中，我们向名为 `jsopr` 的目录中添加数据。

使用以下 [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) SQL 命令创建可写外部表，该表以每行一个对象的格式写入 JSON 数据并使用 PXF 默认服务器。

```sql
CREATE WRITABLE EXTERNAL TABLE add_objperrow_json_tbl(
  created_at TEXT,
  id_str TEXT,
  id INTEGER,
  location TEXT,
  coordinates INTEGER[]
)
LOCATION('pxf://data/pxf_examples/jsopr?PROFILE=hdfs:json')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
```

向该表写入数据：

```sql
INSERT INTO add_objperrow_json_tbl VALUES ( 'SunJun0912:59:07+00002013', '343136551111111111', 311111111, 'FarAway', '{ 6, 50 }' );
INSERT INTO add_objperrow_json_tbl VALUES ( 'MonJun1002:12:06+00002013', '343136557777777777', 377777777, 'NearHere', '{ 13, 93 }' );
```

读取刚写入的数据。请记住，必须先创建一个可读外部表：

```sql
CREATE EXTERNAL TABLE jsopr_tbl(
  created_at TEXT,
  id_str TEXT,
  id INTEGER,
  location TEXT,
  coordinates INTEGER[]
)
LOCATION('pxf://data/pxf_examples/jsopr?PROFILE=hdfs:json')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

查询该表：

```sql
SELECT * FROM jsopr_tbl;

        created_at         |       id_str       |    id     | location | coordinates 
---------------------------+--------------------+-----------+----------+-------------
 MonJun1002:12:06+00002013 | 343136557777777777 | 377777777 | NearHere | {13,93}
 SunJun0912:59:07+00002013 | 343136551111111111 | 311111111 | FarAway  | {6,50}
(2 rows)
```

查看添加到 HDFS 的文件：

```
$ hdfs dfs -cat /data/pxf_examples/jsopr/*
{"created_at":"SunJun0912:59:07+00002013","id_str":"343136551111111111","id":311111111,"location":"FarAway","coordinates":[6,50]}
{"created_at":"MonJun1002:12:06+00002013","id_str":"343136557777777777","id":377777777,"location":"NearHere","coordinates":[13,93]}
```

请注意，PXF 创建的是扁平的 JSON 结构。

### 示例：每个文件一个对象（写） {#example-single-object-per-file-write}

使用以下 [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) SQL 命令创建可写外部表，该表以单对象格式写入 JSON 数据并使用 PXF 默认服务器。

必须在 `LOCATION` 子句中指定 `ROOT` 关键字及其关联值。例如：

```sql
CREATE WRITABLE EXTERNAL TABLE add_singleobj_json_tbl(
  created_at TEXT,
  id_str TEXT,
  id INTEGER,
  location TEXT,
  coordinates INTEGER[]
)
LOCATION('pxf://data/pxf_examples/jso?PROFILE=hdfs:json&ROOT=root')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export');
```

`root` 标识该单个对象的根属性的名称。

向该表写入数据：

```sql
INSERT INTO add_singleobj_json_tbl VALUES ( 'SunJun0912:59:07+00002013', '343136551111111111', 311111111, 'FarAway', '{ 6, 50 }' );
INSERT INTO add_singleobj_json_tbl VALUES ( 'WedJun1212:37:02+00002013', '333333333333333333', 333333333, 'NetherWorld', '{ 9, 63 }' );
```

读取刚写入的数据。请记住，必须先创建一个新的可读外部表：

```sql
CREATE EXTERNAL TABLE jso_tbl(
  created_at TEXT,
  id_str TEXT,
  id INTEGER,
  location TEXT,
  coordinates INTEGER[]
)
LOCATION('pxf://data/pxf_examples/jso?PROFILE=hdfs:json&IDENTIFIER=created_at')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

创建命令中指定的列名必须与可写外部表的列名一致。并且请记住，要读取包含单个对象的 JSON 文件，必须指定 `IDENTIFIER` 选项。

查询该表以读取数据：

```sql
SELECT * FROM jso_tbl;

        created_at         |       id_str       |    id     |   location   | coordinates 
---------------------------+--------------------+-----------+--------------+-------------
 WedJun1212:37:02+00002013 | 333333333333333333 | 333333333 | NetherWorld  | {9,63}
 SunJun0912:59:07+00002013 | 343136551111111111 | 311111111 | FarAway      | {6,50}
(2 rows)
```

查看添加到 HDFS 的文件：

```
$ hdfs dfs -cat /data/pxf_examples/jso/*
{"root":[
{"created_at":"SunJun0912:59:07+00002013","id_str":"343136551111111111","id":311111111,"location":"FarAway","coordinates":[6,50]}
]}
{"root":[
{"created_at":"WedJun1212:37:02+00002013","id_str":"333333333333333333","id":333333333,"location":"NetherWorld","coordinates":[9,63]}
]}
```
