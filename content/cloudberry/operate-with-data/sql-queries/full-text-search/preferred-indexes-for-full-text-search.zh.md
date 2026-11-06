---
title: "文本检索的首选索引类型"
description: "有两类索引可用于加快全文检索：GIN 和 GiST。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/full-text-search/preferred-indexes-for-full-text-search.md"
---

全文检索不强制要求索引，但如果某列需要经常检索，通常应当为其建立索引。

可以使用以下任一方式创建此类索引：

`CREATE INDEX <name> ON <table> USING gin(<column>);`：创建基于 GIN（通用倒排索引）的索引。`<column>` 必须是 `tsvector` 类型。

`CREATE INDEX <name> ON <table> USING gist(<column>);`：创建基于 GiST（通用搜索树）的索引。`<column>` 可以是 `tsvector` 或 `tsquery` 类型。

GIN 索引是首选的文本检索索引类型。作为倒排索引，它为每个单词（词位）包含一个索引项，并附带一个经过压缩的匹配位置列表。多词检索可以先找到第一个匹配项，然后使用索引排除缺少其他单词的行。GIN 索引只存储 `tsvector` 值中的单词（词位），不存储其权重标签。因此，使用包含权重的查询时，需要重新检查表行。

GiST 索引是有损的，也就是说，索引可能产生错误匹配，因此必须检查实际表行以排除这类错误匹配。（需要时 PostgreSQL 会自动执行此操作。）GiST 索引之所以有损，是因为索引中用固定长度的签名表示每个文档。系统将每个单词散列到 n 位字符串中的一个比特位，再将所有这些比特位进行 OR 运算，生成 n 位文档签名。如果两个单词散列到同一个比特位，就会产生错误匹配。如果查询中的所有单词都匹配（无论是真匹配还是错误匹配），就必须取回表行以确认匹配是否正确。

GiST 索引可以是覆盖索引，也就是说可以使用 `INCLUDE` 子句。包含的列可以使用没有 GiST 操作符类的数据类型。包含的属性将以未压缩形式存储。

有损性会导致性能下降，因为系统会不必要地取回最终证明是错误匹配的表记录。由于随机访问表记录速度较慢，这限制了 GiST 索引的实用性。错误匹配的可能性取决于多个因素，尤其是不重复单词的数量，因此建议使用词典减少这一数量。

请注意，提高 `maintenance_work_mem` 的值通常可以缩短 GIN 索引的构建时间，而 GiST 索引的构建时间对该参数并不敏感。

对大型集合进行分区，并正确使用 GiST 和 GIN 索引，可以实现支持在线更新的极快检索。可以在数据库层使用表继承进行分区，也可以将文档分布到多个服务器上，再使用 `dblink` 汇总检索结果。后一种方式之所以可行，是因为排名函数只使用本地信息。
