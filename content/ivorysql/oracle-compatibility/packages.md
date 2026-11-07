---
title: Package
linkTitle: Package
description: 'IvorySQL v5.6 documentation: Package.'
type: docs
weight: 210
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.12.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---


## 1. Objective {#objective}

IvorySQL provides compatibility for Oracle packages. A package is an encapsulated collection of related program objects stored together in the database. Program objects are procedures, functions, variables, constants, cursors, and exceptions.

This document aims to provide a comprehensive understanding of the process of implementing custom packages.

## 2. Function descriptions {#function-descriptions}

IvorySQL provides compatibility for Oracle custom packages, including creation, alteration, and deletion of packages and package bodies. We also add support for package-related commands in the PostgreSQL interactive terminal (psql) with the new \dk command.

### 2.1. Create the specification of a package {#create-the-specification-of-a-package}

The CREATE OR REPLACE PACKAGE statement is used to create or replace the specification of a package. A package is a collection of related stored procedures, functions, and other program objects, stored as a single unit in the database. The package specification declares these objects, and the package body defines them.

To create or replace the specification of a package in your own schema, you must have the CREATE PROCEDURE system privilege. If you are creating or replacing a package in another user’s schema, you need the CREATE ANY PROCEDURE system privilege.

### 2.2. Create package body {#create-package-body}

The CREATE OR REPLACE PACKAGE BODY statement is used to create or replace a package body. To create a package body requires the same privileges as creating the specification of a package, and it is required that the package body and package specification be in the same schema, with the package specification already existing. This statement defines the objects declared in the package specification.

When the package specification contains cursors or subprograms, a package body must be present to define them. Otherwise, the package body is optional.

### 2.3. Alter package {#alter-package}

The ALTER PACKAGE statement is used to modify the properties of a package.The privileges required to execute the ALTER PACKAGE statement are: you must be the owner of the package or have the ALTER ANY PROCEDURE privilege to modify packages owned by other users.

### 2.4. Drop package and package body {#drop-package-and-package-body}

The DROP PACKAGE statement deletes a package in the database. This statement will remove both the package body and the package specification.The DROP PACKAGE BODY statement only deletes the package body.

It is not possible to delete a single object within the package using this statement. The privileges required:the package must be in the user’s schema, or the user must have the DROP ANY PROCEDURE system privilege.

### 2.5. DISCARD PACKAGE {#discard-package}

The DISCARD PACKAGE functionality is implemented for compatibility with PostgreSQL’s DISCARD feature.

### 2.6. Use \dk&#91;+&#93; in psql for package and package body information {#use-dk-in-psql-for-package-and-package-body-information}

In psql, \dk&#91;+&#93; is used to view the definition information of packages and package bodies.

|  |  |
|----|----|
| Command | Descriptions |
| \dk&#91;+&#93; | List the package information currently visible. |
| \dk&#91;+&#93; xxx | List the package specification and package body content of the xxx package. |

## 3. Test cases {#test-cases}

### 3.1. Create the specification of a package {#create-the-specification-of-a-package-2}

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

### 3.2. Create package body {#create-package-body-2}

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

### 3.3. Alter package {#alter-package-2}

```
ivorysql=# alter package pkg noneditionable;
ALTER PACKAGE
```

### 3.4. Drop package and package body {#drop-package-and-package-body-2}

```
ivorysql=# Drop package pkg;
DROP PACKAGE

ivorysql=# Drop package body pkg;
DROP PACKAGE BODY
```

### 3.5. DISCARD PACKAGE {#discard-package-2}

```
ivorysql=# discard package;
DISCARD PACKAGES
```

### 3.6. Use \dk&#91;+&#93; in psql for package and package body information {#use-dk-in-psql-for-package-and-package-body-information-2}

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
