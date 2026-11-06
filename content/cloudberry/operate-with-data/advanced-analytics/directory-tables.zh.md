---
title: "目录表"
description: "Apache Cloudberry 引入了*目录表*，用于统一管理本地存储或对象存储中的非结构化数据。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/advanced-analytics/directory-tables.md"
---

在大规模 AI 的背景下，AI 应用产生了管理非结构化多模态语料库的需求。人们需要持续准备大量经过高质量整理的非结构化语料，通过数据迭代训练大模型，并汇总丰富的知识库。因此，结构化语料的管理和处理面临技术挑战。

为应对这些挑战，Apache Cloudberry 引入目录表来管理多种非结构化数据。开发者用户可以使用简单的 SQL 语句，利用多个计算引擎的能力，实现一站式数据处理和应用开发。

目录表存储、管理和分析非结构化数据对象。目录表位于表空间中。导入非结构化数据文件时，系统会创建一条目录表记录（文件元数据），并将文件本身加载到对象存储中。表元数据仍与相应的对象存储文件关联。

## 用法 {#usage}

> [!NOTE]
> 当前，目录表不支持扩容或缩容。

### 创建目录表 {#create-a-directory-table}

可以在本地表空间中，或在外部存储的表空间中创建目录表；外部存储可以是对象存储服务或 HDFS 等分布式文件系统。

#### 在本地存储中创建 {#create-in-local-storage}

要在本地存储中创建目录表，请使用下面的 SQL 语法。需要将 `<table_name>` 和 `<tablespace_name>` 替换为实际的表名和表空间名。

```sql
-- Method 1: To create a directory table in a tablespace other than the default one,
-- create the tablespace first and then create the directory table within that tablespace.
CREATE TABLESPACE <tablespace_name>
       LOCATION '<tablespace_path>';

CREATE DIRECTORY TABLE <table_name>
       TABLESPACE <tablespace_name>;


-- Method 2: To create a directory table in the default tablespace, simply omit the TABLESPACE clause.
CREATE DIRECTORY TABLE <table_name>;
```

#### 在外部存储中创建 {#create-in-external-storage}

要在外部存储中创建目录表，首先需要在该存储中创建表空间。需要提供外部存储服务器的连接信息，例如服务器 IP 地址、协议和访问凭据。下面的示例展示如何在 QingCloud 对象存储和 HDFS 上创建目录表。

1. 创建服务器对象，并为外部数据源定义连接方式。Apache Cloudberry 支持多种存储选项的协议，包括 S3 对象存储和 HDFS。下面的示例分别在 QingCloud 和 HDFS 上创建名为 `oss_server` 和 `hdfs_server` 的服务器对象。

    - 对于 QingCloud：

        ```sql
        CREATE STORAGE SERVER oss_server OPTIONS(protocol 'qingstor', prefix '<path prefix>', endpoint '<endpoint address>', https 'true', virtual_host 'false');
        ```

    - 对于 HDFS：

        ```sql
        CREATE STORAGE SERVER hdfs_server OPTIONS(protocol 'hdfs', namenode '<HDFS node IP:port>', https 'false');
        ```

    上述命令中的参数说明如下：

    - `protocol`：用于连接外部数据源的协议。在上面的示例中，`'qingstor'` 表示使用 QingCloud 对象存储服务协议，`'hdfs'` 表示使用 HDFS 存储服务协议。
    - `prefix`：访问对象存储时设置路径前缀。如果设置了该前缀，所有操作都会限制在此特定路径下，例如 `prefix '/rose-oss-test4/usf1'`。通常使用它来组织和隔离存储在同一存储桶中的数据。
    - `endpoint`：指定外部对象存储服务的网络地址。例如，`'pek3b.qingstor.com'` 是 QingCloud 服务的一个特定区域节点。Apache Cloudberry 通过该端点访问外部数据。
    - `https`：指定是否使用 HTTPS 协议连接对象存储服务。在此命令中，`'false'` 表示使用未加密的 HTTP 连接。此设置可能受数据传输安全要求影响，通常建议使用 HTTPS 以确保数据安全。
    - `virtual_host`：确定是否使用虚拟主机访问存储桶。`'false'` 表示不使用虚拟主机方式访问存储桶（即 URL 中不包含存储桶名称）。此选项通常取决于存储服务提供商对 URL 格式的支持。
    - `namenode`：表示 HDFS 节点的 IP 地址。需要将 `<HDFS node IP:port>` 替换为实际 IP 地址和端口号，例如 `'192.168.51.106:8020'`。

