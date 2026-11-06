---
title: "访问网络文件系统中的文件"
linkTitle: "使用 PXF 访问网络文件系统中的文件"
description: "使用 PXF 访问网络文件系统中的文件。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-nfs/nfs_pxf.md"
---

您可以使用 PXF 读取位于已挂载到 Apache Cloudberry 主机上的网络文件系统中的数据。PXF 支持对网络文件系统中的以下文件类型进行读取和写入：

| 文件类型 | Profile 名称 | 支持的操作 |
|-------------|--------------|------------|
| 以分隔符分隔的单行文本 | file:text | 读、写 |
| 以逗号分隔的单行文本值 | file:csv | 读、写 |
| 含带引号换行符的分隔文本 | file:text:multi | 读 |
| 定宽单行文本 | file:fixedwidth | 读、写 |
| Avro | file:avro | 读、写 |
| JSON | file:json | 读、写 |
| ORC | file:orc | 读、写 |
| Parquet | file:parquet | 读、写 |

访问网络文件系统时，PXF 不支持用户模拟。PXF 以启动 PXF 进程的操作系统用户（通常为 `gpadmin`）的身份访问文件。

> <b>注意：</b>在网络文件系统上读取这些类型的文件（以及在支持的情况下写入）与在 Hadoop 上读写该文件类型类似。


## 前提条件 {#prerequisites}

在使用 PXF 访问网络文件系统中的文件之前，请确保：

