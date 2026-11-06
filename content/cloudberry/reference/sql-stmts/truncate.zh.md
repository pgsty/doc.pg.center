---
title: "TRUNCATE"
description: "清空一个表或一组表中的所有行。"
weight: 1760
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/truncate.md"
---

> [!NOTE]
> Apache Cloudberry 不强制执行引用完整性语法（外键约束）。即使省略 `CASCADE` 选项，`TRUNCATE` 也会截断外键约束所引用的表。

## 语法概要 {#synopsis}

```sql
TRUNCATE [TABLE] [ONLY] <name> [ * ] [, ...] 
    [ RESTART IDENTITY | CONTINUE IDENTITY ] [CASCADE | RESTRICT]
```

## 说明 {#description}

`TRUNCATE` 快速移除一个表或一组表中的所有行。其效果与对每个表执行不带限定条件的 [`DELETE`](/cloudberry/reference/sql-stmts/delete/) 相同，但由于不实际扫描表，速度更快。此外，它会立即回收磁盘空间，无需随后再执行 [`VACUUM`](/cloudberry/reference/sql-stmts/vacuum/)。这对大表尤其有用。

必须具有表的 `TRUNCATE` 权限才能截断该表。

## 参数 {#parameters}

**`name`**

要截断的表的名称（可以用模式名限定）。如果在表名前指定 `ONLY`，则只截断该表。如果未指定 `ONLY`，则截断该表及其所有后代表（如果有）。也可以在表名后指定 `*`，明确表示包含后代表。

**`RESTART IDENTITY`**

自动重启被截断表的列所拥有的序列。

**`CONTINUE IDENTITY`**

不更改序列的值。这是默认行为。

**`CASCADE`**

由于此关键字适用于外键引用（Apache Cloudberry 不支持），因此没有效果。

**`RESTRICT`**

由于此关键字适用于外键引用（Apache Cloudberry 不支持），因此没有效果。

## 注意事项 {#notes}

`TRUNCATE` 会对操作的每个表获取 `ACCESS EXCLUSIVE` 锁，阻塞该表上所有其他并发操作。指定 `RESTART IDENTITY` 时，要重启的任何序列也会被排他锁定。如果需要并发访问表，请改用 `DELETE` 命令。

`TRUNCATE` 不会触发表上可能存在的任何用户定义的 `ON DELETE` 触发器。

`TRUNCATE` 不会截断继承自指定表的任何表。只截断指定的表，不截断其子表。

`TRUNCATE` 不具备 MVCC 安全性。截断之后，如果并发事务使用的是截断发生之前获取的快照，则它们看到的表将为空。

就表中的数据而言，`TRUNCATE` 具有事务安全性：如果所在事务未提交，截断操作会安全地回滚。

指定 `RESTART IDENTITY` 时，隐含的 `ALTER SEQUENCE RESTART` 操作也会以事务方式执行；即如果所在事务未提交，这些操作也会回滚。请注意，如果在事务回滚之前对重启的序列执行了其他序列操作，这些操作对序列的影响也会回滚。

目前不支持对外表执行 `TRUNCATE`。这意味着，如果指定表的任何后代表是外表，该命令就会失败。

## 示例 {#examples}

清空表 `films` 和 `distributors`：

```sql
TRUNCATE films, distributors;
```

执行相同操作，并重置所有关联的序列生成器：

```sql
TRUNCATE films, distributors RESTART IDENTITY;
```

## 兼容性 {#compatibility}

SQL:2008 标准包含 `TRUNCATE` 命令，其语法为 `TRUNCATE TABLE tablename`。`CONTINUE IDENTITY`/`RESTART IDENTITY` 子句也出现在该标准中，但含义虽有关联，却略有不同。标准将此命令的部分并发行为留给实现自行定义，因此应考虑上述注意事项，并在必要时与其他实现比较。

## 另请参阅 {#see-also}

[`DELETE`](/cloudberry/reference/sql-stmts/delete/)
