---
title: 使用 Python
linkTitle: Python
description: 通过 ODBC、原生 TDS 或 FreeTDS 连接，并在 Python 中读写数据与处理事务。
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_client/python.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 文档快照
> 本文译自上游网站，中文翻译由 PGSTY 文档项目整理。上游自 2023 年起将新文档迁至 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)；请结合所用版本的[发行说明](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)核对功能支持。

## 在 Python 中使用 Babelfish {#using-python-with-babelfish}

本节介绍如何使用 Python 连接 Babelfish 并读取服务器数据，涵盖三种方式：

- Python 与 ODBC。
- Python 与原生 TDS。
- Python 与 FreeTDS（原文所述环境中，arm64 架构没有 `msobdcsql`）。

三种方式均包含帮助理解 Babelfish 事务操作的示例。

### 使用 Python 与 ODBC {#using-python-and-odbc}

运行 Python 代码前，确认所需库均已安装。在 Ubuntu 20.04 上，可使用以下命令补齐缺失的软件包：

```bash
#!/bin/bash
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

不同 Linux 发行版的安装过程略有差别，但基本要求一致：确保库已安装。

运行示例前，还需创建名为 `contacts` 的 Babelfish 表。使用任意合适的客户端连接数据库的 TDS 端口，执行：

```sql
CREATE TABLE contacts (
    contact_id INT PRIMARY KEY,
    first_name VARCHAR (10) NOT NULL,
    last_name VARCHAR (20) NOT NULL,
    visited DATE
);

INSERT INTO contacts VALUES ('1', 'Alex', 'Arthur', '20210831');
INSERT INTO contacts VALUES ('2', 'Bonnie', 'Bret', '20210831');
INSERT INTO contacts VALUES ('3', 'Colin', 'Cristobal', '20210901');
INSERT INTO contacts VALUES ('4', 'Danielle', 'Dexter', '20210907');
INSERT INTO contacts VALUES ('5', 'Earl', 'Edwards', '20210908');
INSERT INTO contacts VALUES ('6', 'Fiona', 'Ferdinand', '20210917');
```

本例使用 Python、ODBC 和 Babelfish 建立连接、读取数据并输出到屏幕。首先导入所需库：

```python
import sys
import os
import pyodbc
```

然后连接 SQL Server 主机。连接字符串必须以正确格式包含所有相关信息：

```python
# Provide your SQL Server credentials
server = 'host.example.com'
database = 'postgres'
username = 'postgres'
password = '********'

# Establish a connection
try:
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()
    print("Connection established for select examples\n")
except pyodbc.ProgrammingError:
    print("Cannot connect to the database\nPlease check credentials")
    exit(1)
```

接着创建游标，遍历并显示 `contacts` 表中的行：

```python
# Select values
cursor.execute("SELECT * FROM contacts")

for row in cursor.fetchall():
    print(row)
```

输出如下：

```bash
Connection established for select examples

(1, 'Alex', 'Arthur', 20210831)
(2, 'Bonnie', 'Bret', 20210831)
(3, 'Colin', 'Cristobal', 20210901)
(4, 'Danielle', 'Dexter', 20210907)
(5, 'Earl', 'Edwards', 20210908)
(6, 'Fiona', 'Ferdinand', 20210917)

```

### 事务处理 {#transaction-handling}

下一个示例使用游标与原生 TDS 执行基本的事务操作。首先连接服务器：

```python
# Transaction example
# Establish a Babelfish connection
try:
    transact_connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password, autocommit=False)
    t_cursor = transact_connection.cursor()
    print("\nConnection established\n")
except pyodbc.ProgrammingError:
    print("\nConnection attempt failed\nPlease check credentials")
    exit(1)
```

然后使用游标向数据库添加记录：

```python
# Insert values into your contacts table
try:
    t_cursor.execute("INSERT INTO contacts VALUES('Gaston', 'Gordon', '20210918')")
    t_cursor.execute("INSERT INTO contacts VALUES('Hermione', 'Henry', '20210925')")
except pyodbc.Error as e:
    t_cursor.rollback()
    print("Insert failed: {}".format(e))
else:
    t_cursor.commit()
    print("Insert successful\n")
```

接着遍历表并显示内容：

```python
t_cursor.execute("SELECT * FROM contacts")

for row in t_cursor.fetchall():
    print(row)

