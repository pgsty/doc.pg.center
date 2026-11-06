---
title: "内置函数概览"
linkTitle: "内置函数"
description: "了解 Apache Cloudberry 的内置函数类别，以及不可变、稳定和易变函数的执行限制。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/functions/index.md"
---

Apache Cloudberry 支持内置函数和操作符，包括可在窗口表达式中使用的分析函数和窗口函数。

## Apache Cloudberry 函数类型 {#apache-cloudberry-function-types}

Apache Cloudberry 会对 SQL 表达式中使用的函数和操作符进行求值。有些函数和操作符只允许运行在 Coordinator 上，因为它们可能导致 Apache Cloudberry 的 Segment 实例之间出现不一致。下表介绍 Apache Cloudberry 的函数类型。

|函数类型|Cloudberry 支持情况|描述|说明|
|-------------|-----------------|-----------|--------|
|IMMUTABLE|是|只依赖直接包含在参数列表中的信息。给定相同的参数值，始终返回相同的结果。| |
|STABLE|大多数情况下支持|在一次表扫描中，相同参数值返回相同结果，但不同 SQL 语句之间的结果可能变化。|结果取决于数据库查询或参数值。`current_timestamp` 系列函数属于 `STABLE`；其值在一次执行期间不会变化。|
|VOLATILE|受限|函数值可能在一次表扫描中变化，例如 `random()`、`timeofday()`。|任何带有副作用的函数都是易变函数，即使其结果可预测也是如此，例如 `setval()`。|

在 Apache Cloudberry 中，数据分布在各个 Segment 上，每个 Segment 都是一个独立的 PostgreSQL 数据库。为避免不一致或意外结果，如果归类为 `VOLATILE` 的函数包含 SQL 命令，或以任何方式修改数据库，就不要在 Segment 级别运行这些函数。例如，Apache Cloudberry 不允许在分布式数据上运行 `setval()` 等函数，因为它们可能导致 Segment 实例之间的数据不一致。

为确保数据一致性，可以在由 Coordinator 求值和执行的语句中安全地使用 `VOLATILE` 和 `STABLE` 函数。例如，以下语句在 Coordinator 上运行（不含 `FROM` 子句的语句）：

```sql
SELECT setval('myseq', 201);
SELECT foo();
```

如果一条语句的 `FROM` 子句包含分布式表，*并且*该 `FROM` 子句中的函数返回一组行，那么这条语句可以在 Segment 上运行：

```sql
SELECT * from foo();
```

Apache Cloudberry 不支持返回表引用（`rangeFuncs`）的函数，也不支持使用 `refCursor` 数据类型的函数。

## 内置函数和操作符 {#built-in-functions-and-operators}

