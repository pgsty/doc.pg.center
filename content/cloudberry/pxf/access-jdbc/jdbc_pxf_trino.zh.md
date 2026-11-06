---
title: "示例：读写 Trino（原 Presto SQL）表"
description: "在 Trino 中使用 PXF JDBC。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-jdbc/jdbc_pxf_trino.md"
---

由于 PXF 通过 JDBC 连接器访问 Trino，因此本示例适用于所有受支持的 PXF 版本。

在本示例中，您将：

- 创建内存 Trino 表，并向表中插入数据
- 配置 PXF JDBC 连接器以访问 Trino 数据库
- 创建引用该 Trino 表的 PXF 可读外部表
- 使用 PXF 读取 Trino 表中的数据
- 创建引用该 Trino 表的 PXF 可写外部表
- 使用 PXF 向 Trino 表写入数据
- 再次读取 Trino 表中的数据

## 创建 Trino 表 {#create-a-trino-table}

本示例假定您的 Trino 服务器已配置自带的 `memory` 连接器。
有关配置该连接器的说明，请参阅 [Trino 文档 - Memory 连接器](https://trino.io/docs/current/connector/memory.html)。

创建名为 `names` 的 Trino 表，并向表中插入一些数据：

```sql
> CREATE TABLE memory.default.names(id int, name varchar, last varchar);
> INSERT INTO memory.default.names(1, 'John', 'Smith'), (2, 'Mary', 'Blake');
```

## 配置 Trino 连接器 {#configure-the-trino-connector}

您必须为 Trino 创建 JDBC 服务器配置，将 Trino 驱动程序 JAR 文件下载到您的系统，将该 JAR 文件复制到 PXF 用户配置目录，同步 PXF 配置，然后重启 PXF。

此过程通常由 Apache Cloudberry 管理员执行。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

1. 下载 Trino JDBC 驱动程序，并将其放置在 `$PXF_BASE/lib` 下。
   如果您[迁移了 $PXF_BASE](/cloudberry/pxf/administering/configuring/about_pxf_dir/#relocating-pxf_base)，请确保使用更新后的位置。
   有关下载 Trino JDBC 驱动程序的说明，请参阅 [Trino 文档 - JDBC 驱动程序](https://trino.io/docs/current/client/jdbc.html#installing)。
   下面的示例下载驱动程序，并将其放置在 `$PXF_BASE/lib` 下：

    1. 如果您没有迁移 `$PXF_BASE`，请在 Cloudberry Coordinator 上运行以下命令：

        ```shell
        gpadmin@coordinator$ cd /usr/local/cloudberry-pxf-<version>/lib
        gpadmin@coordinator$ wget <url-to-trino-jdbc-driver>
        ```

    2. 如果您迁移了 `$PXF_BASE`，请在 Cloudberry Coordinator 上运行以下命令：

        ```shell
        gpadmin@coordinator$ cd $PXF_BASE/lib
        gpadmin@coordinator$ wget <url-to-trino-jdbc-driver>
        ```

1. 同步 PXF 配置，然后重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    gpadmin@coordinator$ pxf cluster restart
    ```

1. 按照[示例配置过程](/cloudberry/pxf/administering/configuring/jdbc-connector/#example-configuration-procedure)中的说明为 Trino 创建 JDBC 服务器配置，并将服务器目录命名为 `trino`。
   `jdbc-site.xml` 文件的内容应与下面类似（请将 `trinoserverhost` 替换为您的 Trino 主机系统）：

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <property>
            <name>jdbc.driver</name>
            <value>io.trino.jdbc.TrinoDriver</value>
            <description>Class name of the JDBC driver</description>
        </property>
        <property>
            <name>jdbc.url</name>
            <value>jdbc:trino://trinoserverhost:8443</value>
            <description>The URL that the JDBC driver can use to connect to the database</description>
        </property>
        <property>
            <name>jdbc.user</name>
            <value>trino-user</value>
            <description>User name for connecting to the database</description>
        </property>
        <property>
            <name>jdbc.password</name>
            <value>trino-pw</value>
            <description>Password for connecting to the database</description>
        </property>

        <!-- Connection properties -->
        <property>
            <name>jdbc.connection.property.SSL</name>
            <value>true</value>
            <description>Use HTTPS for connections; authentication using username/password requires SSL to be enabled.</description>
        </property>
    </configuration>
    ```

1. 如果您的 Trino 服务器配置了[全球信任证书](https://trino.io/docs/current/security/tls.html#add-a-tls-certificate)，可以跳过此步骤。如果您的 Trino 服务器配置为使用企业信任证书或生成的自签名证书，PXF 需要一份该服务器证书的副本，格式为 PEM 编码文件或 Java 密钥库（JKS）文件。
 
    **注意：** 您不需要 Trino 服务器的私钥。

    将证书复制到 `$PXF_BASE/servers/trino`；将服务器证书存放在 `$PXF_BASE/servers/trino` 内，可确保 `pxf cluster sync` 将证书复制到所有 Segment 主机。

    ```shell
    $ cp <path-to-trino-server-certificate> /usr/local/cloudberry-pxf-<version>/servers/trino
    ```

    将以下连接属性添加到您在上一步中创建的 `jdbc-site.xml` 文件中。其中 `trino.cert` 是您复制到 `$PXF_BASE/servers/trino` 中的证书文件的名称：

    ```xml
    <configuration>
    ...
        <property>
            <name>jdbc.connection.property.SSLTrustStorePath</name>
            <value>/usr/local/cloudberry-pxf-<version>/servers/trino/trino.cert</value>
            <description>The location of the Java TrustStore file that will be used to validate HTTPS server certificates.</description>
        </property>
        <!-- the following property is only required if the server's certificate is stored in a JKS file; if using a PEM-encoded file, it should be omitted.-->
        <!--
        <property>
            <name>jdbc.connection.property.SSLTrustStorePassword</name>
            <value>java-keystore-password</value>
            <description>The password for the TrustStore.</description>
        </property>
        -->
    </configuration>
    ```

1. 将 PXF 服务器配置同步到 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

## 读取 Trino 表 {#read-from-a-trino-table}

执行以下步骤，创建引用 `names` Trino 表的 PXF 外部表，并读取该表中的数据：

1. 指定 `jdbc` Profile 创建 PXF 外部表。
   在 `LOCATION` URL 中指定 Trino 的 catalog 和模式。下面的示例读取位于 `memory` catalog 的 `default` 模式中的 `names` 表：

    ```sql
    CREATE EXTERNAL TABLE pxf_trino_memory_names (id int, name text, last text)
    LOCATION('pxf://memory.default.names?PROFILE=jdbc&SERVER=trino')
    FORMAT 'CUSTOM' (formatter='pxfwritable_import');
    ```
    或者创建外表
    ```sql
    CREATE SERVER "trino" FOREIGN DATA WRAPPER jdbc_pxf_fdw;
    CREATE USER MAPPING FOR CURRENT_USER SERVER "trino";
    CREATE FOREIGN TABLE pxf_trino_memory_names (id int, name text, last text)
		SERVER "trino"
		OPTIONS ( resource 'memory.default.names' );
    ```

1. 显示 `pxf_trino_memory_names` 表的所有行：

    ```sql
    gpadmin=# SELECT * FROM pxf_trino_memory_names;
     id | name | last
    ----+------+-------
      1 | John | Smith
      2 | Mary | Blake
    (2 rows)
    ```

## 写入 Trino 表 {#write-to-the-trino-table}

执行以下步骤，向 `names` Trino 表中插入一些数据，然后从该表读取。
您必须为写操作创建新的外部表。

1. 指定 `jdbc` Profile 创建 PXF 可写外部表。例如：

    ```sql
    gpadmin=# CREATE WRITABLE EXTERNAL TABLE pxf_trino_memory_names_w (id int, name text, last text)
              LOCATION('pxf://memory.default.names?PROFILE=jdbc&SERVER=trino')
              FORMAT 'CUSTOM' (formatter='pxfwritable_export');
    ```
    或者复用前面步骤中创建的外表

1. 向 `pxf_trino_memory_names_w` 表中插入一些数据。例如：

    ```sql
    gpadmin=# INSERT INTO pxf_trino_memory_names_w VALUES (3, 'Muhammad', 'Ali');
    ```

1. 使用您在上一节中创建的 `pxf_trino_memory_names` 可读外部表，查看 `names` Trino 表中的新数据：

    ```sql
    gpadmin=# SELECT * FROM pxf_trino_memory_names;
     id |   name   | last
    ----+----------+-------
      1 | John     | Smith
      2 | Mary     | Blake
      3 | Muhammad | Ali
    (3 rows)
    ```