t_cursor.close()
transact_connection.close()
```

随后删除两行：

```python
# Remove inserted values
cursor.execute("DELETE FROM contacts WHERE last_name = 'Bret' OR last_name = 'Edwards'")
cursor.commit()

# Select metadata
print(f"\nDeleted Rows: {cursor.rowcount}\n")
```

最后关闭连接并通知用户：

```python
# Close connection
cursor.close()
connection.close()
print("Success")
```

示例应输出以下消息：

```bash
Connection established

Insert successful

(1, 'Alex', 'Arthur', 20210831)
(3, 'Colin', 'Cristobal', 20210901)
(4, 'Danielle', 'Dexter', 20210907)
(6, 'Fiona', 'Ferdinand', 20210917)
(7, 'Gaston', 'Gordon', 20210918)
(8, 'Hermione', 'Henry', 20210925)

Deleted Rows: 2

Success
```

此时，表中已反映示例所做的修改。

## 使用 Python 与 FreeTDS {#using-python-with-freetds}

在 arm64 架构上，可使用 FreeTDS 驱动通过 TDS 协议连接。

运行示例前，先安装必要软件：

```bash
sudo apt install python3-pip python3-venv freetds-dev
python3 -m venv .venv
source .venv/bin/activate
pip install pymssql psycopg2
```

示例使用 [`pymssql` API](http://www.pymssql.org/pymssql_examples.html) 向 Babelfish 写入数据，再使用 [`psycopg2` 库](http://www.freetds.org/userguide/Python.html) 读取。先导入相应库，再连接 Babelfish 主机：

```python
import sys
import os
import pymssql
import psycopg2

server = 'host.example.com'
port = 1433
database = 'master'  
username = 'babelfish_user'
password = '********'

pg_database = "babelfish_db"
pg_schema   = "master_dbo"

def main():

    with pymssql.connect(server, username, password, database) as conn:
        with conn.cursor() as cursor:
```

随后删除并重建简单的 `contacts` 表及 `find_contact` 过程：

```python
            try:
                cursor.execute("DROP TABLE contacts")
                cursor.execute("DROP PROCEDURE find_contact")
                conn.commit()
            except Exception as e:
                # For the sake of this example, we 
                # ignore exceptions if the objects do not exist.
                pass
            
            try:
                print("-- create table: ")
                cursor.execute("""
                    CREATE TABLE contacts (
                        contact_id INT PRIMARY KEY,
                        first_name VARCHAR (10) NOT NULL,
                        last_name VARCHAR (20) NOT NULL,
                        visited DATE
                    )
                """)
                cursor.execute("""
                    CREATE PROCEDURE find_contact
                        @last_name VARCHAR(100)
                    AS BEGIN
                        SELECT * FROM contacts WHERE last_name like '%'+@last_name+'%'
                    END
                """)
                conn.commit()
            except Exception as e:
                print("Cannot create table: {}".format(e))
                exit(1)

```

向表中添加联系人：

```python
            try:
                print("-- Insert")
                cursor.executemany(
                    "INSERT INTO contacts VALUES (%d, %s, %s, %s)",
                    [
                        (11, 'Imelda', 'Imani', '20211004'),
                        (12, 'Julian', 'Joyce', '20211015'),
                        (13, 'Katia', 'Kirk', '20211027')
                    ])
                conn.commit()
            except Exception as e:
                print("Transaction could not be committed: {} ".format(e))
                exit(2) # Duplicate key error
```

接着先使用 `psycopg2`，再使用 `pymssql` 查询表：

```python
    with psycopg2.connect(user=username, password=password, host=server,database=pg_database) as connpg:
        with connpg.cursor() as cursorpg:
            print("-- Output from Babelfish: ")
            try:
                cursorpg.execute("SELECT * FROM {}.contacts WHERE last_name like '%{}%'".format(pg_schema,"Joyce"))
                for row in cursorpg:
                    print("{}".format(row))
            except Exception as e:
                print("Read query couldn't be executed: {}".format(e))
                pass
    
    with pymssql.connect(server, username, password, database) as conn:
        with conn.cursor() as cursor:
            print("-- Executing PROCEDURE ")
            cursor.callproc('find_contact', ('Joyce',))
            for row in cursor:
                print("{}".format(row))
```

`with` 语句会在代码块结束后清理游标和连接，使资源管理更清晰。

最后，添加对 `main()` 函数的初始化调用：

```python
if __name__ == "__main__":
    main()
```
