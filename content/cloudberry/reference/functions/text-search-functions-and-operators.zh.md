---
title: "Apache Cloudberry 文本搜索函数和操作符"
linkTitle: "文本搜索函数和操作符"
description: "下表汇总了用于全文搜索的函数和操作符。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/functions/text-search-functions-and-operators.md"
---

|操作符|描述|示例|结果|
|--------|-----------|-------|------|
|`@@`|`tsvector` 是否匹配 `tsquery`？|`to_tsvector('fat cats ate rats') @@ to_tsquery('cat & rat')`|`t`|
|`@@@`|`@@` 已弃用的同义操作符|`to_tsvector('fat cats ate rats') @@@ to_tsquery('cat & rat')`|`t`|
|`\|\|`|连接多个 `tsvector`|`'a:1 b:2'::tsvector \|\| 'c:1 d:2 b:3'::tsvector`|`'a':1 'b':2,5 'c':3 'd':4`|
|`&&`|对多个 `tsquery` 进行 AND 运算|`'fat \| rat'::tsquery && 'cat'::tsquery`|`( 'fat' \| 'rat' ) & 'cat'`|
|`\|\|`|对多个 `tsquery` 进行 OR 运算|`'fat \| rat'::tsquery \|\| 'cat'::tsquery`|`( 'fat' \| 'rat' ) \| 'cat'`|
|`!!`|对 `tsquery` 取反|`!! 'cat'::tsquery`|`!'cat'`|
|`@>`|`tsquery` 是否包含另一个查询？|`'cat'::tsquery @> 'cat & rat'::tsquery`|`f`|
|`<@`|`tsquery` 是否包含于另一个查询？|`'cat'::tsquery <@ 'cat & rat'::tsquery`|`t`|

> **注意** `tsquery` 的包含操作符只考虑两个查询中列出的词位，忽略组合操作符。

除了表中列出的操作符，还为 `tsvector` 和 `tsquery` 类型定义了普通的 B-树比较操作符（`=`、`<` 等）。它们对文本搜索用处不大，但例如可以用于在这些类型的列上构建唯一索引。

|函数|返回类型|描述|示例|结果|
|--------|-----------|-----------|-------|------|
|`get_current_ts_config()`|regconfig|获取默认文本搜索配置|get_current_ts_config()|english|
|`length(tsvector)`|integer|tsvector 中的词位数|length('fat:2,4 cat:3 rat:5A'::tsvector)|3|
|`numnode(tsquery)`|integer|tsquery 中词位和操作符的总数|numnode('(fat & rat) \| cat'::tsquery)|5|
|`plainto_tsquery([ config regconfig , ] querytext)`|tsquery|生成 tsquery，忽略标点|plainto_tsquery('english', 'The Fat Rats')|'fat' & 'rat'|
|`querytree(query tsquery)`|text|获取 tsquery 中可用于索引的部分|querytree('foo & ! bar'::tsquery)|'foo'|
|`setweight(tsvector, "char")`|tsvector|为 tsvector 中的每个元素赋予权重|setweight('fat:2,4 cat:3 rat:5B'::tsvector, 'A')|'cat':3A 'fat':2A,4A 'rat':5A|
|`strip(tsvector)`|tsvector|移除 tsvector 中的位置和权重|strip('fat:2,4 cat:3 rat:5A'::tsvector)|'cat' 'fat' 'rat'|
|`to_tsquery([ config regconfig , ] query text)`|tsquery|规范化单词并转换为 tsquery|to_tsquery('english', 'The & Fat & Rats')|'fat' & 'rat'|
|`to_tsvector([ config regconfig , ] documenttext)`|tsvector|将文档文本转换为 tsvector|to_tsvector('english', 'The Fat Rats')|'fat':2 'rat':3|
|`ts_headline([ config regconfig, ] documenttext, query tsquery [, options text ])`|text|显示查询匹配结果|ts_headline('x y z', 'z'::tsquery)|x y <b>z</b>|
|`ts_rank([ weights float4[], ] vector tsvector,query tsquery [, normalization integer ])`|float4|计算文档相对于查询的排名|ts_rank(textsearch, query)|0.818|
|`ts_rank_cd([ weights float4[], ] vectortsvector, query tsquery [, normalizationinteger ])`|float4|使用覆盖密度计算文档相对于查询的排名|ts_rank_cd('{0.1, 0.2, 0.4, 1.0}', textsearch, query)|2.01317|
|`ts_rewrite(query tsquery, target tsquery,substitute tsquery)`|tsquery|在查询中将 target 替换为 substitute|ts_rewrite('a & b'::tsquery, 'a'::tsquery, 'foo\|bar'::tsquery)|'b' & ( 'foo' \| 'bar' )|
|`ts_rewrite(query tsquery, select text)`|tsquery|使用 SELECT 命令提供的目标和替换项进行替换|SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM aliases')|'b' & ( 'foo' \| 'bar' )|
|`tsvector_update_trigger()`|trigger|自动更新 tsvector 列的触发器函数|CREATE TRIGGER ... tsvector_update_trigger(tsvcol, 'pg_catalog.swedish', title, body)| |
|`tsvector_update_trigger_column()`|trigger|自动更新 tsvector 列的触发器函数|CREATE TRIGGER ... tsvector_update_trigger_column(tsvcol, configcol, title, body)| |

> **注意** 所有接受可选 `regconfig` 参数的文本搜索函数，在省略该参数时都会使用 `default_text_search_config` 指定的配置。

下表单独列出了一些函数，因为日常文本搜索操作通常不会用到它们。这些函数有助于开发和调试新的文本搜索配置。

|函数|返回类型|描述|示例|结果|
|--------|-----------|-----------|-------|------|
|`ts_debug([ *config* regconfig, ] *document* text, OUT *alias* text, OUT *description* text, OUT *token* text, OUT *dictionaries* regdictionary[], OUT *dictionary* regdictionary, OUT *lexemes* text[])`|`setof record`|测试配置|`ts_debug('english', 'The Brightest supernovaes')`|`(asciiword,"Word, all ASCII",The,{english_stem},english_stem,{}) ...`|
|`ts_lexize(*dict* regdictionary, *token* text)`|`text[]`|测试字典|`ts_lexize('english_stem', 'stars')`|`{star}`|
|`ts_parse(*parser_name* text, *document* text, OUT *tokid* integer, OUT *token* text)`|`setof record`|测试解析器|`ts_parse('default', 'foo - bar')`|``(1,foo) ...``|
|`ts_parse(*parser_oid* oid, *document* text, OUT *tokid* integer, OUT *token* text)`|`setof record`|测试解析器|`ts_parse(3722, 'foo - bar')`|`(1,foo) ...`|
|`ts_token_type(*parser_name* text, OUT *tokid* integer, OUT *alias* text, OUT description text)`|`setof record`|获取解析器定义的词元类型|`ts_token_type('default')`|`(1,asciiword,"Word, all ASCII") ...`|
|`ts_token_type(*parser_oid* oid, OUT *tokid* integer, OUT *alias* text, OUT *description* text)`|`setof record`|获取解析器定义的词元类型|`ts_token_type(3722)`|`(1,asciiword,"Word, all ASCII") ...`|
|`ts_stat(*sqlquery* text, [ *weights* text, ] OUT *word* text, OUT *ndocinteger*, OUT *nentry* integer)`|`setof record`|获取 tsvector 列的统计信息|`ts_stat('SELECT vector from apod')`|`(foo,10,15) ...`|
