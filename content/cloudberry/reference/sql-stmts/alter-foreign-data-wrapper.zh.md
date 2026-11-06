---
title: "ALTER FOREIGN DATA WRAPPER"
description: "更改一个外部数据包装器的定义。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-foreign-data-wrapper.md"
---

## 概要 {#synopsis}

```sql
ALTER FOREIGN DATA WRAPPER <name>
    [ HANDLER <handler_function> | NO HANDLER ]
    [ VALIDATOR <validator_function> | NO VALIDATOR ]
    [ OPTIONS ( [ ADD | SET | DROP ] <option> ['<value>'] [, ... ] ) ]

ALTER FOREIGN DATA WRAPPER <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
ALTER FOREIGN DATA WRAPPER <name> RENAME TO <new_name>
```

## 描述 {#description}

`ALTER FOREIGN DATA WRAPPER` 更改一个外部数据包装器的定义。该命令的第一种形式更改外部数据包装器的支持函数或通用选项。Apache Cloudberry 要求至少提供一个子句。第二种和第三种形式分别更改外部数据包装器的所有者或名称。

只有超级用户才能更改外部数据包装器。此外，只有超级用户才能拥有外部数据包装器。

## 参数 {#parameters}

**`name`**

一个现有外部数据包装器的名称。

**`HANDLER handler_function`**

为外部数据包装器指定新的处理函数。

**`NO HANDLER`**

指定外部数据包装器不再具有处理函数。

> **注意** 你不能访问使用了没有处理函数的外部数据包装器的外表。

**`VALIDATOR validator_function`**

为外部数据包装器指定新的验证函数。

请注意，更改验证函数时，外部数据包装器本身已有的选项，或依赖于它的服务器、用户映射或外表的选项，有可能变为无效。Apache Cloudberry 不会检查这一点。在使用修改后的外部数据包装器之前，你必须确保这些选项是正确的。不过，Apache Cloudberry 会使用新的验证函数检查此 `ALTER FOREIGN DATA WRAPPER` 命令中指定的任何选项。

**`NO VALIDATOR`**

指定外部数据包装器不再具有验证函数。

**`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`**

更改外部数据包装器的选项。`ADD`、`SET` 和 `DROP` 指定要执行的操作。如果没有显式指定操作，则默认操作为 `ADD`。选项名称必须唯一。如果外部数据包装器有验证函数，Apache Cloudberry 会使用它来验证名称和值。

**`OWNER TO new_owner`**

指定外部数据包装器的新所有者的用户名。只有超级用户才能拥有外部数据包装器。

**`RENAME TO new_name`**

指定外部数据包装器的新名称。

## 示例 {#examples}

更改名为 `dbi` 的外部数据包装器的定义：添加一个名为 `foo` 的新选项，并移除名为 `bar` 的选项：

```sql
ALTER FOREIGN DATA WRAPPER dbi OPTIONS (ADD foo '1', DROP 'bar');
```

将名为 `dbi` 的外部数据包装器的验证函数更改为 `bob.myvalidator`：

```sql
ALTER FOREIGN DATA WRAPPER dbi VALIDATOR bob.myvalidator;
```

## 兼容性 {#compatibility}

`ALTER FOREIGN DATA WRAPPER` 符合 ISO/IEC 9075-9（SQL/MED），但 `HANDLER`、`VALIDATOR`、`OWNER TO` 和 `RENAME TO` 子句除外，它们是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/)、[DROP FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/drop-foreign-data-wrapper/)
