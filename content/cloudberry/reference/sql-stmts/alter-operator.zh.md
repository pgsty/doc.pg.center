---
title: "ALTER OPERATOR"
description: "更改操作符的定义。"
weight: 190
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-operator.md"
---

## 概要 {#synopsis}

```sql
ALTER OPERATOR <name> ( {<left_type> | NONE} , {<right_type> | NONE} ) 
   OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER OPERATOR <name> ( {<left_type> | NONE} , {<right_type> | NONE} ) 
    SET SCHEMA <new_schema>

ALTER OPERATOR name ( { <left_type> | NONE } , { <right_type> | NONE } )
    SET ( {  RESTRICT = { <res_proc> | NONE }
           | JOIN = { <join_proc> | NONE }
         } [, ... ] )
```

## 描述 {#description}

`ALTER OPERATOR` 更改操作符的定义。

要使用 `ALTER OPERATOR`，你必须拥有该操作符。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该操作符所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该操作符无法做到的事情。不过，超级用户无论如何都可以更改任何操作符的所有权。）

## 参数 {#parameters}

**`name`**

一个现有操作符的名称（可以是模式限定的）。

**`left_type`**

操作符左操作数的数据类型；如果该操作符没有左操作数，则写为 `NONE`。

**`right_type`**

操作符右操作数的数据类型；如果该操作符没有右操作数，则写为 `NONE`。

**`new_owner`**

操作符的新所有者。

**`new_schema`**

操作符的新模式。

**`res_proc`**

此操作符的限制选择性估计函数；写为 `NONE` 可移除现有的选择性估计函数。

**`join_proc`**

此操作符的连接选择性估计函数；写为 `NONE` 可移除现有的选择性估计函数。

## 示例 {#examples}

更改类型为 `text` 的自定义操作符 `a @@ b` 的所有者：

```sql
ALTER OPERATOR @@ (text, text) OWNER TO joe;
```

更改类型为 `int[]` 的自定义操作符 `a && b` 的限制选择性估计函数和连接选择性估计函数：

```sql
ALTER OPERATOR && (_int4, _int4) SET (RESTRICT = _int_contsel, JOIN = _int_contjoinsel);
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER OPERATOR` 语句。

## 另见 {#see-also}

[CREATE OPERATOR](/cloudberry/reference/sql-stmts/create-operator/)、[DROP OPERATOR](/cloudberry/reference/sql-stmts/drop-operator/)
