---
title: "DROP SERVER"
description: "删除外部服务器描述符。"
weight: 1300
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-server.md"
---

## 概要 {#synopsis}

```sql
DROP SERVER [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP SERVER` 删除现有外部服务器描述符。运行此命令的用户必须是该服务器的所有者。

## 参数 {#parameters}

**`IF EXISTS`**

如果服务器不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有服务器的名称。

**`CASCADE`**

自动删除依赖此服务器的对象（例如用户映射），以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此服务器，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除名为 `foo` 的服务器（如果存在）：

```sql
DROP SERVER IF EXISTS foo;
```

## 兼容性 {#compatibility}

`DROP SERVER` 符合 ISO/IEC 9075-9（SQL/MED）。`IF EXISTS` 子句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/), [ALTER SERVER](/cloudberry/reference/sql-stmts/alter-server/)
