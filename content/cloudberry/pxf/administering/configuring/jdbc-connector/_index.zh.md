---
title: "配置 JDBC 连接器（可选）"
description: "配置 PXF JDBC 连接器。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/jdbc-connector/jdbc_cfg.md"
---

您可以使用 PXF 访问外部 SQL 数据库，包括 MySQL、ORACLE、Microsoft SQL Server、DB2、PostgreSQL、Hive 和 Apache Ignite。本主题介绍如何配置 PXF JDBC 连接器以访问这些外部数据源。

*如果您不打算使用 PXF JDBC 连接器，则无需执行此过程。*

## 关于 JDBC 配置 {#about-jdbc-configuration}

要使用 PXF JDBC 连接器访问外部 SQL 数据库中的数据，您必须：

- 注册兼容的 JDBC 驱动程序 JAR 文件
- 指定 JDBC 驱动程序类名、数据库 URL 和客户端凭据

您可以通过两种方式之一提供 JDBC 驱动程序类名、数据库 URL 和客户端凭据：作为 `CREATE EXTERNAL TABLE`/`CREATE SERVER` 命令中的选项，或在 JDBC 连接器的基于文件的 PXF 服务器配置中提供。以下各节介绍基于文件的方式。

## JDBC 驱动程序 JAR 注册 {#jdbc-driver-jar-registration}

PXF 自带 `postgresql-42.7.2.jar` JAR 文件。如果您需要其他 JDBC 驱动程序，请确保在每台 Apache Cloudberry 主机的 `$PXF_BASE/lib` 目录中安装外部 SQL 数据库对应的 JDBC 驱动程序 JAR 文件。请务必安装与您的 JRE 版本兼容的 JDBC 驱动程序 JAR 文件。更多信息请参见[注册 PXF 库依赖项](/cloudberry/pxf/administering/reg_jar_depend/)。

## JDBC 服务器配置 {#jdbc-server-configuration}

配置 PXF JDBC 连接器时，您需要按照[配置 PXF 服务器](/cloudberry/pxf/administering/configuring/cfg_server/)中的说明，为该连接器至少添加一个具名的 PXF 服务器配置。您还可以配置一个或多个静态定义的查询，使其在远程 SQL 数据库上运行。

PXF 为 JDBC 连接器提供了一个模板配置文件。该服务器模板配置文件位于 `<PXF_INSTALL_DIR>/templates/jdbc-site.xml`，其中列出了可用于建立到外部 SQL 数据库连接的属性。该模板还包含可选属性，您可以在外部数据库会话中运行查询或插入命令之前设置这些属性。

`jdbc-site.xml` 服务器模板文件中的必需属性如下：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| jdbc.driver | JDBC 驱动程序的类名。 | JDBC 驱动程序的 Java 类名；例如 `org.postgresql.Driver`。 |
| jdbc.url | JDBC 驱动程序用于连接数据库的 URL。 | 数据库连接 URL（因数据库而异）；例如 `jdbc:postgresql://phost:pport/pdatabase`。 |
| jdbc.user | 数据库用户名。 | 用于连接数据库的用户名。 |
| jdbc.password | `jdbc.user` 的密码。 | 用于连接数据库的密码。 |

> <b>注意：</b>配置 PXF JDBC 服务器时，您需要在配置文件中以明文形式向 PXF 指定外部数据库的用户凭据。

### 连接级属性 {#connection-level-properties}

要设置其他 JDBC 连接级属性，请将 `jdbc.connection.property.<CPROP_NAME>` 属性添加到 `jdbc-site.xml`。PXF 在建立到外部 SQL 数据库的连接（`DriverManager.getConnection()`）时，会将这些属性传递给 JDBC 驱动程序。

将 `<CPROP_NAME>` 替换为连接属性名，并指定其值：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| jdbc.connection.property.\<CPROP_NAME\> | PXF 建立到外部 SQL 数据库的连接时传递给 JDBC 驱动程序的属性名称（\<CPROP_NAME\>）。 | \<CPROP_NAME\> 属性的值。 |

示例：要在到 PostgreSQL 数据库的 JDBC 连接上设置 `createDatabaseIfNotExist` 连接属性，请在 `jdbc-site.xml` 中包含以下属性块：

