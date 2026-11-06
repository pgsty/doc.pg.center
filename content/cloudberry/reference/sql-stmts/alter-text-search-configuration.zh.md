---
title: "ALTER TEXT SEARCH CONFIGURATION"
description: "更改文本检索配置的定义。"
weight: 340
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-text-search-configuration.md"
---

## 概要 {#synopsis}

```sql
ALTER TEXT SEARCH CONFIGURATION <name>
    ADD MAPPING FOR <token_type> [, ... ] WITH <dictionary_name> [, ... ]
ALTER TEXT SEARCH CONFIGURATION <name>
    ALTER MAPPING FOR <token_type> [, ... ] WITH <dictionary_name> [, ... ]
ALTER TEXT SEARCH CONFIGURATION <name>
    ALTER MAPPING REPLACE <old_dictionary> WITH <new_dictionary>
ALTER TEXT SEARCH CONFIGURATION <name>
    ALTER MAPPING FOR <token_type> [, ... ] REPLACE <old_dictionary> WITH <new_dictionary>
ALTER TEXT SEARCH CONFIGURATION <name>
    DROP MAPPING [ IF EXISTS ] FOR <token_type> [, ... ]
ALTER TEXT SEARCH CONFIGURATION <name> RENAME TO <new_name>
ALTER TEXT SEARCH CONFIGURATION <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
ALTER TEXT SEARCH CONFIGURATION <name> SET SCHEMA <new_schema>
```

## 描述 {#description}

`ALTER TEXT SEARCH CONFIGURATION` 用于更改文本检索配置的定义。可以修改其从词元类型到词典的映射，也可以更改配置的名称或所有者。

必须是配置的所有者才能使用 `ALTER TEXT SEARCH CONFIGURATION`。

## 参数 {#parameters}

**`name`**

现有文本检索配置的名称（可以带模式限定）。

**`token_type`**

该配置的解析器所产生的词元类型的名称。

**`dictionary_name`**

针对指定词元类型要查询的文本检索词典的名称。如果列出了多个词典，则按指定的顺序依次查询。

**`old_dictionary`**

要在映射中被替换的文本检索词典的名称。

**`new_dictionary`**

用来替代 old_dictionary 的文本检索词典的名称。

**`new_name`**

文本检索配置的新名称。

**`new_owner`**

文本检索配置的新所有者。

**`new_schema`**

文本检索配置的新模式。

`ADD MAPPING FOR` 形式会安装一个词典列表，用于针对指定的词元类型进行查询；如果其中任一词元类型已有映射，则会报错。`ALTER MAPPING FOR` 形式的作用相同，但会先删除这些词元类型的现有映射。`ALTER MAPPING REPLACE` 形式会在 old_dictionary 出现的所有位置用 new_dictionary 替代它。出现 `FOR` 时，仅对指定的词元类型执行此替换；未出现时，则对该配置的所有映射执行。`DROP MAPPING` 形式会删除指定词元类型的所有词典，使文本检索配置忽略这些类型的词元。如果这些词元类型没有映射，则会报错，除非出现 `IF EXISTS`。

## 示例 {#examples}

下面的示例在 `my_config` 中，将 `english` 词典替换为 `swedish`，覆盖所有使用该 `english` 词典的位置。

```sql
ALTER TEXT SEARCH CONFIGURATION my_config
  ALTER MAPPING REPLACE english WITH swedish;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER TEXT SEARCH CONFIGURATION` 语句。

## 另请参阅 {#see-also}

[CREATE TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/create-text-search-configuration/)、[DROP TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/drop-text-search-configuration/)
