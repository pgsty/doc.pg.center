---
title: 使用 JDBC
linkTitle: Java / JDBC
description: 使用 SQL Server JDBC 驱动连接 Java 应用。
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_client/java.md
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

## 使用 JDBC {#utilizing-jdbc}

介绍 Python、C# 等常用语言之后，本节说明如何结合 Java 与 JDBC 使用 Babelfish，同样通过基本操作展示代码编写方法。

为 Babelfish 编写 JDBC 客户端，与为 Microsoft SQL Server 编写客户端并没有实质区别。下面看一个示例。

### JDBC 示例代码 {#sample-code-using-jdbc}

编译 Java 代码需要 Microsoft SQL Server JDBC 驱动。本例使用 9.4 版（`mssql-jdbc-9.4.0.jre11.jar`）。由于代码只涉及基础功能，其他版本的驱动也应能够运行。

代码如下：

```java
package sample;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class sample {
	public static void main(String[] args) {
		Connection connection;
		// Setting up MSSQL Credentials
		String connectionUrl =
			"jdbc:sqlserver://PUT_HOSTNAME_HERE;"
			+ "database=PUT_NAME_OF_DATABASE_HERE;"
			+ "user=PUT_USERNAME_HERE;"
			+ "password=PUT_PASSWORD_HERE;";

		try {
			// Trying to establish connection
			connection = DriverManager.getConnection(connectionUrl);
			System.out.println("Connection established for select examples!\n");
			
			// Select values example
			select_all(connection);
			
			// Transaction example
			connection.setAutoCommit(false);
			
			// Insert values into sample table
			try {
				connection.setAutoCommit(false);
			
				String insert = "INSERT INTO sample VALUES('Max', 'Mustermann', '1020')";
				Statement statement = connection.createStatement();
				statement.execute(insert);
				
				insert = "INSERT INTO sample VALUES('Erika', 'Musterfrau', '1021')";
				statement.execute(insert);
				
				connection.commit();
				System.out.println("\nInsert successful!\n");
			}
			catch (SQLException e){
				connection.rollback();
				System.out.println("\nInsert failed!\n");
			}
			
			select_all(connection);
			
			connection.setAutoCommit(true);
			
			// Removing inserted values and displaying rowcount
			try {
				String delete = "DELETE FROM sample WHERE vorname = 'Max' or vorname = 'Erika'";
				Statement statement = connection.createStatement();
				int rowcount = statement.executeUpdate(delete);
				
				System.out.println("\nDeleted Rows: " + rowcount + "\n");
				
				// Select column names
				String select = "SELECT * FROM sample";
				ResultSet result = statement.executeQuery(select);
				
				String value = "";
				
				for(int i = 1; i <= result.getMetaData().getColumnCount(); i++) {
					value += result.getMetaData().getColumnName(i) + " ";
				}
				
				System.out.println(value);
			}
			catch (SQLException e) {
				e.printStackTrace();
			}
		}
		catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
	private static void select_all(Connection connection) {
		try {
			Statement statement = connection.createStatement();
			
			String select = "SELECT * FROM sample";
			ResultSet result = statement.executeQuery(select);
			
			while(result.next()) {
				String value = "";
				for(int i = 1; i <= result.getMetaData().getColumnCount(); i++) {
					value += result.getString(i) + " ";
				}
				System.out.println(value);
			}
		}
		catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
```

首先创建标准 JDBC 连接。JDBC 是一个抽象层，因此关键在于连接字符串：`jdbc:sqlserver` 告诉程序使用 Microsoft SQL Server 驱动连接 Babelfish。

其余代码基本上就是普通的 JDBC 应用程序。
