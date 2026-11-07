---
title: 双模式设计
linkTitle: 双模式设计
description: IvorySQL v5.6 文档：双模式设计。
type: docs
weight: 760
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.4.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#objective}

- 为了满足PG模式和兼容Oracle模式， IvorySQL在initdb时，可以指定-m参数，来获取PG模式数据库或Oracle兼容模式数据库。

> [!TIP]
>
> 1.  不指定-m参数时，默认为Oracle兼容模式
>
> 2.  指定-m参数为pg时，数据库将不再兼容Oracle语法

## 2. 功能 {#function}

- initdb -m 初始化，需要判断不同的模式，其中Oracle模式下，需要执行postgres_oracle.bki的SQL语句;

- 启动时会根据初始化模式，判断是否为oracle兼容模式。

```
database_mode：用于表示初始化模式；
database_mode=DB_PG，PG模式，且不可切换；
database_mode=DB_ORACLE，Oracle兼容模式；
```

## 3. 测试用例 {#test-cases}

```
初始化PG模式：
./initdb -D ../data -m pg

初始化oracle兼容模式：
./initdb -D ../data -m oracle
或
./initdb -D ../data
```
