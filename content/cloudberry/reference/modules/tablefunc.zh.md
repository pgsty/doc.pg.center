---
title: tablefunc
description: tablefunc 提供 normal_rand()、crosstab() 和 connectby() 等返回表的函数。
weight: 250
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/tablefunc.md
---

`tablefunc` 模块提供多种返回表（即多行）的函数，例如 `normal_rand()`、`crosstab()` 和 `connectby()`。

Apache Cloudberry 的 `tablefunc` 模块与 PostgreSQL 的 `tablefunc` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `tablefunc`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION tablefunc;
```

## 模块文档 {#module-documentation}

此模块各个函数的详细信息，参见 PostgreSQL 文档中的 [tablefunc](https://www.postgresql.org/docs/14/tablefunc.html)。
