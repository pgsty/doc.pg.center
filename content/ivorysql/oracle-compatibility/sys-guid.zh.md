---
title: sysguid() 函数
linkTitle: sys_guid 函数
description: IvorySQL v5.6 文档：sysguid() 函数。
type: docs
weight: 290
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.20.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

IvorySQL的sys_guid() 是一个强大的随机数产生函数，它产生并返回一个由16个字节组成的数据库级别唯一的标识符(原始值)。

## 2. 使用示例 {#usage-example}

```
ivorysql=# select sys_guid() from dual;
              sys_guid
------------------------------------
 \x3ed9426c8a093442a38bea09a74f44a1
(1 row)
```

## 3. sys_guid函数在建表时可以作为主键 {#the-sys_guid-function-can-generate-default-values-for-primary-keys-when-creating-a-table}

```
create table student
(
student_id raw(16) default sys_guid() primary key,
student_name varchar2(100) not null
);
```

## 4. 新增数据时自动填充主键 {#the-primary-key-is-automatically-populated-when-new-data-is-added}

```
insert into student(student_name) values ('Steven');
```
