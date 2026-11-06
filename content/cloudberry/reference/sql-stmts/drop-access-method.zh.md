---
title: "DROP ACCESS METHOD"
description: "删除访问方法。"
weight: 1000
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-access-method.md"
---

## 概要 {#synopsis}

```sql
DROP ACCESS METHOD [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP ACCESS METHOD` 删除现有访问方法。只有超级用户才能删除访问方法。

## 参数 {#parameters}

**`IF EXISTS`**

如果访问方法不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有访问方法的名称。

**`CASCADE`**

自动删除依赖此访问方法的对象（例如操作符类、操作符族和索引），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此访问方法，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除访问方法 `heptree`：

``` sql
DROP ACCESS METHOD heptree;
```

## 兼容性 {#compatibility}

`DROP ACCESS METHOD` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE ACCESS METHOD](/cloudberry/reference/sql-stmts/create-access-method/)
