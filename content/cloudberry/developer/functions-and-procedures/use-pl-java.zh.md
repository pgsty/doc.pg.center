---
title: "使用 PL/Java"
description: "PL/Java 是一种嵌入式受信任过程语言，允许使用 Java 编程语言编写 PostgreSQL 函数和触发器。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/functions-and-procedures/use-pl-java.md"
---

使用 PL/Java 可以：

- 用 Java 编写函数，并从 SQL 调用这些函数。
- 使用 Java 标准库。
- 在 Java 函数中通过 JDBC 访问数据库。

## 启用 PL/Java {#enable-pljava}

要使用 PL/Java，必须在数据库中启用它。

1. 使用 `psql` 连接数据库。

    ```bash
    psql -d <database_name>
    ```

2. 创建 `pljava` 扩展。

    ```sql
    CREATE EXTENSION pljava;
    ```

    这会注册受信任语言（`pljava`）和不受信任语言（`javau`）。如果只需要受信任语言，请使用 `CREATE EXTENSION pljavat`。

3. 配置 classpath 头信息。

    需要设置 `pljava_classpath` 配置参数，使其包含 Java 类所在的 JAR 文件。

    ```sql
    SET pljava_classpath = 'examples.jar:myclasses.jar';
    ```

    要让此更改对数据库永久生效：

    ```sql
    ALTER DATABASE <database_name> SET pljava_classpath = 'examples.jar:myclasses.jar';
    ```

## 编写 PL/Java 函数 {#write-pljava-functions}

要创建 PL/Java 函数，需要编写包含静态方法的 Java 类，将其编译为 JAR 文件，然后在 SQL 中声明该函数。

### SQL 声明 {#sql-declaration}

Java 函数声明包含类名以及该类中的静态方法。

```sql
CREATE FUNCTION getsysprop(VARCHAR)
RETURNS VARCHAR
AS 'java.lang.System.getProperty'
LANGUAGE java;
```

之后即可像调用其他 SQL 函数一样调用此函数：

```sql
SELECT getsysprop('user.home');
```

### 类型映射 {#type-mapping}

PL/Java 会自动将 PostgreSQL 类型映射为 Java 类型。

| PostgreSQL 类型 | Java 类型 |
| :--- | :--- |
| `boolean` | `boolean` |
| `smallint` | `short` |
| `integer` | `int` |
| `bigint` | `long` |
| `real` | `float` |
| `double precision` | `double` |
| `text`、`varchar`、`char` | `java.lang.String` |
| `date` | `java.sql.Date` |
| `time` | `java.sql.Time` |
| `timestamp` | `java.sql.Timestamp` |
| `bytea` | `byte[]` |

### NULL 处理 {#null-handling}

Java 基本类型（例如 `int`、`double`、`boolean`）不能为 `NULL`。如果将 SQL `NULL` 传给需要基本类型的 Java 函数，除非将其映射到相应的包装类（例如 `java.lang.Integer`），否则会导致错误。

处理 NULL 的示例：

1. 创建 Java 方法。

    ```java
    package com.example;
    public class Utils {
        public static boolean trueIfEvenOrNull(Integer value) {
            return (value == null) ? true : (value.intValue() % 2) == 0;
        }
    }
    ```

2. 使用完整类名在 SQL 中声明函数。

    ```sql
    CREATE FUNCTION true_if_even_or_null(integer)
    RETURNS boolean
    AS 'com.example.Utils.trueIfEvenOrNull(java.lang.Integer)'
    LANGUAGE java;
    ```

### 复杂类型 {#complex-types}

可以向 Java 函数传递复杂类型和行。PL/Java 支持使用 `Complex` 类型和 `ResultSet` 处理行和集合。

## 使用 JDBC {#use-jdbc}

PL/Java 包含 JDBC 驱动程序，允许 Java 代码访问函数运行所在的数据库。

建立到当前数据库会话的连接：

```java
import java.sql.Connection;
import java.sql.DriverManager;

Connection conn = DriverManager.getConnection("jdbc:default:connection");
```

### 限制 {#limitations}

使用内部 JDBC 驱动程序（`jdbc:default:connection`）时：
- 不能显式管理事务（不允许使用 `commit()`、`rollback()` 等）。函数在调用它的 SQL 语句的事务上下文中运行。
- 允许使用 `Savepoint` 操作，但必须在同一个函数中释放。
- `executeQuery()` 返回的 `ResultSet` 始终为 `FETCH_FORWARD` 和 `CONCUR_READ_ONLY`。

## 处理异常 {#handle-exceptions}

PL/Java 将数据库错误映射为 `java.sql.SQLException`。可以在 Java 代码中捕获标准 SQL 异常。如果 Java 代码抛出异常，该异常会作为错误报告给 PostgreSQL 客户端，并且事务会中止（除非由保存点捕获）。

## 记录消息 {#log-messages}

PL/Java 使用标准的 `java.util.logging.Logger`。通过此记录器记录的消息会重定向到 PostgreSQL 日志系统（`elog`）。

```java
import java.util.logging.Logger;

Logger.getAnonymousLogger().info("Time is " + new java.util.Date());
```

数据库配置 `log_min_messages` 决定实际发送到客户端或写入服务器日志的日志级别。

## 安全性 {#security}

- **受信任语言（`java`）**：使用受信任的 `java` 语言时，Java 安全管理器通过标准 Java 安全策略阻止访问文件系统和其他敏感系统资源。任何用户都可以使用受信任语言创建函数。
- **不受信任语言（`javau`）**：不受信任的 `javau` 语言允许不受限制的访问（例如文件系统访问），类似于独立 Java 应用程序。只有超级用户才能使用 `javau` 创建函数。
