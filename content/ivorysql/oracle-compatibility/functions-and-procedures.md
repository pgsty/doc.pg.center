---
title: PL/iSQL function and stored procedure
linkTitle: functions and stored procedures
description: 'IvorySQL v5.6 documentation: PL/iSQL function and stored procedure.'
type: docs
weight: 160
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.7.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Purpose {#purpose}

PostgreSQL supports functions and stored procedures, but there are syntax differences between PostgreSQL and Oracle. To enable Oracle’s PL/SQL statements to run on IvorySQL—i.e., to achieve "syntax compatibility"—IvorySQL adopts the following solution: If an Oracle clause has a counterpart clause with the same function in IvorySQL, it is directly mapped to the corresponding IvorySQL clause; otherwise, only the syntax of the Oracle clause is implemented, while its function is not.

## 2. Compatibility support {#compatibility-support}

The specific Oracle compatibility support includes the following aspects:

### 2.1. EDITIONABLE/NONEDITIONABLE is supported in CREATE FUNCTION syntax {#editionablenoneditionable-is-supported-in-create-function-syntax}

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

### 2.2. Keyword 'RETURN' and 'IS' are supported in CREATE FUNCTION syntax {#keyword-return-and-is-are-supported-in-create-function-syntax}

```
CREATE or replace EDITIONABLE FUNCTION ora_func RETURN integer IS
BEGIN
    RETURN 1;
END;
/
```

### 2.3. In the CREATE FUNCTION syntax, a function can have no parameters, and no parentheses () after the function name {#in-the-create-function-syntax-a-function-can-have-no-parameters-and-no-parentheses-after-the-function-name}

```
CREATE or replace FUNCTION ora_func RETURN integer
SHARING = METADATA
IS
BEGIN
    RETURN 1;
END;
/
```

### 2.4. Increase the number of parameters in CREATE FUNCTION syntax, the max value can be specified by configure command {#increase-the-number-of-parameters-in-create-function-syntax-the-max-value-can-be-specified-by-configure-command}

```
configure --help
    --with-max-funarg=MAXFUNARG
```

### 2.5. Psql uses slash (/) as terminator of statement in CREATE FUNCTION syntax {#psql-uses-slash-as-terminator-of-statement-in-create-function-syntax}

```
CREATE or replace EDITIONABLE FUNCTION ora_func RETURN integer IS
BEGIN
    RETURN 1;
END;
/
```

### 2.6. No DECLARE keyword before variable in CREATE FUNCTION syntax {#no-declare-keyword-before-variable-in-create-function-syntax}

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

### 2.7. Support NOCOPY for OUT parameter in CREATE FUNCTION syntax {#support-nocopy-for-out-parameter-in-create-function-syntax}

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

### 2.8. Support sharing clause in CREATE FUNCTION syntax {#support-sharing-clause-in-create-function-syntax}

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

### 2.9. Support invoker_rights (AUTHID) in CREATE FUNCTION syntax，and change default permission to be DR（DEFINER） {#support-invoker_rights-authid-in-create-function-syntaxand-change-default-permission-to-be-drdefiner}

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

### 2.10. Support ACCESSIBLE BY in CREATE FUNCTION syntax {#support-accessible-by-in-create-function-syntax}

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

### 2.11. Support DEFAULT COLLATION in CREATE FUNCTION syntax {#support-default-collation-in-create-function-syntax}

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

### 2.12. Support deterministic clause in CREATE FUNCTION syntax {#support-deterministic-clause-in-create-function-syntax}

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

### 2.13. Support parallel_enable clause in CREATE FUNCTION syntax {#support-parallel_enable-clause-in-create-function-syntax}

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

### 2.14. Support result_cache clause in CREATE FUNCTION syntax {#support-result_cache-clause-in-create-function-syntax}

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

### 2.15. Support aggregate clause in CREATE FUNCTION syntax {#support-aggregate-clause-in-create-function-syntax}

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

### 2.16. Support pipelined clause in CREATE FUNCTION syntax {#support-pipelined-clause-in-create-function-syntax}

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

### 2.17. Support sql_macro clause in CREATE FUNCTION syntax {#support-sql_macro-clause-in-create-function-syntax}

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

### 2.18. Compatibility with ALTER FUNCTION syntax {#compatibility-with-alter-function-syntax}

```
alter function public.test_func noneditionable;
alter function test_func compile;
alter function test_func compile debug;
alter function test_func compile debug sd = mv;
alter function test_func compile debug reuse settings;
```

### 2.19. Support EDITIONABLE/NONEDITIONABLE in CREATE PROCEDURE syntax {#support-editionablenoneditionable-in-create-procedure-syntax}

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

### 2.20. In the CREATE PROCEDURE syntax, a procedure can have no parameters, and no parentheses () after the procedure name {#in-the-create-procedure-syntax-a-procedure-can-have-no-parameters-and-no-parentheses-after-the-procedure-name}

```
CREATE OR REPLACE EDITIONABLE PROCEDURE ora_procedure
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.21. Psql uses slash (/) as terminator of statement in CREATE PROCEDURE syntax {#psql-uses-slash-as-terminator-of-statement-in-create-procedure-syntax}

```
CREATE OR REPLACE EDITIONABLE PROCEDURE ora_procedure
IS
        p integer := 20;
begin
        raise notice '%', p;
end;
/
```

### 2.22. Support sharing clause in CREATE PROCEDURE syntax {#support-sharing-clause-in-create-procedure-syntax}

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

### 2.23. Support DEFAULT COLLATION clause in CREATE PROCEDURE syntax {#support-default-collation-clause-in-create-procedure-syntax}

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

### 2.24. Support invoker_rights clause (AUTHID) in CREATE PROCEDURE syntax {#support-invoker_rights-clause-authid-in-create-procedure-syntax}

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

### 2.25. Support ACCESSIBLE BY clause in CREATE PROCEDURE syntax {#support-accessible-by-clause-in-create-procedure-syntax}

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

### 2.26. Compatibility with ALTER PROCEDURE syntax {#compatibility-with-alter-procedure-syntax}

```
alter procedure test_proc editionable;
alter procedure public.test_proc noneditionable;
alter procedure test_proc compile;
alter procedure test_proc compile debug;
alter procedure test_proc compile debug sd = mv;
alter procedure test_proc compile debug reuse settings;
```

### 2.27. Function and procedure can have no parameter {#function-and-procedure-can-have-no-parameter}

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

### 2.28. Views related with function and stored procedure {#views-related-with-function-and-stored-procedure}

```
They can be found in file contrib/ivorysql_ora/src/sysview/sysview--1.0.sql.
Including DBA_PROCEDURES, ALL_PROCEDURES, USER_PROCEDURES, DBA_SOURCE, ALL_SOURCE, USER_SOURCE, DBA_ARGUMENTS, ALL_ARGUMENTS, USER_ARGUMENTS etc.
```

### 2.29. Support (--) and (/\* \*/) {#support-and}

### 2.30. pg_dump adds one slash (/) at the end of definition of function/procedure when backup SQL file {#pg_dump-adds-one-slash-at-the-end-of-definition-of-functionprocedure-when-backup-sql-file}
