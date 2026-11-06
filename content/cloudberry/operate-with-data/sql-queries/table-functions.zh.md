---
title: "表函数"
description: "表函数是生成一组行的函数，这些行由基础数据类型（标量类型）或复合数据类型（表行）组成。"
weight: 120
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/table-functions.md"
---

它们在查询的 `FROM` 子句中以类似表、视图或子查询的方式使用。表函数返回的列可以像表、视图或子查询的列一样，用于 `SELECT`、`JOIN` 或 `WHERE` 子句。

表函数还可以使用 `ROWS FROM` 语法组合，结果按并行列返回；此时结果行数取所有函数结果中最大的行数，较小的结果会用空值填充，以匹配该行数。

```sql
function_call [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
ROWS FROM( function_call [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

如果指定了 `WITH ORDINALITY` 子句，函数结果列中会额外添加一个 bigint 类型的列。此列从 1 开始为函数结果集中的行编号。（这是对 SQL 标准 `UNNEST ... WITH ORDINALITY` 语法的泛化。）默认情况下，序号列名为 ordinality，但可以使用 `AS` 子句为其指定其他列名。

特殊表函数 `UNNEST` 可以接受任意数量的数组参数，并返回相应数量的列，就像分别对每个参数调用 `UNNEST`，再使用 `ROWS FROM` 构造将结果组合起来一样。

```sql
UNNEST( array_expression [, ... ] ) [WITH ORDINALITY] [[AS] table_alias [(column_alias [, ... ])]]
```

如果未指定 table_alias，则使用函数名作为表名；对于 `ROWS FROM()` 构造，则使用第一个函数的名称。

如果未提供列别名，那么对于返回基础数据类型的函数，列名也与函数名相同。对于返回复合类型的函数，结果列使用该类型各个属性的名称。

下面是一些示例：

```sql
CREATE TABLE foo (fooid int, foosubid int, fooname text);

CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT * FROM getfoo(1) AS t1;

SELECT * FROM foo
    WHERE foosubid IN (
                        SELECT foosubid
                        FROM getfoo(foo.fooid) z
                        WHERE z.fooid = foo.fooid
                      );

CREATE VIEW vw_getfoo AS SELECT * FROM getfoo(1);

SELECT * FROM vw_getfoo;
```

在某些情况下，定义能够根据调用方式返回不同列集的表函数很有用。为此，可以将表函数声明为返回伪类型 record，且不带 `OUT` 参数。在查询中使用此类函数时，必须在查询本身中指定预期的行结构，以便系统知道如何解析和规划查询。语法如下：

```sql
function_call [AS] alias (column_definition [, ... ])
function_call AS [alias] (column_definition [, ... ])
ROWS FROM( ... function_call AS (column_definition [, ... ]) [, ... ] )
```

不使用 `ROWS FROM()` 语法时，`column_definition` 列表会替代原本可以附加到 FROM 项的列别名列表；列定义中的名称充当列别名。使用 `ROWS FROM()` 语法时，可以分别为每个成员函数附加 `column_definition` 列表；或者，如果只有一个成员函数且没有 `WITH ORDINALITY` 子句，可以将 `column_definition` 列表写在 `ROWS FROM()` 后面列别名列表所在的位置。

考虑以下示例：

```sql
SELECT *
    FROM dblink('dbname=mydb', 'SELECT proname, prosrc FROM pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

`dblink` 函数（属于 `dblink` 模块）执行远程查询。它被声明为返回 record，因为它可能用于任意类型的查询。必须在调用查询中指定实际列集，以便解析器知道例如 `*` 应展开为什么。

此示例使用 `ROWS FROM`：

```sql
SELECT *
FROM ROWS FROM
    (
        json_to_recordset('[{"a":40,"b":"foo"},{"a":"100","b":"bar"}]')
            AS (a INTEGER, b TEXT),
        generate_series(1, 3)
    ) AS x (p, q, s)
ORDER BY p;

  p  |  q  | s
-----+-----+---
  40 | foo | 1
 100 | bar | 2
     |     | 3
```

它将两个函数连接为单个 `FROM` 目标。`json_to_recordset()` 被指定返回两列，第一列为 integer，第二列为 text。`generate_series()` 的结果直接使用。`ORDER BY` 子句将列值按整数排序。
