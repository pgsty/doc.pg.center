---
title: "CREATE INDEX"
description: "定义新索引。"
weight: 650
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-index.md"
---

## 语法概要 {#synopsis}

```sql
CREATE [UNIQUE] INDEX [[IF NOT EXISTS] <name>] ON [ONLY] <table_name> [USING <method>]
       ( {<column_name> | (<expression>)} [COLLATE <collation>] [<opclass>] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
       [ INCLUDE ( column_name [, ...] ) ]
       [ WITH ( <storage_parameter> [= <value>] [, ... ] ) ]
       [ TABLESPACE <tablespace_name> ]
       [ WHERE <predicate> ]
```

## 说明 {#description}

`CREATE INDEX` 在指定表或物化视图的指定列上构建索引。索引主要用于提高数据库性能，不过使用不当也可能降低性能。

索引的键字段可以指定为列名，也可以指定为括号中的表达式。如果索引方法支持多列索引，就可以指定多个字段。

索引字段可以是根据表中一行的一个或多个列值计算出的表达式。此功能可用于根据基础数据的某种变换快速访问数据。例如，基于 `upper(col)` 计算的索引可让 `WHERE upper(col) = 'JIM'` 子句使用索引。

Apache Cloudberry 提供 B-树、hash、bitmap、GiST、SP-GiST、GIN 和 BRIN 索引方法。用户也可以定义自己的索引方法，但这相当复杂。

