---
title: '%ROWTYPE、%TYPE'
linkTitle: '%TYPE、%ROWTYPE'
description: IvorySQL v5.6 文档：%ROWTYPE、%TYPE。
type: docs
weight: 250
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.16.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

IvorySQL提供了兼容Oracle的plsql数据类型功能，包括%TYPE、%ROWTYPE。

本文档旨在为使用人员介绍%TYPE、%ROWTYPE的功能。

## 2. 功能说明 {#function-descriptions}

IvorySQL提供了兼容Oracle的%TYPE、%ROWTYPE功能，包括如下内容。

### 2.1. 引用发生改变，%TYPE或%ROWTYPE声明的变量也相应改变。 {#if-the-reference-changes-variables-declared-with-type-or-rowtype-will-change-accordingly}

创建表以及函数。

```
CREATE TABLE t1(id int, name varchar(20));

--function's parameter datatype is tablename.columnname%TYPE
CREATE OR REPLACE FUNCTION fun1(v t1.id%TYPE) RETURN varchar AS
BEGIN
  RETURN v;
END;
/
```

函数状态是valid，并且执行函数能够成功。

```
SELECT prostatus FROM pg_proc WHERE proname like 'fun1'; --v
 prostatus
-----------
 v
(1 row)

SELECT fun1(1) FROM dual;
 fun1
------
 1
(1 row)
```

修改引用的先前定义的声明，函数状态变为invalid，但是函数能够执行成功。

```
ALTER TABLE t1 ALTER COLUMN id TYPE varchar(20);

SELECT prostatus FROM pg_proc WHERE proname like 'fun1'; --n
 prostatus
-----------
 n
(1 row)

--after changing the column id type from int to varchar, call the function again
SELECT fun1('a') FROM dual;  --successfully
 fun1
------
 a
(1 row)
```

重新编译函数，状态重新变成valid。

```
ALTER FUNCTION fun1 COMPILE;
SELECT prostatus FROM pg_proc WHERE proname like 'fun1'; --v
 prostatus
-----------
 v
(1 row)
```

### 2.2. %TYPE声明的变量继承引用变量的约束 {#variables-declared-with-type-inherit-the-constraints-of-the-referenced-variable}

示例：

```
--the following testcase will fail
DECLARE
  name     VARCHAR(25) NOT NULL := 'Niu';
  surname  name%TYPE ;
BEGIN
  raise notice 'name=%' ,name;
  raise notice 'surname=%' ,surname;
END;
/

ERROR:  variable "surname" must have a default value, since it's declared NOT NULL
LINE 3:   surname  name%TYPE ;
          ^
```

### 2.3. 表名%ROWTYPE或视图名%ROWTYPE作为函数或存储过程的参数类型和函数返回值类型 {#use-table_namerowtype-or-view_namerowtype-as-the-parameter-type-of-a-function-stored-procedure-or-the-return-type-of-a-function}

示例：

```
CREATE TABLE employees(first_name varchar(20) not null,
last_name varchar(20) not null,
phone_number varchar(50));

INSERT INTO employees VALUES ('Steven','Niu','1-650-555-1234');

CREATE OR REPLACE PROCEDURE p0(v employees%ROWTYPE) AS
BEGIN
  raise notice 'v.first_name = %, v.last_name = %, v.phone_number = %',
    v.first_name, v.last_name, v.phone_number;
END;
/

DECLARE
  a employees%ROWTYPE;
BEGIN
  select * into a from employees ;
  raise notice 'a=%', a;
  call p0(a);
END;
/

NOTICE:  a=(Steven,Niu,1-650-555-1234)
NOTICE:  v.first_name = Steven, v.last_name = Niu, v.phone_number = 1-650-555-1234

\df p0
                        List of functions
 Schema | Name | Result data type |  Argument data types   | Type
--------+------+------------------+------------------------+------
 public | p0   |                  | IN v employees%ROWTYPE | proc
(1 row)
```

### 2.4. INSERT语句增强 {#enhancement-to-insert-statement}

INSERT语句增强支持把一个%ROWTYPE声明的变量插入表中。

语法为：

```
INSERT INTO table_name VALUES row_variable ;
```

示例：

```
CREATE TABLE t1(id int, name varchar(20));

DECLARE
  v1 t1%ROWTYPE;
BEGIN
  FOR i IN 1 .. 5 LOOP
    v1.id := i;
    v1.name := 'a' || i;
    INSERT INTO t1 VALUES v1;
  END LOOP;
END;
/


SELECT * FROM t1;
 id | name
----+------
  1 | a1
  2 | a2
  3 | a3
  4 | a4
  5 | a5
(5 rows)
```

### 2.5. UPDATE语句增强 {#enhancement-to-update-statement}

示例：

```
CREATE TABLE t1(id int, name varchar(20));

DELETE FROM t1;

DECLARE
  v1 t1%ROWTYPE;
  v2 t1%ROWTYPE;
BEGIN
  v1.id := 11;
  v1.name := 'abc';
  INSERT INTO t1 VALUES v1;
  v2.id := 22;
  v2.name := 'new';
  UPDATE t1 SET ROW = v2;
END;
/

SELECT * FROM t1;
 id | name
----+------
 22 | new
(1 row)
```
