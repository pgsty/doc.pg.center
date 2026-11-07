---
title: 新增Oracle兼容模式的端口与IP
linkTitle: 端口与IP
description: IvorySQL v5.6 文档：新增Oracle兼容模式的端口与IP。
type: docs
weight: 180
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.9.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#objective}

- 为了将Oracle端口、IP与PG的端口IP进行区分。现需要增加对ORAPORT和ORAHOST的处理;

## 2. 功能 {#function}

- 新增ivoryhost：需要在连接时新增参数ivoryhost即可指定，其功能类似 host;

- 新增ivoryport：相较于host，port的功能相对复杂一些。其中涉及到可以在configure阶段配置，连接阶段指定端口;

## 3. 测试用例： {#test-method}

```
   ./configure --with-oraport=5555
   ./initdb ....
   ./pg_ctl -D ../data start

   ./pg_ctl -o "-p 5433 -o 1522" -D ../data
```
