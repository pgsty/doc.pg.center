---
title: 动态定义游标
linkTitle: 动态游标
description: 通过临时表重写动态定义的游标。
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_workaround/dynamically_defined_cursor.md
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

## 动态定义游标 {#dynamically-defined-cursors}

原文所述版本的 Babelfish 无法识别在存储过程或函数中动态定义的游标。变通方法是用临时表重写游标逻辑。

准备代码：

```sql
DROP TABLE IF EXISTS my_table
GO
CREATE TABLE my_table (c1 int, c2 varchar(64), c3 tinyint, c4 money, c5 datetime)
GO
```

以下过程可在 SQL Server 中编译、运行，但无法在 Babelfish 中运行：

```sql
DROP PROC IF EXISTS sp_cur_test
GO

CREATE PROC sp_cur_test (@TableName varchar(100))
AS
DECLARE @exec_str VARCHAR(4000);
DECLARE @table_schema VARCHAR(100), @table_name VARCHAR(100), @column_name VARCHAR(100);
SELECT @exec_str = 'DECLARE fetch_cursor
CURSOR FOR SELECT table_schema, table_name, column_name
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = ''' + @TableName + '''';

EXEC(@exec_str);
OPEN fetch_cursor;
FETCH fetch_cursor INTO @table_schema, @table_name, @column_name;
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @table_schema;
    PRINT @table_name;
    PRINT @column_name;
    FETCH fetch_cursor INTO @table_schema, @table_name, @column_name;
  END;
CLOSE fetch_cursor;
DEALLOCATE fetch_cursor;
GO

execute sp_cur_test 'MY_TABLE';
GO
```

改用临时表重写游标后，以下过程可在 SQL Server 和 Babelfish 中运行：

```sql
DROP PROC IF EXISTS sp_cur_test;
GO

CREATE PROC sp_cur_test (@TableName varchar(100))
AS
DECLARE @exec_str VARCHAR(4000);
DECLARE @table_schema VARCHAR(100), @table_name VARCHAR(100), @column_name VARCHAR(100);
CREATE TABLE #temp_cur (table_schema VARCHAR(100), table_name VARCHAR(100), column_name
VARCHAR(100));
SELECT @exec_str = 'INSERT INTO #temp_cur
SELECT table_schema, table_name, column_name
FROM INFORMATION_SCHEMA.COLUMNS
WHERE lower(table_name) = LOWER(''' + @TableName + ''')';
EXEC(@exec_str);
DECLARE fetch_cursor CURSOR FOR SELECT * FROM #temp_cur;
OPEN fetch_cursor;
FETCH fetch_cursor INTO @table_schema, @table_name, @column_name;
WHILE @@FETCH_STATUS = 0
  BEGIN
    PRINT @table_schema;
    PRINT @table_name;
    PRINT @column_name;
    FETCH fetch_cursor INTO @table_schema, @table_name, @column_name;
  END;
CLOSE fetch_cursor;
DEALLOCATE fetch_cursor;
GO

execute sp_cur_test 'MY_TABLE';
GO
```

关于同时通过 TDS 与 PostgreSQL 端口使用 Babelfish，参见[互操作指南](/zh/babelfish/usage/interoperability/)。
