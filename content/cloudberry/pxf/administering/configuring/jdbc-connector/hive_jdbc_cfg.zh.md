---
title: "配置用于 Hive 访问的 JDBC 连接器（可选）"
description: "配置用于 Hive 访问的 PXF JDBC 连接器。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/jdbc-connector/hive_jdbc_cfg.md"
---

你可以使用 PXF JDBC 连接器从 Hive 检索数据。你也可以使用 JDBC 命名查询向 Hive 提交自定义 SQL 查询，并通过 JDBC 连接器检索结果。

本主题介绍如何配置 PXF JDBC 连接器以访问 Hive。通过 JDBC 配置 Hive 访问时，必须考虑 Hive 用户模拟设置，以及 Hadoop 集群是否通过 Kerberos 保护。

*如果不打算使用 PXF JDBC 连接器访问 Hive，则无需执行此步骤。*


## JDBC 服务器配置 {#jdbc-server-configuration}

PXF JDBC 连接器安装时附带了通过 JDBC 访问 Hive 所需的 JAR 文件 `hive-jdbc-<version>.jar` 和 `hive-service-<version>.jar`，并会自动注册这些 JAR。

为 Hive 访问配置 PXF JDBC 服务器时，必须指定 JDBC 驱动类名、数据库 URL 和客户端凭据，就像配置到 SQL 数据库的客户端连接一样。

要通过 JDBC 访问 Hive，必须在 `jdbc-site.xml` 服务器配置文件中指定以下属性和值：

| 属性 |  值 |
|----------------|--------|
| jdbc.driver | org.apache.hive.jdbc.HiveDriver |
| jdbc.url | jdbc:hive2://\&lt;hiveserver2_host&gt;:\&lt;hiveserver2_port&gt;/\&lt;database&gt; |

HiveServer2 认证属性（`hive.server2.authentication`）和用户模拟属性（`hive.server2.enable.doAs`）的值，以及 Hive 服务是否使用 Kerberos 认证，将决定其他 JDBC 服务器配置属性的设置。这些属性定义在 Hadoop 集群的 `hive-site.xml` 配置文件中。你需要获取这些属性的值。

下表列举了 PXF JDBC 连接器支持的 Hive2 认证与用户模拟的组合。表中列出了可能的 Hive 用户身份，以及每种身份所需的 JDBC 服务器配置。

表头说明：

- *authentication* -> Hive `hive.server2.authentication` 设置
- *enable.doAs* -> Hive `hive.server2.enable.doAs` 设置
- *用户身份* -> HiveServer2 访问数据所使用的身份
- *所需配置* -> *用户身份*所需的 PXF JDBC 连接器或 Hive 配置

| authentication  |  enable.doAs | 用户身份 | 所需配置 |
|------------------|---------------|----------------|-------------------|
| `NOSASL` | 不适用 | 无认证 | 必须设置 `jdbc.connection.property.auth` = `noSasl`。  |
| `NONE`，或未指定 | `TRUE` | 你提供的用户名 | 设置 `jdbc.user`。 |
| `NONE`，或未指定 | `TRUE` | Apache Cloudberry 用户名 | 在 `jdbc-site.xml` 中将 `pxf.service.user.impersonation` 设置为 `true`。 |
| `NONE`，或未指定 | `FALSE` | 启动 Hive 的用户名，通常为 `hive`  | 无 |
| `KERBEROS` | `TRUE` | PXF Kerberos 主体中提供的身份，通常为 `gpadmin` | 必须在 `jdbc-site.xml` 中将 `hadoop.security.authentication` 设置为 `kerberos`。 |
| `KERBEROS` | `TRUE` | 你提供的用户名  | 在 `jdbc.url` 中设置 `hive.server2.proxy.user`，并在 `jdbc-site.xml` 中将 `hadoop.security.authentication` 设置为 `kerberos`。  |
| `KERBEROS` | `TRUE` | Apache Cloudberry 用户名  | 在 `jdbc-site.xml` 中将 `pxf.service.user.impersonation` 设置为 `true`，并将 `hadoop.security.authentication` 设置为 `kerberos`。 |
| `KERBEROS` | `FALSE` | `jdbc.url` 的 `principal` 参数中提供的身份，通常为 `hive` |  必须在 `jdbc-site.xml` 中将 `hadoop.security.authentication` 设置为 `kerberos`。 |

