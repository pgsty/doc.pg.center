---
title: PL/iSQL函数与存储过程
linkTitle: 函数与存储过程
description: IvorySQL v5.6 文档：PL/iSQL函数与存储过程。
type: docs
weight: 160
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.7.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

PostgreSQL支持函数(FUNCTION)和存储过程(PROCEDURE)，但是在语法上和Oracle有差异，为了让Oracle的PLSQL语句可以在IvorySQL上执行，也就是“语法兼容”，IvorySQL采取这样的解决方案：如果Oracle的子句在IvorySQL中存在相同功能的子句，则直接映射为对应的IvorySQL子句，否则只实现其语法，不实现其功能。

## 2. 兼容支持 {#compatibility-support}

具体的Oracle兼容支持包括以下几个方面：

### 2.1. CREATE FUNCTION 语法支持 EDITIONABLE/NONEDITIONABLE {#editionablenoneditionable-is-supported-in-create-function-syntax}

```
CREATE or replace EDITIONABLE FUNCTION ora_func RETURN integer AS
BEGIN
    RETURN 1;
END;
/

CREATE or replace NONEDITIONABLE FUNCTION ora_func RETURN integer IS
BEGIN
    RETURN 1;
END;
/
```

### 2.2. CREATE FUNCTION 语法支持 RETURN/IS 关键字，无需指定语言 {#keyword-return-and-is-are-supported-in-create-function-syntax}

```
CREATE or replace EDITIONABLE FUNCTION ora_func RETURN integer IS
BEGIN
    RETURN 1;
END;
/
```

