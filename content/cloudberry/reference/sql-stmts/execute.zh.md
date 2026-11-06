---
title: "EXECUTE"
description: "执行预备 SQL 语句。"
weight: 1450
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/execute.md"
---

## 概要 {#synopsis}

```sql
EXECUTE <name> [ (<parameter> [, ...] ) ]
```

## 描述 {#description}

`EXECUTE` 用于执行先前准备的语句。由于预备语句只在会话期间存在，该语句必须由当前会话中先前执行的 `PREPARE` 语句创建。

如果用于创建该语句的 `PREPARE` 语句指定了参数，就必须向 `EXECUTE` 语句传递一组兼容的参数，否则 Apache Cloudberry 会报错。由于预备语句不像函数那样根据参数类型或数量进行重载，其名称在数据库会话中必须唯一。

关于预备语句的创建和使用，见 [PREPARE](/cloudberry/reference/sql-stmts/prepare/)。

## 参数 {#parameters}

**`name`**

要执行的预备语句名称。

**`parameter`**

预备语句参数的实际值。它必须是一个表达式，其结果值与创建预备语句时确定的该参数的数据类型兼容。

## 输出 {#outputs}

`EXECUTE` 返回的命令标签属于预备语句，而不是 `EXECUTE`。

## 示例 {#examples}

为 `INSERT` 语句创建预备语句，然后执行它：

```sql
PREPARE fooplan (int, text, bool, numeric) AS
    INSERT INTO foo VALUES($1, $2, $3, $4);
EXECUTE fooplan(1, 'Hunter Valley', 't', 200.00);
```

## 兼容性 {#compatibility}

SQL 标准包含 `EXECUTE` 语句，但仅用于嵌入式 SQL。此版本的 `EXECUTE` 语句所用语法也有所不同。

## 另见 {#see-also}

[DEALLOCATE](/cloudberry/reference/sql-stmts/deallocate/), [PREPARE](/cloudberry/reference/sql-stmts/prepare/)
