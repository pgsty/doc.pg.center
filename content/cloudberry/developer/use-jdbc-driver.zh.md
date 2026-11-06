---
title: "使用 JDBC"
description: "Apache Cloudberry 与 Greenplum 和 PostgreSQL 兼容，因此 JDBC 访问方法与 Greenplum/PostgreSQL 相同。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/use-jdbc-driver.md"
---

本指南介绍如何使用 JDBC 连接 Apache Cloudberry 并执行数据库操作。

## 前提条件 {#prerequisites}

通过 JDBC 连接 Apache Cloudberry 之前，请确保已准备好以下内容：

- 已安装 Java 运行环境（JDK 1.8 或更高版本）。
- 已下载 PostgreSQL JDBC 驱动程序（`postgresql-<version>.jar`）。
- Apache Cloudberry 的连接信息，包括主机、端口、数据库名、用户名和密码。

## 步骤 1：下载 JDBC 驱动程序 {#step-1-download-the-jdbc-driver}

可以从 [PostgreSQL 官方网站](https://jdbc.postgresql.org/)下载 JDBC 驱动程序。请使用与 Apache Cloudberry 兼容的最新稳定版本。

下载命令示例（以 42.5.0 版本为例）：

```sh
wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar
```

## 步骤 2：连接 Apache Cloudberry {#step-2-connect-to-apache-cloudberry}

要连接 Apache Cloudberry，请在 Java 程序中使用以下格式的连接字符串。

```text
jdbc:postgresql://<host>:<port>/<database>?parameters
```

常用参数：

- `user=<username>`：指定数据库用户名。
- `password=<password>`：指定数据库密码。
- `ssl=<true|false>`：启用或禁用 SSL 连接。
- `ApplicationName=<app_name>`：可选，用于标识客户端应用程序。

示例：

```text
jdbc:postgresql://db.example.com:5432/mydb?user=myuser&password=mypass&ssl=true
```

以下示例演示如何使用 JDBC 连接 Apache Cloudberry：

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class DBExample {
   public static void main(String[] args) {
      String url = "jdbc:postgresql://your-db-host:5432/your_database";
      String user = "your_username";
      String password = "your_password";

      try (Connection conn = DriverManager.getConnection(url, user, password);
          Statement stmt = conn.createStatement();
          ResultSet rs = stmt.executeQuery("SELECT version();")) {

         while (rs.next()) {
            System.out.println("Database Version: " + rs.getString(1));
         }
      } catch (SQLException e) {
         e.printStackTrace();
      }
   }
}
```

## 步骤 3：设置环境 {#step-3-set-up-the-environment}

### 下载 PostgreSQL JDBC 驱动程序 {#download-postgresql-jdbc-driver}

连接数据库之前，请下载 PostgreSQL JDBC 驱动程序：

```bash
wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar
```

### 编译 Java 代码 {#compile-java-code}

编写 Java 程序后，使用下载的 JDBC 驱动程序编译：

```bash
javac -cp postgresql-42.5.0.jar YourJavaProgram.java
```

### 运行 Java 程序 {#run-the-java-program}

将类路径设置为包含 JDBC 驱动程序，然后执行 Java 程序：

```bash
java -cp .:postgresql-42.5.0.jar YourJavaProgram
```

## 执行 SQL 语句 {#execute-sql-statements}

要通过 JDBC 执行 SQL 语句，可以参照以下各节将代码添加到 Java 程序中。

### 查询数据 {#query-data}

```java
String query = "SELECT id, name FROM users";
try (Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery(query)) {
   while (rs.next()) {
      int id = rs.getInt("id");
      String name = rs.getString("name");
      System.out.println("ID: " + id + ", Name: " + name);
   }
}
```

### 插入数据 {#insert-data}

```java
String insertSQL = "INSERT INTO users (id, name) VALUES (1, 'Alice')";
try (Statement stmt = conn.createStatement()) {
   int rowsAffected = stmt.executeUpdate(insertSQL);
   System.out.println("Rows inserted: " + rowsAffected);
}
```

### 更新数据 {#update-data}

```java
String updateSQL = "UPDATE users SET name = 'Bob' WHERE id = 1";
try (Statement stmt = conn.createStatement()) {
   int rowsAffected = stmt.executeUpdate(updateSQL);
   System.out.println("Rows updated: " + rowsAffected);
}
```

### 删除数据 {#delete-data}

```java
String deleteSQL = "DELETE FROM users WHERE id = 1";
try (Statement stmt = conn.createStatement()) {
   int rowsAffected = stmt.executeUpdate(deleteSQL);
   System.out.println("Rows deleted: " + rowsAffected);
}
```

## 事务管理 {#transaction-management}

JDBC 允许显式控制事务：

```java
conn.setAutoCommit(false);
try (Statement stmt = conn.createStatement()) {
   stmt.executeUpdate("INSERT INTO users (id, name) VALUES (2, 'Charlie')");
   stmt.executeUpdate("UPDATE users SET name = 'Charlie Updated' WHERE id = 2");
   conn.commit();
} catch (SQLException e) {
   conn.rollback();
   e.printStackTrace();
}
```

## 使用连接池 {#use-connection-pools}

在生产环境中，使用连接池（例如 HikariCP）可以提高性能。

### 添加 HikariCP 依赖 {#add-hikaricp-dependency}

对于 Maven：

```xml
<dependency>
   <groupId>com.zaxxer</groupId>
   <artifactId>HikariCP</artifactId>
   <version>5.0.1</version>
</dependency>
```

### 配置 HikariCP {#configure-hikaricp}

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:postgresql://your-db-host:5432/your_database");
config.setUsername("your_username");
config.setPassword("your_password");
config.setMaximumPoolSize(10);
HikariDataSource dataSource = new HikariDataSource(config);
```

## 排查连接问题 {#troubleshoot-connection-issues}

如果连接失败，请检查：

- 是否能够通过网络访问 Apache Cloudberry。
- 防火墙或安全组设置是否允许访问 PostgreSQL 端口（默认为 5432）。
- JDBC URL、用户名和密码是否正确。
- 数据库日志中是否有详细的错误消息。
