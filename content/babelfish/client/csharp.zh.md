---
title: 使用 C# 编程
linkTitle: C# / .NET
description: 在 C# 中建立连接、读取记录并执行事务。
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_client/csharp.md
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

## 使用 C# 编程 {#programming-in-c}

Microsoft SQL Server 是 Windows 平台上主流的数据库系统之一，C# 则是这一生态中常用的语言。因此，有必要了解如何从 C# 建立连接并读取数据。

### C# 示例代码 {#sample-code-in-c}

先看示例：

```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace sample
{
    class Program
    {
        static void Main(string[] args)
        {
            // Setting up MSSQL Credentials
            SqlConnection con;

            string conString = "Server=" + @"PUT_HOSTNAME_HERE" + ";" +
                               "User id=" + "PUT_USERNAME_HERE" + ";" +
                               "Password=" + "PUT_PASSWORD_HERE" + ";" +
                               "Database=" + "PUT_DATABASE_HERE" + ";" +
                               "MultipleActiveResultSets=true;";

            con = new SqlConnection(conString);
            SqlCommand cmd = new SqlCommand();

            // Creating MSSQL Connection
            try
            {
                con.Open();
                Console.WriteLine("Connection established\n") ;
            }
            catch
            {
                Console.WriteLine("Can not connect to database!\nPlease check credentials!");
                Environment.Exit(1);
            }

            string sqlQuery = "";

            // Select values example
            select_all(con);

            // Transaction example
            // Insert values into sample table
            cmd = con.CreateCommand();
            SqlTransaction transaction = con.BeginTransaction("SampleTransaction");

            try
            {
                sqlQuery = "INSERT INTO sample VALUES(@vorname, @nachname, @persoid)";
                cmd.Parameters.AddWithValue("@vorname", "Max");
                cmd.Parameters.AddWithValue("@nachname", "Mustermann");
                cmd.Parameters.AddWithValue("@persoid", "1020");
                cmd.CommandType = System.Data.CommandType.Text;
                cmd.CommandText = sqlQuery;
                cmd.Transaction = transaction;

                cmd.ExecuteNonQuery();

                cmd.Parameters.Clear();
                cmd.Parameters.AddWithValue("@vorname", "Erika");
                cmd.Parameters.AddWithValue("@nachname", "Musterfrau");
                cmd.Parameters.AddWithValue("@persoid", "1021");

                cmd.ExecuteNonQuery();

                transaction.Commit();

                Console.WriteLine("\nInsert successful!\n");
            }
            catch
            {
                transaction.Rollback();
                Console.WriteLine("\nInsert failed!\n");
            }

            select_all(con);

            // Removing inserted values
            sqlQuery = "DELETE FROM sample WHERE vorname = 'Max' or vorname = 'Erika'";
            cmd = con.CreateCommand();
            cmd.CommandText = sqlQuery;

            int row_count = cmd.ExecuteNonQuery();

            // Select metadata
            // Select row count from delete
            Console.WriteLine("\nDeleted rows: " + row_count + "\n");

            // Select column names from table
            sqlQuery = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sample'";
            cmd = con.CreateCommand();
            cmd.CommandText = sqlQuery;

            SqlDataReader reader = cmd.ExecuteReader();

            string value = "";

            while (reader.Read())
            {
                value += reader.GetValue(0) + " ";
            }

            Console.WriteLine(value);
            reader.Close();

            // Closing connection
            con.Close();
            Console.WriteLine("\nConnection closed!");
        }

        private static void select_all(SqlConnection con)
        {
            string sqlQuery = "SELECT * FROM sample";
            SqlCommand cmd = con.CreateCommand();
            cmd.CommandText = sqlQuery;
            SqlDataReader reader = cmd.ExecuteReader();

            while (reader.Read())
            {
                string value = "";
                for (int i = 0; i != reader.FieldCount; i++)
                {
                    value += reader.GetValue(i) + " ";
                }
                Console.WriteLine(value);
            }

            reader.Close();
        }

    }
}
```

代码比较直接：首先创建并打开连接。在 C# 中，可使用 `try`/`catch` 处理错误；本例在无法建立连接时直接终止程序。

然后调用 `select_all` 函数。它创建一条 SQL 命令，读取 `sample` 表中的全部数据，遍历每一行和每一列，并输出到屏幕，最后关闭 `SqlDataReader`。这展示了从 Babelfish 读取数据的基本方法。

接下来演示事务处理：调用 `BeginTransaction` 开启事务，执行 SQL 后提交，并通过 `try`/`catch` 处理错误。

可以使用 Microsoft Studio 或其他工具编译代码。关键在于，访问 Babelfish 的代码可以采用与直接访问 Microsoft SQL Server 相同的编写方式。
