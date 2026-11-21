---
title: pg_trgm
description: pg_trgm 基于三元组匹配判断字母数字文本的相似性。
weight: 200
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/pg-trgm.md
---

`pg_trgm` 模块提供基于三元组匹配判断字母数字文本相似性的函数和操作符，还提供支持快速搜索相似字符串的 GiST 和 GIN 索引操作符类。

Apache Cloudberry 的 `pg_trgm` 模块与 PostgreSQL 的 `pg_trgm` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `pg_trgm`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION pg_trgm;
```

## 模块文档 {#module-documentation}

此模块的函数、操作符和索引操作符类的详细信息，参见 PostgreSQL 文档中的 [pg_trgm](https://www.postgresql.org/docs/14/pgtrgm.html)。
