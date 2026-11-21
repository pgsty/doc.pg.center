---
title: hstore
description: hstore 在单个值中存储一组键值对。
weight: 140
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/hstore.md
---

`hstore` 模块实现 `hstore` 数据类型，用于在单个值中存储一组键值对。这适用于多种场景，例如包含大量很少查询的属性的行，或半结构化数据。

Apache Cloudberry 的 `hstore` 模块与 PostgreSQL 的 `hstore` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `hstore`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION hstore;
```

## 模块文档 {#module-documentation}

此模块定义的数据类型、操作符和函数的详细信息，参见 PostgreSQL 文档中的 [hstore](https://www.postgresql.org/docs/14/hstore.html)。
