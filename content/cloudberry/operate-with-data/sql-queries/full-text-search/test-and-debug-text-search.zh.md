---
title: "测试与调试文本检索"
description: "本文介绍可用于测试和调试检索配置，或配置中指定的单个解析器和词典的 Apache Cloudberry 函数。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/test-and-debug-text-search.md"
---

定制的文本检索配置的行为很容易变得令人困惑。本节介绍的函数可用于测试文本检索对象。可以测试完整配置，也可以分别测试解析器和词典。

本节包含以下子主题：

- [配置测试](#configuration-testing)
- [解析器测试](#parser-testing)
- [词典测试](#dictionary-testing)

## 配置测试 {#configuration-testing}

`ts_debug` 函数可以方便地测试文本检索配置。

```sql
ts_debug([<config> regconfig, ] <document> text,
         OUT <alias> text,
         OUT <description> text,
         OUT <token> text,
         OUT <dictionaries> regdictionary[],
         OUT <dictionary> regdictionary,
         OUT <lexemes> text[])
         returns setof record
```

`ts_debug` 显示 `*document*` 中每个词元的信息；这些词元由解析器生成，再由配置的词典处理。它使用 `*config*` 指定的配置；如果省略该参数，则使用 `default_text_search_config`。

`ts_debug` 为解析器在文本中识别出的每个词元返回一行。返回的列如下：

- `*alias* text` —— 词元类型的短名称
- `*description* text` —— 词元类型的描述
- `*token* text` —— 词元文本
- `*dictionaries* regdictionary[]` —— 配置为此词元类型选择的词典
- `*dictionary* regdictionary` —— 识别出该词元的词典；如果没有词典识别出它，则为 `NULL`
- `*lexemes* text[]` —— 识别出该词元的词典生成的词位；如果没有词典识别出它，则为 `NULL`；空数组（`{}`）表示该词元被识别为停用词

下面是一个简单示例：

```sql
SELECT * FROM ts_debug('english', 'a fat  cat sat on a mat - it ate a fat rats');
   alias   |   description   | token |  dictionaries  |  dictionary  | lexemes 
-----------+-----------------+-------+----------------+--------------+---------
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | fat   | {english_stem} | english_stem | {fat}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | cat   | {english_stem} | english_stem | {cat}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | sat   | {english_stem} | english_stem | {sat}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | on    | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | mat   | {english_stem} | english_stem | {mat}
 blank     | Space symbols   |       | {}             |              | 
 blank     | Space symbols   | -   | {}             |              | 
 asciiword | Word, all ASCII | it    | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | ate   | {english_stem} | english_stem | {ate}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | a     | {english_stem} | english_stem | {}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | fat   | {english_stem} | english_stem | {fat}
 blank     | Space symbols   |       | {}             |              | 
 asciiword | Word, all ASCII | rats  | {english_stem} | english_stem | {rat}
```

要进行更完整的演示，首先为英语创建 `public.english` 配置和 Ispell 词典：

```sql
CREATE TEXT SEARCH CONFIGURATION public.english ( COPY = pg_catalog.english );

CREATE TEXT SEARCH DICTIONARY english_ispell (
    TEMPLATE = ispell,
    DictFile = english,
    AffFile = english,
    StopWords = english
);

ALTER TEXT SEARCH CONFIGURATION public.english
   ALTER MAPPING FOR asciiword WITH english_ispell, english_stem;
```

```sql
SELECT * FROM ts_debug('public.english', 'The Brightest supernovaes');
   alias   |   description   |    token    |         dictionaries          |   dictionary   |   lexemes   
-----------+-----------------+-------------+-------------------------------+----------------+-------------
 asciiword | Word, all ASCII | The         | {english_ispell,english_stem} | english_ispell | {}
 blank     | Space symbols   |             | {}                            |                | 
 asciiword | Word, all ASCII | Brightest   | {english_ispell,english_stem} | english_ispell | {bright}
 blank     | Space symbols   |             | {}                            |                | 
 asciiword | Word, all ASCII | supernovaes | {english_ispell,english_stem} | english_stem   | {supernova}
```

在本示例中，解析器将单词 `Brightest` 识别为 `ASCII` 单词（别名 `asciiword`）。对于这种词元类型，词典列表为 `english_ispell` 和 `english_stem`。`english_ispell` 识别出了这个单词，并将它归约为名词 `bright`。`english_ispell` 词典不认识单词 `supernovaes`，因此将其传递给下一个词典；幸运的是，它被下一个词典识别了。（事实上，`english_stem` 是一个能够识别所有内容的 Snowball 词典，这就是将它放在词典列表末尾的原因。）

`english_ispell` 词典将单词 `The` 识别为停用词（[停用词](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-dictionaries/#stop-words)），因此不会为其建立索引。空格也会被丢弃，因为配置根本没有为其提供词典。

可以明确指定要查看的列，以缩短输出宽度：

```sql
SELECT alias, token, dictionary, lexemes FROM ts_debug('public.english', 'The Brightest supernovaes'); 
  alias    |    token    |   dictionary   |    lexemes 
-----------+-------------+----------------+------------- 
 asciiword | The         | english_ispell | {} 
 blank     |             |                | 
 asciiword | Brightest   | english_ispell | {bright} 
 blank     |             |                | 
 asciiword | supernovaes | english_stem   | {supernova}
```

## 解析器测试 {#parser-testing}

以下函数允许直接测试文本检索解析器。

```sql
ts_parse(<parser_name> text, <document> text,
         OUT <tokid> integer, OUT <token> text) returns setof record
ts_parse(<parser_oid> oid, <document> text,
         OUT <tokid> integer, OUT <token> text) returns setof record
```

`ts_parse` 解析给定文档，并返回一系列记录，每条记录对应解析生成的一个词元。每条记录包含 `tokid`（表示分配的词元类型）和 `token`（词元文本）。例如：

```sql
SELECT * FROM ts_parse('default', '123 - a number');
 tokid | token
-------+--------
    22 | 123
    12 |
    12 | -
     1 | a
    12 |
     1 | number
```

```sql
ts_token_type(<parser_name> text, OUT <tokid> integer,
              OUT <alias> text, OUT <description> text) returns setof record
ts_token_type(<parser_oid> oid, OUT <tokid> integer,
              OUT <alias> text, OUT <description> text) returns setof record
```

`ts_token_type` 返回一个表，描述指定解析器能够识别的每一种词元类型。对于每种词元类型，该表提供解析器用于标记该类型词元的整数 `tokid`、在配置命令中为该词元类型命名的 `alias`，以及简短的 `description`。例如：

```sql
SELECT * FROM ts_token_type('default');
 tokid |      alias      |               description                
-------+-----------------+------------------------------------------
     1 | asciiword       | Word, all ASCII
     2 | word            | Word, all letters
     3 | numword         | Word, letters and digits
     4 | email           | Email address
     5 | url             | URL
     6 | host            | Host
     7 | sfloat          | Scientific notation
     8 | version         | Version number
     9 | hword_numpart   | Hyphenated word part, letters and digits
    10 | hword_part      | Hyphenated word part, all letters
    11 | hword_asciipart | Hyphenated word part, all ASCII
    12 | blank           | Space symbols
    13 | tag             | XML tag
    14 | protocol        | Protocol head
    15 | numhword        | Hyphenated word, letters and digits
    16 | asciihword      | Hyphenated word, all ASCII
    17 | hword           | Hyphenated word, all letters
    18 | url_path        | URL path
    19 | file            | File or path name
    20 | float           | Decimal notation
    21 | int             | Signed integer
    22 | uint            | Unsigned integer
    23 | entity          | XML entity
```

## 词典测试 {#dictionary-testing}

`ts_lexize` 函数简化了词典测试。

```sql
ts_lexize(*dictreg* dictionary, *token* text) returns text[]
```

如果输入的 `*token*` 是词典已知的单词，`ts_lexize` 会返回词位数组；如果词典认识该词元但它是停用词，则返回空数组；如果是未知单词，则返回 `NULL`。

示例：

```sql
SELECT ts_lexize('english_stem', 'stars');
 ts_lexize
-----------
 {star}

SELECT ts_lexize('english_stem', 'a');
 ts_lexize
-----------
 {}
```

> [!NOTE]
> `ts_lexize` 函数需要单个词元，而不是文本。下面是一个可能令人困惑的情况：
>
> ```sql
> SELECT ts_lexize('thesaurus_astro','supernovae stars') is null;
>  ?column?
> ----------
>  t
> ```

分类词典 `thesaurus_astro` 确实认识短语 `supernovae stars`，但 `ts_lexize` 会失败，因为它不会解析输入文本，而是将其作为单个词元处理。可以使用 `plainto_tsquery` 或 `to_tsvector` 测试分类词典，例如：

```sql
SELECT plainto_tsquery('supernovae stars');
 plainto_tsquery
-----------------
 'sn'
```
