---
title: "文本检索词典"
description: "Apache Cloudberry 全文检索解析器生成的词元会依次经过一系列词典，生成规范化的术语或“词位”。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/text-search-dictionaries.md"
---

词典可以针对不同方式和不同语言过滤、转换词元。本节包含以下子主题：

- [关于文本检索词典](#about-text-search-dictionaries)
- [停用词](#stop-words)
- [简单词典](#simple-dictionary)
- [同义词词典](#synonym-dictionary)
- [分类词典](#thesaurus-dictionary)
- [Ispell 词典](#ispell-dictionary)
- [SnowBall 词典](#snowball-dictionary)

## 关于文本检索词典 {#about-text-search-dictionaries}

词典用于消除不应参与检索的单词（*停用词*），并*规范化*单词，使同一个单词的不同派生形式能够匹配。成功规范化后的单词称为*词位*。除了提升检索质量之外，规范化和移除停用词还会减小文档 `tsvector` 表示的大小，从而提高性能。规范化不一定具有语言学意义，通常取决于应用语义。

下面是一些规范化示例：

- 语言学规范化 —— Ispell 词典会尝试将输入单词归约为规范形式；词干词典会移除单词结尾
- URL 地址可以规范化，使等价 URL 能够匹配：
    - `http://www.pgsql.ru/db/mw/index.html`
    - `http://www.pgsql.ru/db/mw/`
    - `http://www.pgsql.ru/db/../db/mw/index.html`
- 颜色名称可以替换为十六进制值，例如 `red`、`green`、`blue`、`magenta` → `FF0000`、`00FF00`、`0000FF`、`FF00FF`
- 如果要为数字建立索引，可以移除部分小数位，以减少可能的数字范围。例如，如果小数点后只保留两位，`3.14159265359`、`3.1415926` 和 `3.14` 在规范化后就会相同。

词典是一个接受词元作为输入并返回以下内容的程序：

- 如果输入词元为词典所知，则返回词位数组（请注意，一个词元可以生成多个词位）
- 返回一个设置了 `TSL_FILTER` 标志的单个词位，以便用新词元替换原词元，并将新词元传递给后续词典（执行此操作的词典称为*过滤词典*）
- 如果词典认识该词元，但它是停用词，则返回空数组
- 如果词典无法识别输入词元，则返回 `NULL`

Apache Cloudberry 为多种语言提供了预定义词典。系统还提供了若干预定义模板，可以使用自定义参数创建新词典。下面会介绍每个预定义词典模板。如果没有合适的现有模板，也可以创建新模板；Apache Cloudberry 发行版的 `contrib/` 目录中有相关示例。

文本检索配置将解析器与一组词典绑定起来，以处理解析器输出的词元。对于解析器可能返回的每种词元类型，配置都会指定一个单独的词典列表。解析器发现该类型的词元后，会依次查询列表中的每个词典，直到某个词典将其识别为已知单词。如果它被识别为停用词，或者没有词典识别出该词元，则会丢弃它，不为其建立索引，也不会检索它。通常，第一个返回 `non-NULL` 输出的词典会决定结果，系统不会再查询其余词典；但过滤词典可以用修改后的单词替换给定单词，再将修改后的单词传递给后续词典。

配置词典列表的一般规则是：首先放置最狭窄、最具体的词典，然后放置更通用的词典，最后放置能够识别所有内容的非常通用的词典，例如 Snowball 词干词典或 `simple`。例如，对于天文学专用检索（`astro_en` 配置），可以将 `asciiword`（ASCII 单词）词元类型绑定到天文学术语同义词词典、通用英语词典和 Snowball 英语词干词典：

```sql
ALTER TEXT SEARCH CONFIGURATION astro_en
    ADD MAPPING FOR asciiword WITH astrosyn, english_ispell, english_stem;
```

过滤词典可以放在列表中的任何位置，但放在末尾就没有用。过滤词典可用于对单词进行部分规范化，从而简化后续词典的工作。例如，可以使用过滤词典移除带重音字母的重音符号，[unaccent](https://www.postgresql.org/docs/14/unaccent.html) 模块就是这样做的。

## 停用词 {#stop-words}

停用词是非常常见、几乎出现在每份文档中、没有区分价值的单词。因此，在全文检索中可以忽略它们。例如，每份英文文本都包含 `a` 和 `the` 这样的单词，将它们存储在索引中没有意义。不过，停用词会影响 `tsvector` 中的位置，而位置又会影响排名：

```sql
SELECT to_tsvector('english', 'in the list of stop words');
        to_tsvector
----------------------------
 'list':3 'stop':5 'word':6
```

缺少位置 1、2、4 是因为这些位置对应停用词。对包含和不包含停用词的文档计算出的排名差异很大：

```sql
SELECT ts_rank_cd (to_tsvector('english', 'in the list of stop words'), to_tsquery('list & stop'));
 ts_rank_cd
------------
       0.05

SELECT ts_rank_cd (to_tsvector('english', 'list stop words'), to_tsquery('list & stop'));
 ts_rank_cd
------------
        0.1
```

词典如何处理停用词取决于具体词典。例如，`ispell` 词典先规范化单词，再检查停用词列表；`Snowball` 词干词典则先检查停用词列表。两者行为不同的原因是试图减少噪声。

## 简单词典 {#simple-dictionary}

简单词典模板将输入词元转换为小写，并在停用词文件中检查它。如果在文件中找到该词，则返回空数组，使该词元被丢弃。否则，返回该单词的小写形式作为规范化词位。也可以将词典配置为把非停用词报告为未识别，从而让它们传递给列表中的下一个词典。

下面是使用简单模板定义词典的示例：

```sql
CREATE TEXT SEARCH DICTIONARY public.simple_dict (
    TEMPLATE = pg_catalog.simple,
    STOPWORDS = english
);
```

这里，`english` 是停用词文件的基本名称。文件的完整名称是 `$SHAREDIR/tsearch_data/english.stop`，其中 `$SHAREDIR` 表示 Apache Cloudberry 安装的共享数据目录，通常为 `/usr/local/cloudberry-db-<version>/share/postgresql`（如果不确定，可以使用 `pg_config --sharedir` 确定）。文件格式很简单，每行一个单词。空行和行尾空格会被忽略，大写字母会折叠为小写，但不会对文件内容执行其他处理。

现在测试该词典：

```sql
SELECT ts_lexize('public.simple_dict', 'YeS');
 ts_lexize
-----------
 {yes}

SELECT ts_lexize('public.simple_dict', 'The');
 ts_lexize
-----------
 {}
```

如果单词不在停用词文件中，也可以选择返回 `NULL`，而不是返回小写单词。将词典的 `Accept` 参数设置为 false，即可选择此行为。继续上面的示例：

```sql
ALTER TEXT SEARCH DICTIONARY public.simple_dict ( Accept = false );

SELECT ts_lexize('public.simple_dict', 'YeS');
 ts_lexize
-----------
 {yes}

SELECT ts_lexize('public.simple_dict', 'The');
 ts_lexize
-----------
 {}
```

`Accept = true` 是默认设置，此时只有将简单词典放在词典列表末尾才有用，因为它永远不会将任何词元传递给后续词典。相反，`Accept = false` 只有在至少存在一个后续词典时才有用。

> [!WARNING]
> 大多数词典类型依赖配置文件，例如停用词文件。这些文件*必须*使用 UTF-8 编码存储。如果数据库使用其他编码，服务器读取文件时会将其转换为实际的数据库编码。
>
> 通常，数据库会话只在首次使用词典时读取一次词典配置文件。如果修改了配置文件，并希望强制现有会话读取新内容，请对该词典执行 `ALTER TEXT SEARCH DICTIONARY` 命令。这个更新可以是实际上不改变任何参数值的“空操作”更新。

## 同义词词典 {#synonym-dictionary}

该词典模板用于创建将单词替换为同义词的词典。不支持短语；如需支持短语，请使用分类词典模板（[分类词典](#thesaurus-dictionary)）。同义词词典可用于解决语言学问题，例如防止英语词干词典将单词“Paris”归约为“pari”。只需在同义词词典中加入一行 `Paris paris`，并将该词典放在 `english_stem` 词典之前即可。例如：

```sql
SELECT * FROM ts_debug('english', 'Paris');
   alias   |   description   | token |  dictionaries  |  dictionary  | lexemes 
-----------+-----------------+-------+----------------+--------------+---------
 asciiword | Word, all ASCII | Paris | {english_stem} | english_stem | {pari}

CREATE TEXT SEARCH DICTIONARY my_synonym (
    TEMPLATE = synonym,
    SYNONYMS = my_synonyms
);

ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR asciiword
    WITH my_synonym, english_stem;

SELECT * FROM ts_debug('english', 'Paris');
   alias   |   description   | token |       dictionaries        | dictionary | lexemes 
-----------+-----------------+-------+---------------------------+------------+---------
 asciiword | Word, all ASCII | Paris | {my_synonym,english_stem} | my_synonym | {paris}
```

同义词模板唯一必需的参数是 `SYNONYMS`，它是配置文件的基本名称；上例中为 `my_synonyms`。文件的完整名称是 `$SHAREDIR/tsearch_data/my_synonyms.syn`（其中 `$SHAREDIR` 表示 Apache Cloudberry 安装的共享数据目录）。文件格式是每行一个要替换的单词，单词后跟其同义词，中间用空白分隔。空行和行尾空格会被忽略。

同义词模板还有一个可选参数 `CaseSensitive`，默认值为 `false`。当 `CaseSensitive` 为 `false` 时，同义词文件中的单词和输入词元都会折叠为小写。当它为 `true` 时，单词和词元不会折叠为小写，而是按原样比较。

可以在配置文件中的同义词末尾放置星号（`*`）。这表示该同义词是一个前缀。在 `to_tsvector()` 中使用该条目时会忽略星号，但在 `to_tsquery()` 中使用时，结果会包含前缀匹配标记（参见[解析查询](/cloudberry/operate-with-data/sql-queries/full-text-search/control-text-search/#parse-queries)）。例如，假设 `$SHAREDIR/tsearch_data/synonym_sample.syn` 中包含以下条目：

```sql
postgres pgsql postgresql pgsql postgre pgsql 
gogle googl 
indices index*
```

此时会得到以下结果：

```sql
mydb=# CREATE TEXT SEARCH DICTIONARY syn (template=synonym, synonyms='synonym_sample');
mydb=# SELECT ts_lexize('syn', 'indices');
 ts_lexize
-----------
 {index}
(1 row)

mydb=# CREATE TEXT SEARCH CONFIGURATION tst (copy=simple);
mydb=# ALTER TEXT SEARCH CONFIGURATION tst ALTER MAPPING FOR asciiword WITH syn;
mydb=# SELECT to_tsvector('tst', 'indices');
 to_tsvector
-------------
 'index':1
(1 row)

mydb=# SELECT to_tsquery('tst', 'indices');
 to_tsquery
------------
 'index':*
(1 row)

mydb=# SELECT 'indexes are very useful'::tsvector;
            tsvector             
---------------------------------
 'are' 'indexes' 'useful' 'very'
(1 row)

mydb=# SELECT 'indexes are very useful'::tsvector @@ to_tsquery('tst', 'indices');
 ?column?
----------
 t
(1 row)
```

## 分类词典 {#thesaurus-dictionary}

分类词典（有时缩写为 TZ）是单词集合，其中包含单词和短语之间关系的信息，也就是更宽泛的术语（BT）、更狭窄的术语（NT）、首选术语、非首选术语、相关术语等。

分类词典的基本行为是将所有非首选术语替换为一个首选术语，并可选择保留原始术语以便建立索引。Apache Cloudberry 当前的分类词典实现是在同义词词典基础上扩展而来，并增加了*短语*支持。分类词典需要采用以下格式的配置文件：

```sql
# this is a comment
sample word(s) : indexed word(s)
more sample word(s) : more indexed word(s)
...
```

其中冒号（`:`）用作短语与其替换项之间的分隔符。

分类词典使用一个*子词典*（在词典配置中指定），在检查短语匹配之前规范化输入文本。只能选择一个子词典。如果子词典无法识别某个单词，则会报告错误。此时，应删除该单词，或让子词典能够识别它。可以在索引单词开头放置星号（`*`），以跳过对子词典的应用，但所有示例单词*必须*为子词典所知。

如果有多个短语匹配输入，分类词典会选择最长匹配；如果长度相同，则使用最后一个定义打破平局。

不能指定由子词典识别的特定停用词；相反，应使用 `?` 标记任意停用词可以出现的位置。例如，假设根据子词典，`a` 和 `the` 是停用词：

```sql
? one ? two : swsw
```

该定义会匹配 `a one the two` 和 `the one a two`；两者都会被替换为 `swsw`。

由于分类词典能够识别短语，它必须保存状态并与解析器交互。分类词典使用这些分配来检查是否应处理下一个单词，或停止累积。必须谨慎配置分类词典。例如，如果将分类词典配置为只处理 `asciiword` 词元，那么类似 `one 7` 的分类词典定义将无法工作，因为 `uint` 词元类型没有分配给分类词典。

> [!WARNING]
> 分类词典在建立索引期间使用，因此分类词典参数的任何更改都要求重新建立索引。对于大多数其他词典类型，添加或删除停用词等小改动不要求重新建立索引。

**分类词典配置**

要定义新的分类词典，请使用 `thesaurus` 模板。例如：

```sql
CREATE TEXT SEARCH DICTIONARY thesaurus_simple (
    TEMPLATE = thesaurus,
    DictFile = mythesaurus,
    Dictionary = pg_catalog.english_stem
);
```

这里：

- `thesaurus_simple` 是新词典的名称
- `mythesaurus` 是分类词典配置文件的基本名称。（完整名称为 `$SHAREDIR/tsearch_data/mythesaurus.ths`，其中 `$SHAREDIR` 表示安装的共享数据目录。）
- `pg_catalog.english_stem` 是用于分类词典规范化的子词典（这里是 Snowball 英语词干词典）。请注意，子词典有自己的配置（例如停用词），此处未显示。

现在可以在配置中将分类词典 `thesaurus_simple` 绑定到所需的词元类型，例如：

```sql
ALTER TEXT SEARCH CONFIGURATION russian
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart
    WITH thesaurus_simple;
```

**分类词典示例**

考虑一个简单的天文学分类词典 `thesaurus_astro`，其中包含一些天文学词组：

```sql
supernovae stars : sn
crab nebulae : crab
```

下面创建一个词典，并将某些词元类型绑定到天文学分类词典和英语词干词典：

```sql
CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
    TEMPLATE = thesaurus,
    DictFile = thesaurus_astro,
    Dictionary = english_stem
);

ALTER TEXT SEARCH CONFIGURATION russian
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart
    WITH thesaurus_astro, english_stem;
```

现在可以查看它的工作方式。`ts_lexize` 不太适合测试分类词典，因为它会将输入作为单个词元处理。相反，可以使用 `plainto_tsquery` 和 `to_tsvector`，它们会将输入字符串拆分为多个词元：

```sql
SELECT plainto_tsquery('supernova star');
 plainto_tsquery
-----------------
 'supernova' & 'star'

SELECT to_tsvector('supernova star');
 to_tsvector
-------------
 'star':2 'supernova':1
```

原则上，如果将参数加引号，也可以使用 `to_tsquery`：

```sql
SELECT to_tsquery('''supernova star''');
 to_tsquery
------------
 'supernova' & 'star'
```

请注意，`supernova star` 会在 `thesaurus_astro` 中匹配 `supernovae stars`，因为在 `thesaurus` 定义中指定了 `english_stem` 词干词典。词干词典移除了 `e` 和 `s`。

如果要同时为原始短语和替换项建立索引，只需将原始短语包含在定义的右侧部分：

```sql
supernovae stars : sn supernovae stars

SELECT plainto_tsquery('supernova star');
       plainto_tsquery
-----------------------------
 'supernova' & 'star'
```

## Ispell 词典 {#ispell-dictionary}

Ispell 词典模板支持*形态词典*，可以将一个单词的许多不同语言形式规范化为同一个词位。例如，英语 Ispell 词典可以匹配检索词 `bank` 的各种词形变化，例如 `banking`、`banked`、`banks`、`banks`' 和 `bank's`。

Apache Cloudberry 标准发行版不包含任何 Ispell 配置文件。可以从 [Ispell](https://www.cs.hmc.edu/~geoff/ispell.html) 获取多种语言的词典。此外，还支持一些较新的词典文件格式：[MySpell](http://en.wikipedia.org/wiki/MySpell)（OO \< 2.0.1）和 [Hunspell](http://sourceforge.net/projects/hunspell/)（OO \>= 2.0.2）。[OpenOffice Wiki](http://wiki.services.openoffice.org/wiki/Dictionaries) 上提供了大量词典。

创建 Ispell 词典需要执行以下步骤：

1. 下载词典配置文件。OpenOffice 扩展文件使用 `.oxt` 扩展名。需要提取 `.aff` 和 `.dic` 文件，并将扩展名改为 `.affix` 和 `.dict`。对于某些词典文件，还需要使用命令将字符转换为 UTF-8 编码（例如，对于挪威语词典）：

    ```bash
    iconv -f ISO_8859-1 -t UTF-8 -o nn_no.affix nn_NO.aff
    iconv -f ISO_8859-1 -t UTF-8 -o nn_no.dict nn_NO.dic
    ```

2. 将文件复制到 `$SHAREDIR/tsearch_data` 目录。
3. 使用以下命令将文件加载到 PostgreSQL 中：

    ```sql
    CREATE TEXT SEARCH DICTIONARY english_hunspell (
    TEMPLATE = ispell,
    DictFile = en_us,
    AffFile = en_us,
    Stopwords = english);
    ```

这里，`DictFile`、`AffFile` 和 `StopWords` 指定词典文件、词缀文件和停用词文件的基本名称。停用词文件的格式与上面 `simple` 词典类型中说明的格式相同。其他文件的格式未在此说明，但可以从上面提到的网站获取。

Ispell 词典通常只能识别有限的单词集合，因此后面应接一个更宽泛的词典，例如能够识别所有内容的 Snowball 词典。

Ispell 的 `.affix` 文件具有以下结构：

```sql
prefixes
flag *A:
    .           >   RE      # As in enter > reenter
suffixes
flag T:
    E           >   ST      # As in late > latest
    [^AEIOU]Y   >   -Y,IEST # As in dirty > dirtiest
    [AEIOU]Y    >   EST     # As in gray > grayest
    [^EY]       >   EST     # As in small > smallest
```

`.dict` 文件具有以下结构：

```
lapse/ADGRS
lard/DGRS
large/PRTY
lark/MRS
```

`.dict` 文件的格式如下：

```
basic_form/affix_class_name
```

在 `.affix` 文件中，每个词缀标志使用以下格式描述：

```
condition > [-stripping_letters,] adding_affix
```

这里，condition 的格式类似正则表达式的格式，可以使用 `[...]` 和 `[^...]` 分组。例如，`[AEIOU]Y` 表示单词的最后一个字母是“y”，倒数第二个字母是“a”、“e”、“i”、“o”或“u”。`[^EY]` 表示最后一个字母既不是“e”也不是“y”。

Ispell 词典支持拆分复合词，这是一个有用的功能。请注意，词缀文件应使用 `compoundwords controlled` 语句指定一个特殊标志，用于标记可以参与复合构造的词典单词：

```
compoundwords  controlled z
```

下面是挪威语的几个示例：

```
SELECT ts_lexize('norwegian_ispell', 'overbuljongterningpakkmesterassistent');
   {over,buljong,terning,pakk,mester,assistent}
SELECT ts_lexize('norwegian_ispell', 'sjokoladefabrikk');
   {sjokoladefabrikk,sjokolade,fabrikk}
```

MySpell 格式是 Hunspell 格式的子集。Hunspell 的 `.affix` 文件具有以下结构：

```
PFX A Y 1
PFX A   0     re         .
SFX T N 4
SFX T   0     st         e
SFX T   y     iest       [^aeiou]y
SFX T   0     est        [aeiou]y
SFX T   0     est        [^ey]
```

词缀类的第一行是头部。词缀规则的字段列在头部之后：

- 参数名称（PFX 或 SFX）
- 标志（词缀类的名称）
- 从单词开头（前缀）或结尾（后缀）剥离的字符
- 添加的词缀
- 条件，其格式类似正则表达式的格式。

`.dict` 文件与 Ispell 的 `.dict` 文件类似：

```
larder/M
lardy/RT
large/RSPMYT
largehearted
```

> [!NOTE]
> MySpell 不支持复合词。Hunspell 对复合词有复杂的支持。目前，Apache Cloudberry 只实现了 Hunspell 的基本复合词操作。

## SnowBall 词典 {#snowball-dictionary}

Snowball 词典模板基于 Martin Porter 的项目；Martin Porter 是广受欢迎的英语 Porter 词干算法的发明者。Snowball 现在为多种语言提供词干提取算法（更多信息请参见 [Snowball 网站](http://snowballstem.org/)）。每种算法都知道如何在其语言范围内，将单词的常见变体归约为基本形式或词干形式。Snowball 词典需要一个语言参数来确定使用哪种词干算法，还可以选择指定停用词文件名，以提供要消除的单词列表。（Apache Cloudberry 的标准停用词列表也由 Snowball 项目提供。）例如，系统内置了一个等价于以下内容的定义：

```sql
CREATE TEXT SEARCH DICTIONARY english_stem (
    TEMPLATE = snowball,
    Language = english,
    StopWords = english
);
```

停用词文件的格式与前面说明的相同。

Snowball 词典会识别所有内容，无论它是否能够简化某个单词，因此应将它放在词典列表末尾。如果放在其他词典之前，就没有用，因为词元永远不会经过它传递到下一个词典。
