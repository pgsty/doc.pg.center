---
title: sysguid() function
linkTitle: sys_guid Function
description: 'IvorySQL v5.6 documentation: sysguid() function.'
type: docs
weight: 290
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.20.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Purpose {#purpose}

IvorySQL’s sys_guid() is a powerful random number generation function that generates and returns a 16-byte database-level unique identifier (raw value).

## 2. Usage example {#usage-example}

```
ivorysql=# select sys_guid() from dual;
              sys_guid
------------------------------------
 \x3ed9426c8a093442a38bea09a74f44a1
(1 row)
```

## 3. The sys_guid function can generate default values for primary keys when creating a table {#the-sys_guid-function-can-generate-default-values-for-primary-keys-when-creating-a-table}

```
create table student
(
student_id raw(16) default sys_guid() primary key,
student_name varchar2(100) not null
);
```

## 4. The primary key is automatically populated when new data is added {#the-primary-key-is-automatically-populated-when-new-data-is-added}

```
insert into student(student_name) values ('Steven');
```
