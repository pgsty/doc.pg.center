---
title: "ALTER VIEW"
description: "更改视图的属性。"
weight: 420
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-view.md"
---

## 概要 {#synopsis}

```sql
ALTER VIEW [ IF EXISTS ] <name> ALTER [ COLUMN ] <column_name> SET DEFAULT <expression>

ALTER VIEW [ IF EXISTS ] <name> ALTER [ COLUMN ] <column_name> DROP DEFAULT

ALTER VIEW [ IF EXISTS ] <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER VIEW [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER VIEW [ IF EXISTS ] <name> SET SCHEMA <new_schema>

ALTER VIEW [ IF EXISTS ] <name> SET ( <view_option_name> [= <view_option_value>] [, ... ] )

ALTER VIEW [ IF EXISTS ] <name> RESET ( <view_option_name> [, ... ] )
```

## 描述 {#description}

`ALTER VIEW` 用于更改视图的各种辅助属性。（如果要修改视图的定义查询，请使用 `CREATE OR REPLACE VIEW`。）

必须拥有视图才能使用 `ALTER VIEW`。要更改视图的模式，还必须对新模式具有 `CREATE` 权限。要更改所有者，还必须是新所有者角色的直接或间接成员，并且该角色必须对视图所在的模式具有 `CREATE` 权限。这些限制确保了更改所有者不会做出通过删除并重新创建视图无法做到的事情。不过，超级用户可以更改任何视图的所有权。

## 参数 {#parameters}

**`name`**

现有视图的名称（可以带模式限定）。

**`IF EXISTS`**

如果视图不存在，不抛出错误。在这种情况下，Apache Cloudberry 会发出一条通知。

**`SET/DROP DEFAULT`**

这些形式用于设置或移除列的默认值。视图列的默认值会在应用视图的任何规则或触发器之前，被代入以该视图为目标的任何 `INSERT` 或 `UPDATE` 命令中。因此，视图的默认值将优先于来自底层关系的任何默认值。

**`new_owner`**

视图的新所有者的用户名。

**`new_name`**

视图的新名称。

**`new_schema`**

视图的新模式。

**`SET ( view_option_name [= view_option_value] [, ... ] )`**<br />
**`RESET ( view_option_name [, ... ] )`**

设置或重置视图选项。目前支持的选项有：

**`check_option (string)`**

更改视图的检查选项。其值必须是 `local` 或 `cascaded`。

**`security_barrier (boolean)`**

更改视图的安全屏障属性。其值必须是布尔值，例如 `true` 或 `false`。

## 注意事项 {#notes}

出于历史原因，`ALTER TABLE` 也可以用于视图；但是，`ALTER TABLE` 允许用于视图的变体只有与上面所示语句等价的那些。

## 示例 {#examples}

将视图 `foo` 重命名为 `bar`：

```sql
ALTER VIEW foo RENAME TO bar;
```

为可更新视图附加默认列值：

```sql
CREATE TABLE base_table (id int, ts timestamptz);
CREATE VIEW a_view AS SELECT * FROM base_table;
ALTER VIEW a_view ALTER COLUMN ts SET DEFAULT now();
INSERT INTO base_table(id) VALUES(1);  -- ts will receive a NULL
INSERT INTO a_view(id) VALUES(2);  -- ts will receive the current time
```

## 兼容性 {#compatibility}

`ALTER VIEW` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另请参阅 {#see-also}

[CREATE VIEW](/cloudberry/reference/sql-stmts/create-view/)、[DROP VIEW](/cloudberry/reference/sql-stmts/drop-view/)
