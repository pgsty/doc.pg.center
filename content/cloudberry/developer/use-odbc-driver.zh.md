---
title: "使用 ODBC"
description: "Apache Cloudberry 与 Greenplum 和 PostgreSQL 兼容，因此 ODBC 访问方法与 Greenplum/PostgreSQL 相同。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/use-odbc-driver.md"
---

本指南介绍如何在 Linux 或 macOS 上使用 ODBC 连接 Apache Cloudberry 并执行数据库操作。

## 前提条件 {#prerequisites}

通过 ODBC 连接 Apache Cloudberry 之前，请确保已准备好以下内容：

- 已安装 PostgreSQL ODBC 驱动程序。
- 符合 ODBC 标准的应用程序或工具（例如 `psqlODBC`、`isql`、Tableau 等 BI 工具）。
- Apache Cloudberry 的连接信息，包括主机、端口、数据库名、用户名和密码。

## 安装 ODBC 驱动程序 {#install-the-odbc-driver}

可以从 [PostgreSQL ODBC 官方网站](https://odbc.postgresql.org/)下载 PostgreSQL ODBC 驱动程序。请确保安装适合操作系统的版本。

1. 安装所需的软件包（适用于 Ubuntu/Debian）：

    ```sh
    sudo apt update && sudo apt install -y unixodbc odbc-postgresql
    ```

2. 验证安装：

    ```sh
    odbcinst -q -d
    ```

    输出应将 `PostgreSQL` 列为受支持的驱动程序。

## 配置 ODBC 连接 {#configure-odbc-connection}

编辑 ODBC 驱动程序配置文件（`/etc/odbcinst.ini`）：

```ini
[PostgreSQL]
Description = ODBC for PostgreSQL
Driver = /usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so
Setup = /usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so
```

编辑 ODBC 数据源文件（`/etc/odbc.ini`）：

```ini
[YourDataSource]
Driver = PostgreSQL
ServerName = your-db-host
Port = 5432
Database = your_database
UserName = your_username
Password = your_password
SSLmode = prefer
```

## 通过 ODBC 连接 Apache Cloudberry {#connect-to-apache-cloudberry-via-odbc}

### 使用 `isql` {#use-isql}

配置好 DSN 后，可以使用 `isql` 测试连接：

```sh
isql -v YourDataSource your_username your_password
```

如果连接成功，将进入交互式 SQL shell。

### 使用 Python（`pyodbc`） {#use-python-pyodbc}

如果希望使用 Python 连接，请安装 `pyodbc` 软件包，并使用以下脚本：

```python
import pyodbc

conn = pyodbc.connect(
   "DSN=YourDataSource;UID=your_username;PWD=your_password"
)
cursor = conn.cursor()
cursor.execute("SELECT version();")
row = cursor.fetchone()
print("Database Version:", row[0])
conn.close()
```

## 执行 SQL 语句 {#execute-sql-statements}

### 查询数据 {#query-data}

```python
cursor.execute("SELECT id, name FROM users;")
for row in cursor.fetchall():
   print(f"ID: {row[0]}, Name: {row[1]}")
```

### 插入数据 {#insert-data}

```python
cursor.execute("INSERT INTO users (id, name) VALUES (1, 'Alice');")
conn.commit()
```

### 更新数据 {#update-data}

```python
cursor.execute("UPDATE users SET name = 'Bob' WHERE id = 1;")
conn.commit()
```

### 删除数据 {#delete-data}

```python
cursor.execute("DELETE FROM users WHERE id = 1;")
conn.commit()
```

## 排查连接问题 {#connection-troubleshooting}

如果连接失败，请检查：

- 是否能够通过网络访问 Apache Cloudberry。
- 防火墙或安全组设置是否允许访问 PostgreSQL 端口（默认为 5432）。
- ODBC DSN 设置是否正确。
- 数据库日志中是否有错误消息。