- 您能够确定 PXF 运行时配置目录（`$PXF_BASE`）。
- 您已经配置了 PXF，并且 PXF 正在每台 Apache Cloudberry 主机上运行。更多信息请参见[配置 PXF](/cloudberry/pxf/administering/configuring/)。
- 所有文件都可以由 `gpadmin` 或启动 PXF 进程的操作系统用户访问。
- 网络文件系统已在每台 Apache Cloudberry 主机上正确挂载到相同的本地挂载点。
- 您能够确定网络文件系统的挂载点或共享点。
- 您已经按照[配置 PXF 网络文件系统服务器](#configuring-a-pxf-network-file-system-server)中的说明，创建了一个或多个具名的 PXF 服务器配置。

## 配置 PXF 网络文件系统服务器 {#configuring-a-pxf-network-file-system-server}

在使用 PXF 访问网络文件系统中的文件之前，必须创建服务器配置，然后将 PXF 配置同步到所有 Apache Cloudberry 主机。此过程通常由 Apache Cloudberry 管理员执行。

配置 PXF 的网络文件系统服务器时，请使用服务器模板配置文件 `<PXF_INSTALL_DIR>/templates/pxf-site.xml`。该模板文件包含必需属性 `pxf.fs.basePath`，您需要配置该属性以指明网络文件系统的共享路径。对于使用该服务器的 `CREATE EXTERNAL TABLE` `LOCATION` 子句，PXF 将其中指定的文件路径视为相对于此共享路径。

访问网络文件系统时，PXF 不支持用户模拟；您必须在网络文件系统服务器配置中显式关闭用户模拟。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 为文件系统服务器选择一个名称。您需要将该名称提供给被允许读取或写入网络文件系统中文件的 Apache Cloudberry 用户。

    **注意**：服务器名称 `default` 为保留名称。

3. 创建 `$PXF_BASE/servers/<server_name>` 目录。例如，使用以下命令创建名为 `nfssrvcfg` 的文件系统服务器配置：

    ```shell
    gpadmin@coordinator$ mkdir $PXF_BASE/servers/nfssrvcfg
    ````

4. 将 PXF 的 `pxf-site.xml` 模板文件复制到 `nfssrvcfg` 服务器配置目录。例如：

    ```shell
    gpadmin@coordinator$ cp <PXF_INSTALL_DIR>/templates/pxf-site.xml $PXF_BASE/servers/nfssrvcfg/
    ```

5. 在您选择的编辑器中打开模板服务器配置文件，取消注释并提供适合您环境的属性值。例如，如果文件系统共享点是名为 `/mnt/extdata/pxffs` 的目录，请取消注释并设置以下服务器属性：

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
    ...
        <property>
            <name>pxf.service.user.impersonation</name>
            <value>false</value>
        </property>

        <property>
            <name>pxf.fs.basePath</name>
            <value>/mnt/extdata/pxffs</value>
        </property>
    ...
    </configuration>
    ```

6. 保存更改并退出编辑器。

7. 将 PXF 服务器配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ``` 

## 创建外部表 {#creating-the-external-table}

以下语法创建引用网络文件系统中文件的 Apache Cloudberry 外部表。请根据要访问的文件类型使用相应的 `file:*` Profile。

<pre>
CREATE [READABLE | WRITABLE] EXTERNAL TABLE &lt;table_name>
    ( &lt;column_name> &lt;data_type> [, ...] | LIKE &lt;other_table> )
LOCATION ('pxf://&lt;file-path>?PROFILE=file:&lt;file-type>[&SERVER=&lt;server_name>][&&lt;custom-option>=&lt;value>[...]]')
FORMAT '[TEXT|CSV|CUSTOM]' (&lt;formatting-properties>);
</pre>


下表说明 Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 命令中使用的关键字和取值。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<file&#8209;path\>    | 网络文件系统上目录或文件的路径。PXF 将该文件或路径视为相对于 \<server_name\> 服务器配置中指定的 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性值。\<file&#8209;path\> 不得指定相对路径，也不得包含美元符号（`$`）字符。 |
| PROFILE    | `PROFILE` 关键字的值必须指定为上表中列出的某个 `file:<file-type>`。 |
| SERVER=\<server_name\>   | PXF 用于访问网络文件系统的具名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| \<custom&#8209;option\>=\<value\>  | \<custom-option\> 取决于具体 Profile。|
| FORMAT&nbsp;\<value\>| PXF Profile 支持 `TEXT`、`CSV` 和 `CUSTOM` 格式。  |
| \<formatting&#8209;properties\> | Profile 支持的格式化属性；例如 `FORMATTER` 或 `delimiter`。 |

> <b>注意：</b>访问网络文件系统中的文件时，您指定的 &lt;custom-option>、FORMAT 和 &lt;formatting&#8209;properties> 取决于 &lt;file-type>。有关这些设置，请参阅与所需 &lt;file-type> 对应的 <a href="/cloudberry/pxf/access-hadoop/#connectors-data-formats-and-profiles">Hadoop 文档</a>。

## 示例：读写网络文件系统中的 CSV 文件 {#example-reading-from-and-writing-to-a-csv-file-on-a-network-file-system}

本示例假定您已在 Apache Cloudberry Coordinator 主机、Standby Coordinator 主机以及每台 Segment 主机上配置并挂载了共享点为 `/mnt/extdata/pxffs` 的网络文件系统。

在本示例中，您将：

- 在网络文件系统上创建 CSV 文件并向文件中添加数据。
- 为该共享点配置网络文件系统服务器。
- 创建引用包含该 CSV 文件的目录的 PXF 可读外部表，并读取数据。
- 创建引用包含该 CSV 文件的目录的 PXF 可写外部表，并写入一些数据。
- 再次从最初的可读外部表读取。


### 创建 CSV 文件 {#create-a-csv-file}

1.  创建名为 `/mnt/extdata/pxffs/ex1` 的目录（相对于网络文件系统共享点）：

    ```shell
    gpadmin@coordinator$ mkdir -p /mnt/extdata/pxffs/ex1
    ````

2. 在该目录中创建名为 `somedata.csv` 的 CSV 文件：

    ```shell
    $ echo 'Prague,Jan,101,4875.33
    Rome,Mar,87,1557.39
    Bangalore,May,317,8936.99
    Beijing,Jul,411,11600.67' > /mnt/extdata/pxffs/ex1/somedata.csv
    ```

### 创建网络文件系统服务器 {#create-the-network-file-system-server}

按照[配置 PXF 网络文件系统服务器](#configuring-a-pxf-network-file-system-server)中的说明，创建共享点为 `/mnt/extdata/pxffs`、名为 `nfssrvcfg` 的服务器配置。


### 读取数据 {#read-data}

执行以下步骤，创建引用您在前面小节中创建的 `ex1` 目录的 PXF 外部表，然后读取该目录中 `somedata.csv` 文件的数据：

1. 创建引用 `ex1` 并指定 `file:text` Profile 的 PXF 外部表。例如：

    ```sql
    gpadmin=# CREATE EXTERNAL TABLE pxf_read_nfs(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://ex1/?PROFILE=file:text&SERVER=nfssrvcfg')
                FORMAT 'CSV';
    ```

    由于 `nfssrvcfg` 服务器配置的 `pxf.fs.basePath` 属性值为 `/mnt/exdata/pxffs`，PXF 会构造路径 `/mnt/extdata/pxffs/ex1` 来读取文件。

2. 显示 `pxf_read_nfs` 表的所有行：

    ```sql
    gpadmin=# SELECT * FROM pxf_read_nfs ORDER BY num_orders DESC;
     location  | month | num_orders | total_sales 
    -----------+-------+------------+-------------
     Beijing   | Jul   |        411 |    11600.67
     Bangalore | May   |        317 |     8936.99
     Prague    | Jan   |        101 |     4875.33
     Rome      | Mar   |         87 |     1557.39
    (4 rows)
    ```

### 写入数据并再次读取 {#write-data-and-read-again}

执行以下步骤，向 `ex1` 目录中插入一些数据，然后再次读取数据。您必须为写操作创建新的外部表。

1. 创建引用 `ex1` 并指定 `file:text` Profile 的 PXF 可写外部表。例如：

    ```sql
    gpadmin=# CREATE WRITABLE EXTERNAL TABLE pxf_write_nfs(location text, month text, num_orders int, total_sales float8)
                LOCATION ('pxf://ex1/?PROFILE=file:text&SERVER=nfssrvcfg')
              FORMAT 'CSV' (delimiter=',');
    ```

4. 向 `pxf_write_nfs` 表中插入一些数据。例如：

    ```sql
    gpadmin=# INSERT INTO pxf_write_nfs VALUES ( 'Frankfurt', 'Mar', 777, 3956.98 );
    INSERT 0 1
    gpadmin=# INSERT INTO pxf_write_nfs VALUES ( 'Cleveland', 'Oct', 3812, 96645.37 );
    INSERT 0 1
    ```

    向 `pxf_write_nfs` 表插入数据时，PXF 会向 `ex1/` 目录写入一个或多个文件。

5. 使用您在上一节中创建的 `pxf_read_nfs` 可读外部表，查看您插入 `pxf_write_nfs` 表中的新数据：

    ```sql
    gpadmin=# SELECT * FROM pxf_read_nfs ORDER BY num_orders DESC;
     location  | month | num_orders | total_sales 
    -----------+-------+------------+-------------
     Cleveland | Oct   |       3812 |    96645.37
     Frankfurt | Mar   |        777 |     3956.98
     Beijing   | Jul   |        411 |    11600.67
     Bangalore | May   |        317 |     8936.99
     Prague    | Jan   |        101 |     4875.33
     Rome      | Mar   |         87 |     1557.39
    (6 rows)
    ```

    此处从 `pxf_read_nfs` 表查询时，PXF 会读取 `somedata.csv` 文件以及上一步中添加到 `ex1/` 目录的新文件。

## 关于指定 Parquet 模式文件位置 {#about-specifying-a-parquet-schema-file-location}

如果您使用 `file:parquet` Profile 写入引用 Parquet 文件的外部表，并希望提供 Parquet 模式，请在创建可写外部表时在 `LOCATION` 子句中指定 `SCHEMA` 自定义选项。有关创建外部表时可用选项的更多信息，请参阅 PXF HDFS Parquet 文档中的[创建外部表](/cloudberry/pxf/access-hadoop/hdfs_parquet/#creating-the-external-table)一节。

您必须将 `SCHEMA` 设置为 Parquet 模式文件在指定 `SERVER=<server_name>` 的文件系统上的位置。当 `<server_name>` 配置包含 [`pxf.fs.basePath`](/cloudberry/pxf/administering/configuring/cfg_server/#about-the-pxffsbasepath-property) 属性设置时，PXF 将您指定的模式文件视为相对于所指定的挂载点。
