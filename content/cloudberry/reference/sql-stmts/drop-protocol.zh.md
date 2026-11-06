---
title: "DROP PROTOCOL"
description: "从数据库中删除数据访问协议。"
weight: 1220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-protocol.md"
---

## 概要 {#synopsis}

```sql
DROP PROTOCOL [IF EXISTS] <name>
```

## 描述 {#description}

`DROP PROTOCOL` 从数据库中删除指定协议。在 `CREATE EXTERNAL TABLE` 命令中指定协议名，可以从外部数据源读取数据或向其中写入数据。

必须是超级用户或协议所有者才能删除协议。

> **注意** 如果删除数据访问协议，使用该协议定义的外部表将无法再访问外部数据源。

## 参数 {#parameters}

**`IF EXISTS`**

如果协议不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有数据访问协议的名称。

## 注意事项 {#notes}

删除数据访问协议不会删除该协议的调用处理函数。必须手动删除这些函数。

请务必从 Apache Cloudberry 主机中删除该协议使用的共享库。

## 兼容性 {#compatibility}

`DROP PROTOCOL` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/), [CREATE PROTOCOL](/cloudberry/reference/sql-stmts/create-protocol/)