### 2.3. CREATE FUNCTION 语法函数没有参数，函数名后面不带() {#in-the-create-function-syntax-a-function-can-have-no-parameters-and-no-parentheses-after-the-function-name}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = METADATA
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.4. CREATE FUNCTION 参数个数增加，最大值可在configure时指定 {#increase-the-number-of-parameters-in-create-function-syntax-the-max-value-can-be-specified-by-configure-command}

```
configure --help
    --with-max-funarg=MAXFUNARG
```

### 2.5. CREATE FUNCTION 语法中 END; 在psql中以/结束 {#psql-uses-slash-as-terminator-of-statement-in-create-function-syntax}

```
CREATE or replace EDITIONABLE FUNCTION ora_func RETURN integer IS
BEGIN
    RETURN 1;
END;
/
```

### 2.6. CREATE FUNCTION 语法变量声明前面没有 DECLARE 关键字 {#no-declare-keyword-before-variable-in-create-function-syntax}

```
CREATE OR REPLACE
FUNCTION ora_func (num1 IN int, num2 IN int)
RETURN int
AS
 num3 int :=10;
 num4 int :=10;
 num5 int;
BEGIN
 num3 := num1 + num2;
 num4 := num1 * num2;
 num5 := num3 * num4;
RETURN num5;
END;
/
CREATE FUNCTION

select ora_func(5,9)from dual;
 ora_func
----------
      630
(1 row)
```

### 2.7. CREATE FUNCTION 语法支持 OUT 参数 NOCOPY 功能 {#support-nocopy-for-out-parameter-in-create-function-syntax}

```
CREATE OR REPLACE FUNCTION test_nocopy(a IN int, b OUT NOCOPY int, c IN OUT NOCOPY int)
RETURN int
IS
BEGIN
   b := a;
   c := a;
   return 1;
END;
/
```

### 2.8. CREATE FUNCTION 语法支持 sharing 子句 {#support-sharing-clause-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = METADATA
IS
BEGIN
    RETURN 1;
END;
/

CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.9. CREATE FUNCTION 语法支持 invoker_rights (AUTHID) 子句，默认权限改成 DR（DEFINER） {#support-invoker_rights-authid-in-create-function-syntaxand-change-default-permission-to-be-drdefiner}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID CURRENT_USER
IS
BEGIN
    RETURN 1;
END;
/

CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.10. CREATE FUNCTION 语法支持 ACCESSIBLE BY {#support-accessible-by-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER ACCESSIBLE BY ( B )
IS
BEGIN
    RETURN 1;
END;
/
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER ACCESSIBLE BY ( A.B )
IS
BEGIN
    RETURN 1;
END;
/
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER ACCESSIBLE BY ( FUNCTION A.B )
IS
BEGIN
    RETURN 1;
END;
/
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
IS
BEGIN
    RETURN 1;
END;
/
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D, PACKAGE E,
TRIGGER F, TYPE G )
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.11. CREATE FUNCTION 语法支持 DEFAULT COLLATION {#support-default-collation-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.12. CREATE FUNCTION 语法支持 deterministic 子句，功能与 IvorySQL 的 IMMUTABLE 相同 {#support-deterministic-clause-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.13. CREATE FUNCTION 语法支持 parallel_enable 子句，功能与 IvorySQL 的 PARALLEL SAFE 相同 {#support-parallel_enable-clause-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.14. CREATE FUNCTION 语法支持 result_cache 子句 {#support-result_cache-clause-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE ( PARTITION A BY RANGE ( B, C ) CLUSTER A BY ( E,F ) )
RESULT_CACHE
IS
BEGIN
    RETURN 1;
END;
/
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE ( PARTITION A BY RANGE ( B, C ) CLUSTER A BY ( E,F ) )
RESULT_CACHE RELIES_ON ()
IS
BEGIN
    RETURN 1;
END;
/
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE ( PARTITION A BY RANGE ( B, C ) CLUSTER A BY ( E,F ) )
RESULT_CACHE RELIES_ON ( data_source1, data_source2)
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.15. CREATE FUNCTION 语法支持 aggregate 子句 {#support-aggregate-clause-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE ( PARTITION A BY RANGE ( B, C ) CLUSTER A BY ( E,F ) )
RESULT_CACHE RELIES_ON ( data_source1, data_source2)
AGGREGATE USING pg_catalog.int4
IS
BEGIN
    RETURN 1;
END;
/
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE ( PARTITION A BY RANGE ( B, C ) CLUSTER A BY ( E,F ) )
RESULT_CACHE RELIES_ON ( data_source1, data_source2)
AGGREGATE USING int
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.16. CREATE FUNCTION 语法支持 pipelined 子句 {#support-pipelined-clause-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE ( PARTITION A BY RANGE ( B, C ) CLUSTER A BY ( E,F ) )
RESULT_CACHE RELIES_ON ( data_source1, data_source2)
AGGREGATE USING int
PIPELINED
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.17. CREATE FUNCTION 语法支持 sql_macro 子句 {#support-sql_macro-clause-in-create-function-syntax}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = NONE AUTHID DEFINER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
DEFAULT COLLATION USING_NLS_COMP
DETERMINISTIC
PARALLEL_ENABLE ( PARTITION A BY RANGE ( B, C ) CLUSTER A BY ( E,F ) )
RESULT_CACHE RELIES_ON ( data_source1, data_source2)
AGGREGATE USING int
PIPELINED TABLE POLYMORPHIC USING pg_catalog.int4
SQL_MACRO
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.18. ALTER FUNCTION 语法兼容 {#compatibility-with-alter-function-syntax}

```
alter function public.test_func noneditionable;
alter function test_func compile;
alter function test_func compile debug;
alter function test_func compile debug sd = mv;
alter function test_func compile debug reuse settings;
```

### 2.19. CREATE PROCEDURE 语法支持 EDITIONABLE / NONEDITIONABLE {#support-editionablenoneditionable-in-create-procedure-syntax}

```
CREATE OR REPLACE EDITIONABLE PROCEDURE ora_procedure
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/

CREATE OR REPLACE NONEDITIONABLE PROCEDURE ora_procedure
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.20. CREATE PROCEDURE 语法函数没有参数，函数名后面不带() {#in-the-create-procedure-syntax-a-procedure-can-have-no-parameters-and-no-parentheses-after-the-procedure-name}

```
CREATE OR REPLACE EDITIONABLE PROCEDURE ora_procedure
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.21. CREATE PROCEDURE 语法中 END; 在psql中以 / 结束 {#psql-uses-slash-as-terminator-of-statement-in-create-procedure-syntax}

```
CREATE OR REPLACE PROCEDURE ora_procedure
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.22. CREATE PROCEDURE 语法支持 sharing 子句 {#support-sharing-clause-in-create-procedure-syntax}

```
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = NONE
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.23. CREATE PROCEDURE 语法支持 DEFAULT COLLATION 子句 {#support-default-collation-clause-in-create-procedure-syntax}

```
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.24. CREATE PROCEDURE 语法支持 invoker_rights (AUTHID) 子句 {#support-invoker_rights-clause-authid-in-create-procedure-syntax}

```
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
AUTHID DEFINER
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.25. CREATE PROCEDURE 语法支持 ACCESSIBLE BY 子句 {#support-accessible-by-clause-in-create-procedure-syntax}

```
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
ACCESSIBLE BY ( B )
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
ACCESSIBLE BY ( A.B )
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
ACCESSIBLE BY ( FUNCTION A.B )
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D )
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
CREATE OR REPLACE PROCEDURE ora_procedure
SHARING = METADATA
DEFAULT COLLATION USING_NLS_COMP
AUTHID CURRENT_USER
ACCESSIBLE BY ( FUNCTION A.B, PROCEDURE C.D, PACKAGE E, TRIGGER F, TYPE G )
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.26. ALTER PROCEDURE 语法兼容 {#compatibility-with-alter-procedure-syntax}

```
alter procedure test_proc editionable;
alter procedure public.test_proc noneditionable;
alter procedure test_proc compile;
alter procedure test_proc compile debug;
alter procedure test_proc compile debug sd = mv;
alter procedure test_proc compile debug reuse settings;
```

### 2.27. 存储过程和函数没有参数，SELECT调用支持不带 () {#function-and-procedure-can-have-no-parameter}

```
create or replace function f_noparentheses
return int is
begin
return 11;
end;
/
select f_noparentheses from dual;

create or replace procedure protest
as
begin
raise notice 'protest';
end;
/
CALL protest();
```

### 2.28. 函数和存储过程相关的视图 {#views-related-with-function-and-stored-procedure}

```
相关视图位于文件 contrib/ivorysql_ora/src/sysview/sysview--1.0.sql 中，包括DBA_PROCEDURES，ALL_PROCEDURES，USER_PROCEDURES，DBA_SOURCE，ALL_SOURCE，USER_SOURCE，DBA_ARGUMENTS，ALL_ARGUMENTS，USER_ARGUMENTS等。
```

### 2.29. 支持—​和/\*\*/两种注释方法 {#support-and}

### 2.30. pg_dump备份SQL脚本文件的备份格式时，在函数的定义最后增加一个斜线 / {#pg_dump-adds-one-slash-at-the-end-of-definition-of-functionprocedure-when-backup-sql-file}
