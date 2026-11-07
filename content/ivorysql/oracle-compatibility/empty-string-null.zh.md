---
title: 兼容Oracle 空字符串转NULL
linkTitle: 空字符串转null
description: IvorySQL v5.6 文档：兼容Oracle 空字符串转NULL。
type: docs
weight: 300
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.21.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

- 在 IvorySQL 的 Oracle 兼容模式下,支持将空字符串转换成NULL进行存储,提供与Oracle数据库一致的行为。

## 2. 功能说明 {#feature-description}

- Oracle兼容模式下支持将空字符串转换成NULL进行存储。

- 通过参数 `ivorysql.enable_emptystring_to_null` 控制该特性,默认值为 `on`。

- 当该参数开启时,插入空字符串会自动转换为NULL值存储。

- 可以通过 `IS NULL` 条件查询到转换后的NULL值。

## 3. 测试用例 {#test-cases}

```
-- 创建测试表
ivorysql=# create table abc (id int);
CREATE TABLE

-- 查看空字符串转NULL参数状态
ivorysql=# show ivorysql.enable_emptystring_to_null;
 ivorysql.enable_emptystring_to_NULL
-------------------------------------
 on
(1 row)

-- 插入空字符串
ivorysql=# insert into abc values('');
INSERT 0 1

-- 查询表数据,显示为NULL
ivorysql=# select * from abc;
 id
\----

(1 row)

-- 使用IS NULL条件查询
ivorysql=# select * from abc where id is null;
 id
\----

(1 row)
```
