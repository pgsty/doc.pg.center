---
title: "在数据库表中检索文本"
description: "本文介绍如何使用文本检索运算符搜索数据库表，以及如何创建索引来加快文本检索。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/search-text-in-db.md"
---

上一节中的示例使用简单的常量字符串展示了全文匹配。本节介绍如何搜索表数据，以及如何选择使用索引。

本节包含以下子主题：

- [搜索表](#search-a-table)
- [创建索引](#create-indexes)

## 搜索表 {#search-a-table}

即使没有索引，也可以执行全文检索。下面是一个简单查询，用于输出每一行的 `title`，其中 `body` 字段包含单词 `friend`：

```sql
SELECT title
FROM pgweb
WHERE to_tsvector('english', body) @@ to_tsquery('english', 'friend');
```

由于这些单词都会被归约为同一个规范化词位，因此该查询也会找到 `friends` 和 `friendly` 等相关单词。

上面的查询指定使用 `english` 配置解析和规范化字符串。也可以省略配置参数：

```sql
SELECT title
FROM pgweb
WHERE to_tsvector(body) @@ to_tsquery('friend');
```

此查询会使用 `default_text_search_config` 设置的配置。

更复杂的示例是：选择最近的十份文档，这些文档的 `title` 或 `body` 中包含 `create` 和 `table`：

```sql
SELECT title
FROM pgweb
WHERE to_tsvector(title || ' ' || body) @@ to_tsquery('create & table')
ORDER BY last_mod_date DESC
LIMIT 10;
```

为清楚起见，示例省略了可能需要的 `coalesce` 函数调用；如果两个字段之一包含 `NULL`，这些调用可能是必需的。

虽然这些查询不使用索引也能工作，但除非只是偶尔进行临时检索，否则大多数应用都会认为这种方式太慢。实际使用文本检索通常需要创建索引。

## 创建索引 {#create-indexes}

可以创建 GIN 索引（[文本检索的 GiST 和 GIN 索引](/cloudberry/operate-with-data/sql-queries/full-text-search/preferred-indexes-for-full-text-search/)）来加快文本检索：

```sql
CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector('english', body));
```

请注意，这里使用的是 `to_tsvector` 的双参数版本。只有指定配置名称的文本检索函数才能用于表达式索引。这是因为索引内容必须不受 `default_text_search_config` 影响。如果受其影响，索引内容可能不一致，因为不同索引项可能包含使用不同文本检索配置创建的 `tsvector`，而且没有办法判断每个索引项使用的是哪一种配置。这样的索引也无法正确转储和恢复。

由于上面的索引使用了 `to_tsvector` 的双参数版本，只有使用相同配置名称的 `to_tsvector` 双参数版本的查询引用，才会使用该索引。也就是说，`WHERE to_tsvector('english', body) @@ 'a & b'` 可以使用该索引，但 `WHERE to_tsvector(body) @@ 'a & b'` 不能。这可以确保索引只会与创建索引项时使用的同一配置配合使用。

还可以创建更复杂的表达式索引，将配置名称指定为另一个列。例如：

```sql
CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector(config_name, body));
```

其中 `config_name` 是 `pgweb` 表中的一列。这样，同一个索引中可以混合使用不同配置，同时记录每个索引项使用的配置。例如，如果文档集合包含不同语言的文档，这就很有用。同样，打算使用该索引的查询也必须采用匹配的形式，例如 `WHERE to_tsvector(config_name, body) @@ 'a & b'`。

索引甚至可以连接多个列：

```sql
CREATE INDEX pgweb_idx ON pgweb USING GIN (to_tsvector('english', title || ' ' || body));
```

另一种方法是创建一个单独的 `tsvector` 列，用来保存 `to_tsvector` 的输出。要使该列根据源数据自动保持最新，可以使用存储式生成列。此示例将标题和正文连接起来，并使用 `coalesce` 确保其中一个字段为 NULL 时，另一个字段仍然可以建立索引：

```sql
ALTER TABLE pgweb 
    ADD COLUMN textsearchable_index_col tsvector
        GENERATED ALWAYS AS (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))) STORED;
```

然后可以创建 GIN 索引来加快检索：

```sql
CREATE INDEX textsearch_idx ON pgweb USING GIN (textsearchable_index_col);
```

现在可以执行快速全文检索了：

```sql
SELECT title FROM pgweb WHERE textsearchable_index_col @@ to_tsquery('create & table') 
ORDER BY last_mod_date DESC LIMIT 10;
```

与表达式索引相比，单独列方法的一个优点是，为了使用索引，查询中不必显式指定文本检索配置。如上面的示例所示，查询可以依赖 `default_text_search_config`。另一个优点是检索速度更快，因为不必重新执行 `to_tsvector` 调用来验证索引匹配。（使用 GiST 索引时，这一点比使用 GIN 索引时更重要；参见[文本检索的 GiST 和 GIN 索引](/cloudberry/operate-with-data/sql-queries/full-text-search/preferred-indexes-for-full-text-search/)。）不过，表达式索引方法更容易设置，而且占用更少的磁盘空间，因为 `tsvector` 表示不会被显式存储。
