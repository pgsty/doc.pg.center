---
title: "CREATE TEXT SEARCH CONFIGURATION"
description: "定义新的文本检索配置。"
weight: 850
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-text-search-configuration.md"
---

## 概要 {#synopsis}

```sql
CREATE TEXT SEARCH CONFIGURATION <name> (
    PARSER = <parser_name> |
    COPY = <source_config>
)
```

## 描述 {#description}

`CREATE TEXT SEARCH CONFIGURATION` 创建新的文本检索配置。文本检索配置指定一个将字符串拆分为词元的文本检索解析器，以及用于确定哪些词元与搜索有关的字典。

如果只指定解析器，新文本检索配置最初没有词元类型到字典的映射，因此会忽略所有词。必须随后使用 [ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/) 命令创建映射，才能使配置发挥作用。也可以复制现有文本检索配置。

如果提供模式名，则在指定模式中创建文本检索配置；否则在当前模式中创建。

定义文本检索配置的用户成为其所有者。

## 参数 {#parameters}

**`name`**

要创建的文本检索配置名称，可以带模式限定。

**`parser_name`**

此配置使用的文本检索解析器名称。

**`source_config`**

要复制的现有文本检索配置名称。

## 注意事项 {#notes}

`PARSER` 和 `COPY` 选项互斥，因为复制现有配置时，也会复制它所选择的解析器。

## 兼容性 {#compatibility}

SQL 标准中没有 `CREATE TEXT SEARCH CONFIGURATION` 语句。

## 另见 {#see-also}

[ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/), [DROP TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/drop-text-search-configuration/)
