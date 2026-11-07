---
title: Ivorysql框架设计
linkTitle: 框架设计
description: IvorySQL v5.6 文档：Ivorysql框架设计。
type: docs
weight: 740
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#目的}

- 在对原有的PostgreSQL改动最小的前提下，实现对Oracle兼容。我们需要实现双parser、双端口、模式PL/PGSQL实现PL/iSQL的框架。实现流程图如下：

![p18](/ivorysql/assets/images/upstream/8040c462f47de5b85fb0692d71b3b01f8760858e0e7cb416831441954e71e7aa.png)

## 2. 功能 {#功能}

### 2.1. 双端口设计 {#双端口设计}

- 保持了Ivorysql 5432端口兼容原有postgres情况，因此 Ivorysql采用另一个独立的端口登录，默认为1521。从该端口登录，默认采用Oracle兼容模式。如果需要从5432端口登录且还要进入兼容模式，则需要通过`SET ivorysql.compatible_mode=oracle`进行设置。

### 2.2. parser模块设计 {#parser模块设计}

- 为了将Oracle语法与PostgreSQL语法间的相互干扰降到最低，因此新增parser模块，用于处理Oracle相关的语法。

### 2.3. 新增PL/iSQL过程语言 {#新增plisql过程语言}

- 新增PL/iSQL过程语言兼容Oracle的PL/SQL过程语言。
