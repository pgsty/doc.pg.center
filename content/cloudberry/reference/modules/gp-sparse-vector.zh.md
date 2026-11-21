---
title: gp_sparse_vector
description: gp_sparse_vector 实现 svec 稀疏向量数据类型及相关函数、操作符和聚合。
weight: 120
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/gp-sparse-vector.md
---

`gp_sparse_vector` 模块实现名为 `svec` 的稀疏向量数据类型，以及相关函数、操作符和聚合。此类型压缩存储零值，以加快浮点数的向量计算。

## 安装 {#installation}

`gp_sparse_vector` 始终随 Apache Cloudberry 构建和安装。它属于默认的 `gpcontrib` 构建目标，不依赖任何 `configure` 选项。

此模块是一个扩展（版本为 `1.0.1`）。使用前，在每个需要使用它的数据库中创建扩展：

```sql
CREATE EXTENSION gp_sparse_vector;
```

此模块不需要 `shared_preload_libraries`，也不需要重启。

> [!NOTE]
> 扩展在 `sparse_vector` 模式中创建所有对象。使用时需以模式限定对象名（例如 `sparse_vector.svec`），或将该模式加入搜索路径：
>
```sql
SET search_path TO sparse_vector, public;
```
>
> 本文中的示例假定 `sparse_vector` 已在搜索路径中。

## 关于 svec 数据类型 {#about-the-svec-data-type}

使用浮点数数组进行各种计算时，常会遇到很长的连续零值。在科学计算、零售优化和文本处理应用中，这种情况很常见。每个浮点数在内存或磁盘上占用 8 字节，因此存储这些零值往往不现实。许多计算也可以通过跳过零值获益。

例如，假设以下双精度浮点数数组以 `float8[]` 存储：

```
'{0, 33, <40,000 zeros>, 12, 22 }'::float8[]
```

这种数组在文本处理中很常见：词典可能包含 4 万到 10 万个词项，每个向量存储各个单词在某篇文档中的出现次数。此数组占用略多于 320KB 的内存或磁盘空间，其中大部分是零。对这些数据的任何操作都会处理 40,001 个无关紧要的字段。

内置数组数据类型为空值提供位图，但并不适合此场景。它没有针对 `float8[]` 或连续零值（而非空值）进行优化，位图也未经过游程编码（RLE）压缩。即使将数组中的每个零存为 `NULL`，标记空值的位图仍需占用 5KB。

`svec` 类型采用简单的 RLE 方案，特别注重零值处理效率。使用该方案，示例向量的位图仅需 6 字节。

> [!NOTE]
> `svec` 只支持 `float8` 向量值。

### 创建 svec 值 {#create-svec-values}

可以直接从浮点数数组构造 `svec`：

```sql
SELECT ('{0, 13, 37, 53, 0, 71 }'::float8[])::svec;
```

`svec` 的文本表示形式为 `{counts}:{values}`，每个计数表示对应值重复的次数。例如，`'{1,2,3,4}:{3,4,5,6}'::svec` 是含有 10 个元素的向量：一个 `3`、两个 `4`、三个 `5` 和四个 `6`。

此模块定义了 `svec` 与 `float8[]` 之间的双向隐式类型转换，以及从 `int2`、`integer`、`bigint`、`float4`、`float8` 和 `numeric` 到 `svec` 的隐式类型转换。

## 操作符 {#operators}

操作符利用稀疏存储格式，加快对 `svec` 值的计算。`+`、`-`、`*`、`/` 和 `%*%` 操作符接受任意组合的 `svec` 和 `float8[]` 操作数。转换为 `svec` 的单个数字是标量，会应用到另一个操作数的每个元素；其他情况下，两个操作数的维数必须相同。

| 操作符 | 说明 |
|---|---|
| `+` | 将两个向量的对应元素相加。 |
| `-` | 将两个向量的对应元素相减。 |
| `*` | 将两个向量的对应元素相乘。 |
| `/` | 将两个向量的对应元素相除。 |
| `^` | 将左侧 `svec` 的每个元素提升到右操作数指定的幂次。右操作数必须是标量，例如 `a ^ 2::svec`。右侧为向量时会报错。 |
| `%*%` | 以 `float8` 返回两个向量的点积。 |
| `\|\|` | 连接两个 `svec` 值。 |
| `*\|\|` | 将右操作数 `svec` 与自身连接，次数由左侧 `int4` 操作数指定。 |
| `=` | 检查两个 `svec` 值或两个 `float8[]` 值是否相等。 |
| `<`, `<=`, `==`, `>=`, `>` | 按 L2 范数比较两个 `svec` 值。这些操作符属于 `svec_l2_ops` B-树操作符类。 |
| `<>` | 已定义，但不属于该操作符类。此版本中，它绑定到与 `==` 相同的函数，因此 L2 范数相等时返回 `true`。不要依赖此操作符。 |