```xml
<property>
    <name>jdbc.connection.property.createDatabaseIfNotExist</name>
    <value>true</value>
 </property>
```

请确保外部 SQL 数据库的 JDBC 驱动程序支持您指定的所有连接级属性。

### 连接事务隔离属性 {#connection-transaction-isolation-property}

SQL 标准定义了四种事务隔离级别。您为到外部 SQL 数据库的某个连接指定的级别，决定了在该连接上运行的一个事务所做的更改何时以及如何对另一个事务可见。

PXF JDBC 连接器公开了一个名为 `jdbc.connection.transactionIsolation` 的可选服务器配置属性，用于指定事务隔离级别。PXF 在建立到外部 SQL 数据库的连接之后立即设置该级别（`setTransactionIsolation()`）。

JDBC 连接器支持以下 `jdbc.connection.transactionIsolation` 属性值：


| SQL 级别 | PXF 属性值 |
|----------------|-------------------------|
| Read uncommitted | READ_UNCOMMITTED |
| Read committed | READ_COMMITTED |
| Repeatable Read | REPEATABLE_READ |
| Serializable | SERIALIZABLE |

例如，要将事务隔离级别设置为 *Read uncommitted*，请将以下属性块添加到 `jdbc-site.xml` 文件：

```xml
<property>
    <name>jdbc.connection.transactionIsolation</name>
    <value>READ_UNCOMMITTED</value>
</property>
```

不同的 SQL 数据库支持不同的事务隔离级别。请确保外部数据库支持您指定的级别。

### 语句级属性 {#statement-level-properties}

PXF JDBC 连接器在一个*语句*中对外部 SQL 数据库表运行查询或插入命令。该连接器公开了一些属性，使您可以在命令于外部数据库中运行之前配置语句的某些方面。连接器支持以下语句级属性：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| jdbc.statement.batchSize | 批量写入外部数据库表的行数。 | 行数。默认的写入批大小为 100。 |
| jdbc.statement.fetchSize | 从外部数据库表读取时获取/缓冲的行数。 | 行数。MySQL 的默认读取获取大小为 `-2147483648`（`Integer.MIN_VALUE`）。所有其他数据库的默认读取获取大小为 1000。 |
| jdbc.statement.queryTimeout | JDBC 驱动程序等待语句运行的时间（以秒为单位）。此超时适用于为读取和写入操作创建的语句。 | 超时时长（以秒为单位）。默认等待时间不受限制。 |

对于您未显式配置的任何语句级属性，PXF 使用其默认值。

示例：要将读取获取大小设置为 5000，请将以下属性块添加到 `jdbc-site.xml`：

```xml
<property>
    <name>jdbc.statement.fetchSize</name>
    <value>5000</value>
</property>
```

请确保外部 SQL 数据库的 JDBC 驱动程序支持您指定的所有语句级属性。

### 预编译语句 {#prepared-statements}

默认情况下，PXF JDBC 连接器使用 JDBC `Statement` 从外部数据源读取数据。

PXF 的 `jdbc.read.prepared-statement` 属性控制连接器是否使用 `PreparedStatements`。如果您用于访问外部数据源的 JDBC 驱动程序要求使用 `PreparedStatement`，请将该属性设置为 `true`：

| 属性 | 说明 | 默认值 |
|----------------|--------------------------------------------|---------------|
| jdbc.read.prepared-statement | 从外部数据源读取时，使用 `PreparedStatement` 而不是 `Statement`。 | false |

### 会话级属性 {#session-level-properties}

要设置会话级属性，请将 `jdbc.session.property.<SPROP_NAME>` 属性添加到 `jdbc-site.xml`。PXF 会在运行查询之前，在外部数据库中对这些属性执行 `SET`。

 将 `<SPROP_NAME>` 替换为会话属性名，并指定其值：

| 属性 | 说明 | 值 |
|----------------|--------------------------------------------|-------|
| jdbc.session.property.\<SPROP_NAME\> | PXF 运行查询之前要设置的会话属性的名称（\<SPROP_NAME\>）。 | \<SPROP_NAME\> 属性的值。 |