2. 创建用户映射，为当前用户提供访问这些外部服务器所需的身份验证信息。

    - 对于 QingCloud：

        ```sql
        CREATE STORAGE USER MAPPING FOR CURRENT_USER STORAGE SERVER oss_server OPTIONS (accesskey '<QingCloud access key>', secretkey '<QingCloud secret key>');
        ```

    - 对于 HDFS：

        ```sql
        CREATE STORAGE USER MAPPING FOR CURRENT_USER STORAGE SERVER hdfs_server OPTIONS (auth_method 'simple');
        ```

    上述命令中的参数说明如下：

    - `accesskey` 和 `secretkey`：这些参数提供必要的身份验证信息。`'accesskey'` 和 `'secretkey'` 类似于用户名和密码，用于访问对象存储服务。

    - `auth_method`：表示访问 HDFS 的身份验证方法。`simple` 表示简单身份验证模式，`kerberos` 表示使用 Kerberos 身份验证模式。

3. 在外部服务器上创建表空间。这些表空间专门与之前定义的外部服务器关联，表空间的 `location` 选项指定外部存储上的特定路径。下面的示例分别在 QingCloud 和 HDFS 上创建 `dir_oss` 和 `dir_hdfs` 表空间。

    - 对于 QingCloud：

        ```sql
        CREATE TABLESPACE dir_oss location '<object_storage_path>' SERVER oss_server HANDLER '$libdir/dfs_tablespace, remote_file_handler';

        -- You need to replace <object_storage_path> with the actual path on the object storage, such as /tbs-49560-0-mgq-multi/oss-server-01-17.
        ```

    - 对于 HDFS：

        ```sql
        CREATE TABLESPACE dir_hdfs location '<object_storage_path>' SERVER hdfs_server HANDLER '$libdir/dfs_tablespace, remote_file_handler';

        -- You need to replace <object_storage_path> with the actual path on the object storage, such as /tbs-49560-0-mgq-multi/oss-server-01-17.
        ```

4. 在这些表空间中创建目录表。下面的语句分别在 `dir_oss` 和 `dir_hdfs` 表空间中创建 `dir_table_oss` 和 `dir_table_hdfs` 目录表。

    ```sql
    CREATE DIRECTORY TABLE dir_table_oss TABLESPACE dir_oss;
    CREATE DIRECTORY TABLE dir_table_hdfs TABLESPACE dir_hdfs;
    ```

    > [!TIP]
    > 如果创建表空间时遇到错误消息 `directory ... does not exist`，需要为集群配置 `shared_preload_libraries`，然后将该库导入对象存储。请按以下步骤操作：
    >
    > 1. 执行命令 `gpconfig -c shared_preload_libraries -v 'dfs_tablespace'` 配置集群。
    > 2. 使用命令 `gpstop -ra` 重启集群。

### 查看目录表的字段信息 {#view-the-field-information-of-directory-table}

```sql
\dY    -- Lists all the directory tables.
\d <directory_table>    -- Shows the field information of a directory table.
```

目录表通常包含以下字段：

| **字段名**      | **数据类型**    | 备注                                                                       |
| --------------- | --------------- | ------------------------------------------------------------------------------ |
| `RELATIVE_PATH` | `TEXT`          |                                                                                |
| `SIZE`          | `NUMBER`        |                                                                                |
| `LAST_MODIFIED` | `TIMESTAMP_LTZ` |                                                                                |
| `MD5`           | `HEX`           |                                                                                |
| `TAGS`          | `JSONB`         | 用户自定义标签。可用于标记数据血缘、文件上传部门或团队、分类。“k1=v1, k2=v2” |