**注意**：当 Hive 使用 Kerberos 认证时，还需要额外的配置步骤。

## 配置示例步骤 {#example-configuration-procedure}

请执行以下步骤，为 Hive 配置 PXF JDBC 服务器：

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 为 JDBC 服务器选择一个名称。

3. 创建 `$PXF_BASE/servers/<server_name>` 目录。例如，使用以下命令创建名为 `hivejdbc1` 的 JDBC 服务器配置：

    ```shell
    gpadmin@coordinator$ mkdir $PXF_BASE/servers/hivejdbc1
    ````

3. 进入服务器配置目录。例如：

    ```shell
    gpadmin@coordinator$ cd $PXF_BASE/servers/hivejdbc1
    ```

4. 将 PXF JDBC 服务器模板文件复制到服务器配置目录。例如：

    ```shell
    gpadmin@coordinator$ cp <PXF_INSTALL_DIR>/templates/jdbc-site.xml .
    ```
        
4. 访问受 Kerberos 保护的 Hive 时，还需要在 `pxf-site.xml` 文件中指定配置属性。*如果服务器配置中尚不存在此文件*，请将 `pxf-site.xml` 模板文件复制到服务器配置目录。例如：

    ```shell
    gpadmin@coordinator$ cp <PXF_INSTALL_DIR>/templates/pxf-site.xml .
    ```
        
5. 在你选择的编辑器中打开 `jdbc-site.xml` 文件，并设置 `jdbc.driver` 和 `jdbc.url` 属性。请务必指定你的 Hive 主机、端口和数据库名称：

    ```xml
    <property>
        <name>jdbc.driver</name>
        <value>org.apache.hive.jdbc.HiveDriver</value>
    </property>
    <property>
        <name>jdbc.url</name>
        <value>jdbc:hive2://<hiveserver2_host>:<hiveserver2_port>/<database></value>
    </property>
    ```

6. 从 Hadoop 集群获取 `hive-site.xml` 文件并检查该文件。

7. 如果 `hive-site.xml` 中的 `hive.server2.authentication` 属性设置为 `NOSASL`，则 HiveServer2 不执行认证。请将以下连接级属性添加到 `jdbc-site.xml`：

    ```xml
    <property>
        <name>jdbc.connection.property.auth</name>
        <value>noSasl</value>
    </property>
    ```
    或者，你也可以选择将 `;auth=noSasl` 添加到 `jdbc.url`。

8. 如果 `hive-site.xml` 中的 `hive.server2.authentication` 属性设置为 `NONE`，或未指定该属性，则必须设置 `jdbc.user` 属性。`jdbc.user` 属性应设置的值取决于 `hive-site.xml` 中的 `hive.server2.enable.doAs` 用户模拟设置：

    1. 如果 `hive.server2.enable.doAs` 设置为 `TRUE`（默认），Hive 代表连接 Hive 的用户运行 Hadoop 操作。*请选择/执行以下选项之一*：

        **设置** `jdbc.user`，指定对 Apache Cloudberry 访问的所有 Hive 数据具有读权限的用户。例如，要连接 Hive 并以用户 `gpadmin` 身份运行所有请求：

        ```xml
        <property>
            <name>jdbc.user</name>
            <value>gpadmin</value>
        </property>
        ```
        **或者**，开启 JDBC 服务器级别的用户模拟，使 PXF 自动使用 Apache Cloudberry 用户名连接 Hive；取消 `jdbc-site.xml` 中 `pxf.service.user.impersonation` 属性的注释，并将值设置为 `true`：

        ```xml
        <property>
            <name>pxf.service.user.impersonation</name>
            <value>true</value>
        </property>
        ```
        如果以这种方式启用 JDBC 用户模拟，则不得指定 `jdbc.user`，也不得在 `jdbc.url` 中包含该设置。

    2. 如有需要，请按照[配置 PXF 用户](/cloudberry/pxf/administering/configuring/cfg_server/#configuring-a-pxf-user)中的说明创建 PXF 用户配置文件，以管理密码设置。
    3. 如果 `hive.server2.enable.doAs` 设置为 `FALSE`，Hive 以启动 HiveServer2 进程的用户（通常是用户 `hive`）身份运行 Hadoop 操作。在这种情况下，PXF 会忽略 `jdbc.user` 设置。

9. 如果 `hive-site.xml` 中的 `hive.server2.authentication` 属性设置为 `KERBEROS`：
    1. 确定服务器配置的名称。
    2. 确保已按照[为安全 HDFS 配置 PXF](/cloudberry/pxf/administering/configuring/hadoop-connectors/pxf_kerbhdfs/)中的说明为 PXF 配置了 Kerberos 认证，并已按该步骤的说明在 `pxf-site.xml` 属性中指定 Kerberos 主体和 keytab。
    3. 注释掉 `pxf-site.xml` 文件中的 `pxf.service.user.impersonation` 属性。如果需要用户模拟，将在后续步骤中取消注释并设置该属性。
    3. 取消 `$PXF_BASE/servers/<name>/jdbc-site.xml` 中 `hadoop.security.authentication` 设置的注释：

        ```xml
        <property>
            <name>hadoop.security.authentication</name>
            <value>kerberos</value>
        </property>
        ```
    4. 将 `saslQop` 属性添加到 `jdbc.url`，并将其设置为与 `hive-site.xml` 中的 `hive.server2.thrift.sasl.qop` 属性设置一致。例如，如果 `hive-site.xml` 文件包含以下属性设置：

        ```xml
        <property>
            <name>hive.server2.thrift.sasl.qop</name>
            <value>auth-conf</value>
        </property>
        ```
        则应将 `;saslQop=auth-conf` 添加到 `jdbc.url`。
       
    5. 将 HiverServer2 的 `principal` 名称添加到 `jdbc.url`。例如：

        ```text
        jdbc:hive2://hs2server:10000/default;principal=hive/hs2server@REALM;saslQop=auth-conf
        ```
    6. 如果 `hive.server2.enable.doAs` 设置为 `TRUE`（默认），Hive 代表连接 Hive 的用户运行 Hadoop 操作。*请选择/执行以下选项之一*：

        **不要**指定任何其他属性。在这种情况下，PXF 使用 PXF Kerberos 主体中提供的身份（通常是 `gpadmin`）发起所有 Hadoop 访问。

        **或者**，在 `jdbc.url` 中设置 `hive.server2.proxy.user` 属性，指定对所有 Hive 数据具有读权限的用户。例如，要连接 Hive 并以名为 `integration` 的用户身份运行所有请求，请使用以下 `jdbc.url`：

        ```text
        jdbc:hive2://hs2server:10000/default;principal=hive/hs2server@REALM;saslQop=auth-conf;hive.server2.proxy.user=integration
        ```

        **或者**，在 `pxf-site.xml` 文件中启用 PXF JDBC 用户模拟，使 PXF 自动使用 Apache Cloudberry 用户名连接 Hive。添加或取消注释 `pxf.service.user.impersonation` 属性，并将值设置为 `true`。例如：

        ```xml
        <property>
            <name>pxf.service.user.impersonation</name>
            <value>true</value>
        </property>
        ```
        如果启用了 JDBC 用户模拟，则不得在 `jdbc.url` 中显式指定 `hive.server2.proxy.user`。
    6. 如有需要，创建 PXF 用户配置文件以管理密码设置。
    7. 如果 `hive.server2.enable.doAs` 设置为 `FALSE`，Hive 使用 PXF Kerberos 主体提供的身份（通常是 `gpadmin`）运行 Hadoop 操作。

10. 保存更改并退出编辑器。

11. 使用 `pxf cluster sync` 命令，将新的服务器配置复制到 Apache Cloudberry 集群：
    
    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```
