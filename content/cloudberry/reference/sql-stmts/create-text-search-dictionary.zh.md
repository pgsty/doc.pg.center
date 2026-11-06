---
title: "CREATE TEXT SEARCH DICTIONARY"
description: "定义新的文本检索字典。"
weight: 860
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-text-search-dictionary.md"
---

## 概要 {#synopsis}

```sql
CREATE TEXT SEARCH DICTIONARY <name> (
    TEMPLATE = <template>
    [, <option> = <value> [, ... ]]
)
```

## 描述 {#description}

CREATE TEXT SEARCH DICTIONARY 创建新的文本检索字典。文本检索字典指定识别搜索中有用或无用词语的方法。字典依赖文本检索模板，模板指定实际执行工作的函数。字典通常提供一些选项，以控制模板函数的具体行为。

如果给出模式名，则在指定模式中创建文本检索字典；否则在当前模式中创建。

定义文本检索字典的用户成为其所有者。

## 参数 {#parameters}

**`name`**

要创建的文本检索字典名称，可以带模式限定。

**`template`**

定义此字典基本行为的文本检索模板名称。

**`option`**

要为此字典设置的模板特有选项名称。

**`value`**

模板特有选项的值。如果不是简单标识符或数字，必须加引号（也可以始终加引号）。

选项可以按任意顺序出现。

## 示例 {#examples}

下面的示例命令创建一个基于 Snowball 的字典，并使用非标准停用词列表。

```sql
CREATE TEXT SEARCH DICTIONARY my_russian (
    template = snowball,
    language = russian,
    stopwords = myrussian
);
```

## 兼容性 {#compatibility}

SQL 标准中没有 `CREATE TEXT SEARCH DICTIONARY` 语句。

## 另见 {#see-also}

[ALTER TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/alter-text-search-dictionary/), [DROP TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/drop-text-search-dictionary/)
