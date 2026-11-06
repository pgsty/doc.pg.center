---
title: "其他文本检索功能"
description: "Apache Cloudberry 提供了其他函数和运算符，可用于操作检索向量和查询向量，以及重写检索查询。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/additional-text-search-features.md"
---

本节包含以下子主题：

- [操作文档](#manipulate-documents)
- [操作查询](#manipulate-queries)
- [重写查询](#rewrite-queries)
- [收集文档统计信息](#gather-document-statistics)

## 操作文档 {#manipulate-documents}

[解析文档](/cloudberry/operate-with-data/sql-queries/full-text-search/control-text-search/#parse-documents)介绍了如何将原始文本文档转换为 `tsvector` 值。Apache Cloudberry 还提供了用于操作已经采用 `tsvector` 形式的文档的函数和运算符。

`tsvector || tsvector`：`tsvector` 连接运算符返回一个向量，其中包含两个参数向量的词位和位置信息。连接时会保留位置和权重标签。右侧向量中的位置会按左侧向量中提到的最大位置进行偏移，因此结果几乎等同于对两个原始文档字符串的连接结果执行 `to_tsvector`。（这种等价并不完全成立，因为从左侧参数末尾移除的停用词不会影响结果；而如果使用文本连接，它们原本会影响右侧参数中词位的位置。）

与在应用 `to_tsvector` 之前连接文本相比，使用向量形式的连接有一个优点：可以使用不同配置解析文档的不同部分。此外，由于 `setweight` 函数会以相同方式标记给定向量中的所有词位，如果希望为文档不同部分设置不同权重，就必须先解析文本并执行 `setweight`，然后再连接。

`setweight(<vector> tsvector, <weight> "char") returns tsvector`：`setweight` 返回输入向量的副本，其中每个位置都标记为给定的 `<weight>`，可以是 `A`、`B`、`C` 或 `D`。（`D` 是新向量的默认值，因此不会显示在输出中。）连接向量时会保留这些标签，因此排名函数可以为文档不同部分的单词设置不同权重。

请注意，权重标签应用于**位置**，而不是**词位**。如果输入向量已去除位置，则 `setweight` 不执行任何操作。

`length(<vector> tsvector) returns integer`：返回向量中存储的词位数量。

`strip(vector tsvector) returns tsvector`：返回一个向量，其中列出与给定向量相同的词位，但不包含位置或权重信息。结果通常比未去除信息的向量小得多，但用途也更少。去除信息的向量在相关性排名方面不如未去除信息的向量。由于无法确定词位出现之间的距离，`<->`（FOLLOWED BY）`tsquery` 运算符也永远不会匹配已去除信息的输入。

完整的 tsvector 相关函数列表请参见 PostgreSQL 文档中的[文本检索函数和运算符](https://www.postgresql.org/docs/14/functions-textsearch.html)。

## 操作查询 {#manipulate-queries}

[解析查询](/cloudberry/operate-with-data/sql-queries/full-text-search/control-text-search/#parse-queries)介绍了如何将原始文本查询转换为 `tsquery` 值。Apache Cloudberry 还提供了用于操作已经采用 `tsquery` 形式的查询的函数和运算符。

`tsquery && tsquery`
:   返回给定两个查询的 AND 组合。

`tsquery || tsquery`：返回给定两个查询的 OR 组合。

`!! tsquery`：返回给定查询的否定（NOT）。

`tsquery <-> tsquery`：使用 `<->`（FOLLOWED BY）`tsquery` 运算符，返回一个查询，用于搜索第一个给定查询的匹配项后面紧邻第二个给定查询匹配项的情况。例如：

```sql
SELECT to_tsquery('fat') <-> to_tsquery('cat | rat');
          ?column?
----------------------------
 'fat' <-> ( 'cat' | 'rat' )
```

`tsquery_phrase(<query1> tsquery, <query2> tsquery [, <distance> integer ]) returns tsquery`：使用 `<N>` `tsquery` 运算符，返回一个查询，用于搜索第一个给定查询的匹配项后面、相距恰好 `<distance>` 个词位的第二个给定查询匹配项。例如：

```sql
SELECT tsquery_phrase(to_tsquery('fat'), to_tsquery('cat'), 10);
  tsquery_phrase
------------------
 'fat' <10> 'cat'
```

`numnode(<query> tsquery) returns integer`：返回一个 tsquery 中的节点数（词位加运算符）。此函数可用于确定**查询**是否有意义（返回值大于 0），或者是否只包含停用词（返回值为 0）。例如：

```sql
SELECT numnode(plainto_tsquery('the any'));
NOTICE:  query contains only stopword(s) or doesn't contain lexeme(s), ignored
 numnode
---------
       0

SELECT numnode('foo & bar'::tsquery);
 numnode
---------
       3
```

`querytree(<query> tsquery) returns text`：返回 tsquery 中可以用于搜索索引的部分。此函数可用于检测无法建立索引的查询，例如只包含停用词或只包含否定项的查询。例如：

```sql
SELECT querytree(to_tsquery('!defined'));
 querytree
-----------
```

## 重写查询 {#rewrite-queries}

`ts_rewrite` 函数族会在给定的 `tsquery` 中搜索目标子查询的出现，并将每一次出现替换为替代子查询。从本质上说，该操作是针对 `tsquery` 的子串替换。目标与替代的组合可以视为一条*查询重写规则*。一组这样的重写规则可以成为非常强大的检索辅助工具。例如，可以使用同义词扩展检索（例如 `new york`、`big apple`、`nyc`、`gotham`），或者收窄检索，将用户引向某个热门主题。此功能与分类词典（[分类词典](/cloudberry/operate-with-data/sql-queries/full-text-search/text-search-dictionaries/#thesaurus-dictionary)）在功能上存在一定重叠。不过，可以随时修改一组重写规则而无需重建索引，而更新分类词典必须重建索引才能生效。

`ts_rewrite(<query> tsquery, <target> tsquery, <substitute> tsquery) returns tsquery`：这种形式的 `ts_rewrite` 只应用一条重写规则：无论 `<target>` 在 `<query>` 中何处出现，都将其替换为 `<substitute>`。例如：

```sql
SELECT ts_rewrite('a & b'::tsquery, 'a'::tsquery, 'c'::tsquery);
 ts_rewrite
------------
 'b' & 'c'
```

`ts_rewrite(<query> tsquery, <select> text) returns tsquery`：这种形式的 `ts_rewrite` 接受一个起始 `<query>` 和一条 SQL `<select>` 命令，后者以文本字符串形式提供。`<select>` 必须生成两个 `tsquery` 类型的列。对于 `<select>` 结果的每一行，都会在当前 `<query>` 值中，将第一列的值（目标）替换为第二列的值（替代）。例如：

```sql
CREATE TABLE aliases (id int, t tsquery, s tsquery);
INSERT INTO aliases VALUES(1, 'a', 'c');

SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM aliases');
 ts_rewrite
------------
 'b' & 'c'
```

请注意，以这种方式应用多条重写规则时，应用顺序可能很重要；因此，实际使用中应让源查询按某个排序键执行 `ORDER BY`。

考虑一个真实的天文学示例。我们将使用表驱动的重写规则扩展查询 `supernovae`：

```sql
CREATE TABLE aliases (id int, t tsquery primary key, s tsquery);
INSERT INTO aliases VALUES(1, to_tsquery('supernovae'), to_tsquery('supernovae|sn'));

SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT t, s FROM aliases');
           ts_rewrite            
---------------------------------
 'crab' & ( 'supernova' | 'sn' )
```

只需更新表，就可以更改重写规则：

```sql
UPDATE aliases
SET s = to_tsquery('supernovae|sn & !nebulae')
WHERE t = to_tsquery('supernovae');

SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT t, s FROM aliases');
                 ts_rewrite                  
---------------------------------------------
 'crab' & ( 'supernova' | 'sn' & !'nebula' )
```

重写规则很多时，重写可能会很慢，因为系统会检查每条规则是否可能匹配。可以使用 `tsquery` 类型的包含运算符过滤掉明显不可能成为候选项的规则。在下面的示例中，只选择可能匹配原始查询的规则：

```sql
SELECT ts_rewrite('a & b'::tsquery,
                  'SELECT t,s FROM aliases WHERE ''a & b''::tsquery @> t');
 ts_rewrite
------------
 'b' & 'c'
```

## 收集文档统计信息 {#gather-document-statistics}

`ts_stat` 函数可用于检查配置以及寻找停用词候选项。

```sql
ts_stat(<sqlquery> text, [ <weights> text, ]
        OUT <word> text, OUT <ndoc> integer,
        OUT <nentry> integer) returns setof record
```

`<sqlquery>` 是一个文本值，其中包含一条 SQL 查询；该查询必须返回单个 `tsvector` 列。`ts_stat` 执行该查询，并返回 `tsvector` 数据中每个不重复词位（单词）的统计信息。返回的列如下：

- `<word> text` —— 词位的值
- `<ndoc> integer` —— 该单词出现过的文档数（`tsvector` 数量）
- `<nentry> integer` —— 该单词出现的总次数

如果提供 weights，则只统计具有这些权重之一的出现。

例如，要找出文档集合中出现频率最高的十个单词：

```sql
SELECT * FROM ts_stat('SELECT vector FROM apod')
ORDER BY nentry DESC, ndoc DESC, word
LIMIT 10;
```

下面的示例相同，但只统计权重为 `A` 或 `B` 的单词出现次数：

```sql
SELECT * FROM ts_stat('SELECT vector FROM apod', 'ab')
ORDER BY nentry DESC, ndoc DESC, word
LIMIT 10;
```
