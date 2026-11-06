---
title: "使用 s3 协议从 Amazon S3 加载数据"
linkTitle: "从 Amazon S3 加载数据"
description: "`s3` 协议用于 URL 中，指定 Amazon S3 存储桶的位置，以及读取或写入桶内文件时使用的前缀。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-from-s3.md"
---

Amazon Simple Storage Service（Amazon S3）提供安全、持久且高度可扩展的对象存储。有关 Amazon S3 的信息，请参阅 [Amazon S3](https://aws.amazon.com/s3/)。

你可以定义只读外部表，以 S3 存储桶中已有的数据文件作为表数据；也可以定义可写外部表，将 `INSERT` 操作的数据存储到 S3 存储桶的文件中。Apache Cloudberry 根据协议 URL 中指定的 S3 URL 和前缀，为只读表选择一个或多个文件，或者在向可写表执行 `INSERT` 操作时，确定上传 S3 文件所用的位置和文件名格式。

`s3` 协议还支持 [Dell Elastic Cloud Storage](https://www.dell.com/en-us/dt/learn/data-storage/ecs.htm)（ECS），这是一项兼容 Amazon S3 的服务。

> [!NOTE]
> `pxf` 协议可以访问 S3 以及 Azure、Google Cloud Storage、Minio 等其他对象存储系统中的数据。`pxf` 协议还可以访问外部 Hadoop 系统（HDFS、Hive、HBase）和 SQL 数据库中的数据。请参阅 [`pxf://` 协议](/cloudberry/data-loading/cloud/load-data-using-pxf/)。

## 配置 s3 协议 {#configure-the-s3-protocol}

使用 `s3` 协议之前，必须先配置该协议。在每个需要使用该协议的数据库中执行以下步骤：

1. 为 `s3` 协议库创建读取和写入函数：

    ```sql
    CREATE OR REPLACE FUNCTION write_to_s3() RETURNS integer AS
       '$libdir/gps3ext.so', 's3_export' LANGUAGE C STABLE;
    ```

    ```sql
    CREATE OR REPLACE FUNCTION read_from_s3() RETURNS integer AS
       '$libdir/gps3ext.so', 's3_import' LANGUAGE C STABLE;
    ```

2. 声明 `s3` 协议，并指定上一步创建的读取和写入函数：

    如果只允许 Apache Cloudberry 超级用户使用该协议，请按以下方式创建：

    ```sql
    CREATE PROTOCOL s3 (writefunc = write_to_s3, readfunc = read_from_s3);
    ```

    如果希望允许非超级用户使用 `s3` 协议，请将其创建为 `TRUSTED` 协议，并使用 `GRANT` 向这些用户授予访问权限。例如：

    ```sql
    CREATE TRUSTED PROTOCOL s3 (writefunc = write_to_s3, readfunc = read_from_s3);
    GRANT ALL ON PROTOCOL s3 TO user1, user2;
    ```

    > [!NOTE]
    > 为访问 S3 资源而创建外部表时，协议名称 `s3` 必须与为该表指定的 URL 中的协议一致。

    每个 Apache Cloudberry Segment 实例都会调用相应的函数。

## 使用 s3 外部表 {#use-s3-external-tables}

按照以下基本步骤，在 Apache Cloudberry 外部表中使用 `s3` 协议。各步骤包含相关主题的链接，可供进一步了解。

1. [配置 s3 协议](#configure-the-s3-protocol)。
2. 创建 `s3` 协议配置文件：

    1. 使用 `gpcheckcloud` 工具创建 `s3` 协议配置文件模板：

        ```shell
        gpcheckcloud -t > ./mytest_s3.config
        ```

    2. （可选）编辑模板文件，指定连接 S3 位置所需的 `accessid` 和 `secret` 认证凭据。

3. 如果 `s3` 协议配置文件位于每个 Segment 主机上，或由 `http/https` 服务器提供，Apache Cloudberry 就可以访问该文件。确定计划存放配置文件的位置，并记下该位置和配置选项（如适用）。

    如果使用 AWS 凭据文件进行认证，该文件必须位于每个 Apache Cloudberry Segment 主机的 `~/.aws/credentials` 路径。

4. 使用 `gpcheckcloud` 工具验证与 S3 存储桶的连通性。必须指定要检查的 S3 端点名称和存储桶。

    例如，如果 `s3` 协议配置文件位于默认位置，可以运行以下命令：

    ```shell
    gpcheckcloud -c "s3://<s3-endpoint>/<s3-bucket>"
    ```

    `gpcheckcloud` 会尝试连接 S3 端点，并列出 S3 存储桶中存在的文件（如果有）。连接成功时，最后会显示以下消息：

    ```
    Your configuration works well.
    ```

    你也可以使用 `gpcheckcloud` 验证向 S3 存储桶上传文件和从中下载文件的功能。

5. 在 `CREATE EXTERNAL TABLE` 命令的 `LOCATION` 子句中指定 `s3` 协议 URL，创建 s3 外部表。

### 创建可读 S3 外部表 {#create-a-readable-s3-external-table}

要从 S3 读取数据，请指定 S3 位置和文件匹配模式：

```sql
CREATE EXTERNAL TABLE sales_data (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('s3://s3-us-west-2.amazonaws.com/your-bucket/sales-data/ config=/path/to/s3.config')
FORMAT 'CSV' (HEADER);
```

### 创建可写 S3 外部表 {#create-a-writable-s3-external-table}

向 S3 写入数据：

```sql
CREATE WRITABLE EXTERNAL TABLE sales_export (LIKE sales_data)
LOCATION ('s3://s3-us-west-2.amazonaws.com/your-bucket/exports/ config=/path/to/s3.config')
FORMAT 'CSV'
DISTRIBUTED BY (transaction_id);
```

对于只读 s3 表，URL 定义位置和前缀，用于选择构成该 s3 表的已有数据文件。例如：

```sql
CREATE READABLE EXTERNAL TABLE S3TBL (date text, time text, amt int)
   LOCATION('s3://s3-us-west-2.amazonaws.com/s3test.example.com/dataset1/normal/ config=/home/gpadmin/aws_s3/s3.conf')
   FORMAT 'csv';
```

对于可写 s3 表，协议 URL 指定 Apache Cloudberry 在执行 `INSERT` 操作时写入表数据文件的 S3 位置。你还可以指定一个前缀，Apache Cloudberry 会将其添加到所创建文件的文件名中。例如：

```sql
CREATE WRITABLE EXTERNAL TABLE S3WRIT (LIKE S3TBL)
   LOCATION('s3://s3-us-west-2.amazonaws.com/s3test.example.com/dataset1/normal/ config=/home/gpadmin/aws_s3/s3.conf')
   FORMAT 'csv';
```

## 关于 s3 协议的 LOCATION URL {#about-the-s3-protocol-location-url}

使用 `s3` 协议时，在 `CREATE EXTERNAL TABLE` 命令的 `LOCATION` 子句中指定 S3 文件位置，以及可选的配置文件位置和区域参数。语法如下：

```
's3://<S3_endpoint>[:<port>]/<bucket_name>/[<S3_prefix>] [region=<S3_region>] [config=<config_file_location> | config_server=<url>] [section=<section_name>]'
```

`s3` 协议要求指定 S3 端点和 S3 存储桶名称。每个 Apache Cloudberry Segment 主机都必须能够访问该 S3 位置。可选的 S3_prefix 值用于为只读 S3 表选择文件，或用作可写 s3 表上传文件时的文件名前缀。

> [!NOTE]
> Apache Cloudberry 的 `s3` 协议 URL 必须包含 S3 端点的主机名。

要在 `LOCATION` 子句中指定 ECS 端点（兼容 Amazon S3 的服务），必须将 `s3` 协议配置文件中的 `version` 参数设置为 `2`。`version` 参数控制是否在 `LOCATION` 子句中使用 `region` 参数。当 `version` 参数为 2 时，也可以指定 Amazon S3 位置。

> [!NOTE]
> 虽然 S3_prefix 在语法上是可选的，但对于可写和只读 s3 表，都应在 `CREATE EXTERNAL TABLE` 语句中包含 S3 前缀，以区分不同的数据集。

对于可写 s3 表，`s3` 协议 URL 指定 Apache Cloudberry 为该表上传数据文件时所用的端点和存储桶名称。向表中插入数据时，上传到该 S3 位置的每个新文件都会使用 S3 文件前缀。

对于只读 s3 表，S3 文件前缀是可选的。如果指定 S3_prefix，`s3` 协议会选择所有以该前缀开头的文件作为外部表的数据文件。`s3` 协议不使用斜杠字符（`/`）作为分隔符，因此前缀后面的斜杠会被视为前缀本身的一部分。

例如，以下 5 个文件的 S3_endpoint 均为 `s3-us-west-2.amazonaws.com`，bucket_name 均为 `test1`：

```
s3://s3-us-west-2.amazonaws.com/test1/abc
s3://s3-us-west-2.amazonaws.com/test1/abc/
s3://s3-us-west-2.amazonaws.com/test1/abc/xx
s3://s3-us-west-2.amazonaws.com/test1/abcdef
s3://s3-us-west-2.amazonaws.com/test1/abcdefff
```

- 如果提供的 S3 URL 为 `s3://s3-us-west-2.amazonaws.com/test1/abc`，则 `abc` 前缀会选中全部 5 个文件。
- 如果提供的 S3 URL 为 `s3://s3-us-west-2.amazonaws.com/test1/abc/`，则 `abc/` 前缀会选中文件 `s3://s3-us-west-2.amazonaws.com/test1/abc/` 和 `s3://s3-us-west-2.amazonaws.com/test1/abc/xx`。
- 如果提供的 S3 URL 为 `s3://s3-us-west-2.amazonaws.com/test1/abcd`，则 `abcd` 前缀会选中文件 `s3://s3-us-west-2.amazonaws.com/test1/abcdef` 和 `s3://s3-us-west-2.amazonaws.com/test1/abcdefff`。

S3_prefix 不支持通配符；不过，S3 前缀的匹配效果如同在前缀之后紧接着一个通配符。

S3 URL（S3_endpoint/bucket_name/S3_prefix）选中的所有文件都用作外部表的数据源，因此它们必须具有相同的格式。每个文件还必须包含完整的数据行。一个数据行不能拆分到多个文件中。

使用 `config` 或 `config_server` 参数指定必需的 `s3` 协议配置文件的位置，该文件包含 AWS 连接凭据和通信参数。

使用 `section` 参数指定配置文件节的名称，`s3` 协议将从该节读取配置参数。默认 `section` 名称为 `default`。在配置文件中指定节名时，请将其放在方括号中（例如 `[default]`）。

## 进一步了解 {#learn-more}

- [Amazon S3 文档](https://aws.amazon.com/documentation/s3/)
- [AWS S3 端点](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region)