**注意**：PXF JDBC 连接器将会话属性名和属性值严格按照 `jdbc-site.xml` 服务器配置文件中的指定内容传递给外部 SQL 数据库。为了限制潜在的 SQL 注入威胁，连接器会拒绝任何包含 `;`、`\n`、`\b` 或 `\0` 字符的属性名或属性值。

PXF JDBC 连接器会为所有受支持的外部 SQL 数据库处理会话属性的 `SET` 语法。

示例：要在 PostgreSQL 数据库中运行查询之前设置 `search_path` 参数，请将以下属性块添加到 `jdbc-site.xml`：

```xml
<property>
    <name>jdbc.session.property.search_path</name>
    <value>public</value>
</property>
```

请确保外部 SQL 数据库的 JDBC 驱动程序支持您指定的所有属性。

### 其他属性 {#other-properties}

PXF JDBC 连接器支持的其他属性：

| 属性 | 说明 | 默认值 |
|----------------|--------------------------------------------|---------------|
| jdbc.date.wideRange | 布尔值，用于在年份包含四个以上字母数字字符时启用对日期的特殊解析。设置为 `true` 时，PXF 使用扩展类解析日期，并能识别指定了 `BC` 或 `AD` 的年份。 | false |

### 关于 JDBC 连接池 {#about-jdbc-connection-pooling}

