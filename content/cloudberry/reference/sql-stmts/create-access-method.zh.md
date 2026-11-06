---
title: "CREATE ACCESS METHOD"
description: "定义一个新的访问方法。"
weight: 520
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-access-method.md"
---

## 概要 {#synopsis}

```sql
CREATE ACCESS METHOD <name>
    TYPE <access_method_type>
    HANDLER <handler_function>
```

## 描述 {#description}

`CREATE ACCESS METHOD` 创建一个新的访问方法。

访问方法名称在数据库内必须唯一。

只有超级用户才能定义新的访问方法。

## 参数 {#parameters}

**`name`**

要创建的访问方法的名称。

**`access_method_type`**

要定义的访问方法的类型。目前仅支持 `TABLE` 和 `INDEX` 类型。

**`handler_function`**

handler_function 是先前已注册、用于表示该访问方法的函数的名称（可以带模式限定）。该处理函数必须声明为接受一个 `internal` 类型的参数，其返回类型取决于访问方法的类型：对于 `TABLE` 访问方法，必须是 `table_am_handler`；对于 `INDEX` 访问方法，必须是 `index_am_handler`。处理函数必须实现的 C 级 API 因访问方法类型而异。表访问方法 API 在 PostgreSQL 文档的[表访问方法接口定义](https://www.postgresql.org/docs/12/tableam.html)中说明。索引访问方法 API 在[索引访问方法接口定义](https://www.postgresql.org/docs/12/indexam.html)中说明。

## 示例 {#examples}

创建一个索引访问方法 `heptree`，其处理函数为 `heptree_handler`：

``` sql
CREATE ACCESS METHOD heptree TYPE INDEX HANDLER heptree_handler;
```

## 兼容性 {#compatibility}

`CREATE ACCESS METHOD` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[DROP ACCESS METHOD](/cloudberry/reference/sql-stmts/drop-access-method/)、[CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/)、[CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/)