加法（`+`）操作符对两个同维向量的对应元素求和。例如，向量 `a = {0,1,5}` 与向量 `b = {4,3,2}` 的加法计算如下：

```sql
SELECT ('{0,1,5}'::float8[]::svec + '{4,3,2}'::float8[]::svec)::float8[];
```

```
 float8
---------
 {4,4,7}
```

向量 `a` 和 `b` 的点积（`%*%`）返回 `float8` 类型的标量结果。点积（`0*4 + 1*3 + 5*2 = 13`）计算如下：

```sql
SELECT '{0,1,5}'::float8[]::svec %*% '{4,3,2}'::float8[]::svec;
```

```
 ?column?
----------
       13
```

## 函数与聚合 {#functions-and-aggregates}

| 函数 | 说明 |
|---|---|
| `dot(a, b)` | 返回点积。每个参数为 `svec` 或 `float8[]`。 |
| `l1norm(svec)`, `l1norm(float8[])` | 返回向量的 L1 范数。 |
| `l2norm(svec)`, `l2norm(float8[])` | 返回向量的 L2 范数。 |
| `log(svec)` | 返回包含每个元素自然对数的 `svec`。 |
| `dimension(svec)` | 返回向量元素数。 |
| `unnest(svec)` | 将向量元素作为一组 `float8` 值返回。 |
| `vec_sum(svec)`, `vec_sum(float8[])` | 返回向量元素之和。 |
| `vec_median(svec)`, `vec_median(float8[])` | 返回向量元素的中位数。 |
| `vec_pivot(svec, float8)` | 将一个 `float8` 值追加到 `svec`。 |
| `dmin(float8, float8)`, `dmax(float8, float8)` | 返回两个 `float8` 值中的较小值或较大值。 |
| `gp_extract_feature_histogram(text[], text[])` | 根据词典（第一个参数），返回文档（第二个参数）的稀疏特征向量。 |

| 聚合 | 说明 |
|---|---|
| `sum(svec)` | 返回输入向量按元素求和的结果。 |
| `vec_count_nonzero(svec)` | 返回一个 `svec`，各位置的值为该位置具有非零元素的输入向量数量。 |
| `count_vec(svec)` | `vec_count_nonzero(svec)` 的旧名称。 |
| `array_agg(float8)` | 将 `float8` 值聚合为 `svec`。 |
| `median_inmemory(float8)` | 返回输入 `float8` 值的中位数。 |

例如，对于向量集合 `{0,1,5}`、`{10,0,3}`、`{0,0,3}` 和 `{0,1,0}`，各位置非零元素的计数为 `{1,2,3}`：

```sql
CREATE TABLE listvecs(a svec);

INSERT INTO listvecs VALUES ('{0,1,5}'::float8[]),
    ('{10,0,3}'::float8[]),
    ('{0,0,3}'::float8[]),
    ('{0,1,0}'::float8[]);

SELECT vec_count_nonzero(a)::float8[] AS count_nonzero FROM listvecs;
```

```
 count_nonzero
---------------
 {1,2,3}
(1 row)
```

## 示例 {#example}

此文本分类示例创建表示词典和若干文档的表，然后对各文档中词典单词的次数和占比进行向量运算，实现文档分类。

启用扩展并设置搜索路径：

```sql
CREATE EXTENSION gp_sparse_vector;
SET search_path TO sparse_vector, public;
```

假设词典由文本数组中的单词组成。创建表存储词典，并插入单词：

```sql
CREATE TABLE features (dictionary text[][]) DISTRIBUTED RANDOMLY;
INSERT INTO features
    VALUES ('{am,before,being,bothered,corpus,document,i,in,is,me,never,now,one,really,second,the,third,this,until}');
```

每篇文档同样定义为单词数组。创建表示这些文档的表，并插入一些数据：

```sql
CREATE TABLE documents (docnum int, document text[]) DISTRIBUTED RANDOMLY;
INSERT INTO documents VALUES
    (1,'{this,is,one,document,in,the,corpus}'),
    (2,'{i,am,the,second,document,in,the,corpus}'),
    (3,'{being,third,never,really,bothered,me,until,now}'),
    (4,'{the,document,before,me,is,the,third,document}');
```

要找出每篇文档中出现的词典单词，为每篇文档准备一个稀疏特征向量（SFV）。SFV 是 N 维向量，N 为词典单词数；每个 SFV 包含各个词典单词在该文档中的出现次数。

使用 `gp_extract_feature_histogram()` 函数从文档创建 SFV。函数返回 `svec`，按照词典的顺序位置存储各个词典单词的计数。为这些文档生成的向量称为语料库：

```sql
CREATE TABLE corpus (docnum int, feature_vector svec) DISTRIBUTED RANDOMLY;

INSERT INTO corpus
    (SELECT docnum,
        gp_extract_feature_histogram(
            (SELECT dictionary FROM features LIMIT 1), document)
     FROM documents);
```

