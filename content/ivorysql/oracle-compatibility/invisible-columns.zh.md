---
title: 不可见列
linkTitle: 不可见列
description: IvorySQL v5.6 文档：不可见列。
type: docs
weight: 220
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.13.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#objective}

本功能的引入是为了兼容Oracle的不可见列功能，将使数据库设计更加简洁，数据管理的灵活性得到提高，用户可以更好地控制列的可见性。

在应用迁移过程中，不可见列也很有用。使新列不可见意味着它们不会被任何现有应用程序看到，但仍然可以被任何新应用程序引用，从而使应用程序的在线迁移更加简单。

## 2. 功能说明 {#function-descriptions}

不可见列功能使用户能够在执行诸如SELECT \* 等操作时隐藏特定列。可以使用不可见列对表进行更改，而不会干扰使用该表的应用程序。对表的任何通用访问都不会显示不可见的列，必须通过列名显式引用不可见列，查询和其他操作才能访问不可见列。

在Oracle模式下，psql的扩展描述命令（\d+）增加了对不可见列的支持。

## 3. 测试用例 {#test-cases}

### 3.1. 创建包含不可见列的表 {#create-a-table-with-invisible-columns}

```
ivorysql=# CREATE TABLE mytable (a INT, b INT INVISIBLE, c INT);
CREATE TABLE
```

### 3.2. 向不可见列插入值 {#insert-values-into-invisible-columns}

只有在INSERT语句中显式指定不可见列时，才能向不可见列插入值。向包含不可见列的表插入值时不能省略列列表，否则会报错。

```
ivorysql=# INSERT INTO mytable (a, b, c) VALUES (1,2,3);
INSERT 0 1

ivorysql=# INSERT INTO mytable VALUES (4,5,6);
ERROR:  INSERT has more expressions than target columns
LINE 1: INSERT INTO mytable  VALUES (4,5,6);
```

### 3.3. 显示不可见列的输出 {#display-output-for-invisible-columns}

使用SELECT语句查询时，如果要显示不可见列信息，必须显式指定该不可见列，否则将不显示该不可见列。

```
ivorysql=# select * from mytable;
 a | c
---+---
 1 | 3
(1 row)

ivorysql=# select a,b,c from mytable;
 a | b | c
---+---+---
 1 | 2 | 3
(1 row)
```

### 3.4. 在Oracle模式下psql扩展描述命令（\d+）对不可见列的支持 {#support-for-invisible-columns-in-psql-extended-describe-d-in-oracle-mode}

```
ivorysql=# \d+ mytable
                                                   Table "public.mytable"
 Column |      Type       | Collation | Nullable | Default | Invisible | Storage | Compression | Stats target | Description
--------+-----------------+-----------+----------+---------+-----------+---------+-------------+--------------+-------------
 a      | pg_catalog.int4 |           |          |         |           | plain   |             |              |
 b      | pg_catalog.int4 |           |          |         | invisible | plain   |             |              |
 c      | pg_catalog.int4 |           |          |         |           | plain   |             |              |
Access method: heap
```

## 4. 限制 {#limitations}

- 目前不支持modify column，将在未来版本实现；

- 在Oracle中，不可见列和列顺序有特别的注意事项。当一个表包含一个或多个不可见列时，这些不可见列不会包含在表的列顺序中。目前我们尚未对这块做处理。