下表列出 PostgreSQL 支持的内置函数和操作符类别。Apache Cloudberry 与 PostgreSQL 一样支持所有这些函数和操作符，但 `STABLE` 和 `VOLATILE` 函数需遵守 [Apache Cloudberry 函数类型](#built-in-functions-and-operators)中所述的限制。有关这些内置函数和操作符的更多信息，请参阅 PostgreSQL 文档的[函数和操作符](https://www.postgresql.org/docs/14/functions.html)一节。

|操作符/函数类别|VOLATILE 函数|STABLE 函数|限制|
|--------------------------|------------------|----------------|------------|
|[逻辑操作符](https://www.postgresql.org/docs/14/functions-logical.html)| | | |
|[比较操作符](https://www.postgresql.org/docs/14/functions-comparison.html)| | | |
|[数学函数和操作符](https://www.postgresql.org/docs/14/functions-math.html)|random<br/><br/>setseed| | |
|[字符串函数和操作符](https://www.postgresql.org/docs/14/functions-string.html)|*所有内置转换函数*|convert<br/><br/>pg_client_encoding| |
|[二进制串函数和操作符](https://www.postgresql.org/docs/14/functions-binarystring.html)| | | |
|[位串函数和操作符](https://www.postgresql.org/docs/14/functions-bitstring.html)| | | |
|[模式匹配](https://www.postgresql.org/docs/14/functions-matching.html)| | | |
|[数据类型格式化函数](https://www.postgresql.org/docs/14/functions-formatting.html)| |to_char<br/><br/>to_timestamp| |
|[日期/时间函数和操作符](https://www.postgresql.org/docs/14/functions-datetime.html)|timeofday|age<br/><br/>current_date<br/><br/>current_time<br/><br/>current_timestamp<br/><br/>localtime<br/><br/>localtimestamp<br/><br/>now| |
|[枚举支持函数](https://www.postgresql.org/docs/14/functions-enum.html)| | | |
|[几何函数和操作符](https://www.postgresql.org/docs/14/functions-geometry.html)| | | |
|[网络地址函数和操作符](https://www.postgresql.org/docs/14/functions-net.html)| | | |
|[序列操作函数](https://www.postgresql.org/docs/14/functions-sequence.html)|nextval()<br/><br/>setval()| | |
|[条件表达式](https://www.postgresql.org/docs/14/functions-conditional.html)| | | |
|[数组函数和操作符](https://www.postgresql.org/docs/14/functions-array.html)| |*所有数组函数*| |
|[聚合函数](https://www.postgresql.org/docs/14/functions-aggregate.html)| | | |
|[子查询表达式](https://www.postgresql.org/docs/14/functions-subquery.html)| | | |
|[行和数组比较](https://www.postgresql.org/docs/14/functions-comparisons.html)| | | |
|[返回集合的函数](https://www.postgresql.org/docs/14/functions-srf.html)|generate_series| | |
|[系统信息函数](https://www.postgresql.org/docs/14/functions-info.html)| |*所有会话信息函数*<br/><br/>*所有访问权限查询函数*<br/><br/>*所有模式可见性查询函数*<br/><br/>*所有系统目录信息函数*<br/><br/>*所有注释信息函数*<br/><br/>*所有事务 ID 和快照*| |
|[系统管理函数](https://www.postgresql.org/docs/14/functions-admin.html)|set_config<br/><br/>pg_cancel_backend<br/><br/>pg_reload_conf<br/><br/>pg_rotate_logfile<br/><br/>pg_start_backup<br/><br/>pg_stop_backup<br/><br/>pg_size_pretty<br/><br/>pg_ls_dir<br/><br/>pg_read_file<br/><br/>pg_stat_file<br/><br/>|current_setting<br/><br/>*所有数据库对象大小函数*|> **注意** 函数 `pg_column_size` 显示存储该值所需的字节数，其中可能包含 TOAST 压缩的影响。|
|[XML 函数](https://www.postgresql.org/docs/14/functions-xml.html)以及类似函数的表达式| |cursor_to_xml(cursor refcursor, count int, nulls boolean, tableforest boolean, targetns text)<br/><br/> cursor_to_xmlschema(cursor refcursor, nulls boolean, tableforest boolean, targetns text)<br/><br/>database_to_xml(nulls boolean, tableforest boolean, targetns text)<br/><br/>database_to_xmlschema(nulls boolean, tableforest boolean, targetns text)<br/><br/>database_to_xml_and_xmlschema(nulls boolean, tableforest boolean, targetns text)<br/><br/>query_to_xml(query text, nulls boolean, tableforest boolean, targetns text)<br/><br/>query_to_xmlschema(query text, nulls boolean, tableforest boolean, targetns text)<br/><br/>query_to_xml_and_xmlschema(query text, nulls boolean, tableforest boolean, targetns text)<br/><br/> schema_to_xml(schema name, nulls boolean, tableforest boolean, targetns text)<br/><br/>schema_to_xmlschema(schema name, nulls boolean, tableforest boolean, targetns text)<br/><br/>schema_to_xml_and_xmlschema(schema name, nulls boolean, tableforest boolean, targetns text)<br/><br/>table_to_xml(tbl regclass, nulls boolean, tableforest boolean, targetns text)<br/><br/>table_to_xmlschema(tbl regclass, nulls boolean, tableforest boolean, targetns text)<br/><br/>table_to_xml_and_xmlschema(tbl regclass, nulls boolean, tableforest boolean, targetns text)<br/><br/>xmlagg(xml)<br/><br/>xmlconcat(xml[, ...])<br/><br/>xmlelement(name name [, xmlattributes(value [AS attname] [, ... ])] [, content, ...])<br/><br/>xmlexists(text, xml)<br/><br/>xmlforest(content [AS name] [, ...])<br/><br/>xml_is_well_formed(text)<br/><br/>xml_is_well_formed_document(text)<br/><br/>xml_is_well_formed_content(text)<br/><br/>xmlparse ( `{ DOCUMENT \| CONTENT }` value)<br/><br/>xpath(text, xml)<br/><br/>xpath(text, xml, text[])<br/><br/>xpath_exists(text, xml)<br/><br/>xpath_exists(text, xml, text[])<br/><br/>xmlpi(name target [, content])<br/><br/>xmlroot(xml, version text \| no value [, standalone yes\|no\|no value])<br/><br/>xmlserialize ( `{ DOCUMENT \| CONTENT }` value AS type )<br/><br/>xml(text)<br/><br/>text(xml)<br/><br/>xmlcomment(xml)<br/><br/>xmlconcat2(xml, xml)<br/><br/>| |
