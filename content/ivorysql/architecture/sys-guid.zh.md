---
title: sysguid() 函数
linkTitle: sys_guid 函数
description: IvorySQL v5.6 文档：sysguid() 函数。
type: docs
weight: 680
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/6.3.10.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

IvorySQL的sys_guid() 是一个强大的随机数产生函数，它产生并返回一个由16个字节组成的数据库级别唯一的标识符(原始值)。

## 2. 实现说明 {#implementation-description}

IvorySQL的sys_guid()函数通过修改插件uuid-ossp的代码实现。为了充分利用uuid的多种基础库，采用如下逻辑：

1.  如果系统有uuid-ossp，就使用uuid_make();

2.  如果系统有uuid-e2fs，就使用 uuid_generate_random();

3.  否则就调用 arc4random();

同时修改代码使得IvorySQL能够自动载入uuid-ossp插件。
