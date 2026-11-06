---
title: "DROP LANGUAGE"
description: "删除过程语言。"
weight: 1140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-language.md"
---

## 概要 {#synopsis}

```sql
DROP [PROCEDURAL] LANGUAGE [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP LANGUAGE` 删除先前注册的过程语言定义。必须是超级用户或该语言的所有者才能删除语言。

## 参数 {#parameters}

**`PROCEDURAL`**

可选关键字，没有效果。

**`IF EXISTS`**

如果语言不存在，不报错，而是发出一条提示。

**`name`**

现有过程语言的名称。为保持向后兼容，名称可以用单引号括起来。

**`CASCADE`**

自动删除依赖此语言的对象（例如用该语言编写的函数），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此语言，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除过程语言 `plsample`：

```sql
DROP LANGUAGE plsample;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP LANGUAGE` 语句。

## 另见 {#see-also}

[ALTER LANGUAGE](/cloudberry/reference/sql-stmts/alter-language/), [CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/)