PXF JDBC 连接器使用由 [HikariCP](https://github.com/brettwooldridge/HikariCP) 实现的 JDBC 连接池。当用户查询或写入外部表时，连接器首次遇到 `jdbc.url`、`jdbc.user`、`jdbc.password`、连接属性和连接池属性设置的某个唯一组合，就会为相关联的服务器配置建立一个连接池。连接器在一定的连接和超时设置约束下复用连接池中的连接。

对于给定的服务器配置，可能存在一个或多个连接池；用户对指定同一服务器的不同外部表的访问可以共享同一个连接池。

**注意**：如果您已在服务器配置中启用 JDBC 用户模拟，则对于每个访问指定了该服务器配置的任意外部表的 Apache Cloudberry 用户，JDBC 连接器都会创建一个单独的连接池。

`jdbc.pool.enabled` 属性控制服务器配置的 JDBC 连接池。连接池默认处于启用状态。要停用某个服务器配置的 JDBC 连接池，请将该属性设置为 false：

```xml
<property>
    <name>jdbc.pool.enabled</name>
    <value>false</value>
</property>
```

如果您停用了某个服务器配置的 JDBC 连接池，PXF 不会为该服务器复用 JDBC 连接。PXF 会为查询的每个分区创建一个到远程数据库的连接，并在该分区的查询完成时关闭该连接。

PXF 公开了可在 JDBC 服务器定义中配置的连接池属性。这些属性以 `jdbc.pool.property.` 为前缀命名，并*适用于每个 PXF JVM*。JDBC 连接器会自动设置以下连接池属性及默认值：

| 属性 | 说明 | 默认值 |
|----------------|--------------------------------------------|-------|
| jdbc.pool.property.maximumPoolSize | 到数据库后端的最大连接数。 | 15 |
| jdbc.pool.property.connectionTimeout | 等待连接池提供连接的最长时间，以毫秒为单位。 | 30000 |
| jdbc.pool.property.idleTimeout | 非活动连接被视为空闲所经过的最长时间，以毫秒为单位。 | 30000 |
| jdbc.pool.property.minimumIdle | 连接池中维持的最小空闲连接数。 | 0 |

您可以通过在服务器的 `jdbc-site.xml` 配置文件中指定 `jdbc.pool.property.<HIKARICP_PROP_NAME>` 及所需的值，为服务器配置设置其他 HikariCP 特有的连接池属性。另请注意，JDBC 连接器在向 JDBC `DriverManager` 请求连接时，会传递您以 `jdbc.connection.property.` 为前缀指定的所有属性。请参阅上文的[连接级属性](#connection-level-properties)。

#### 调整最大连接池大小 {#tuning-the-maximum-connection-pool-size}

为了既不超出目标数据库允许的最大连接数，又确保每个 PXF JVM 分担到合理份额的 JDBC 连接，请根据 Apache Cloudberry 集群的规模，按如下方式确定 `maximumPoolSize` 的最大值：

```text
max_conns_allowed_by_remote_db / #_cloudberry_segment_hosts
```

例如，如果您的 Apache Cloudberry 集群有 16 台 Segment 主机，目标数据库允许 160 个并发连接，则按如下方式计算 `maximumPoolSize`：

```text
160 / 16 = 10
```

在实践中，您可以选择将 `maximumPoolSize` 设置为更低的值，因为每个 JDBC 查询的并发连接数取决于查询所使用的分区数。当查询不使用分区时，由单个 PXF JVM 为该查询提供服务。如果查询使用 12 个分区，PXF 会建立 12 个到远程数据库的并发 JDBC 连接。理想情况下，这些连接在各 PXF JVM 之间平均分配，但这并不能保证。


## JDBC 用户模拟 {#jdbc-user-impersonation}

PXF JDBC 连接器使用 `jdbc.user` 设置或 `jdbc.url` 中的信息来确定连接外部数据存储的用户身份。当 PXF JDBC 用户模拟处于停用状态（默认）时，JDBC 连接器的行为还取决于外部数据存储。例如，如果您使用 JDBC 连接器访问 Hive，则连接器使用某些 Hive 身份验证和用户模拟属性的设置来确定用户。您可能需要提供 `jdbc.user` 设置，或在服务器 `jdbc-site.xml` 文件的 `jdbc.url` 设置中添加属性。有关此过程的更多信息，请参阅[通过 JDBC 连接器配置 Hive 访问](/cloudberry/pxf/administering/configuring/jdbc-connector/hive_jdbc_cfg/)。

启用 PXF JDBC 用户模拟后，PXF JDBC 连接器代表 Apache Cloudberry 终端用户访问外部数据存储。连接器使用访问 PXF 外部表的 Apache Cloudberry 用户的名称来尝试连接外部数据存储。

为 PXF 服务器启用 JDBC 用户模拟后，PXF 会用 Apache Cloudberry 用户名覆盖在 `jdbc-site.xml` 或 `<cloudberry_user_name>-user.xml` 中定义、或在外部表 DDL 中指定的 `jdbc.user` 属性值。如果外部数据存储要求使用密码对连接的用户进行身份验证，为使用户模拟有效工作，您必须在每个可被模拟的用户各自的 `<cloudberry_user_name>-user.xml` 属性覆盖文件中，指定该用户的 `jdbc.password` 设置。有关按服务器、按 Cloudberry 用户配置的更多信息，请参阅[配置 PXF 用户](/cloudberry/pxf/administering/configuring/cfg_server/#configuring-a-pxf-user)。

`jdbc-site.xml` 配置文件中的 `pxf.service.user.impersonation` 属性控制 JDBC 用户模拟。


### 示例配置过程 {#example-configuration-procedure}

默认情况下，PXF JDBC 用户模拟处于停用状态。请执行以下过程，为某个 JDBC 服务器配置开启或关闭 PXF 用户模拟。

1. 以管理员用户身份登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 确定要更新的 PXF JDBC 服务器配置的名称。

3. 进入服务器配置目录。例如，如果服务器名为 `mysqldb`：

    ```shell
    gpadmin@coordinator$ cd $PXF_BASE/servers/mysqldb
    ```

5. 在您选择的编辑器中打开 `jdbc-site.xml` 文件，添加或取消注释用户模拟属性及其设置。例如，如果此服务器配置需要用户模拟，请将 `pxf.service.user.impersonation` 属性设置为 `true`：

    ```xml
    <property>
        <name>pxf.service.user.impersonation</name>
        <value>true</value>
    </property>
    ```

7. 保存 `jdbc-site.xml` 文件并退出编辑器。

8. 使用 `pxf cluster sync` 命令将 PXF JDBC 服务器配置同步到您的 Apache Cloudberry 集群：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

## 关于会话授权 {#about-session-authorization}

某些 SQL 数据库（包括 PostgreSQL 和 DB2）允许特权用户更改在会话中运行命令的有效数据库用户。例如，如果您以代理用户身份连接远程数据库，并希望在建立数据库连接之后切换会话授权，就可以利用此功能。

在支持此功能的数据库中，您可以配置会话属性来切换有效用户。例如，在 DB2 中，您使用 `SET SESSION_USER <username>` 命令切换有效的 DB2 用户。如果您通过 `jdbc-site.xml` 文件中的 PXF 会话级属性（`jdbc.session.property.<SPROP_NAME>`）配置了 DB2 的 `session_user` 变量，PXF 会为您运行此命令。

例如，要将有效的 DB2 用户切换为名为 `bill` 的用户，请按如下方式配置 `jdbc-site.xml`：

```xml
<property>
    <name>jdbc.session.property.session_user</name>
    <value>bill</value>
</property>
```

建立数据库连接之后，PXF 会隐式运行以下命令，将 `session_user` DB2 会话变量设置为您配置的值：

```sql
SET SESSION_USER = bill
```

PXF 可识别一个合成属性值 `${pxf.session.user}`，它标识 Apache Cloudberry 用户名。当您配置的属性所需的值会随运行会话的 Cloudberry 用户而变化时，可以选择使用该值。

可以使用 `${pxf.session.user}` 的一种场景是：您使用 Kerberos 向远程 SQL 数据库进行身份验证，Kerberos 主体的主要组成部分标识 Apache Cloudberry 用户名，并且您希望使用该有效用户名在远程数据库中运行查询。例如，如果您访问的是 DB2，则应配置 `jdbc-site.xml` 以指定 Kerberos 的 `securityMechanism` 和 `KerberosServerPrincipal`，然后按如下方式设置 `session_user` 变量：

```xml
<property>
    <name>jdbc.session.property.session_user</name>
    <value>${pxf.session.user}</value>
</property>
```

采用此配置后，PXF 会将 DB2 的 `session_user` 变量 `SET` 为当前 Apache Cloudberry 用户名，并以该用户的身份对 DB2 表运行后续操作。

### 连接池的会话授权注意事项 {#session-authorization-considerations-for-connection-pooling}

当 PXF 代您执行会话授权且 JDBC 连接池处于启用状态（默认）时，您可以选择设置 `jdbc.pool.qualifier` 属性。设置该属性会指示 PXF 在创建和复用连接池所用的条件中包含该属性值。在实践中，您不会将其设置为固定值，而是设置为随用户/会话/事务等变化的值。当您将该属性设置为 `${pxf.session.user}` 时，PXF 会在创建和复用连接池所用的条件中包含 Apache Cloudberry 用户名。默认设置为无限定符。

要使用此功能，请在 `jdbc-site.xml` 中添加或取消注释以下属性块，以提示 PXF 在连接池创建/复用条件中包含 Cloudberry 用户名：

```xml
<property>
    <name>jdbc.pool.qualifier</name>
    <value>${pxf.session.user}</value>
</property>
```

## JDBC 命名查询配置 {#jdbc-named-query-configuration}

PXF *命名查询*（named query）是您配置的静态查询，由 PXF 在远程 SQL 数据库中运行。

要配置并使用 PXF JDBC 命名查询：

1. 在文本文件中[定义查询](#defining-a-named-query)。
2. 向 Apache Cloudberry 用户提供[查询名称](#query-naming)。
3. Apache Cloudberry 用户在 Apache Cloudberry 外部表定义中[引用该查询](#referencing-a-named-query)。

每当用户对该 Apache Cloudberry 外部表调用 `SELECT` 命令时，PXF 都会运行该查询。


### 定义命名查询 {#defining-a-named-query}

您可以通过将查询语句添加到采用以下命名格式的文本文件来创建命名查询：`<query_name>.sql`。您可以为一个 JDBC 服务器配置定义一个或多个命名查询。每个查询必须位于单独的文本文件中。

您必须将查询文本文件放在将要访问它的 PXF JDBC 服务器配置目录中。如果要让多个 JDBC 服务器配置都能使用该查询，则必须将查询文本文件复制到每个 JDBC 服务器的配置目录中。

查询文本文件必须只包含一条要在远程 SQL 数据库中运行的查询。您必须按照该数据库所支持的语法构造查询。

例如，如果某个 MySQL 数据库有一个 `customers` 表和一个 `orders` 表，您可以在查询文本文件中包含以下 SQL 语句：

```sql
SELECT c.name, c.city, sum(o.amount) AS total, o.month
  FROM customers c JOIN orders o ON c.id = o.customer_id
  WHERE c.state = 'CO'
GROUP BY c.name, c.city, o.month
```

您可以选择在 SQL 语句末尾加上分号（`;`）。

### 查询命名 {#query-naming}

Apache Cloudberry 用户通过指定不带扩展名的查询文件名来引用命名查询。例如，如果您在名为 `report.sql` 的文件中定义了查询，则该查询的名称为 `report`。

命名查询与特定的 JDBC 服务器配置相关联。您需要向被允许使用该服务器配置创建外部表的 Apache Cloudberry 用户提供可用的查询名称。

#### 引用命名查询 {#referencing-a-named-query}

Apache Cloudberry 用户在创建外部表/外表时，指定 `query:<query_name>`，而不是远程 SQL 数据库表的名称。例如，如果查询定义在文件 `$PXF_BASE/servers/mydb/report.sql` 中，则 `CREATE EXTERNAL TABLE` 的 `LOCATION` 子句将包含以下组成部分：

```sql
LOCATION ('pxf://query:report?PROFILE=jdbc&SERVER=mydb ...')
```

有关使用 PXF JDBC 命名查询的信息，请参阅[关于使用命名查询](/cloudberry/pxf/access-jdbc/#about-using-named-queries)。

## 覆盖 JDBC 服务器配置 {#overriding-the-jdbc-server-configuration}

您可以通过 `CREATE EXTERNAL TABLE` 命令 `LOCATION` 子句中的自定义选项直接指定某些 JDBC 属性，从而覆盖 JDBC 服务器配置。更多信息请参阅[通过 DDL 覆盖 JDBC 服务器配置](/cloudberry/pxf/access-jdbc/#overriding-the-jdbc-server-configuration-with-ddl)。


## 配置对 Hive 的访问 {#configuring-access-to-hive}

您可以使用 JDBC 连接器访问 Hive。有关此配置过程的详细信息，请参阅[配置 JDBC 连接器以访问 Hive](/cloudberry/pxf/administering/configuring/jdbc-connector/hive_jdbc_cfg/)。


## 示例配置过程 {#example-configuration-procedure-1}

在此过程中，您将为 PostgreSQL 数据库命名并添加一个 PXF JDBC 服务器配置，并将服务器配置同步到 Apache Cloudberry 集群。

1. 登录您的 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 为 JDBC 服务器选择一个名称。您需要将该名称提供给被允许以所配置用户的身份引用外部 SQL 数据库中表的 Cloudberry 用户。

    **注意**：服务器名称 `default` 为保留名称。

3. 创建 `$PXF_BASE/servers/<server_name>` 目录。例如，使用以下命令创建名为 `pg_user1_testdb` 的 JDBC 服务器配置：

    ```shell
    gpadmin@coordinator$ mkdir $PXF_BASE/servers/pg_user1_testdb
    ````

4. 将 PXF JDBC 服务器模板文件复制到服务器配置目录。例如：

    ```shell
    gpadmin@coordinator$ cp <PXF_INSTALL_DIR>/templates/jdbc-site.xml $PXF_BASE/servers/pg_user1_testdb/
    ```
        
5. 在您选择的编辑器中打开模板服务器配置文件，并提供适合您环境的属性值。例如，如果您要为运行在名为 `pgserverhost` 的主机上的 PostgreSQL 实例中、名为 `testdb` 的 PostgreSQL 数据库，配置名为 `user1` 的用户的访问：

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <property>
            <name>jdbc.driver</name>
            <value>org.postgresql.Driver</value>
        </property>
        <property>
            <name>jdbc.url</name>
            <value>jdbc:postgresql://pgserverhost:5432/testdb</value>
        </property>
        <property>
            <name>jdbc.user</name>
            <value>user1</value>
        </property>
        <property>
            <name>jdbc.password</name>
            <value>changeme</value>
        </property>
    </configuration>
    ```
6. 保存更改并退出编辑器。

7. 使用 `pxf cluster sync` 命令将新的服务器配置复制到 Apache Cloudberry 集群：
    
    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```
