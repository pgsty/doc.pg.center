---
title: "CREATE COLLATION"
description: "定义一个新的排序规则。"
weight: 550
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-collation.md"
---

## 概要 {#synopsis}

```sql
CREATE COLLATION [ IF NOT EXISTS ] <name> (
    [ LOCALE = <locale>, ]    
    [ LC_COLLATE = <lc_collate>, ]    
    [ LC_CTYPE = <lc_ctype>, ]
    [ PROVIDER = <provider>, ]
    [ DETERMINISTIC = <boolean>, ]
    [ VERSION = <version> ])

CREATE COLLATION [ IF NOT EXISTS ] <name> FROM <existing_collation>
```

## 描述 {#description}

`CREATE COLLATION` 使用指定的操作系统区域设置，或者通过复制现有排序规则，来定义一个新的排序规则。

要能够创建排序规则，必须对目标模式具有 `CREATE` 权限。

## 参数 {#parameters}

**`IF NOT EXISTS`**

如果已存在同名的排序规则，不抛出错误。这种情况下会发出一条提示。注意，不保证现有的排序规则与本应创建的排序规则有任何相似之处。

**`name`**

排序规则的名称。排序规则名称可以带模式限定。如果不带模式限定，则在当前模式中定义该排序规则。排序规则名称在该模式内必须唯一。（系统目录中可能包含针对其他编码的同名排序规则，但如果数据库编码不匹配，这些排序规则会被忽略。）

**`locale`**

这是同时设置 `LC_COLLATE` 和 `LC_CTYPE` 的快捷方式。如果指定了它，就不能再指定这两个参数中的任何一个。

**`lc_collate`**

对 `LC_COLLATE` 区域类别使用指定的操作系统区域设置。

**`lc_ctype`**

对 `LC_CTYPE` 区域类别使用指定的操作系统区域设置。

**`provider`**

指定用于与此排序规则相关联的区域设置服务的提供者。可能的值有：`icu`、`libc`。默认为 `libc`。可用的选项取决于操作系统和构建选项。

**`DETERMINISTIC`**

指定排序规则是否应使用确定性比较。默认为 `true`。确定性比较会将逐字节不相等的字符串视为不相等，即使比较时认为它们在逻辑上相等。Apache Cloudberry 使用逐字节比较来打破平局。非确定性比较可以使排序规则例如不区分大小写或不区分重音。为此，需要选择合适的 `LC_COLLATE` 设置，并在此处将排序规则设为非确定性。

非确定性排序规则仅在 `icu` 提供者下受支持。

**`version`**

指定与排序规则一起存储的版本字符串。通常应省略它，这会使版本根据操作系统提供的排序规则的实际版本计算得出。此选项旨在供 `pg_upgrade` 使用，用于从现有安装复制版本。

有关如何处理排序规则版本不匹配，另请参见 [ALTER COLLATION](/cloudberry/reference/sql-stmts/alter-collation/)。

**`existing_collation`**

要复制的现有排序规则的名称。新排序规则将具有与现有排序规则相同的属性，但它是一个独立的对象。

## 注解 {#notes}

`CREATE COLLATION` 会对 `pg_collation` 系统目录获取 `SHARE ROW EXCLUSIVE` 锁，该锁与自身冲突，因此同一时间只能运行一个 `CREATE COLLATION` 命令。

使用 [DROP COLLATION](/cloudberry/reference/sql-stmts/drop-collation/) 删除用户定义的排序规则。

有关 Apache Cloudberry 中排序规则支持的更多信息，参见 PostgreSQL 文档中的[排序规则支持](https://www.postgresql.org/docs/12/collation.html)。

使用 `libc` 排序规则提供者时，区域设置必须适用于当前数据库编码。确切规则参见 [CREATE DATABASE](/cloudberry/reference/sql-stmts/create-database/)。

## 示例 {#examples}

从操作系统区域设置 `fr_FR.utf8` 创建一个排序规则（假定当前数据库编码为 `UTF8`）：

```sql
CREATE COLLATION french (LOCALE = 'fr_FR.utf8');
```

使用 `icu` 提供者和德语电话簿排序顺序创建一个排序规则：

```sql
CREATE COLLATION german_phonebook (provider = icu, locale = 'de-u-co-phonebk');
```

从现有排序规则创建一个排序规则：

```sql
CREATE COLLATION german FROM "de_DE";
```

这样便于在应用程序中使用与操作系统无关的排序规则名称。

## 兼容性 {#compatibility}

SQL 标准中有 `CREATE COLLATION` 语句，但仅限于复制现有的排序规则。创建新排序规则的语法是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER COLLATION](/cloudberry/reference/sql-stmts/alter-collation/)、[DROP COLLATION](/cloudberry/reference/sql-stmts/drop-collation/)
