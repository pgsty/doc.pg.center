---
title: "ALTER EXTERNAL TABLE"
description: "更改一个外部表的定义。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-external-table.md"
---

## 概要 {#synopsis}

```sql
ALTER EXTERNAL TABLE <name> <action> [, ... ]
```

其中 action 为下列之一：

```sql
  ADD [COLUMN] <new_column> <type>
  DROP [COLUMN] <column> [RESTRICT|CASCADE]
  ALTER [COLUMN] <column> TYPE <type>
  OWNER TO <new_owner>
```

## 描述 {#description}

`ALTER EXTERNAL TABLE` 更改一个现有外部表的定义。`ALTER EXTERNAL TABLE` 支持以下操作：

- **ADD COLUMN** — 向外部表定义中添加一个新列。
- **DROP COLUMN** — 从外部表定义中删除一列。如果你删除可读外部表的列，则只会更改 Apache Cloudberry 中的表定义。如果表外有任何对象依赖于该列（例如引用该列的视图），则必须使用 `CASCADE` 关键字。
- **ALTER COLUMN TYPE** — 更改表列的数据类型。
- **OWNER** — 把外部表的所有者更改为指定的用户。

要对外部表执行以下操作，请使用 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 命令：

- 设置（更改）表所在的模式。
- 重命名表。
- 重命名表列。
- 设置（更改）分布策略（仅限可写外部表）。

要使用 `ALTER EXTERNAL TABLE` 或 `ALTER TABLE`，你必须拥有该外部表。要更改外部表的模式，你还必须在新模式上具有 `CREATE` 权限。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该外部表所在的模式上具有 `CREATE` 权限。超级用户自动拥有这些权限。

你使用 `ALTER EXTERNAL TABLE` 或 `ALTER TABLE` 对外部表定义所做的更改不会影响外部数据。

`ALTER EXTERNAL TABLE` 和 `ALTER TABLE` 命令不能修改外部表的类型（读、写、web）、表的 `FORMAT` 信息，或外部数据的位置。要修改这些信息，你必须删除并重新创建该外部表定义。

## 参数 {#parameters}

**`name`**

要更改的现有外部表定义的名称（可以是模式限定的）。

**`column`**

现有列的名称。

**`new_column`**

新列的名称。

**`type`**

新列的数据类型，或现有列的新数据类型。

**`new_owner`**

外部表的新所有者的角色名称。

**`CASCADE`**

自动删除依赖于被删除列的对象，例如引用该列的视图。

**`RESTRICT`**

如果存在任何依赖对象，则拒绝删除该列或约束。这是默认行为。

## 示例 {#examples}

向外部表定义中添加一个新列：

```sql
ALTER EXTERNAL TABLE ext_expenses ADD COLUMN manager text;
```

更改外部表的所有者：

```sql
ALTER EXTERNAL TABLE ext_data OWNER TO jojo;
```

更改外部表某列的数据类型：

```sql
ALTER EXTERNAL TABLE ext_leads ALTER COLUMN acct_code TYPE integer;
```

## 兼容性 {#compatibility}

`ALTER EXTERNAL TABLE` 是 Apache Cloudberry 的扩展。SQL 标准和常规 PostgreSQL 中都没有 `ALTER EXTERNAL TABLE` 语句。

## 另见 {#see-also}

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/)、[DROP EXTERNAL TABLE](/cloudberry/reference/sql-stmts/drop-external-table/)、[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)
