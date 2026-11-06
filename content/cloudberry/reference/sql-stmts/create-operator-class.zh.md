---
title: "CREATE OPERATOR CLASS"
description: "定义新的操作符类。"
weight: 680
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-operator-class.md"
---

## 语法概要 {#synopsis}

```sql
CREATE OPERATOR CLASS <name> [DEFAULT] FOR TYPE <data_type>  
  USING <index_method> [ FAMILY <family_name> ] AS 
  { OPERATOR <strategy_number> <operator_name> [ ( <op_type>, <op_type> ) ] [ FOR SEARCH | FOR ORDER BY <sort_family_name> ]
  | FUNCTION <support_number> [ ( <op_type> [ , <op_type> ] ) ] <function_name> (<argument_type> [, ...] )
  | STORAGE <storage_type>
  } [, ... ]
```

## 说明 {#description}

`CREATE OPERATOR CLASS` 创建新的操作符类。操作符类定义特定数据类型如何与索引配合使用，指定某些操作符在该数据类型和索引方法中所承担的角色或策略。它还指定在为索引列选择该操作符类后，索引方法所使用的支持函数。操作符类使用的所有操作符和函数都必须在创建操作符类之前定义。实现操作符类的所有函数都必须定义为 `IMMUTABLE`。

如果给出模式名，则在指定模式中创建操作符类；否则在当前模式中创建。同一模式中的两个操作符类只有在面向不同索引方法时才能同名。

定义操作符类的用户成为其所有者。目前，创建者必须是超级用户。（施加此限制是因为错误的操作符类定义可能导致服务器混乱甚至崩溃。）

`CREATE OPERATOR CLASS` 目前不检查操作符类定义是否包含索引方法所需的所有操作符和函数，也不检查这些操作符和函数是否构成自洽的集合。用户有责任定义有效的操作符类。

相关操作符类可以归入操作符族。要将新操作符类加入现有族，在 `CREATE OPERATOR CLASS` 中指定 `FAMILY` 选项。不使用此选项时，新类会被放入与其同名的族（如果该族不存在，Apache Cloudberry 会创建它）。

更多信息参见 PostgreSQL 文档中的[索引扩展接口](https://www.postgresql.org/docs/12/xindex.html)。

## 参数 {#parameters}

**`name`**

要定义的操作符类的名称（可以用模式名限定）。同一模式中的两个操作符类只有在面向不同索引方法时才能同名。

**`DEFAULT`**

如果出现，则将该操作符类设为其数据类型的默认操作符类。对于特定数据类型和索引方法，最多只能有一个默认操作符类。

**`data_type`**

此操作符类面向的列数据类型。

**`index_method`**

此操作符类面向的索引方法名称。

**`family_name`**

要将此操作符类加入的现有操作符族的名称。如果未指定，则使用与操作符类同名的族（如果不存在则创建）。

**`strategy_number`**

索引方法中与操作符类关联的操作符的策略编号。操作符类关联的操作符通过*策略编号*标识；这些编号用于标识各操作符在其操作符类上下文中的语义。

**`operator_name`**

与操作符类关联的操作符名称（可以用模式名限定）。

**`op_type`**

在 `OPERATOR` 子句中，表示操作符操作数的数据类型，或用 `NONE` 表示左一元或右一元操作符。在操作数数据类型与操作符类数据类型相同的常见情况下，可以省略操作数数据类型。

在 `FUNCTION` 子句中，如果函数要支持的操作数数据类型与函数的输入数据类型（对 B-树比较函数和哈希函数而言）或类的数据类型（对 B-树排序支持函数，以及 GiST、SP-GiST、GIN 和 BRIN 操作符类中的所有函数而言）不同，则在此指定。上述默认值通常是正确的，因此 `FUNCTION` 子句中无需指定 op_type，只有用于支持跨数据类型比较的 B-树排序支持函数例外。

**`sort_family_name`**

现有 `btree` 操作符族的名称（可以用模式名限定），该族描述排序操作符关联的排序顺序。

如果既未指定 `FOR SEARCH` 也未指定 `FOR ORDER BY`，则默认为 `FOR SEARCH`。

**`support_number`**

索引方法中与操作符类关联的函数的支持函数编号。

**`function_name`**

为此操作符类提供索引方法支持的函数名称（可以用模式名限定）。

**`argument_type`**

函数参数的数据类型。

**`storage_type`**

索引中实际存储的数据类型。通常与列数据类型相同，但某些索引方法（目前包括 GiST、GIN 和 BRIN）允许其不同。除非索引方法允许使用不同类型，否则必须省略 `STORAGE` 子句。如果列 data_type 指定为 `anyarray`，可将 storage_type 声明为 `anyelement`，表示索引条目属于每个具体索引所针对的实际数组类型的元素类型。

`OPERATOR`、`FUNCTION` 和 `STORAGE` 子句可以按任意顺序出现。

## 注意事项 {#notes}

由于索引机制在使用函数前不检查函数访问权限，将函数或操作符加入操作符类等同于向公众授予它的执行权限。对于适用于操作符类的函数类型，这通常不是问题。

不应使用 SQL 函数定义操作符。SQL 函数可能被内联到调用查询中，这会使优化器无法识别查询与索引的匹配关系。

用于实现操作符类的所有函数都必须定义为 `IMMUTABLE`。

在 Apache Cloudberry 6.0 之前，`OPERATOR` 子句可以包含 `RECHECK` 选项。现在不再支持此选项。Apache Cloudberry 会在运行时动态判断索引操作符是否“有损”，从而更高效地处理操作符可能有损也可能无损的情况。

## 示例 {#examples}

以下示例命令为数据类型 `_int4`（int4 数组）定义 GiST 索引操作符类。完整示例参见 `intarray` contrib 模块。

```sql
CREATE OPERATOR CLASS gist__int_ops
    DEFAULT FOR TYPE _int4 USING gist AS
        OPERATOR 3 &&,
        OPERATOR 6 = (anyarray, anyarray),
        OPERATOR 7 @>,
        OPERATOR 8 <@,
        OPERATOR 20 @@ (_int4, query_int),
        FUNCTION 1 g_int_consistent (internal, _int4, smallint, oid, internal),
        FUNCTION 2 g_int_union (internal, internal),
        FUNCTION 3 g_int_compress (internal),
        FUNCTION 4 g_int_decompress (internal),
        FUNCTION 5 g_int_penalty (internal, internal, internal),
        FUNCTION 6 g_int_picksplit (internal, internal),
        FUNCTION 7 g_int_same (_int4, _int4, internal);
```

## 兼容性 {#compatibility}

`CREATE OPERATOR CLASS` 是 Apache Cloudberry 的扩展。SQL 标准中没有 `CREATE OPERATOR CLASS` 语句。

## 另请参阅 {#see-also}

[ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/), [DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/), [CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/), [ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/), [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)
