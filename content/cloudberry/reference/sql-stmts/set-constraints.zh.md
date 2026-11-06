---
title: "SET CONSTRAINTS"
description: "设置当前事务的约束检查时机。"
weight: 1690
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/set-constraints.md"
---

> **注意** 接受引用完整性语法（外键约束），但不强制执行。

## 语法概要 {#synopsis}

```sql
SET CONSTRAINTS { ALL | <name> [, ...] } { DEFERRED | IMMEDIATE }
```

## 说明 {#description}

`SET CONSTRAINTS` 设置当前事务内约束检查的行为。`IMMEDIATE` 约束在每条语句结束时检查。`DEFERRED` 约束直到事务提交时才检查。每个约束都有自己的 `IMMEDIATE` 或 `DEFERRED` 模式。

创建约束时，会赋予其以下三种特性之一：`DEFERRABLE INITIALLY DEFERRED`、`DEFERRABLE INITIALLY IMMEDIATE` 或 `NOT DEFERRABLE`。第三类始终为 `IMMEDIATE`，不受 `SET CONSTRAINTS` 命令影响。前两类在每个事务开始时采用指定的模式，但可以在事务内通过 `SET CONSTRAINTS` 更改其行为。

带有约束名称列表的 `SET CONSTRAINTS` 只更改这些约束的模式（它们必须都可延迟）。每个约束名称都可以用模式名限定。如果未指定模式名，则使用当前模式搜索路径查找第一个匹配的名称。`SET CONSTRAINTS ALL` 更改所有可延迟约束的模式。

当 `SET CONSTRAINTS` 将约束模式从 `DEFERRED` 改为 `IMMEDIATE` 时，新模式会追溯生效：原本要在事务结束时检查的所有尚未检查的数据修改，都会在执行 `SET CONSTRAINTS` 命令期间检查。如果违反了任何此类约束，`SET CONSTRAINTS` 就会失败（并且不更改约束模式）。因此，可以用 `SET CONSTRAINTS` 强制在事务内的某个特定时点检查约束。

目前，只有 `UNIQUE`、`PRIMARY KEY`、`REFERENCES`（外键）和 `EXCLUDE` 约束受此设置影响。`NOT NULL` 和 `CHECK` 约束总是在插入或修改行时立即检查（*不是*在语句结束时）。未声明为 `DEFERRABLE` 的唯一约束和排除约束也会立即检查。

声明为“约束触发器”的触发器的触发时机也受此设置控制：它们会在关联约束应当被检查时触发。

## 注意事项 {#notes}

由于 Apache Cloudberry 不要求约束名称在模式内唯一（只要求在表内唯一），指定的约束名称可能匹配多个约束。在这种情况下，`SET CONSTRAINTS` 会作用于所有匹配项。对于不带模式限定的名称，一旦在搜索路径中的某个模式内找到一个或多个匹配项，就不再搜索路径中后续的模式。

此命令仅更改当前事务内约束的行为。在事务块之外执行此命令会发出警告，除此之外没有任何效果。

## 兼容性 {#compatibility}

此命令遵循 SQL 标准定义的行为，但有一项限制：在 Apache Cloudberry 中，它不适用于 `NOT NULL` 和 `CHECK` 约束。此外，Apache Cloudberry 会立即检查不可延迟的唯一约束，而不是按标准的规定在语句结束时检查。
