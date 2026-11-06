---
title: "DROP TRANSFORM"
description: "删除转换。"
weight: 1380
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-transform.md"
---

## 概要 {#synopsis}

```sql
DROP TRANSFORM [IF EXISTS] FOR <type_name> LANGUAGE <lang_name> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP TRANSFORM` 删除先前定义的转换。

必须拥有相应的类型和语言才能删除转换。这与创建转换所需的权限相同。

## 参数 {#parameters}

**`IF EXISTS`**

如果转换不存在，不报错；Apache Cloudberry 会发出一条提示。

**`type_name`**

转换所对应的数据类型名称。

**`lang_name`**

转换所对应的语言名称。

**`CASCADE`**

自动删除依赖此转换的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此转换，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除用于类型 `hstore` 和语言 `plpython3u` 的转换：

``` sql
DROP TRANSFORM FOR hstore LANGUAGE plpython3u;
```

## 兼容性 {#compatibility}

这种形式的 `DROP TRANSFORM` 是 Apache Cloudberry 的扩展。详情见 [CREATE TRANSFORM](/cloudberry/reference/sql-stmts/create-transform/)。

## 另见 {#see-also}

[CREATE TRANSFORM](/cloudberry/reference/sql-stmts/create-transform/)
