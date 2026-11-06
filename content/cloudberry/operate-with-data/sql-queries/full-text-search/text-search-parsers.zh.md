---
title: "文本检索解析器"
description: "本文介绍 Apache Cloudberry 文本检索解析器从原始文本生成的词元类型。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/text-search-parsers.md"
---

文本检索解析器负责将原始文档文本拆分为*词元*，并识别每个词元的类型；可能的类型集合由解析器本身定义。请注意，解析器不会修改文本——它只识别可能的单词边界。由于作用范围有限，与定制词典相比，应用程序对定制解析器的需求较少。目前，Apache Cloudberry 只提供一个内置解析器，但实践证明它适用于各种应用。

内置解析器名为 `pg_catalog.default`。它可以识别 23 种词元类型，如下表所示。

|别名|描述|示例|
|-----|-----------|-------|
|asciiword|单词，全部为 ASCII 字母|`elephant`|
|word|单词，全部为字母|`mañana`|
|numword|单词，由字母和数字组成|`beta1`|
|asciihword|连字符单词，全部为 ASCII|`up-to-date`|
|hword|连字符单词，全部为字母|`lógico-matemática`|
|numhword|连字符单词，由字母和数字组成|`postgresql-beta1`|
|hword_asciipart|连字符单词部分，全部为 ASCII|在 `postgresql-beta1` 上下文中的 `postgresql`|
|hword_part|连字符单词部分，全部为字母|在 `lógico-matemática` 上下文中的 `lógico` 或 `matemática`|
|hword_numpart|连字符单词部分，由字母和数字组成|在 `postgresql-beta1` 上下文中的 `beta1`|
|email|电子邮件地址|`foo@example.com`|
|protocol|协议头|`http://`|
|url|URL|`example.com/stuff/index.html`|
|host|主机|`example.com`|
|url_path|URL 路径|URL 上下文中的 `/stuff/index.html`|
|file|文件或路径名|不在 URL 中时的 `/usr/local/foo.txt`|
|sfloat|科学计数法|`-1.234e56`|
|float|十进制计数法|`-1.234`|
|int|有符号整数|`-1234`|
|uint|无符号整数|`1234`|
|version|版本号|`8.3.0`|
|tag|XML 标签|`<a href="dictionaries.html">`|
|entity|XML 实体|`&amp;`|
|blank|空白符号|`(any whitespace or punctuation not otherwise recognized)`|

> [!NOTE]
> 解析器对“字母”的理解由数据库的区域设置决定，具体来说是 `lc_ctype`。只包含基本 ASCII 字母的单词会作为单独的词元类型报告，因为有时区分它们很有用。在大多数欧洲语言中，应将 `word` 和 `asciiword` 词元类型视为相同。

`email` 不支持 RFC 5322 定义的所有有效电子邮件字符。具体来说，电子邮件用户名中只有句点、短横线和下划线这三种非字母数字字符受支持。

解析器可能从同一段文本生成重叠的词元。例如，一个带连字符的单词会同时作为完整单词和每个组成部分报告：

```sql
SELECT alias, description, token FROM ts_debug('foo-bar-beta1');
      alias      |               description                |     token     
-----------------+------------------------------------------+---------------
 numhword        | Hyphenated word, letters and digits      | foo-bar-beta1
 hword_asciipart | Hyphenated word part, all ASCII          | foo
 blank           | Space symbols                            | -
 hword_asciipart | Hyphenated word part, all ASCII          | bar
 blank           | Space symbols                            | -
 hword_numpart   | Hyphenated word part, letters and digits | beta1
```

这种行为很有用，因为它允许检索同时适用于整个复合单词及其组成部分。下面是另一个有说明性的示例：

```sql
SELECT alias, description, token FROM ts_debug('http://example.com/stuff/index.html');
  alias   |  description  |            token             
----------+---------------+------------------------------
 protocol | Protocol head | http://
 url      | URL           | example.com/stuff/index.html
 host     | Host          | example.com
 url_path | URL path      | /stuff/index.html
```