### 将文件上传到目录表 {#upload-file-into-directory-table}

将文件上传到目录表后，Apache Cloudberry 会管理文件向本地存储或对象存储的上传，并将文件元数据存储在目录表中。在 Apache Cloudberry 中，用户不能直接管理对象存储目录中的文件。

将文件从本地存储上传到数据库对象存储：

```sql
\COPY '<directory_table_name>' FROM '<local_path_to_file> <target_path>';
COPY '<directory_table_name>' FROM '<local_path_to_file> <target_path>';  -- Optionally omits the starting slash \

-- <directory_table_name> is the directory table name.
-- <local_path_to_file> is the local path to the file to be uploaded.
-- <target_path> is the target path to the local or object storage, and the file will be uploaded to this path.
```

> [!TIP]
> 建议使用 `<path>` 的子目录功能，以确保上传后的目录路径与本地路径一致，从而简化文件管理。

为了加强文件管理和数据流跟踪，可以在上传命令中添加标签。这些标签可以为文件提供其他信息或标记。

```sql
\COPY '<directory_table_name>' FROM '<local_path_to_file>' '<target_path>' WITH tag '<tag_name>';
```

示例：

```sql
-- Uploads the file to the root path.
\COPY BINARY dir_table_oss FROM '/data/country.data' 'country.data';

-- Uploads the file to a specified path top_level/second_level
\COPY BINARY dir_table_oss FROM '/data/region.tbl' 'top_level/second_level/region.tbl';

-- Uploads the file to the root path with a tag
\COPY BINARY dir_table_oss FROM '/data/country1.data' 'country1.data' with tag 'country';

-- Uploads the file to a specified path top_level/second_level with a tag
\COPY BINARY dir_table_oss FROM '/data/region1.tbl' 'top_level/second_level/region1.tbl' with tag 'region';
```

还可以使用命令行工具 `cbload` 将文件批量上传到对象存储。使用语法 `cbload --inputfile <directory>` 将目录中的文件上传到对象存储。`cbload` 的命令行标志如下：

```shell
Usage:
  cbload [flags]

Flags:
      --database string       Database to connect to (default gpadmin)
      --dest-path string      Path relative to the table root directory (default: root directory of the table)
      --force-password-auth   Force a password prompt (default false)
      --help                  Print help info and exit
      --host string           Host to connect to (default localhost)
      --input-file strings    Input files or directory
      --logfile string        Log output to logfile (default none)
      --port int              Port to connect to (default 5432)
      --stop-on-error         Stop loading files when an error occurs (default false)
      --table string          Table to load to
      --tag string            File tag
      --tasks int             The maximum number of files that concurrently loads (default 1)
      --user string           User to connect as (default gpadmin)
      --verbose               Indicates that the tool should generate verbose output (default false)
      --version               Print version info and exit
```

### 查询和使用目录表管理的文件 {#query-and-use-the-files-managed-by-directory-table}

查询目录表中文件的元数据：

```sql
-- Uses the table function directory_table() to read the file metadata and content.
SELECT relative_path, 
       size, 
       last_modified, 
       md5,
       tag,
       content
       FROM directory_table('<directory_table>');

-- You can use one of the following statements to query the data of a directory table.
SELECT * FROM <directory_table>;
SELECT * FROM DIRECTORY_TABLE('<directory_table>');
```

### 删除目录表管理的文件 {#delete-the-file-managed-by-directory--table}

要删除目录表管理的文件，需要管理员权限：

```sql
SELECT remove_file('dir_table_oss', 'country.data');

-- This command deletes the file country.data managed in the table dir_table_oss.
```

### 删除目录表 {#delete-a-directory-table}

删除目录表。删除后，该表管理的所有文件也会被删除。要删除目录表，需要管理员权限。

```sql
DROP DIRECTORY TABLE <table_name>;
```
