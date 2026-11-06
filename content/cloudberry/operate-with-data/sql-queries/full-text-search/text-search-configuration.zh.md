---
title: "文本检索配置示例"
description: "本文介绍如何创建定制的文本检索配置，以处理文档文本和查询文本。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/text-search-configuration.md"
---

文本检索配置指定了将文档转换为 `tsvector` 所需的全部选项：用于将文本拆分为词元的解析器，以及用于将每个词元转换为词位的词典。每次调用 `to_tsvector` 或 `to_tsquery` 都需要一个文本检索配置来执行处理。`default_text_search_config` 配置参数指定默认配置的名称；如果省略了显式配置参数，文本检索函数就会使用该配置。可以使用 `gpconfig` 命令行工具在 `postgresql.conf` 中设置它，也可以使用 `SET` 命令为单个会话设置它。

有多个预定义的文本检索配置可用，也可以轻松创建定制配置。为便于管理文本检索对象，系统提供了一组 SQL 命令；此外还有多个 psql 命令可以显示文本检索对象的信息（[psql 支持](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-psql-support/)）。

例如，可以创建一个名为 `pg` 的配置，首先复制内置的 `english` 配置：

```sql
CREATE TEXT SEARCH CONFIGURATION public.pg ( COPY = pg_catalog.english );
```

可以使用 PostgreSQL 专用的同义词列表，并将其存储在 `$SHAREDIR/tsearch_data/pg_dict.syn` 中。文件内容如下：

```sql
postgres    pg
pgsql       pg
postgresql  pg
```

按如下方式定义同义词词典：

```sql
CREATE TEXT SEARCH DICTIONARY pg_dict (
    TEMPLATE = synonym,
    SYNONYMS = pg_dict
);
```

接下来注册 Ispell 词典 `english_ispell`，它有自己的配置文件：

```sql
CREATE TEXT SEARCH DICTIONARY english_ispell (
    TEMPLATE = ispell,
    DictFile = english,
    AffFile = english,
    StopWords = english
);
```

为配置 `pg` 中的单词设置映射：

```sql
ALTER TEXT SEARCH CONFIGURATION pg
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
                      word, hword, hword_part
    WITH pg_dict, english_ispell, english_stem;
```

选择不为内置配置也会处理的某些词元类型建立索引或执行检索：

```sql
ALTER TEXT SEARCH CONFIGURATION pg
    DROP MAPPING FOR email, url, url_path, sfloat, float;
```

现在测试该配置：

```sql
SELECT * FROM ts_debug('public.pg', '
PostgreSQL, the highly scalable, SQL compliant, open source object-relational
database management system, is now undergoing beta testing of the next
version of our software.
');
```

下一步是将会话设置为使用新配置；该配置是在 `public` 模式中创建的：

```sql
SET text_search_config = 'public.pg';
=> \dF
   List of text search configurations
 Schema  | Name | Description
---------+------+-------------
 public  | pg   |

SET default_text_search_config = 'public.pg';
SET

SHOW default_text_search_config;
 default_text_search_config
----------------------------
 public.pg
```
