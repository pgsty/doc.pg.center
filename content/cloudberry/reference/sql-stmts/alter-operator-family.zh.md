---
title: "ALTER OPERATOR FAMILY"
description: "更改操作符族的定义。"
weight: 180
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-operator-family.md"
---

## 概要 {#synopsis}

```sql
ALTER OPERATOR FAMILY <name> USING <index_method> ADD
  {  OPERATOR <strategy_number> <operator_name> ( <op_type>, <op_type> ) [ FOR SEARCH | FOR ORDER BY <sort_family_name> ]
    | FUNCTION <support_number> [ ( <op_type> [ , <op_type> ] ) ] <function_name> ( <argument_type> [, ...] )
  } [, ... ]

ALTER OPERATOR FAMILY <name> USING <index_method> DROP
  {  OPERATOR <strategy_number> ( <op_type> [ , <op_type> ] ) 
    | FUNCTION <support_number> ( <op_type> [ , <op_type> ] ) 
  } [, ... ]

ALTER OPERATOR FAMILY <name> USING <index_method> RENAME TO <new_name>

ALTER OPERATOR FAMILY <name> USING <index_method> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER OPERATOR FAMILY <name> USING <index_method> SET SCHEMA <new_schema>
```

## 描述 {#description}

`ALTER OPERATOR FAMILY` 更改操作符族的定义。你可以向操作符族中添加操作符和支持函数，从中移除它们，或者更改该族的名称或所有者。

当使用 `ALTER OPERATOR FAMILY` 向操作符族添加操作符和支持函数时，它们不属于该族内任何特定的操作符类，而只是在该族内“松散”存在。这表明这些操作符和函数与该族的语义兼容，但并不是任何特定索引正确工作所必需的。（所需的操作符和函数应改为声明为操作符类的一部分；请参见 [CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/)。）你可以随时从族中删除该族的松散成员，但操作符类的成员不能被删除，除非同时删除整个操作符类以及依赖于它的所有索引。通常，单一数据类型的操作符和函数属于操作符类，因为它们是支持该特定数据类型上的索引所必需的；而跨数据类型的操作符和函数则被设为该族的松散成员。

要使用 `ALTER OPERATOR FAMILY`，你必须是超级用户。（设置此限制是因为错误的操作符族定义可能会使服务器混乱，甚至崩溃。）

`ALTER OPERATOR FAMILY` 目前不会检查操作符族定义是否包含索引方法所需的全部操作符和函数，也不会检查这些操作符和函数是否构成一个自洽的集合。定义有效的操作符族是用户的责任。

## 参数 {#parameters}

**`name`**

一个现有操作符族的名称（可以是模式限定的）。

**`index_method`**

该操作符族所对应的索引方法的名称。

**`strategy_number`**

与该操作符族关联的操作符在索引方法中的策略号。

**`operator_name`**

与该操作符族关联的操作符的名称（可以是模式限定的）。

**`op_type`**

在 `OPERATOR` 子句中，指操作符的操作数数据类型，或者用 `NONE` 表示左一元或右一元操作符。与 `CREATE OPERATOR CLASS` 中类似的语法不同，这里必须始终指定操作数数据类型。

在 `ADD FUNCTION` 子句中，指该函数打算支持的操作数数据类型（如果与该函数的输入数据类型不同）。对于 B-树比较函数和哈希函数，不必指定 op_type，因为函数的输入数据类型始终就是应使用的正确类型。对于 B-树排序支持函数，以及 GiST、SP-GiST 和 GIN 操作符类中的所有函数，必须指定该函数要配合使用的操作数数据类型。

在 `DROP FUNCTION` 子句中，必须指定该函数打算支持的操作数数据类型。

**`sort_family_name`**

一个现有 `btree` 操作符族的名称（可以是模式限定的），该操作符族描述与排序操作符相关联的排序顺序。

如果既未指定 `FOR SEARCH` 也未指定 `FOR ORDER BY`，则默认为 `FOR SEARCH`。

**`support_number`**

与该操作符族关联的函数在索引方法中的支持函数号。

**`function_name`**

作为该操作符族的索引方法支持函数的函数名称（可以是模式限定的）。如果未指定参数列表，则该名称在其模式中必须是唯一的。

**`argument_type`**

函数的参数数据类型。

**`new_name`**

操作符族的新名称。

**`new_owner`**

操作符族的新所有者。

**`new_schema`**

操作符族的新模式。

`OPERATOR` 和 `FUNCTION` 子句可以按任意顺序出现。

## 注解 {#notes}

请注意，`DROP` 语法只指定操作符族中的“槽位”，即通过策略号或支持函数号以及输入数据类型来指定。占据该槽位的操作符或函数的名称并不会被提及。另外，对于 `DROP FUNCTION`，要指定的类型是该函数打算支持的输入数据类型；对于 `GiST`、`SP_GiST` 和 `GIN` 索引，这可能与该函数实际的输入参数类型毫无关系。

由于索引机制在使用函数之前不会检查对函数的访问权限，因此把函数或操作符包含进操作符族等同于授予了对它的公共执行权限。对于在操作符族中有用的那类函数，这通常不成问题。

操作符不应由 SQL 函数定义。SQL 函数很可能被内联到调用它的查询中，这会使优化器无法识别该查询与某个索引相匹配。

在 Apache Cloudberry 6.0 之前，`OPERATOR` 子句可以包含 `RECHECK` 选项。该选项已不再受支持。Apache Cloudberry 现在在运行时即时判断索引操作符是否“有损”（lossy）。这使得对操作符可能有损也可能无损的情况可以更高效地处理。

## 示例 {#examples}

下面的示例命令向一个已包含数据类型 `int4` 和 `int2` 的 B-树操作符类的操作符族中添加跨数据类型的操作符和支持函数：

```sql
ALTER OPERATOR FAMILY integer_ops USING btree ADD

  -- int4 vs int2
  OPERATOR 1 < (int4, int2) ,
  OPERATOR 2 <= (int4, int2) ,
  OPERATOR 3 = (int4, int2) ,
  OPERATOR 4 >= (int4, int2) ,
  OPERATOR 5 > (int4, int2) ,
  FUNCTION 1 btint42cmp(int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 < (int2, int4) ,
  OPERATOR 2 <= (int2, int4) ,
  OPERATOR 3 = (int2, int4) ,
  OPERATOR 4 >= (int2, int4) ,
  OPERATOR 5 > (int2, int4) ,
  FUNCTION 1 btint24cmp(int2, int4) ;
```

移除这些条目：

```sql
ALTER OPERATOR FAMILY integer_ops USING btree DROP

  -- int4 vs int2
  OPERATOR 1 (int4, int2) ,
  OPERATOR 2 (int4, int2) ,
  OPERATOR 3 (int4, int2) ,
  OPERATOR 4 (int4, int2) ,
  OPERATOR 5 (int4, int2) ,
  FUNCTION 1 (int4, int2) ,

  -- int2 vs int4
  OPERATOR 1 (int2, int4) ,
  OPERATOR 2 (int2, int4) ,
  OPERATOR 3 (int2, int4) ,
  OPERATOR 4 (int2, int4) ,
  OPERATOR 5 (int2, int4) ,
  FUNCTION 1 (int2, int4) ;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER OPERATOR FAMILY` 语句。

## 另见 {#see-also}

[CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/)、[DROP OPERATOR FAMILY](/cloudberry/reference/sql-stmts/drop-operator-family/)、[ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/)、[CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/)、[DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/)
