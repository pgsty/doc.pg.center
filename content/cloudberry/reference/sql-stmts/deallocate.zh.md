---
title: "DEALLOCATE"
description: "释放预备语句。"
weight: 950
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/deallocate.md"
---

## 概要 {#synopsis}

```sql
DEALLOCATE [PREPARE] { <name> | ALL }
```

## 描述 {#description}

`DEALLOCATE` 用于释放先前准备的 SQL 语句。如果未显式释放预备语句，它会在会话结束时释放。

关于预备语句的更多信息，见 [PREPARE](/cloudberry/reference/sql-stmts/prepare/)。

## 参数 {#parameters}

**`PREPARE`**

可选关键字，会被忽略。

**`name`**

要释放的预备语句名称。

**`ALL`**

释放所有预备语句。

## 示例 {#examples}

释放先前准备的、名为 `insert_names` 的语句：

```sql
DEALLOCATE insert_names;
```

## 兼容性 {#compatibility}

SQL 标准包含 `DEALLOCATE` 语句，但仅用于嵌入式 SQL。

## 另见 {#see-also}

[EXECUTE](/cloudberry/reference/sql-stmts/execute/), [PREPARE](/cloudberry/reference/sql-stmts/prepare/)
