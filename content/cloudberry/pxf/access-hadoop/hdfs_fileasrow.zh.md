---
title: "将多行文本文件读入单个表行"
description: "通过 PXF 将多行文本文件作为单个表行读取。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hdfs_fileasrow.md"
---

您可以使用 PXF HDFS 连接器，将 HDFS 中的一个或多个多行文本文件分别作为单个表行读取。当您希望将多个文件读入同一个 Apache Cloudberry 外部表时，这种方式可能很有用，例如各个 JSON 文件分别包含一条独立记录的情况。

PXF 仅支持以这种方式读取文本文件和 JSON 文件。

**注意**：如果您想使用 PXF 读取包含多条记录的 JSON 文件，请参阅[读写 HDFS 中的 JSON 数据](/cloudberry/pxf/access-hadoop/hdfs_json/)一节。


## 前提条件 {#prerequisites}

在尝试从 HDFS 读取文件之前，请确保已满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。


## 读取多行文本和 JSON 文件 {#reading-multi-line-text-and-json-files}

您可以将单行和多行文件读入单个表行，包括含有内嵌换行符的文件。如果读取多个 JSON 文件，则每个文件必须是一条完整的记录，并且每个文件必须包含相同的记录类型。

PXF 将完整的文件数据读入单个行和单个列。创建用于读取多个文件的外部表时，必须确保要读取的所有文件属于同一类型（文本或 JSON）。还必须根据文件类型，指定单个 `text` 或 `json` 列。

以下语法创建一个引用 HDFS 上一个或多个文本文件或 JSON 文件的 Apache Cloudberry 可读外部表：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> text|json | LIKE <other_table> )
  LOCATION ('pxf://<path-to-files>?PROFILE=hdfs:text:multi[&SERVER=<server_name>][&IGNORE_MISSING_PATH=<boolean>]&FILE_AS_ROW=true')
FORMAT 'CSV');
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的关键字和取值说明如下表所示。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<path&#8209;to&#8209;files\>    | HDFS 数据存储中目录或文件的路径。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将 \<path&#8209;to&#8209;hdfs&#8209;files\> 视为相对于所指定基础路径的路径；否则，PXF 将其视为绝对路径。\<path&#8209;to&#8209;files\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hdfs:text:multi`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| FILE\_AS\_ROW=true    | 必需选项，指示 PXF 将每个文件读入单个表行。 |
| IGNORE_MISSING_PATH=\<boolean\> | 指定当 \<path-to-files\> 缺失或无效时采取的操作。默认值为 `false`，此时 PXF 在这种情况下返回错误。值为 `true` 时，PXF 忽略路径缺失错误并返回空分片。 |
| FORMAT | `FORMAT` 必须指定为 `'CSV'`。  |

**注意**：当指定 `FILE_AS_ROW=true` 选项时，`hdfs:text:multi` Profile 不支持额外的自定义选项或格式选项。

例如，如果 `/data/pxf_examples/jdir` 标识一个包含若干 JSON 文件的 HDFS 目录，则以下语句创建一个引用该目录中所有文件的 Apache Cloudberry 外部表：

```sql
CREATE EXTERNAL TABLE pxf_readjfiles(j1 json)
  LOCATION ('pxf://data/pxf_examples/jdir?PROFILE=hdfs:text:multi&FILE_AS_ROW=true')
FORMAT 'CSV';
```

使用 `SELECT` 语句查询 `pxf_readjfiles` 表时，PXF 会将 `jdir/` 中每个 JSON 文件的内容作为外部表中单独的一行返回。

读取 JSON 文件时，可以使用 Apache Cloudberry 提供的 JSON 函数访问 JSON 记录中的各个数据字段。例如，如果上述 `pxf_readjfiles` 外部表读取的 JSON 文件包含如下 JSON 记录：

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
      }
    }
  ]
}
```

可以使用 `json_array_elements()` 函数从表行中提取特定的 JSON 字段。例如，以下命令显示 `user->id` 字段：

```sql
SELECT json_array_elements(j1->'root')->'record_obj'->'user'->'id'
  AS userid FROM pxf_readjfiles;

  userid  
