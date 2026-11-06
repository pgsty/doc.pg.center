---
title: "DROP USER"
description: "删除数据库角色。"
weight: 1420
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-user.md"
---

## 概要 {#synopsis}

```sql
DROP USER [IF EXISTS] <name> [, ...]
```

## 描述 {#description}

`DROP USER` 是 [`DROP ROLE`](/cloudberry/reference/sql-stmts/drop-role/) 的别名。

## 兼容性 {#compatibility}

`DROP USER` 语句是 Apache Cloudberry 的扩展。SQL 标准将用户定义留给实现自行规定。

## 另见 {#see-also}

[`DROP ROLE`](/cloudberry/reference/sql-stmts/drop-role/)
