---
title: NLS Parameters
linkTitle: NLS Parameters
description: 'IvorySQL v5.6 documentation: NLS Parameters.'
type: docs
weight: 260
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.17.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Purpose {#purpose}

National Language Support(NLS), which refers to the localization support functionality provided by Oracle. IvorySQL offers Oracle-compatible NLS parameter functionality.

## 2. Description {#description}

The following parameters are included:

|  |  |
|----|----|
| Parameter Name | Description |
| ivorysql.datetime_ignore_nls_mask | Indicates whether the date format ignores the influence of NLS parameters. Default is 0 . |
| nls_length_semantics | Oracle-compatible parameter that specifies whether the size unit for CHAR , VARCHAR , and VARCHAR2 type modifiers is bytes or characters. |
| nls_date_format | Specifies the default date format, which can be viewed using the SHOW command. Default is 'YYYY-MM-DD' . |
| nls_timestamp_format | Oracle-compatible parameter that controls the format of timestamps. |
| nls_timestamp_tz_format | Oracle-compatible parameter that controls the format of timestamps with time zones. |
| nls_territory | Oracle-compatible parameter that specifies the default region for the database. |
| nls_iso_currency | Oracle-compatible parameter that assigns a unique currency symbol to a specified country or region. |
| nls_currency | Oracle-compatible parameter that specifies the symbol for the local currency, corresponding to the placeholder L in numeric string formats. |

### 2.1. NLS Date Mask Settings {#nls-date-mask-settings}

Example:

``` sql
ivorysql=# set ivorysql.datetime_ignore_nls_mask = 0;
SET
ivorysql=# select '2025-10-15 11:00:00.102030 CST'::oratimestamp ;
ERROR:  datetime format picture ends before converting entire input string
LINE 1: select '2025-10-15 11:00:00.102030 CST'::oratimestamp ;
               ^
ivorysql=# set ivorysql.datetime_ignore_nls_mask = 2;
SET
ivorysql=# select '2025-10-15 11:00:00.102030 CST'::oratimestamp ;
        oratimestamp
----------------------------
 2025-10-15 11:00:00.102030
(1 row)
```

### 2.2. Disabling NLS Date or Timestamp Format {#disabling-nls-date-or-timestamp-format}

Example:

``` sql
ivorysql=# select '2025-10-15 11:00:00.102030 '::oratimestamp ;
        oratimestamp
----------------------------
 2025-10-15 11:00:00.102030
(1 row)

ivorysql=# set nls_timestamp_format="pg";
SET
ivorysql=# select '2025-10-15 11:00:00.102030 '::oratimestamp ;
ERROR:  date format not recognized
LINE 1: select '2025-10-15 11:00:00.102030 '::oratimestamp ;
               ^
```

### 2.3. Parameter `nls_length_semantics` Settings {#parameter-nls_length_semantics-settings}

IvorySQL uses the value of the `nls_length_semantics` parameter to determine the length type, which can be either BYTE or CHAR (default is BYTE )。

Example:

``` sql
ivorysql=# alter session set nls_length_semantics = char;
SET
ivorysql=# create table character_tb(char_c char(6), char_b varchar2(6 byte), char_v varchar(6));
CREATE TABLE
ivorysql=#
ivorysql=# insert into character_tb values('abcdef', '123456', 'OK');
INSERT 0 1
ivorysql=# select * from character_tb ;
 char_c | char_b | char_v
--------+--------+--------
 abcdef | 123456 | OK
(1 row)

ivorysql=# select length(char_b), length(char_c), length(char_v) from character_tb;
 length | length | length
--------+--------+--------
      6 |      6 |      2
(1 row)
```

### 2.4. NLS Currency Symbols Settings {#nls-currency-symbols-settings}

Example:

``` sql
ivorysql=# show ivorysql.identifier_case_switch;
 ivorysql.identifier_case_switch
---------------------------------
 interchange
(1 row)

ivorysql=# set nls_currency to "CHINA";
SET
ivorysql=# show nls_currency;
 nls_currency
--------------
 CHINA
(1 row)

ivorysql=# set nls_currency to "China";
SET
ivorysql=# show nls_currency;
 nls_currency
--------------
 China
(1 row)
```

> [!NOTE]
>
> The behavior of `nls_currency` and `nls_iso_currency` is impacted by the Oracle `ivorysql.identifier_case_switch` compatibility feature.
