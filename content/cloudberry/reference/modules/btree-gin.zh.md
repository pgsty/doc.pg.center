---
title: btree_gin
description: btree_gin 提供为多种数据类型实现 B-树等价行为的 GIN 操作符类。
weight: 20
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/btree-gin.md
---

`btree_gin` 模块提供一组广义倒排索引（GIN）操作符类示例，为多种数据类型实现与 B-树等价的行为。

Apache Cloudberry 的 `btree_gin` 模块与 PostgreSQL 的 `btree_gin` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `btree_gin`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION btree_gin;
```

## 模块文档 {#module-documentation}

支持的数据类型列表和用法示例，参见 PostgreSQL 文档中的 [btree_gin](https://www.postgresql.org/docs/14/btree-gin.html)。
