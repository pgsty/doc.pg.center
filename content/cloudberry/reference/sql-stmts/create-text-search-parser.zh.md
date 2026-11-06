---
title: "CREATE TEXT SEARCH PARSER"
description: "使用 CREATE TEXT SEARCH PARSER 定义文本检索解析器及其词元处理函数。"
weight: 870
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-text-search-parser.md"
---

## 描述 {#description}

定义一个新的文本检索解析器。

## 概要 {#synopsis}

```sql
CREATE TEXT SEARCH PARSER <name> (
    START = <start_function> ,
    GETTOKEN = <gettoken_function> ,
    END = <end_function> ,
    LEXTYPES = <lextypes_function>
    [, HEADLINE = <headline_function> ]
)
```

## 描述 {#description-1}

`CREATE TEXT SEARCH PARSER` 创建一个新的文本检索解析器。文本检索解析器定义了一种方法，用于将文本字符串拆分为词元，并为这些词元指定类型（类别）。解析器本身并不是特别有用，必须与一些文本检索词典一起绑定到某个文本检索配置中，才能用于搜索。

如果给出了模式名称，则文本检索解析器会创建在指定的模式中。否则，它会创建在当前模式中。

只有超级用户才能使用 `CREATE TEXT SEARCH PARSER`。（之所以有此限制，是因为错误的文本检索解析器定义可能会使服务器陷入混乱，甚至导致服务器崩溃。）

## 参数 {#parameters}

**`name`**

要创建的文本检索解析器的名称。该名称可以是模式限定的。

**`start_function`**

该解析器的启动函数的名称。

**`gettoken_function`**

该解析器的获取下一个词元的函数名称。

**`end_function`**

该解析器的结束函数的名称。

**`lextypes_function`**

该解析器的 lextypes 函数的名称（该函数返回关于它所产生的词元类型集合的信息）。

**`headline_function`**

该解析器的 headline 函数的名称（该函数对一组词元生成摘要）。

如有必要，函数名称可以是模式限定的。这里不给出参数类型，因为每类函数的参数列表都是预先确定的。除 headline 函数外，其余函数都是必需的。

这些参数可以按任意顺序出现，不必与上面所示的顺序一致。

## 兼容性 {#compatibility}

SQL 标准中没有 `CREATE TEXT SEARCH PARSER` 语句。

## 另见 {#see-also}

[ALTER TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/alter-text-search-parser/)、[DROP TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/drop-text-search-parser/)
