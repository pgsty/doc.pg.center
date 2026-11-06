---
title: "CREATE DOMAIN"
description: "定义一个新的域。"
weight: 580
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-domain.md"
---

## 概要 {#synopsis}

```sql
CREATE DOMAIN <name> [AS] <data_type>
       [ COLLATE <collation> ] 
       [ DEFAULT <expression> ]
       [ <constraint> [ ... ] ]

-- where <constraint> is:

[ CONSTRAINT <constraint_name> ]
{ NOT NULL | NULL | CHECK (<expression>)  }
```

## 描述 {#description}

`CREATE DOMAIN` 创建一个新的域。域本质上是带有可选约束（对允许取值集合的限制）的数据类型。定义域的用户成为其所有者。

如果给出了模式名（例如 `CREATE DOMAIN myschema.mydomain ...`），则域在指定的模式中创建。否则在当前模式中创建。域名在其模式中现有的数据类型和域之中必须唯一。

域可用于把字段上的通用约束抽象到单一位置进行维护。例如，多个表可能都包含电子邮件地址列，且都需要相同的 `CHECK` 约束来验证地址语法。此时应定义一个域，而不是为每个表单独设置约束。

要能够创建域，必须对底层类型具有 `USAGE` 权限。

## 参数 {#parameters}

**`name`**

要创建的域的名称（可以带模式限定）。

**`data_type`**

域的底层数据类型。这可以包含数组说明符。

**`collation`**

域的可选排序规则。如果未指定排序规则，则域具有与其底层数据类型相同的排序规则行为。如果指定了 `COLLATE`，底层类型必须是可排序的。

**`DEFAULT expression`**

为该域数据类型的列指定默认值。该值是任意不含变量的表达式（但不允许子查询）。默认表达式的数据类型必须与域的数据类型相匹配。如果未指定默认值，则默认值为空值。

在任何未为该列指定值的插入操作中，都会使用默认表达式。如果为某个特定列定义了默认值，它会覆盖与域相关联的任何默认值。反过来，域的默认值会覆盖与底层数据类型相关联的任何默认值。

**`CONSTRAINT constraint_name`**

约束的可选名称。如果未指定，系统会生成一个名称。

**`NOT NULL`**

该域的值不允许为空（但参见下面的注解）。

**`NULL`**

该域的值允许为空。这是默认设置。

此子句仅用于与非标准 SQL 数据库的兼容。不鼓励在新应用中使用。

**`CHECK (expression)`**

`CHECK` 子句指定域的值必须满足的完整性约束或测试。每个约束必须是产生布尔结果的表达式。它应使用关键字 `VALUE` 来引用正在被测试的值。计算结果为 TRUE 或 UNKNOWN 的表达式表示成功。如果表达式产生 FALSE 结果，则报告错误，并且该值不允许被转换为域类型。

目前，`CHECK` 表达式不能包含子查询，也不能引用 `VALUE` 以外的变量。

当一个域具有多个 `CHECK` 约束时，它们将按名称的字母顺序进行测试。（7.0 之前的 Apache Cloudberry 版本不保证 `CHECK` 约束有任何特定的触发顺序。）

## 注解 {#notes}

域约束，特别是 `NOT NULL`，是在将值转换为域类型时检查的。名义上属于域类型的列，尽管存在这样的约束，仍有可能读出为空。例如，在外连接查询中，如果域列位于外连接的可为空一侧，就会发生这种情况。一个更微妙的例子是：

```sql
INSERT INTO tab (domcol) VALUES ((SELECT domcol FROM tab WHERE false));
```

空的标量子 SELECT 会产生一个被视为属于域类型的空值，因此不会再对其应用进一步的约束检查，插入将会成功。

很难避免这类问题，因为 SQL 通常假定空值是每种数据类型的有效值。因此，最佳实践是将域的约束设计为允许空值，然后根据需要对域类型的列应用列的 `NOT NULL` 约束，而不是直接对域类型应用。

Apache Cloudberry 假定 `CHECK` 约束的条件是不可变的，即对相同的输入值总是给出相同的结果。正是这一假定使得仅在值首次被转换为域类型时检查 `CHECK` 约束，而不在其他时候检查。（这与对表 `CHECK` 约束的处理方式基本相同。）

破坏这一假定的一个常见例子，是在 `CHECK` 表达式中引用用户定义函数，然后更改该函数的行为。Apache Cloudberry 并不禁止这样做，但如果存在现在违反 `CHECK` 约束的、该域类型的已存储值，它也不会察觉。这会导致之后的数据库转储和恢复失败。处理这种更改的推荐方法是：删除约束（使用 `ALTER DOMAIN`），调整函数定义，然后重新添加约束，从而根据已存储的数据重新检查它。

## 示例 {#examples}

此示例创建 `us_postal_code` 数据类型，然后在表定义中使用该类型。使用正则表达式测试来验证值看起来像有效的美国邮政编码。

```sql
CREATE DOMAIN us_postal_code AS TEXT
CHECK(
   VALUE ~ '^\d{5}$'
OR VALUE ~ '^\d{5}-\d{4}$'
);

CREATE TABLE us_snail_addy (
  address_id SERIAL PRIMARY KEY,
  street1 TEXT NOT NULL,
  street2 TEXT,
  street3 TEXT,
  city TEXT NOT NULL,
  postal us_postal_code NOT NULL
);
```

## 兼容性 {#compatibility}

`CREATE DOMAIN` 符合 SQL 标准。

## 另见 {#see-also}

[ALTER DOMAIN](/cloudberry/reference/sql-stmts/alter-domain/)、[DROP DOMAIN](/cloudberry/reference/sql-stmts/drop-domain/)