显示每篇文档的特征向量：

```sql
SELECT docnum AS document_number, feature_vector::float8[] FROM corpus ORDER BY 1;
```

```
 document_number |             feature_vector
-----------------+-----------------------------------------
               1 | {0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,1,0,1,0}
               2 | {1,0,0,0,1,1,1,1,0,0,0,0,0,0,1,2,0,0,0}
               3 | {0,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,1,0,1}
               4 | {0,1,0,0,0,2,0,0,1,1,0,0,0,0,0,2,1,0,0}
(4 rows)
```

单词 "am" 是词典中的第一个词，在第二篇文档 "i am the second document in the corpus" 的 SFV 中出现 `1` 次。单词 "before" 未在此文档中出现，因此其值为 `0`，以此类推。

统计每个特征至少出现一次的文档数量：

```sql
SELECT (vec_count_nonzero(feature_vector))::float8[] AS count_in_document FROM corpus;
```

```
            count_in_document
-----------------------------------------
 {1,1,1,1,2,3,1,2,2,2,1,1,1,1,1,3,2,1,1}
(1 row)
```

统计每个词项在所有文档中的总出现次数：

```sql
SELECT (sum(feature_vector))::float8[] AS sum_in_document FROM corpus;
```

```
             sum_in_document
-----------------------------------------
 {1,1,1,1,2,4,1,2,2,2,1,1,1,1,1,5,2,1,1}
(1 row)
```

分类过程的后续步骤都是向量运算。将计数转换为反映词频/逆文档频率（tf/idf）的权重。某篇文档中某个词项的计算方式如下：

```
#_times_term_appears_in_this_doc * log( #_docs / #_docs_the_term_appears_in )
```

`#_docs` 是文档总数（此例中为 4）。例如，文档 1 中词项 "document" 的权重为 `1 * log(4/3)`，文档 4 中该词项的权重为 `2 * log(4/3)`。出现在每篇文档中的词项权重为 `0`。

计算 tf/idf：

```sql
SELECT docnum, (feature_vector*logidf)::float8[] AS tf_idf
    FROM (SELECT log(count(feature_vector)/vec_count_nonzero(feature_vector)) AS logidf FROM corpus)
    AS foo, corpus ORDER BY docnum;
```

```
 docnum |                                                                                     tf_idf
--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      1 | {0,0,0,0,0.6931471805599453,0.28768207245178085,0,0.6931471805599453,0.6931471805599453,0,0,0,1.3862943611198906,0,0,0.28768207245178085,0,1.3862943611198906,0}
      2 | {1.3862943611198906,0,0,0,0.6931471805599453,0.28768207245178085,1.3862943611198906,0.6931471805599453,0,0,0,0,0,0,1.3862943611198906,0.5753641449035617,0,0,0}
      3 | {0,0,1.3862943611198906,1.3862943611198906,0,0,0,0,0,0.6931471805599453,1.3862943611198906,1.3862943611198906,0,1.3862943611198906,0,0,0.6931471805599453,0,1.3862943611198906}
      4 | {0,1.3862943611198906,0,0,0,0.5753641449035617,0,0,0.6931471805599453,0.6931471805599453,0,0,0,0,0,0.5753641449035617,0.6931471805599453,0,0}
(4 rows)
```

可以对文档向量的点积求 `ACOS`，确定某篇文档与其余文档之间的角距离。首先创建表，存储 tf/idf 加权向量：

```sql
CREATE TABLE weights AS
    (SELECT docnum, (feature_vector*logidf) tf_idf
        FROM (SELECT log(count(feature_vector)/vec_count_nonzero(feature_vector))
       AS logidf FROM corpus) foo, corpus ORDER BY docnum)
    DISTRIBUTED RANDOMLY;
```

然后计算第一篇文档与其他各篇文档之间的角距离：

```sql
SELECT docnum, trunc((180.*(ACOS(dmin(1.,(tf_idf%*%testdoc)/(l2norm(tf_idf)*l2norm(testdoc))))/(4.*ATAN(1.))))::numeric,2)
     AS angular_distance FROM weights,
     (SELECT tf_idf testdoc FROM weights WHERE docnum = 1 LIMIT 1) foo
ORDER BY 1;
```

```
 docnum | angular_distance
--------+------------------
      1 |             0.00
      2 |            78.82
      3 |            90.00
      4 |            80.02
(4 rows)
```

文档 1 与自身的角距离为 0 度，与文档 3 的角距离为 90 度，因为二者完全没有共同特征。

## 更多文档 {#additional-documentation}

此模块的更多信息，参见 Apache Cloudberry 源码 [`gpcontrib/gp_sparse_vector`](https://github.com/apache/cloudberry/tree/REL_2_STABLE/gpcontrib/gp_sparse_vector) 目录中的 README 文件。
