---
title: 包
linkTitle: 包
description: IvorySQL v5.6 文档：包。
type: docs
weight: 210
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.12.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---


## 1. 目的 {#objective}

IvorySQL提供了兼容Oracle自定义包的功能。包（package）是一个封装的相关程序对象集合，这些对象存储在数据库中。程序对象包括过程、函数、变量、常量、游标和异常。

本文档旨在为使用人员提供一个深入了解自定义包实现的过程。

## 2. 功能说明 {#function-descriptions}

IvorySQL提供了兼容Oracle自定义包的功能，包括包和包体的创建、修改和描述，在PostgreSQL交互终端（psql）中增加了与包相关的命令，新增了 \dk 命令。

### 2.1. 创建包规范 {#create-the-specification-of-a-package}

使用CREATE OR REPLACE PACKAGE语句创建或替换一个包的规范。包是相关的存储过程、函数、和其他程序对象的集合，在数据库中作为一个单元存储。包规范声明这些对象，在包体中定义这些对象。

在自己的模式下创建或替换一个包规范，必须有CREATE PROCEDURE系统权限，如果在其他用户的模式下创建或替换一个包，则需要有CREATE ANY PROCEDURE系统权限。

### 2.2. 创建包体 {#create-package-body}

使用CREATE OR REPLACE PACKAGE BODY语句创建或替换一个包体。创建包体需要有与创建包规范一样的权限，要求包体与包规范在同一个模式下，且包规范必须存在，该语句定义包规范中声明的对象。

当包规范中有cursor或子过程时，那么必须拥有一个包体去定义它，否则包体是可选的。

### 2.3. 更新包 {#alter-package}

使用ALTER PACKAGE语句来改变包的属性。执行ALTER PACKAGE语句的权限要求：必须是包的所有者，或者具有ALTER ANY PROCEDURE权限才能修改其他用户的包。

### 2.4. 删除包和包体 {#drop-package-and-package-body}

DROP PACKAGE语句删除数据库中的一个存储包。这个语句会同时删除包体和包规范。DROP PACKAGE BODY则只删除包体。

不能使用此语句删除包中的一个单独对象。权限要求：包必须在用户模式下，或用户有DROP ANY PROCEDURE系统权限。

### 2.5. 丢弃包 {#discard-package}

DISCARD PACKAGE功能是为了兼容PostgreSQL的DISCARD功能而做的。

### 2.6. 在psql中使用 \dk&#91;+&#93; 查看包与包体定义 {#use-dk-in-psql-for-package-and-package-body-information}

psql中支持 \dk&#91;+&#93; 命令查看包与包体的定义信息。

|              |                             |
|--------------|-----------------------------|
| 命令         | 描述                        |
| \dk&#91;+&#93;     | 列出当前能看到的包信息      |
| \dk&#91;+&#93; xxx | 列出xxx包的包规范和包体内容 |

## 3. 测试用例 {#test-cases}

### 3.1. 创建包规范 {#create-the-specification-of-a-package-2}

```
ivorysql=# create or replace package pkg is
ivorysql-#   var1 integer;
ivorysql-#   var2 integer;
ivorysql-#   function test_f(id integer) return integer;
ivorysql-#   procedure test_p(id integer);
ivorysql-# end;
ivorysql-# /
CREATE PACKAGE
```

### 3.2. 创建包体 {#create-package-body-2}

```
ivorysql=# create or replace package body pkg is
ivorysql-#   var3 integer;
ivorysql-#   function test_f(id integer) return integer is
ivorysql-#   begin
ivorysql-#     dbms_output.put_line('pkg test_f');
ivorysql-#     return id;
ivorysql-#   end;
ivorysql-#   procedure test_p(id integer) is
ivorysql-#   begin
ivorysql-#     dbms_output.put_line('pkg proc');
ivorysql-#   end;
ivorysql-#   --privite function
ivorysql-#   function test_piv1(id integer) return integer is
ivorysql-#   begin
ivorysql-#      return id;
ivorysql-#   end;
ivorysql-#   --privite procedure
ivorysql-#   procedure test_piv2(id integer) is
ivorysql-#   begin
ivorysql-#     dbms_output.put_line('privite proc');
ivorysql-#   end;
ivorysql-# begin
ivorysql-#    var1 := 1;
ivorysql-#    var2 := 2;
ivorysql-#    var3 := 4;
ivorysql-# end;
ivorysql-# /
CREATE PACKAGE BODY
```

### 3.3. 更新包 {#alter-package-2}

```
ivorysql=# alter package pkg noneditionable;
ALTER PACKAGE
```

### 3.4. 删除包和包体 {#drop-package-and-package-body-2}

```
ivorysql=# Drop package pkg;
DROP PACKAGE

ivorysql=# Drop package body pkg;
DROP PACKAGE BODY
```

### 3.5. 丢弃包 {#discard-package-2}

```
ivorysql=# discard package;
DISCARD PACKAGES
```

### 3.6. 在psql中使用 \dk&#91;+&#93; 查看包与包体定义 {#use-dk-in-psql-for-package-and-package-body-information-2}

```
ivorysql=# \dk
       List of packages
 Schema |   Name   |  Owner
--------+----------+----------
 public | pkg      | ivorysql
 public | test_pkg | ivorysql
(2 rows)

ivorysql=# \dk pkg
     List of packages
 Schema | Name |  Owner
--------+------+----------
 public | pkg  | ivorysql
(1 row)

ivorysql=# \dk pkg1
Did not find any package named "pkg1".

ivorysql=# \dk+
                                                                                   List of packages
 Schema |   Name   |  Owner   | Security | Editionable | Use Collation |                 Specification                 |                         Package Body

--------+----------+----------+----------+-------------+---------------+-----------------------------------------------+-----------------------------------------------------
---------
 public | pkg      | ivorysql | definer  | Editionable | default       | var1 integer;                                +|
        |          |          |          |             |               | var2 integer;                                +|
        |          |          |          |             |               | function test_f(id integer) return integer;  +|
        |          |          |          |             |               | procedure test_p(id integer);                +|
        |          |          |          |             |               | end                                           |
 public | test_pkg | ivorysql | definer  | Editionable | default       | var1 integer;                                +| FUNCTION test_f(id integer) RETURN integer IS
        +
        |          |          |          |             |               |   FUNCTION test_f(id integer) RETURN integer;+|   BEGIN
        +
        |          |          |          |             |               | end                                           |     dbms_output.put_line('invoke function test_pkg.t
est_f');+
        |          |          |          |             |               |                                               | RETURN 23;
        +
        |          |          |          |             |               |                                               |   end;
        +
        |          |          |          |             |               |                                               | BEGIN
        +
        |          |          |          |             |               |                                               |   var1 := 23;
        +
        |          |          |          |             |               |                                               | end
(2 rows)
```