----------
 31424214
(1 rows)
```

有关在 Apache Cloudberry 中处理 JSON 数据的具体信息，请参阅 Apache Cloudberry 文档中的[处理 JSON 数据](/cloudberry/reference/functions/json-functions-and-operators/)。


### 示例：将 HDFS 文本文件读入单个表行 {#example-reading-an-hdfs-text-file-into-a-single-table-row}

按以下步骤在 HDFS 目录中创建 3 个示例文本文件，并使用 PXF `hdfs:text:multi` Profile 和默认 PXF 服务器，通过一次外部表查询读取所有这些文本文件。


1. 为文本文件创建 HDFS 目录。例如：

    ```shell
    $ hdfs dfs -mkdir -p /data/pxf_examples/tdir
    ```

2. 创建名为 `file1.txt` 的文本数据文件：

    ```shell
    $ echo 'text file with only one line' > /tmp/file1.txt
    ```

3. 创建名为 `file2.txt` 的第二个文本数据文件：

    ```shell
    $ echo 'Prague,Jan,101,4875.33
    Rome,Mar,87,1557.39
    Bangalore,May,317,8936.99
    Beijing,Jul,411,11600.67' > /tmp/file2.txt
    ```

    该文件包含多行。

4. 创建名为 `/tmp/file3.txt` 的第三个文本文件：

    ```shell
    $ echo '"4627 Star Rd.
    San Francisco, CA  94107":Sept:2017
    "113 Moon St.
    San Diego, CA  92093":Jan:2018
    "51 Belt Ct.
    Denver, CO  90123":Dec:2016
    "93114 Radial Rd.
    Chicago, IL  60605":Jul:2017
    "7301 Brookview Ave.
    Columbus, OH  43213":Dec:2018' > /tmp/file3.txt
    ```

    该文件包含内嵌换行符。

5. 保存文件并退出编辑器。

6. 将文本文件复制到 HDFS：

    ```shell
    $ hdfs dfs -put /tmp/file1.txt /data/pxf_examples/tdir
    $ hdfs dfs -put /tmp/file2.txt /data/pxf_examples/tdir
    $ hdfs dfs -put /tmp/file3.txt /data/pxf_examples/tdir
    ```

7. 登录 Apache Cloudberry 系统并启动 `psql` 子系统。

8. 使用 `hdfs:text:multi` Profile 创建引用 HDFS 目录 `tdir` 的外部表。例如：

    ```sql
    CREATE EXTERNAL TABLE pxf_readfileasrow(c1 text)
      LOCATION ('pxf://data/pxf_examples/tdir?PROFILE=hdfs:text:multi&FILE_AS_ROW=true')
    FORMAT 'CSV';
    ```
    
9. 打开扩展显示并查询 `pxf_readfileasrow` 表：

    ```sql
    postgres=# \x on
    postgres=# SELECT * FROM pxf_readfileasrow;
    ```

    ```text
    -[ RECORD 1 ]---------------------------
    c1 | Prague,Jan,101,4875.33
       | Rome,Mar,87,1557.39
       | Bangalore,May,317,8936.99
       | Beijing,Jul,411,11600.67
    -[ RECORD 2 ]---------------------------
    c1 | text file with only one line
    -[ RECORD 3 ]---------------------------
    c1 | "4627 Star Rd.
       | San Francisco, CA  94107":Sept:2017
       | "113 Moon St.
       | San Diego, CA  92093":Jan:2018
       | "51 Belt Ct.
       | Denver, CO  90123":Dec:2016
       | "93114 Radial Rd.
       | Chicago, IL  60605":Jul:2017
       | "7301 Brookview Ave.
       | Columbus, OH  43213":Dec:2018
    ```
