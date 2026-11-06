---
title: "ALTER POLICY"
description: "更改行级安全策略的定义。"
weight: 200
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-policy.md"
---

## 概要 {#synopsis}

```sql
ALTER POLICY <name> ON <table_name> RENAME TO <new_name>

ALTER POLICY <name ON table_name>
    [ TO { <role_name> | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( <using_expression> ) ]
    [ WITH CHECK ( <check_expression> ) ]
```

## 描述 {#description}

`ALTER POLICY` 更改现有行级安全策略的定义。请注意，`ALTER POLICY` 只允许修改该策略所适用的角色集合，以及 `USING` 和 `WITH CHECK` 表达式。要更改策略的其他属性，例如它所适用的命令，或者它是许可型（permissive）还是限制型（restrictive），必须删除该策略并重新创建。

要使用 `ALTER POLICY`，你必须拥有该策略所适用的表。

在 `ALTER POLICY` 的第二种形式中，如果指定了角色列表、using_expression 和 check_expression，则它们各自独立地被替换。当省略其中某个子句时，策略的相应部分保持不变。

## 参数 {#parameters}

**`name`**

要更改的现有策略的名称。

**`table_name`**

该策略所在的表的名称（可以是模式限定的）。

**`new_name`**

策略的新名称。

**`role_name`**

该策略所适用的角色。可以一次指定多个角色。要将策略应用于所有角色，请使用 `PUBLIC`。

**`using_expression`**

策略的 `USING` 表达式。详情请参见 [CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/)。

**`check_expression`**

策略的 `WITH CHECK` 表达式。详情请参见 [CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/)。

## 兼容性 {#compatibility}

`ALTER POLICY` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另见 {#see-also}

[CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/)、[DROP POLICY](/cloudberry/reference/sql-stmts/drop-policy/)
