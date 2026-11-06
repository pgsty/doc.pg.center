---
title: "DROP INDEX"
description: "删除索引。"
weight: 1130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-index.md"
---

## 概要 {#synopsis}

```sql
DROP INDEX [ CONCURRENTLY ] [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP INDEX` 从数据库系统中删除现有索引。必须是索引的所有者才能运行此命令。

## 参数 {#parameters}

**`CONCURRENTLY`**

删除索引时，不阻止对索引所属表的并发查询、插入、更新和删除。普通 `DROP INDEX` 会在表上获取 `ACCESS EXCLUSIVE` 锁，阻塞其他访问，直到索引能够删除。使用此选项时，命令会改为等待冲突事务完成。

使用此选项时有几点需要注意：只能指定一个索引名，且不支持 `CASCADE` 选项。（因此，不能以这种方式删除支撑 `UNIQUE` 或 `PRIMARY KEY` 约束的索引。）另外，普通 `DROP INDEX` 命令可在事务块中执行，但 `DROP INDEX CONCURRENTLY` 不行。

**`IF EXISTS`**

如果索引不存在，不报错，而是发出一条提示。

**`name`**

要删除的索引名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此索引的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此索引，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除索引 `title_idx`：

```sql
DROP INDEX title_idx;
```

## 兼容性 {#compatibility}

`DROP INDEX` 是 Apache Cloudberry 的语言扩展。SQL 标准没有规定索引。

## 另见 {#see-also}

[`ALTER INDEX`](/cloudberry/reference/sql-stmts/alter-index/), [`CREATE INDEX`](/cloudberry/reference/sql-stmts/create-index/)
