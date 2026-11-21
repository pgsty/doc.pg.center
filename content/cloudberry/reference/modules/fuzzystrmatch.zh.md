---
title: fuzzystrmatch
description: fuzzystrmatch 使用 Soundex、Levenshtein、Metaphone 和 Double Metaphone 算法计算字符串相似性和距离。
weight: 60
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/fuzzystrmatch.md
---

`fuzzystrmatch` 模块基于 Soundex、Levenshtein、Metaphone 和 Double Metaphone 算法，提供确定字符串相似性和距离的函数。

Apache Cloudberry 的 `fuzzystrmatch` 模块与 PostgreSQL 的 `fuzzystrmatch` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `fuzzystrmatch`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION fuzzystrmatch;
```

## 模块文档 {#module-documentation}

此模块各个函数的详细信息，参见 PostgreSQL 文档中的 [fuzzystrmatch](https://www.postgresql.org/docs/14/fuzzystrmatch.html)。
