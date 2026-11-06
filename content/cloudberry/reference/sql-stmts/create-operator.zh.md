---
title: "CREATE OPERATOR"
description: "定义新的操作符。"
weight: 700
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-operator.md"
---

## 语法概要 {#synopsis}

```sql
CREATE OPERATOR <name> ( 
       { FUNCTION | PROCEDURE } = <function_name>
       [, LEFTARG = <left_type>] [, RIGHTARG = <right_type>]
       [, COMMUTATOR = <com_op>] [, NEGATOR = <neg_op>]
       [, RESTRICT = <res_proc>] [, JOIN = <join_proc>]
       [, HASHES] [, MERGES] )
```

## 说明 {#description}

`CREATE OPERATOR` 定义新操作符。定义操作符的用户成为其所有者。如果给出模式名，则在指定模式中创建操作符；否则在当前模式中创建。

操作符名称是由下列字符组成的序列，最多包含 `NAMEDATALEN`-1 个字符（默认为 63 个）：<code>+ - * / < > = ~ ! @ # % ^ & | ` ?</code>。

名称选择有以下限制：

- 操作符名称的任何位置都不能出现 `--` 和 `/*`，因为它们会被视为注释的开头。
- 多字符操作符名称不能以 `+` 或 `-` 结尾，除非名称还包含以下至少一个字符：<code>~ ! @ # % ^ & | ` ?</code>

    例如，`@-` 是允许的操作符名称，而 `*-` 不是。此限制使 Apache Cloudberry 可以解析符合 SQL 的命令，而不要求词元之间有空格。

- 使用 `=>` 作为操作符名称已弃用，未来版本可能完全禁止。

操作符 `!=` 在输入时映射为 `<>`，因此这两个名称始终等价。

必须至少定义 `LEFTARG` 和 `RIGHTARG` 之一。二元操作符必须同时定义两者。对于右一元操作符，应只定义 `LEFTARG`；对于左一元操作符，应只定义 `RIGHTARG`。

**注意：** 右一元操作符（也称后缀操作符）已弃用，可能在未来的 Apache Cloudberry 版本中移除。

function_name 函数必须已通过 `CREATE FUNCTION` 定义，必须为 `IMMUTABLE`，并且必须定义为接受正确数量（一个或两个）且类型符合指定要求的参数。

在 `CREATE OPERATOR` 语法中，关键字 `FUNCTION` 和 `PROCEDURE` 等价，但无论如何，被引用的对象必须是函数，而不能是过程。这里使用关键字 `PROCEDURE` 是历史遗留用法，已弃用。

