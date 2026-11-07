---
title: 使用 PostgreSQL 和 Citus 进行可缩放的实时产品搜索
description: 了解如何使用 PostgreSQL 和 Citus 生成可缩放的实时产品搜索，以便处理大型目录。
weight: 80
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/faceted-search?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
linkTitle: 分面搜索
---

**原始文章：** [Marco Slot · 2016 年 4 月 28 日](https://www.citusdata.com/blog/2016/04/28/scalable-product-search/)。中文整理：[PGSTY](https://pgsty.com/)。

> [!NOTE]
> 本文提到了 Citus Cloud 服务。Amazon Web Service（AWS）上的 Citus Cloud 已不再接受新用户注册。如果你刚开始使用 Citus，仍然可以使用它：Citus 是开源软件，也作为 Azure Database for PostgreSQL 中完全集成的部署选项在 Microsoft Azure 云上提供。
>
> 更多信息请参阅[托管服务](/citus/installation/citus-cloud/)。

产品搜索是在线零售商和交易平台的常见需求，但有时也很棘手。它通常结合全文搜索与属性筛选，而不同产品类别的属性各不相同。更复杂的场景中，还可能有多个卖家销售同一产品，但价格和属性有所不同。

PostgreSQL 具备构建产品搜索应用所需的功能，但在大型产品目录上创建索引和执行查询时表现不佳。借助 Citus，PostgreSQL 可以将表分布到多台服务器上，并行执行查询，从而横向扩展内存和计算能力来处理大型产品目录。它的搜索功能不如专用搜索方案全面。不过，将数据保存在 PostgreSQL 中有一个很大的好处：可以实时更新数据，也可以连接各表。本文将介绍如何使用 PostgreSQL 和 Citus 搭建一个具有并行搜索功能的实验性产品数据库，以展示其中的几项强大功能。

使用 4 个 m3.2xlarge 实例作为工作节点，搭建[多节点 Citus](/citus/installation/multi-node/)。更简单的入门方式是使用 [Citus Cloud](https://www.citusdata.com/)，它提供具备全自动故障切换能力的托管 Citus 集群。[数据库模式](https://gist.github.com/marcocitus/fb49a20404f5fa8d4ff16c25ce04599c)中的主表是 product 表，其中包含产品名称、描述、价格，以及 [JSON 格式](http://www.postgresql.org/docs/current/static/datatype-json.html)的属性，以便不同类型的产品使用不同属性：

```sql
CREATE TABLE product (
  product_id int primary key,
  name text not null,
  description text not null,
  price decimal(12,2),
  attributes jsonb
);
```

要用 Citus 分布该表，可调用相应的 `ddl` 函数将表划分为 16 个分片（每个物理核心一个）。这些分片会分布并复制到 4 个工作节点上。

```sql
SELECT create_distributed_table('product', 'product_id');
```

创建 GIN 索引，以便通过 JSONB 包含运算符快速筛选属性。例如，搜索英文书籍时，可以使用表达式 `attributes @> '{"category":"books", "language":"english"}'`，该表达式能够利用 GIN 索引。

```sql
CREATE INDEX attributes_idx ON product USING GIN (attributes jsonb_path_ops);
```

要按名称和描述筛选产品，可以使用 PostgreSQL 的[全文搜索函数](http://www.postgresql.org/docs/current/static/textsearch.html)，查找与用户指定查询相匹配的内容。文本搜索使用文本搜索查询（tsquery）来匹配文本搜索向量（tsvector）。定义一个为产品生成 tsvector 的中间函数会很有帮助。`product_text_search` 函数将产品的名称和描述合并为一个 tsvector，并为名称赋予最高权重（权重等级从 'A' 到 'D'），这样按相关性排序时，名称匹配的结果就会排得更靠前。

```sql
CREATE FUNCTION product_text_search(name text, description text)
RETURNS tsvector LANGUAGE sql IMMUTABLE AS $function$
  SELECT setweight(to_tsvector(name),'A') ||
         setweight(to_tsvector(description),'B');
$function$;
```

设置好函数后，在其上定义一个 GIN 索引，以加速 product 表上的文本搜索。

```sql
CREATE INDEX text_idx ON product USING GIN (product_text_search(name, description));
```

由于没有可用的大型产品数据集，这里改用一个[简单的生成函数](https://gist.github.com/marcocitus/dd315960d5923ad3f4d26b105618ed58)，通过拼接随机单词生成名称、描述和属性，构造 1,000 万个模拟产品（7 GB）。向 words 表添加单词后，可以运行：

```psql
\COPY (SELECT * FROM generate_products(10000000)) TO '/data/base/products.tsv'
```

Citus 新增的 COPY 功能可用于将数据加载到 product 表。文章发表时，[最新版 Citus](https://github.com/citusdata/citus) 和 [Citus Cloud](https://www.citusdata.com/) 已提供哈希分区表的 COPY 支持。在分布式表上使用 COPY 的一个好处是，工作节点可以并行处理多行数据。由于每个分片单独建立索引，索引也能保持较小，从而提高使用 GIN 索引时的数据摄取速率。

```psql
\COPY product FROM '/data/base/products.tsv'
```

数据加载用时不到 7 分钟，平均约每秒 25,000 行。相比之下，将数据加载到普通 PostgreSQL 表中，再在复制完成后创建索引，共耗时 45 分钟（每秒 3,700 行）。

假设要搜索产品“copper oven”。可以使用 `plainto_tsquery` 函数将该短语转为 tsquery，再用 `@@` 运算符匹配名称和描述。另一个筛选条件是产品的“food”属性必须为“waste”或“air”。要按相关性排序，可以使用以 tsvector 和 tsquery 为输入的 `ts_rank` 函数。

```sql
SELECT p.product_id, p.name, p.price
FROM product p
WHERE product_text_search(name, description) @@ plainto_tsquery('copper oven')
  AND (attributes @> '{"food":"waste"}' OR attributes @> '{"food":"air"}')
ORDER BY ts_rank(product_text_search(name, description),
                 plainto_tsquery('copper oven')) DESC
LIMIT 10;
```

```text
 product_id |         name         | price
------------+----------------------+-------
    2016884 | oven copper hot      | 32.33
    8264220 | rifle copper oven    | 92.11
    4021935 | argument chin rub    | 79.33
    5347636 | oven approval circle | 50.78
(4 rows)
Time: 68.832 ms (~78ms on non-distributed table)
```

该查询利用两个 GIN 索引，快速找出少量行。范围更广的搜索可能耗时更长，因为需要按相关性得分对所有结果排序。例如，下面的查询需要对 294,000 个结果排序，才能取出前 10 个：

```sql
SELECT p.product_id, p.name, p.price
FROM product p
WHERE product_text_search(name, description) @@ plainto_tsquery('oven')
  AND price < 50
ORDER BY ts_rank(product_text_search(name, description),
                 plainto_tsquery('oven')) DESC
LIMIT 10;
```

```text
 product_id |         name         | price
------------+----------------------+-------
    6295883 | end oven oven        | 7.80
    3304889 | oven punishment oven | 28.27
    2291463 | town oven oven       | 7.47
...
(10 rows)
Time: 2262.502 ms (37 seconds on non-distributed table)
```

该查询先从 16 个分片中的每个分片取出前 10 个结果，大部分时间都花在这一步，然后再对最终的 160 行排序。使用更多机器和分片时，每个分片需要排序的行数会减少，而最终的排序工作量仍然很小。因此，使用规模更大、分片更多的集群可以缩短查询时间。

除了产品本身，假设零售商还运营一个交易平台，让其他卖家以不同价格销售产品。只要这些报价低于价格上限，也应该出现在搜索结果中。一个产品可能对应许多这样的报价。可以创建另一张分布式表，按 `product_id` 分布，并分配相同数量的分片，这样就能按 `product_id` 连接共置的 product 和 offer 表。

```sql
CREATE TABLE offer (
  product_id int not null,
  offer_id int not null,
  seller_id int,
  price decimal(12,2),
  new bool,
  primary key(product_id, offer_id)
);
SELECT create_distributed_table('offer', 'product_id');
```

可以用 `generate_offers` 函数生成 500 万条随机报价，再通过 COPY 加载。下面的查询搜索价格低于 70 美元的 popcorn oven 产品，也包括卖家报价低于 70 美元的产品。报价以 JSON 对象数组的形式包含在结果中。

```sql
SELECT p.product_id, p.name, p.price, to_json(array_agg(to_json(o)))
FROM   product p LEFT JOIN offer o USING (product_id)
WHERE  product_text_search(p.name, p.description) @@ plainto_tsquery('popcorn oven')
  AND (p.price < 70 OR o.price < 70)
GROUP BY p.product_id, p.name, p.description, p.price
ORDER BY ts_rank(product_text_search(p.name, p.description),
                 plainto_tsquery('popcorn oven')) DESC
LIMIT 10;
```

```text
    .
     product_id |          name          | price |                                        to_json
    ------------+------------------------+-------+---------------------------------------------------------------------------------------
        9354998 | oven popcorn bridge    | 41.18 | [null]
        1172380 | gate oven popcorn      | 24.12 | [{"product_id":1172380,"offer_id":4853987,"seller_id":2088,"price":55.00,"new":true}]
         985098 | popcorn oven scent     | 73.32 | [{"product_id":985098,"offer_id":5890813,"seller_id":5727,"price":67.00,"new":true}]
    ...
    (10 rows)

    Time: 337.441 ms (4 seconds on non-distributed tables)
```

PostgreSQL 提供了丰富的功能，你还可以继续改进。例如，将整行转换为 JSON，或添加筛选条件，只返回匹配程度足够高的结果；也可以确保结果中只包含最低报价。还可以开始对 product 和 offer 表进行实时插入和更新。

## 相关内容 {#related-content}

- [专题概览](/citus/articles/)
- [使用半结构化数据对 PostgreSQL 分片](/citus/articles/semi-structured-data/)
