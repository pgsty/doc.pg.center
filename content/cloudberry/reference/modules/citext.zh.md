---
title: citext
description: citext 提供不区分大小写的字符串数据类型。
weight: 30
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/citext.md
---

`citext` 模块提供不区分大小写的字符串数据类型 `citext`。它在比较值时内部调用 `lower()` 函数，除此之外的行为几乎与 `text` 数据类型完全相同。

Apache Cloudberry 的 `citext` 模块与 PostgreSQL 的 `citext` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `citext`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION citext;
```

## 模块文档 {#module-documentation}

此模块定义的数据类型、操作符和函数的详细信息，参见 PostgreSQL 文档中的 [citext](https://www.postgresql.org/docs/14/citext.html)。