其他子句指定可选的操作符优化信息。其含义详见 PostgreSQL 的[操作符优化信息](https://www.postgresql.org/docs/12/xoper-optimization.html)文档。

要创建操作符，必须对参数类型和返回类型具有 `USAGE` 权限，并对底层函数具有 `EXECUTE` 权限。如果指定交换操作符或否定操作符，必须拥有这些操作符。

## 参数 {#parameters}

**`name`**

要定义的操作符名称（可以用模式名限定）。允许的字符参见上面的*说明*。名称可以带模式限定，例如 `CREATE OPERATOR myschema.+ (...)`。否则，在当前模式中创建操作符。同一模式中的两个操作符，如果操作的数据类型不同，可以使用相同名称。这称为*重载*。

**`function_name`**

用于实现此操作符的函数（必须是 `IMMUTABLE` 函数）。

**`left_type`**

操作符左操作数的数据类型（如果有）。对于左一元操作符应省略此选项。

**`right_type`**

操作符右操作数的数据类型（如果有）。对于右一元操作符应省略此选项。

**`com_op`**

此操作符的交换操作符。可选的 `COMMUTATOR` 子句指定正在定义的操作符的交换操作符。如果对所有可能的输入值 x、y，(x A y) 都等于 (y B x)，就称操作符 A 是操作符 B 的交换操作符。请注意，B 也是 A 的交换操作符。例如，对于特定数据类型，操作符 `<` 和 `>` 通常互为交换操作符，而操作符 + 通常与自身可交换。但操作符 `-` 通常没有交换操作符。可交换操作符的左操作数类型与其交换操作符的右操作数类型相同，反之亦然。因此，在 `COMMUTATOR` 子句中只需提供交换操作符的名称。

**`neg_op`**

此操作符的否定操作符。可选的 `NEGATOR` 子句指定正在定义的操作符的否定操作符。如果操作符 A 和 B 都返回布尔结果，且对所有可能的输入 x、y，(x A y) 都等于 NOT (x B y)，就称 A 是 B 的否定操作符。请注意，B 也是 A 的否定操作符。例如，对大多数数据类型，`<` 和 `>=` 互为否定操作符。否定操作符必须与待定义操作符具有相同的左和/或右操作数类型，因此在 `NEGATOR` 子句中只需给出操作符名称。

**`res_proc`**

此操作符的限制选择率估算函数。可选的 `RESTRICT` 指定操作符的限制选择率估算函数。（请注意，这是函数名称，不是操作符名称。）`RESTRICT` 子句只对返回 `boolean` 的二元操作符有意义。

**`join_proc`**

此操作符的连接选择率估算函数。可选的 `JOIN` 子句指定操作符的连接选择率估算函数。（请注意，这是函数名称，不是操作符名称。）`JOIN` 子句只对返回 `boolean` 的二元操作符有意义。

**`HASHES`**

表示此操作符支持哈希连接。可选的 `HASHES` 子句告诉系统，允许对基于此操作符的连接使用哈希连接方法。`HASHES` 只对返回 `boolean` 的二元操作符有意义。哈希连接操作符只能对哈希到相同哈希码的左右值对返回 true。如果两个值放入不同哈希桶，连接就永远不会比较它们，隐含假设连接操作符的结果必定为 false。因此，对不表示相等关系的操作符指定 `HASHES` 永远没有意义。

**`MERGES`**

表示此操作符支持归并连接。如果出现 `MERGES` 子句，它会告诉系统允许对基于此操作符的连接使用归并连接方法。`MERGES` 只对返回 `boolean` 的二元操作符有意义，而且实际上该操作符必须表示某种数据类型或一对数据类型的相等关系。

要在 com_op 或其他可选参数中给出带模式限定的操作符名称，请使用 `OPERATOR()` 语法，例如：

```sql
COMMUTATOR = OPERATOR(myschema.===) ,
```

## 注意事项 {#notes}

更多信息参见 PostgreSQL 文档中的[用户定义的操作符](https://www.postgresql.org/docs/12/xoper.html)。

用于实现操作符的所有函数都必须定义为 `IMMUTABLE`。

不能在 `CREATE OPERATOR` 中指定操作符的词法优先级，因为解析器的优先级行为是固定的。优先级详情参见 PostgreSQL 文档中的[操作符优先级](https://www.postgresql.org/docs/12/sql-syntax-lexical.html#SQL-PRECEDENCE)。

使用 [DROP OPERATOR](/cloudberry/reference/sql-stmts/drop-operator/) 从数据库中删除用户定义的操作符。使用 [ALTER OPERATOR](/cloudberry/reference/sql-stmts/alter-operator/) 修改数据库中的操作符。

## 示例 {#examples}

以下命令为数据类型 `box` 定义新的面积相等操作符：

```sql
CREATE OPERATOR === (
    LEFTARG = box,
    RIGHTARG = box,
    FUNCTION = area_equal_function,
    COMMUTATOR = ===,
    NEGATOR = !==,
    RESTRICT = area_restriction_function,
    JOIN = area_join_function,
    HASHES, MERGES
);
```

以下示例创建用于两个复数相加的操作符。假定已创建 `complex` 类型的定义。首先定义实际执行运算的函数，再定义操作符：

```sql
CREATE FUNCTION complex_add(complex, complex)
    RETURNS complex
    AS 'filename', 'complex_add'
    LANGUAGE C IMMUTABLE STRICT;
CREATE OPERATOR + (
    leftarg = complex,
    rightarg = complex,
    procedure = complex_add,
    commutator = +
);
```

在查询中使用此操作符：

```sql
SELECT (a + b) AS c FROM test_complex;
```

## 兼容性 {#compatibility}

`CREATE OPERATOR` 是 Apache Cloudberry 对 SQL 标准的扩展。SQL 标准未规定用户定义的操作符。

## 另请参阅 {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [CREATE TYPE](/cloudberry/reference/sql-stmts/create-type/), [ALTER OPERATOR](/cloudberry/reference/sql-stmts/alter-operator/), [CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/), [DROP OPERATOR](/cloudberry/reference/sql-stmts/drop-operator/)