存在 `WHERE` 子句时，会创建部分索引。部分索引只包含表中一部分行的索引项，通常这部分比表的其余部分更值得建立索引。例如，某个表同时包含已开票和未开票的订单，未开票订单只占全表的一小部分，却最常被查询，此时只为这部分数据建立索引就能提高性能。另一种用途是将 `WHERE` 与 `UNIQUE` 配合使用，强制表的一个子集具有唯一性。更多信息请参阅 PostgreSQL 文档中的[部分索引](https://www.postgresql.org/docs/14/indexes-partial.html)。

`WHERE` 子句中的表达式只能引用底层表的列，但可以使用所有列，不限于建立索引的列。`WHERE` 中也不允许子查询和聚合表达式。这些限制同样适用于作为表达式的索引字段。

索引定义中使用的所有函数和操作符都必须是不可变的。它们的结果只能取决于参数，不能受任何外部因素影响（例如其他表的内容或当前时间）。这一限制确保索引行为有明确定义。要在索引表达式或 `WHERE` 子句中使用用户定义函数，创建函数时务必将其标记为 `IMMUTABLE`。

## 参数 {#parameters}

**`UNIQUE`**

在创建索引时（如果已有数据），以及每次添加数据时，检查表中的重复值。重复项会导致错误。唯一索引仅适用于 B-树 索引。

在分区表上使用唯一索引还有其他限制；请参阅 [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/)。

**`IF NOT EXISTS`**

如果已存在同名关系，不抛出错误，而是发出通知。注意，并不能保证现有索引与原本要创建的索引有任何相似之处。指定 `IF NOT EXISTS` 时必须提供索引名。

**`INCLUDE`**

可选的 `INCLUDE` 子句指定一组作为非键列包含在索引中的列。非键列不能用于索引扫描的搜索条件，也不参与索引所实施的任何唯一约束或排他约束。不过，仅索引扫描可以直接从索引项获取非键列的内容，无须访问索引对应的表。因此，添加非键列可以让原本无法使用仅索引扫描的查询使用这种扫描。

应谨慎向索引添加非键列，尤其是较宽的列。如果索引元组超过该索引类型允许的最大大小，数据插入就会失败。无论如何，非键列都会复制索引对应表的数据，使索引膨胀，从而可能减慢搜索。

`INCLUDE` 子句中列出的列不需要适用的操作符类；即使某种数据类型没有为给定访问方法定义操作符类，也可以将该类型的列包含在此子句中。

包含列不支持表达式，因为它们不能用于仅索引扫描。

目前，B-树 和 GiST 索引访问方法支持 `INCLUDE`。在 B-树 和 GiST 索引中，`INCLUDE` 子句所列列的值包含在与堆元组对应的叶子元组中，但不包含在用于树导航的上层索引项中。

**`name`**

要创建的索引名。索引始终创建在其父表所在的模式中。如果省略名称，Apache Cloudberry 会根据父表名和索引列名选择合适的名称。

**`ONLY`**

对于分区表，表示不递归地在分区上创建索引。默认行为是递归创建。

**`table_name`**

要建立索引的表名（可用模式限定）。

**`method`**

要使用的索引方法名称。可选值为 `btree`、`bitmap`、`hash`、`gist`、`spgist`、`gin` 和 `brin`。默认方法为 `btree`。

GPORCA 只支持 B-树、bitmap、GiST、GIN 和 BRIN 索引。GPORCA 会忽略使用不支持的索引方法创建的索引。

**`column_name`**

要创建索引的表中的列名。

**`expression`**

基于表中一个或多个列的表达式。通常必须用括号括起表达式，如语法所示。不过，如果表达式的形式是函数调用，则可以省略括号。

**`collation`**

索引使用的排序规则名称。默认情况下，索引使用被索引列声明的排序规则，或被索引表达式的结果排序规则。对于包含使用非默认排序规则的表达式的查询，具有非默认排序规则的索引可能有用。

**`opclass`**

操作符类的名称。

**`ASC`**

指定升序排列（默认值）。

**`DESC`**

指定降序排列。

**`NULLS FIRST`**

指定空值排在非空值之前。指定 `DESC` 时，这是默认行为。

**`NULLS LAST`**

指定空值排在非空值之后。未指定 `DESC` 时，这是默认行为。

**`storage_parameter`**

索引方法专用的存储参数名称。每种索引方法都有各自允许使用的存储参数。详情请参阅[索引存储参数](#index-storage-parameters)。

**`tablespace_name`**

创建索引的表空间。如果未指定，则使用 default_tablespace；对于临时表的索引，则使用 temp_tablespaces。

**`predicate`**

部分索引的约束表达式。

## 索引存储参数 {#index-storage-parameters}

可选的 `WITH` 子句指定索引的*存储参数*。每种索引方法都有各自允许使用的存储参数。B-树、bitmap、hash、GiST 和 SP-GiST 索引方法都接受以下参数：

**`fillfactor`**

索引的 `fillfactor` 是一个百分比，决定索引方法尝试将索引页面填充到什么程度。对于 B-树，在初始构建索引时，以及向索引右端扩展（添加新的最大键值）时，叶子页面都会填充到这一比例。如果页面随后被完全填满，就会发生页面分裂，使索引效率逐渐下降。B-树 的默认 fillfactor 为 90，但可以选择 10 到 100 之间的任意整数。对于静态表，fillfactor 100 最有利于减小索引的物理大小；对于频繁更新的表，较小的 fillfactor 更有利于减少页面分裂。其他索引方法使用 fillfactor 的方式不同，但大体类似；各方法的默认 fillfactor 也不同。

B-树 索引还接受以下参数：

**`vacuum_cleanup_index_scale_factor`**

为单个索引设置的 `vacuum_cleanup_index_scale_factor` 值。

GiST 索引还接受以下参数：

**`buffering`**

决定 Apache Cloudberry 是否使用 PostgreSQL 文档中 [GiST 缓冲构建](https://www.postgresql.org/docs/14/gist-implementation.html)所述的技术来构建索引。`OFF` 表示禁用，`ON` 表示启用，`AUTO` 表示初始禁用，但索引大小一旦达到 effective_cache_size，就在构建过程中自动启用。默认值为 `AUTO`。

GIN 索引接受不同的参数：

**`fastupdate`**

此设置控制是否使用 PostgreSQL 文档中 [GIN 快速更新技术](https://www.postgresql.org/docs/14/gin-implementation.html#GIN-FAST-UPDATE)所述的技术。它是一个布尔参数，用于禁用或启用 GIN 索引的快速更新技术。值 `ON` 启用快速更新（默认值），`OFF` 则禁用。

> [!NOTE]
> 通过 `ALTER INDEX` 关闭 `fastupdate` 会阻止后续插入进入待处理索引项列表，但不会自行清空已有条目。之后可以对表执行 `VACUUM`，或调用 `gin_clean_pending_list()` 函数，确保待处理列表被清空。

**`gin_pending_list_limit`**

自定义的 `gin_pending_list_limit` 参数。此值以千字节为单位。

BRIN 索引接受不同的参数：

**`pages_per_range`**

定义 BRIN 索引每个条目所对应块范围包含的表块数（详情请参阅 PostgreSQL 文档中的 [BRIN 索引简介](https://www.postgresql.org/docs/14/brin-intro.html)）。默认值为 128。

**`autosummarize`**

定义是否在检测到向下一个页面范围插入数据时，为前一个页面范围安排一次汇总。更多信息请参阅 PostgreSQL 文档中的 [BRIN 索引维护](https://www.postgresql.org/docs/14/brin-intro.html#BRIN-OPERATION)。默认值为 `off`。

## 注意事项 {#notes}
有关何时能使用索引、何时不能使用索引，以及索引在哪些具体情况下有用的信息，请参阅 PostgreSQL 文档的[索引](https://www.postgresql.org/docs/14/indexes.html)主题。

目前，只有 B-树、bitmap、GiST、GIN 和 BRIN 索引方法支持多列索引。默认最多可指定 32 个字段。目前只有 B-树 支持唯一索引。

可以为索引的每个列指定操作符类。操作符类标识索引对该列使用的操作符。例如，四字节整数的 B-树 索引会使用 `int4_ops` 类，该类包含四字节整数的比较函数。实际使用中，列的数据类型所对应的默认操作符类通常就足够了。操作符类存在的主要意义是，某些数据类型可能有不止一种有意义的排序方式。例如，可以希望按绝对值或实部对复数数据类型排序。为该数据类型定义两个操作符类，然后在创建索引时选择合适的类，即可实现。有关操作符类的更多信息，请参阅 PostgreSQL 文档中的[操作符类和操作符族](https://www.postgresql.org/docs/14/indexes-opclass.html)以及[索引扩展接口
](https://www.postgresql.org/docs/14/xindex.html)。

在分区表上调用 `CREATE INDEX` 时，默认会递归处理所有分区，确保它们都有匹配的索引。首先检查每个分区是否已有等价索引；如果有，则将该索引作为分区索引附加到正在创建的索引上，后者成为其父索引。如果没有匹配索引，就创建新索引并自动附加；每个分区中新索引的名称按命令未指定索引名时的规则确定。如果指定 `ONLY` 选项，则不递归，且索引被标记为无效。（当所有分区都有匹配的索引后，`ALTER INDEX ... ATTACH PARTITION` 会将索引标记为有效。）但请注意，无论是否指定 `ONLY`，今后使用 `CREATE TABLE ... PARTITION OF` 或 `ALTER TABLE ... ADD PARTITION` 创建的任何分区都会自动拥有匹配的索引。

对于支持有序扫描的索引方法（目前只有 B-树），可以通过可选子句 `ASC`、`DESC`、`NULLS FIRST` 和/或 `NULLS LAST` 修改索引排序顺序。由于有序索引既可以向前扫描，也可以向后扫描，创建单列 `DESC` 索引通常没有意义，因为普通索引已经能提供这种顺序。这些选项的价值在于，可以创建与混合排序查询要求相符的多列索引，例如 `SELECT ... ORDER BY x ASC, y DESC`。对于依靠索引避免排序步骤的查询，如果需要让空值排在低值端，而非默认的高值端，`NULLS` 选项就很有用。

系统会定期收集表中所有列的统计信息。新创建的非表达式索引可以立即使用这些统计信息来判断索引是否有用。对于新的表达式索引，必须运行 [ANALYZE](/cloudberry/reference/sql-stmts/analyze/) 来生成其统计信息。

对于大多数索引方法，创建索引的速度取决于 `maintenance_work_mem` 的设置。只要不超过实际可用内存，增大此值就能缩短创建索引所需的时间；超过实际可用内存会导致机器进行内存交换。

`bitmap` 索引最适合不同值数量在 100 到 100,000 之间的列。对于不同值超过 100,000 个的列，位图索引的性能和空间效率会下降。位图索引的大小与表中行数乘以被索引列的不同值数量成正比。

使用 [`DROP INDEX`](/cloudberry/reference/sql-stmts/drop-index/) 删除索引。

与任何长时间运行的事务一样，在一个表上执行 `CREATE INDEX` 会影响其他表上并发执行的 `VACUUM` 可以移除哪些元组。

## 示例 {#examples}

在表 `films` 的列 `title` 上创建唯一 B-树 索引：

```sql
CREATE UNIQUE INDEX title_idx ON films (title);
```

在表 `films` 的列 `title` 上创建 B-树 索引，并包含列 `director` 和 `rating`：

```sql
CREATE INDEX title_idx ON films (title) INCLUDE (director, rating);
```

在表达式 `lower(title)` 上创建索引，以便高效执行不区分大小写的搜索：

```sql
CREATE INDEX ON films ((lower(title)));
```

（此例省略了索引名，由系统选择名称，通常为 `films_lower_idx`。）

创建使用非默认排序规则的索引：

```sql
CREATE INDEX title_idx_german ON films (title COLLATE "de_DE");
```

创建使用非默认空值排序顺序的索引：

```sql
CREATE INDEX title_idx_nulls_low ON films (title NULLS FIRST);
```

创建使用非默认填充因子的索引：

```sql
CREATE UNIQUE INDEX title_idx ON films (title) WITH 
(fillfactor = 70);
```

创建禁用快速更新的 GIN 索引：

```sql
CREATE INDEX gin_idx ON documents_table USING gin (locations) WITH (fastupdate = off);
```

在表 `films` 的列 `code` 上创建索引，并将索引放在表空间 `indexspace` 中：

```sql
CREATE INDEX code_idx ON films (code) TABLESPACE indexspace;
```

在点属性上创建 GiST 索引，以便高效地对转换函数的结果使用 box 操作符：

```sql
CREATE INDEX pointloc ON points USING gist (box(location,location));
SELECT * FROM points WHERE box(location,location) && '(0,0),(1,1)'::box;
```

## 兼容性 {#compatibility}

`CREATE INDEX` 是 Apache Cloudberry 对 SQL 标准的扩展。SQL 标准没有关于索引的规定。

## 另请参阅 {#see-also}

[`ALTER INDEX`](/cloudberry/reference/sql-stmts/alter-index/), [`DROP INDEX`](/cloudberry/reference/sql-stmts/drop-index/)
