---
title: "ALTER TEXT SEARCH DICTIONARY"
description: "更改文本检索词典的定义。"
weight: 350
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-text-search-dictionary.md"
---

## 概要 {#synopsis}

```sql
ALTER TEXT SEARCH DICTIONARY <name> (
    <option> [ = <value> ] [, ... ]
)
ALTER TEXT SEARCH DICTIONARY <name> RENAME TO <new_name>
ALTER TEXT SEARCH DICTIONARY <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
ALTER TEXT SEARCH DICTIONARY <name> SET SCHEMA <new_schema>
```

## 描述 {#description}

`ALTER TEXT SEARCH DICTIONARY` 用于更改文本检索词典的定义。可以更改词典中特定于模板的选项，也可以更改词典的名称或所有者。

必须是词典的所有者才能使用 `ALTER TEXT SEARCH DICTIONARY`。

## 参数 {#parameters}

**`name`**

现有文本检索词典的名称（可以带模式限定）。

**`option`**

要为该词典设置的、特定于模板的选项的名称。

**`value`**

特定于模板的选项要使用的新值。如果省略等号和值，则该选项先前的任何设置都会从词典中移除，从而使用默认值。

**`new_name`**

文本检索词典的新名称。

**`new_owner`**

文本检索词典的新所有者。

**`new_schema`**

文本检索词典的新模式。

特定于模板的选项可以按任意顺序出现。

## 示例 {#examples}

下面的示例命令更改基于 Snowball 的词典的停用词列表，其他参数保持不变。

```sql
ALTER TEXT SEARCH DICTIONARY my_dict ( StopWords = newrussian );
```

下面的示例命令将 language 选项更改为 `dutch`，并完全移除停用词选项：

```sql
ALTER TEXT SEARCH DICTIONARY my_dict ( language = dutch, StopWords );
```

下面的示例命令在不实际更改任何内容的情况下“更新”词典的定义：

```sql
ALTER TEXT SEARCH DICTIONARY my_dict ( dummy );
```

（这样做之所以可行，是因为选项移除代码在不存在该选项时不会报错。）这一技巧在更改词典的配置文件时很有用：`ALTER` 会强制现有的数据库会话重新读取配置文件，否则如果这些会话先前已经读取过，就永远不会再读取。

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER TEXT SEARCH DICTIONARY` 语句。

## 另请参阅 {#see-also}

[CREATE TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/create-text-search-dictionary/)、[DROP TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/drop-text-search-dictionary/)
