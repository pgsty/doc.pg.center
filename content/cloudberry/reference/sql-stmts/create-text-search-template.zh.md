---
title: "CREATE TEXT SEARCH TEMPLATE"
description: "使用 CREATE TEXT SEARCH TEMPLATE 定义文本检索字典使用的函数。"
weight: 880
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-text-search-template.md"
---

## 描述 {#description}

定义新的文本检索模板。

## 概要 {#synopsis}

```sql
CREATE TEXT SEARCH TEMPLATE <name> (
    [ INIT = <init_function> , ]
    LEXIZE = <lexize_function>
)
```

## 描述 {#description-1}

`CREATE TEXT SEARCH TEMPLATE` 创建新的文本检索模板。文本检索模板定义实现文本检索字典的函数。模板自身不能直接使用，必须实例化为字典才能使用。字典通常指定传递给模板函数的参数。

如果给出模式名，则在指定模式中创建文本检索模板；否则在当前模式中创建。

必须是超级用户才能使用 `CREATE TEXT SEARCH TEMPLATE`。此限制是因为错误的文本检索模板定义可能导致服务器行为异常，甚至崩溃。将模板与字典分离，是为了让模板封装字典定义中的“不安全”部分。定义字典时可以设置的参数，对非特权用户也是安全的，因此创建字典不必是特权操作。

## 参数 {#parameters}

**`name`**

要创建的文本检索模板名称，可以带模式限定。

**`init_function`**

模板的 init 函数名称。

**`lexize_function`**

模板的 lexize 函数名称。

必要时，函数名可以带模式限定。无需给出参数类型，因为每类函数的参数列表都已预先确定。lexize 函数是必需的，init 函数则可选。

参数可以按任意顺序出现，不限于上面显示的顺序。

## 兼容性 {#compatibility}

SQL 标准中没有 `CREATE TEXT SEARCH TEMPLATE` 语句。

## 另见 {#see-also}

[DROP TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/drop-text-search-template/), [ALTER TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/alter-text-search-template/)
