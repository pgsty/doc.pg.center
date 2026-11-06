---
title: "关于全文检索"
description: "本文概述 Apache Cloudberry 全文检索、基本文本检索表达式，以及文本检索的配置和定制。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/full-text-search-intro.md"
---

本节包含以下子主题：

- [什么是文档？](#what-is-a-document)
- [基本文本匹配](#basic-text-matching)
- [配置](#configurations)

全文检索（或简称“文本检索”）可以识别满足查询条件的自然语言*文档*，并可选择按文档与查询的相关性对结果排名。最常见的检索类型是找出包含给定*查询词*的所有文档，并按照它们与查询的*相似性*排序返回。

Apache Cloudberry 提供 `tsvector` 数据类型来存储预处理后的文档，并提供 `tsquery` 数据类型来存储处理后的查询。这些数据类型有许多可用的函数和运算符，其中最重要的是匹配运算符 `@@`；我们将在[基本文本匹配](#basic-text-matching)中介绍它。可以使用索引（[文本检索的 GiST 和 GIN 索引](/cloudberry/operate-with-data/sql-queries/full-text-search/preferred-indexes-for-full-text-search/)）加速全文检索。

查询和相似性的概念都非常灵活，取决于具体应用。最简单的检索将查询视为一组单词，将相似性视为查询词在文档中的出现频率。

Apache Cloudberry 支持文本数据类型的标准文本匹配运算符 `~`、`~*`、`LIKE` 和 `ILIKE`，但这些运算符缺少文档检索所需的许多基本特性：

- 没有语言学支持，即使是英语也不例外。正则表达式并不够用，因为它们无法轻松处理派生词，例如 `satisfies` 和 `satisfy`。搜索 `satisfy` 时，可能会漏掉包含 `satisfies` 的文档，尽管你通常希望找到这些文档。可以使用 OR 搜索多个派生形式，但这既繁琐又容易出错（有些单词可能有几千个派生形式）。
- 不会对检索结果排序（排名），因此当找到数千份匹配文档时，这些运算符难以发挥作用。
- 通常速度较慢，因为没有索引支持，每次检索都必须处理所有文档。

全文索引允许预处理文档并保存索引，以便之后快速检索。预处理包括：

- **将文档解析为词元。** 识别不同类别的词元很有用，例如数字、单词、复合词和电子邮件地址，以便以不同方式处理它们。原则上，词元类别取决于具体应用，但在大多数情况下，使用预定义的类别集合就足够了。Apache Cloudberry 使用*解析器*执行此步骤。系统提供标准解析器，也可以针对特定需求创建定制解析器。
- **将词元转换为词位。** 词位和词元一样是字符串，但已经过*规范化*，使同一个单词的不同形式变得一致。例如，规范化几乎总是包括将大写字母折叠为小写，通常还会移除后缀（例如英语中的 s 或 es）。这样，检索时无需繁琐地输入所有可能的变体，就可以找到同一个单词的不同形式。此外，这一步通常会消除*停用词*，也就是过于常见、对检索没有帮助的单词。（简而言之，词元是文档文本的原始片段，而词位是被认为适合用于索引和检索的单词。）Apache Cloudberry 使用*词典*执行此步骤。系统提供多种标准词典，也可以针对特定需求创建定制词典。
- **存储经过预处理、针对检索优化的文档。** 例如，可以将每个文档表示为规范化词位的排序数组。除了词位之外，通常还需要存储位置信息，以便进行*邻近排名*，这样包含更“密集”查询词区域的文档会比查询词分散的文档获得更高排名。

词典可以细粒度地控制词元的规范化方式。使用适当的词典，可以：

- 定义不应建立索引的停用词。
- 使用 Ispell 将同义词映射为一个单词。
- 使用分类词典将短语映射为一个单词。
- 使用 Ispell 词典将一个单词的不同变体映射为规范形式。
- 使用 Snowball 词干提取规则将一个单词的不同变体映射为规范形式。

## 什么是文档 {#what-is-a-document}

在全文检索系统中，*文档*是检索的基本单位，例如杂志文章或电子邮件。文本检索引擎必须能够解析文档，并存储词位（关键词）与其所属文档之间的关联。之后，系统使用这些关联搜索包含查询词的文档。

在 Apache Cloudberry 内进行检索时，文档通常是数据库表某行中的文本字段，也可能是这类字段的组合（拼接），这些字段可以存储在多个表中或动态获取。换句话说，文档可以由用于建立索引的不同部分构造出来，并且整体上可能并未存储在任何地方。例如：

```sql
SELECT title || ' ' ||  author || ' ' ||  abstract || ' ' || body AS document
FROM messages
WHERE mid = 12;

SELECT m.title || ' ' || m.author || ' ' || m.abstract || ' ' || d.body AS document
FROM messages m, docs d
WHERE m.mid = d.did AND m.mid = 12;
```

> [!NOTE]
> 在这些示例查询中，应使用 `coalesce`，以防单个 `NULL` 属性导致整个文档的结果为 `NULL`。

另一种做法是将文档作为简单文本文件存储在文件系统中。此时，可以使用数据库存储全文索引并执行检索，再使用某个唯一标识符从文件系统取回文档。然而，从数据库外部取回文件需要超级用户权限或特殊函数支持，因此通常不如将所有数据保存在 Apache Cloudberry 中方便。此外，将所有内容保存在数据库中，可以方便地访问文档元数据，以辅助建立索引和显示文档。

对于文本检索，每个文档都必须转换为预处理后的 `tsvector` 格式。检索和排名完全基于文档的 tsvector 表示执行；只有在选定文档并准备向用户显示时，才需要取回原始文本。因此，我们经常将 `tsvector` 称为文档，但它当然只是完整文档的紧凑表示。

## 基本文本匹配 {#basic-text-matching}

Apache Cloudberry 中的全文检索基于匹配运算符 `@@`。如果 `tsvector`（文档）匹配 `tsquery`（查询），该运算符就返回 `true`。无论先写哪种数据类型，结果都不受影响：

```sql
SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector @@ 'cat & rat'::tsquery;
 ?column?
----------
 t

SELECT 'fat & cow'::tsquery @@ 'a fat cat sat on a mat and ate a fat rat'::tsvector;
 ?column?
----------
 f
```

如上面的示例所示，`tsquery` 并不只是原始文本，`tsvector` 也一样。`tsquery` 包含检索词，这些词必须已经是规范化的词位，并且可以使用 AND、OR、NOT 和 FOLLOWED BY 运算符组合多个词位。`to_tsquery`、`plainto_tsquery` 和 `phraseto_query` 函数可以帮助将用户编写的文本转换为适当的 `tsquery`，例如将文本中的单词规范化。同样，可以使用 `to_tsvector` 解析并规范化文档字符串。因此，实际的文本检索匹配通常更像这样：

```sql
SELECT to_tsvector('fat cats ate fat rats') @@ to_tsquery('fat & rat');
 ?column? 
----------
 t
```

如果写成下面这样，该匹配不会成功：

```sql
SELECT 'fat cats ate fat rats'::tsvector @@ to_tsquery('fat & rat');
 ?column? 
----------
 f
```

这是因为这里不会对单词 `rats` 进行规范化。`tsvector` 的元素是词位，假定它们已经完成规范化，因此 `rats` 与 `rat` 不匹配。

`@@` 运算符还支持 `text` 输入，因此在简单情况下可以跳过将文本字符串显式转换为 `tsvector` 或 `tsquery`。可用的形式如下：

```sql
tsvector @@ tsquery
tsquery  @@ tsvector
text @@ tsquery
text @@ text
```

前两个形式已经在上面见过。`text @@ tsquery` 等价于 `to_tsvector(x) @@ y`。`text @@ text` 等价于 `to_tsvector(x) @@ plainto_tsquery(y)`。

在 `tsquery` 中，`&`（AND）运算符表示两个参数都必须出现在文档中，匹配才会成立。同样，`|`（OR）运算符表示其参数至少有一个必须出现，而 `!`（NOT）运算符表示其参数必须不出现，匹配才会成立。例如，查询 `fat & ! rat` 会匹配包含 `fat` 但不包含 `rat` 的文档。

借助 `<->`（FOLLOWED BY）`tsquery` 运算符可以检索短语；只有当两个参数匹配且相邻、顺序也符合给定顺序时，该运算符才会匹配。例如：

```sql
SELECT to_tsvector('fatal error') @@ to_tsquery('fatal <-> error');
 ?column? 
----------
 t

SELECT to_tsvector('error is not fatal') @@ to_tsquery('fatal <-> error');
 ?column? 
----------
 f
```

FOLLOWED BY 运算符还有一种更通用的形式 `<N>`，其中 _N_ 是整数，表示匹配词位位置之间的差值。`<1>` 与 `<->` 相同，而 `<2>` 允许匹配词之间恰好出现另一个词位，依此类推。`phraseto_tsquery` 函数使用此运算符构造 `tsquery`，即使短语中有些单词是停用词，也能匹配多词短语。例如：

```sql
SELECT phraseto_tsquery('cats ate rats');
       phraseto_tsquery        
-------------------------------
 'cat' <-> 'ate' <-> 'rat'

SELECT phraseto_tsquery('the cats ate the rats');
       phraseto_tsquery        
-------------------------------
 'cat' <-> 'ate' <2> 'rat'
```

有一种有时很有用的特殊情况：可以使用 `<0>` 要求两个模式匹配同一个单词。

可以使用圆括号控制 tsquery 运算符的嵌套。没有圆括号时，`|` 的绑定最弱，其次是 `&`，再其次是 `<->`，而 `!` 的绑定最强。

需要注意的是，`AND`／`OR`／`NOT` 运算符位于 FOLLOWED BY 运算符的参数中时，与不位于其中时的含义略有不同，因为在 FOLLOWED BY 中，匹配的确切位置很重要。例如，通常 `!x` 只匹配任何位置都不包含 `x` 的文档。但 `!x <-> y` 会在 未紧跟在 `x` 后面时匹配 `y`；文档中其他位置出现 `x` 并不会阻止匹配。另一个例子是，`x & y` 通常只要求 `x` 和 `y` 在文档中的某处都出现，但 `(x & y) <-> z` 要求 `x` 和 `y` 在同一位置、紧邻 `z` 之前匹配。因此，该查询与 `x <-> z & y <-> z` 的行为不同；后者会匹配包含两个独立序列 `x z` 和 `y z` 的文档。（按这种写法，当前这个具体查询没有用，因为 `x` 和 `y` 不可能在同一位置匹配；但对于前缀匹配模式等更复杂的情况，这种形式的查询可能有用。）

## 配置 {#configurations}

上面都是简单的文本检索示例。如前所述，全文检索功能还包括许多其他能力：跳过某些单词的索引（停用词）、处理同义词，以及使用复杂的解析方式，例如不仅根据空白进行解析。这些功能由*文本检索配置*控制。Apache Cloudberry 为多种语言提供了预定义配置，也可以轻松创建自己的配置。（psql 的 `dF` 命令显示所有可用配置。）

安装期间会选择适当的配置，并在 `postgresql.conf` 中相应设置 `default_text_search_config`。如果整个集群使用同一个文本检索配置，可以使用 `postgresql.conf` 中的值。如果集群中的不同数据库使用不同配置、但每个数据库内部使用同一配置，请使用 `ALTER DATABASE ... SET`。否则，可以在每个会话中设置 `default_text_search_config`。

每个依赖配置的文本检索函数都有一个可选的 `regconfig` 参数，因此可以显式指定要使用的配置。只有省略该参数时，才会使用 `default_text_search_config`。

为便于构建定制文本检索配置，配置由更简单的数据库对象构成。Apache Cloudberry 的文本检索功能提供四类与配置相关的数据库对象：

- **文本检索解析器**将文档拆分为词元，并对每个词元分类（例如分类为单词或数字）。
- **文本检索词典**将词元转换为规范形式，并拒绝停用词。
- **文本检索模板**提供词典所依赖的函数。（词典只需指定一个模板及该模板的一组参数。）
- **文本检索配置**选择一个解析器和一组词典，用于规范化解析器生成的词元。

文本检索解析器和模板由底层 C 函数组成；因此，开发新的解析器和模板需要具备 C 编程能力，而将其安装到数据库中需要超级用户权限。（Apache Cloudberry 发行版的 `contrib/` 目录中有附加解析器和模板示例。）由于词典和配置只是为底层解析器和模板设置参数并将它们连接起来，因此创建新词典或配置不需要特殊权限。
