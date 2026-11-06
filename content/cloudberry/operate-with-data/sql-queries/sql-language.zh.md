---
title: "SQL 语言"
description: "本文介绍 Apache Cloudberry 所使用 SQL 的基础要素。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/sql-language.md"
---

定义查询时，理解这些要素至关重要，因为它们构成查询语句的基本构件。

## SQL 词法 {#sql-lexicon}

SQL 是一种用于访问数据库的标准语言。该语言由一系列要素组成，可以执行数据存储、检索、分析、查看、操作等任务。可以使用 SQL 命令构造 Apache Cloudberry 引擎能够理解的查询和命令。SQL 查询由一系列命令组成。命令由按正确语法顺序排列的一系列有效词元组成，并以分号（`;`）结束。

Apache Cloudberry 使用 PostgreSQL 的结构和语法，但存在一些例外。有关 PostgreSQL 中 SQL 规则和概念的更多信息，请参见 PostgreSQL 文档中的“SQL 语法”。

## SQL 值表达式 {#sql-value-expressions}

SQL 值表达式由一个或多个值、符号、操作符、SQL 函数和数据组成。这些表达式比较数据或执行计算，并将一个值作为结果返回。计算包括逻辑运算、算术运算和集合运算。

以下是值表达式：

- 聚合表达式
- 数组构造器
- 列引用
- 常量或字面量值
- 相关子查询
- 字段选择表达式
- 函数调用
- `INSERT` 或 `UPDATE` 中的新列值
- 操作符调用的列引用
- 位置参数引用，位于函数定义体或预备语句中
- 行构造器
- 标量子查询
- `WHERE` 子句中的搜索条件
- `SELECT` 命令的目标列表
- 类型转换
- 括号中的值表达式，可用于对子表达式分组并覆盖优先级
- 窗口表达式

函数和操作符等 SQL 构造也是表达式，但不遵循通用的语法规则。有关这些构造的更多信息，请参见[使用函数和操作符](/cloudberry/reference/functions/)。
