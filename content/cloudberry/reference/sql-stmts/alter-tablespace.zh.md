---
title: "ALTER TABLESPACE"
description: "更改表空间的定义。"
weight: 330
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-tablespace.md"
---

## 概要 {#synopsis}

```sql
ALTER TABLESPACE <name> RENAME TO <new_name>

ALTER TABLESPACE <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER TABLESPACE <name> SET ( <tablespace_option> = <value> [, ... ] )

ALTER TABLESPACE <name> RESET ( <tablespace_option> [, ... ] )
```

## 描述 {#description}

`ALTER TABLESPACE` 用于更改表空间的定义。

必须是表空间的所有者才能使用 `ALTER TABLESPACE`。要更改所有者，还必须是新所有者角色的直接或间接成员。（注意，超级用户自动拥有这些权限。）

## 参数 {#parameters}

**`name`**

现有表空间的名称。

**`new_name`**

表空间的新名称。新名称不能以 `pg_` 或 `gp_ `开头（这些前缀保留给系统表空间）。

**`new_owner`**

表空间的新所有者。

**`tablespace_parameter`**

要设置或重置的表空间参数。目前仅有的可用参数是 `seq_page_cost` 和 `random_page_cost`。为某个特定表空间设置其中任一值，都会覆盖规划器对从该表空间中的表读取页面所需代价的常规估计；该常规估计由同名的配置参数确定（参见 `seq_page_cost`、`random_page_cost`）。如果某个表空间所在的磁盘比 I/O 子系统的其余部分更快或更慢，这会很有用。

## 示例 {#examples}

将表空间 `index_space` 重命名为 `fast_raid`：

```sql
ALTER TABLESPACE index_space RENAME TO fast_raid;
```

更改表空间 `index_space` 的所有者：

```sql
ALTER TABLESPACE index_space OWNER TO mary;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER TABLESPACE` 语句。

## 另请参阅 {#see-also}

[`CREATE TABLESPACE`](/cloudberry/reference/sql-stmts/create-tablespace/)、[`DROP TABLESPACE`](/cloudberry/reference/sql-stmts/drop-tablespace/)
