---
title: "控制文本检索"
description: "本文介绍如何创建检索向量和查询向量、如何对检索结果排名，以及如何在文本检索查询的结果中突出显示检索词。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/control-text-search.md"
---

要实现全文检索，必须有一个函数能够从文档创建 `tsvector`，并有一个函数能够从用户查询创建 `tsquery`。此外，还需要按有用的顺序返回结果，因此需要一个能够根据文档与查询的相关性比较文档的函数。能够以良好的方式显示结果也很重要。Apache Cloudberry 为所有这些功能提供了支持。

本文包含以下子主题：

- [解析文档](#parse-documents)
- [解析查询](#parse-queries)
- [对检索结果排名](#rank-search-results)
- [突出显示结果](#highlight-results)

## 解析文档 {#parse-documents}

Apache Cloudberry 提供 `to_tsvector` 函数，用于将文档转换为 `tsvector` 数据类型。

```sql
to_tsvector([<config> regconfig, ] <document> text) returns tsvector
```

`to_tsvector` 会将文本文档解析为词元，将词元归约为词位，并返回一个 `tsvector`，其中列出词位及其在文档中的位置。文档会根据指定的或默认的文本检索配置进行处理。下面是一个简单示例：

```sql
SELECT to_tsvector('english', 'a fat  cat sat on a mat - it ate a fat rats');
                  to_tsvector
-----------------------------------------------------
 'ate':9 'cat':3 'fat':2,11 'mat':7 'rat':12 'sat':4
```

从上面的示例可以看到，结果 tsvector 不包含单词 `a`、`on` 或 `it`，单词 `rats` 变成了 `rat`，标点符号 `-` 被忽略。

`to_tsvector` 函数在内部调用解析器，将文档文本拆分为词元，并为每个词元分配类型。对于每个词元，系统都会查询一个词典列表（[文本检索词典](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-dictionaries/)）；该列表可能随词元类型而变化。第一个能够*识别*该词元的词典会输出一个或多个规范化的*词位*来表示它。例如，`rats` 变成 `rat`，是因为某个词典识别出 `rats` 是 `rat` 的复数形式。某些单词会被识别为*停用词*，因为出现过于频繁、对检索没有帮助，所以会被忽略。在本示例中，`a`、`on` 和 `it` 就是这类停用词。如果列表中没有词典能够识别某个词元，该词元也会被忽略。本示例中的标点符号 `-` 就属于这种情况，因为它的词元类型（`Space symbols`）实际上没有分配任何词典，也就是说，空白词元永远不会建立索引。解析器、词典以及应建立索引的词元类型，都由选定的文本检索配置（[文本检索配置示例](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-configuration/)）决定。同一个数据库可以有许多不同配置，并且系统为多种语言提供了预定义配置。本示例使用英语的默认配置 `english`。

`setweight` 函数可以为 `tsvector` 的条目标记给定的*权重*，权重可以是字母 `A`、`B`、`C` 或 `D` 之一。通常可以用它标记来自文档不同部分的条目，例如 `title` 与 `body`。之后可以使用这些信息对检索结果排名。

由于 `to_tsvector(NULL)` 会返回 `NULL`，因此只要字段可能为空，就建议使用 `coalesce`。下面是从结构化文档创建 tsvector 的推荐方法：

```sql
UPDATE tt SET ti = setweight(to_tsvector(coalesce(title,'')), 'A') 
  || setweight(to_tsvector(coalesce(keyword,'')), 'B') 
  || setweight(to_tsvector(coalesce(abstract,'')), 'C') 
  || setweight(to_tsvector(coalesce(body,'')), 'D');
```

这里，`setweight` 用于标记最终 `tsvector` 中每个词位的来源，然后使用 `tsvector` 连接运算符 `||` 合并带标签的 `tsvector` 值。（[其他文本检索功能](/cloudberry/operate-with-data/sql-queries/full-text-search/additional-text-search-features/)详细介绍了这些操作。）

## 解析查询 {#parse-queries}

Apache Cloudberry 提供 `to_tsquery`、`plainto_tsquery`、`phraseto_tsquery` 和 `websearch_to_tsquery` 函数，用于将查询转换为 `tsquery` 数据类型。`to_tsquery` 比 `plainto_tsquery` 提供更多功能，但对输入的宽容度较低。`websearch_to_tsquery` 是 `to_tsquery` 的简化版本，使用类似网络搜索引擎的另一种语法。

```sql
to_tsquery([<config> regconfig, ] <querytext> text) returns tsquery
```

`to_tsquery` 根据*querytext*创建 `tsquery` 值；*querytext* 必须由使用布尔运算符 `&`（`AND`）、`|`（`OR`）、`!`（`NOT`）和 `<->`（`FOLLOWED BY`）分隔的单个词元组成，也可以使用圆括号进行分组。换句话说，传给 `to_tsquery` 的输入必须已经遵循 tsquery 输入的一般规则。区别在于，基本 `tsquery` 输入会直接使用这些词元，而 `to_tsquery` 会根据指定的或默认配置，将每个词元规范化为词位，并丢弃根据配置属于停用词的词元。例如：

```sql
SELECT to_tsquery('english', 'The & Fat & Rats');
  to_tsquery   
---------------
 'fat' & 'rat'
```

与基本 `tsquery` 输入一样，可以为每个词位附加权重，以限制它只能匹配具有相应权重的 `tsvector` 词位。例如：

```sql
SELECT to_tsquery('english', 'Fat | Rats:AB');
    to_tsquery    
------------------
 'fat' | 'rat':AB
```

还可以为词位附加 `*`，以指定前缀匹配：

```sql
SELECT to_tsquery('supern:*A & star:A*B');
        to_tsquery        
--------------------------
 'supern':*A & 'star':*AB
```

此类词位可以匹配 `tsvector` 中以给定字符串开头的任意单词。

`to_tsquery` 还可以接受用单引号括起的短语。当配置中包含可能对这类短语触发的分类词典时，这一功能尤其有用。在下面的示例中，分类词典包含规则 `supernovae stars : sn`：

```sql
SELECT to_tsquery('''supernovae stars'' & !crab');
  to_tsquery
---------------
 'sn' & !'crab'
```

```sql
SELECT to_tsquery('''supernovae stars'' & !crab');
  to_tsquery
---------------
 'sn' & !'crab'
```

如果不使用引号，`to_tsquery` 会为没有使用 AND、OR 或 FOLLOWED BY 运算符分隔的词元生成语法错误。

```sql
plainto_tsquery([ <config> regconfig, ] <querytext> ext) returns tsquery
```

`plainto_tsquery` 将未格式化的文本 `*querytext*` 转换为 `tsquery`。它会像 `to_tsvector` 一样解析并规范化文本，然后在保留下来的单词之间插入 `&`（AND）布尔运算符。

示例：

```sql
SELECT plainto_tsquery('english', 'The Fat Rats');
 plainto_tsquery 
-----------------
 'fat' & 'rat'
```

请注意，`plainto_tsquery` 无法识别其输入中的布尔运算符、权重标签或前缀匹配标签：

```sql
SELECT plainto_tsquery('english', 'The Fat & Rats:C');
   plainto_tsquery   
---------------------
 'fat' & 'rat' & 'c'
```

这里，所有输入标点符号都被当作空白符号丢弃。

```sql
phraseto_tsquery([ <config> regconfig, ] <querytext> text) returns tsquery
```

`phraseto_tsquery` 的行为与 `plainto_tsquery` 非常相似，但它会在保留下来的单词之间插入 `<->`（FOLLOWED BY）运算符，而不是 `&`（AND）运算符。此外，它不会简单地丢弃停用词，而是通过插入 `<N>` 运算符而不是 `<->` 运算符来计入停用词。此函数适用于搜索精确的词位序列，因为 FOLLOWED BY 运算符会检查词位的顺序，而不只是检查所有词位是否存在。

示例：

```sql
SELECT phraseto_tsquery('english', 'The Fat Rats');
 phraseto_tsquery
------------------
 'fat' <-> 'rat'
```

与 `plainto_tsquery` 一样，`phraseto_tsquery` 函数不会识别其输入中的 `tsquery` 运算符、权重标签或前缀匹配标签：

```sql
SELECT phraseto_tsquery('english', 'The Fat & Rats:C');
      phraseto_tsquery
-----------------------------
 'fat' <-> 'rat' <-> 'c'
```

```sql
websearch_to_tsquery([ <config> regconfig, ] <querytext> text) returns tsquery
```

`websearch_to_tsquery` 使用另一种语法根据 querytext 创建 `tsquery`，在这种语法中，简单的未格式化文本就是有效查询。与 `plainto_tsquery` 和 `phraseto_tsquery` 不同，它还识别某些运算符。此外，该函数不应产生语法错误，因此可以直接使用用户提供的原始输入进行检索。支持以下语法：

- `unquoted text`：引号外的文本会转换为由 `&` 运算符分隔的词项，就像使用 `plainto_tsquery` 处理一样。
- `"quoted text"`：引号内的文本会转换为由 `<->` 运算符分隔的词项，就像使用 `phraseto_tsquery` 处理一样。
- `OR`：逻辑或会转换为 `|` 运算符。
- `-`：逻辑非运算符，会转换为 `!` 运算符。

示例：

```sql
SELECT websearch_to_tsquery('english', 'The fat rats');
 websearch_to_tsquery
----------------------
 'fat' & 'rat'
(1 row)

SELECT websearch_to_tsquery('english', '"supernovae stars" -crab');
       websearch_to_tsquery
----------------------------------
 'supernova' <-> 'star' & !'crab'
(1 row)

SELECT websearch_to_tsquery('english', '"sad cat" or "fat rat"');
       websearch_to_tsquery
-----------------------------------
 'sad' <-> 'cat' | 'fat' <-> 'rat'
(1 row)

SELECT websearch_to_tsquery('english', 'signal -"segmentation fault"');
         websearch_to_tsquery
---------------------------------------
 'signal' & !( 'segment' <-> 'fault' )
(1 row)

SELECT websearch_to_tsquery('english', '""" )( dummy  query <->');
 websearch_to_tsquery
----------------------
 'dummi' & 'queri'
(1 row)
```

## 对检索结果排名 {#rank-search-results}

排名试图衡量文档与特定查询的相关程度，以便匹配项很多时可以先显示最相关的结果。Apache Cloudberry 提供两个预定义的排名函数，它们会考虑词法、邻近和结构信息；也就是说，它们会考虑查询词在文档中出现的频率、查询词在文档中的接近程度，以及查询词所在文档部分的重要性。不过，相关性的概念很模糊，而且高度依赖具体应用。不同应用可能需要其他排名信息，例如文档修改时间。内置排名函数只是示例。你可以编写自己的排名函数，或者将它们的结果与其他因素结合，以适应具体需求。

目前可用的两个排名函数是：

`ts_rank([ <weights> float4[], ] <vector> tsvector, <query> tsquery [, <normalization> integer ]) returns float4`：根据匹配词位的频率为向量排名。

`ts_rank_cd([ <weights> float4[], ] <vector> tsvector, <query> tsquery [, <normalization> integer ]) returns float4`：为给定文档向量和查询计算*覆盖密度*排名，具体定义见 Clarke、Cormack 和 Tudhope 在 1999 年《Information Processing and Management》期刊发表的《Relevance Ranking for One to Three Term Queries》。覆盖密度排名与 `ts_rank` 类似，但还会考虑匹配词位之间的邻近程度。

该函数需要词位的位置信息才能执行计算。因此，它会忽略 `tsvector` 中任何已“去除信息”的词位。如果输入中没有未去除信息的词位，结果为零。（关于 `strip` 函数和 `tsvector` 中位置信息的更多信息，请参见[操作文档](/cloudberry/operate-with-data/sql-queries/full-text-search/additional-text-search-features/#manipulate-documents)。）

对于这两个函数，可选的 `<weights>` 参数可以根据单词实例的标签，对其赋予更大或更小的权重。权重数组按以下顺序指定每个单词类别应具有的权重：

```sql
{D-weight, C-weight, B-weight, A-weight}
```

如果未提供 `<weights>`，则使用以下默认值：

```sql
{0.1, 0.2, 0.4, 1.0}
```

通常，权重用于标记文档特殊区域中的单词，例如标题或开头的摘要，以便相较于正文中的单词赋予它们更大或更小的重要性。

较长的文档更有可能包含查询词，因此考虑文档大小是合理的。例如，包含某个检索词 5 次的百词文档，可能比同样包含该词 5 次的千词文档更相关。两个排名函数都有一个整数 `<normalization>` 选项，用于指定文档长度是否以及如何影响排名。该整数选项控制多种行为，因此是一个位掩码：可以使用 `|` 指定一种或多种行为（例如 `2|4`）。

- 0（默认值）忽略文档长度
- 1 将排名除以 1 加文档长度的对数
- 2 将排名除以文档长度
- 4 将排名除以范围之间的平均调和距离（仅由 `ts_rank_cd` 实现）
- 8 将排名除以文档中不重复单词的数量
- 16 将排名除以 1 加文档中不重复单词数量的对数
- 32 将排名除以排名本身加 1

如果指定了多个标志位，则按列表中的顺序应用这些转换。

需要注意，排名函数不使用任何全局信息，因此无法按有时所需的方式将排名公平地规范化为 1% 或 100%。可以应用规范化选项 `32 (rank/(rank+1))`，将所有排名缩放到 0 到 1 的范围内，但这当然只是外观上的变化，不会影响检索结果的顺序。

下面是一个只选择排名最高的十个匹配项的示例：

```sql
SELECT title, ts_rank_cd(textsearch, query) AS rank
FROM apod, to_tsquery('neutrino|(dark & matter)') query
WHERE query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |   rank
-----------------------------------------------+----------
 Neutrinos in the Sun                          |      3.1
 The Sudbury Neutrino Detector                 |      2.4
 A MACHO View of Galactic Dark Matter          |  2.01317
 Hot Gas and Dark Matter                       |  1.91171
 The Virgo Cluster: Hot Plasma and Dark Matter |  1.90953
 Rafting for Solar Neutrinos                   |      1.9
 NGC 4650A: Strange Galaxy and Dark Matter     |  1.85774
 Hot Gas and Dark Matter                       |   1.6123
 Ice Fishing for Cosmic Neutrinos              |      1.6
 Weak Lensing Distorts the Universe            | 0.818218
```

下面是使用规范化排名的相同示例：

```sql
SELECT title, ts_rank_cd(textsearch, query, 32 /* rank/(rank+1) */ ) AS rank
FROM apod, to_tsquery('neutrino|(dark & matter)') query
WHERE  query @@ textsearch
ORDER BY rank DESC
LIMIT 10;
                     title                     |        rank
-----------------------------------------------+-------------------
 Neutrinos in the Sun                          | 0.756097569485493
 The Sudbury Neutrino Detector                 | 0.705882361190954
 A MACHO View of Galactic Dark Matter          | 0.668123210574724
 Hot Gas and Dark Matter                       |  0.65655958650282
 The Virgo Cluster: Hot Plasma and Dark Matter | 0.656301290640973
 Rafting for Solar Neutrinos                   | 0.655172410958162
 NGC 4650A: Strange Galaxy and Dark Matter     | 0.650072921219637
 Hot Gas and Dark Matter                       | 0.617195790024749
 Ice Fishing for Cosmic Neutrinos              | 0.615384618911517
 Weak Lensing Distorts the Universe            | 0.450010798361481
```

排名可能成本很高，因为需要检查每份匹配文档的 tsvector，这可能受 I/O 限制，因此速度较慢。遗憾的是，几乎无法避免这一点，因为实际查询通常会产生大量匹配项。

## 突出显示结果 {#highlight-results}

为了展示检索结果，理想做法是显示每份文档的一部分，并说明它与查询的关系。通常，搜索引擎会显示带有标记检索词的文档片段。Apache Cloudberry 提供 `ts_headline` 函数来实现此功能。

```sql
ts_headline([<config> regconfig, ] <document> text, <query> tsquery [, <options> text ]) returns text
```

`ts_headline` 接受文档和查询，并返回文档摘录，其中突出显示查询中的词。可以通过 `*config*` 指定用于解析文档的配置；如果省略 `*config*`，则使用 `default_text_search_config` 配置。

如果指定 `*options*` 字符串，则它必须由一个或多个以逗号分隔的 `*option=value*` 对组成。可用选项如下：

- `MaxWords`、`MinWords`（整数）：这两个数字决定输出摘要的最长和最短长度。默认值分别为 35 和 15。
- `ShortWord`（整数）：除非单词是查询词，否则长度小于或等于此值的单词会在摘要开头和结尾被丢弃。默认值为 3，会删除常见的英语冠词。
- `HighlightAll`（布尔值）：整个文档都用作摘要，忽略前面三个参数。默认值为 `false`。
- `MaxFragments`（整数）：要显示的文本片段的最大数量。默认值 0，选择基于非片段的摘要生成方法。大于 0 的值选择基于片段的摘要生成方法（见下文）。
- `StartSel`、`StopSel`（字符串）：使用这些字符串界定文档中出现的查询词，使其与摘录的其他单词区分开来。默认值是“`<b>`”和“`</b>`”，适合用作 HTML 输出。
- `FragmentDelimiter`（字符串）：显示多个片段时，使用此字符串分隔片段。默认值是“`...`”。

这些选项名称不区分大小写。如果字符串值包含空格或逗号，则必须使用双引号。

在基于非片段的摘要生成中，`ts_headline` 会定位给定 `<query>` 的匹配项，并选择一个进行显示，优先选择允许的摘要长度内包含更多查询词的匹配项。在基于片段的摘要生成中，`ts_headline` 会定位查询匹配项，并将每个匹配项拆分为不超过 `MaxWords` 个单词的“片段”，优先选择包含更多查询词的片段，并在可能时“扩展”片段以包含周围单词。因此，当查询匹配范围覆盖文档的大段内容，或希望显示多个匹配项时，基于片段的模式更有用。在任一模式下，如果无法识别查询匹配项，则会显示文档开头 `MinWords` 个单词组成的单个片段。

例如：

```sql
SELECT ts_headline('english',
  'The most common type of search
is to find all documents containing given query terms
and return them in order of their similarity to the
query.',
  to_tsquery('english', 'query & similarity'));
                        ts_headline
------------------------------------------------------------
 containing given <b>query</b> terms                       +
 and return them in order of their <b>similarity</b> to the+
 <b>query</b>.

SELECT ts_headline('english',
  'Search terms may occur
many times in a document,
requiring ranking of the search matches to decide which
occurrences to display in the result.',
  to_tsquery('english', 'search & term'),
  'MaxFragments=10, MaxWords=7, MinWords=3, StartSel=<<, StopSel=>>');
                        ts_headline
------------------------------------------------------------
 <<Search>> <<terms>> may occur                            +
 many times ... ranking of the <<search>> matches to decide
```

`ts_headline` 使用原始文档，而不是 `tsvector` 摘要，因此可能速度较慢，应谨慎使用。
