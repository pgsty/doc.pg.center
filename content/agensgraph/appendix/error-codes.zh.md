---
title: 错误码
linkTitle: 错误码
description: 与 PostgreSQL 一样，AgensGraph 服务端产生的每条消息都带有一个五个字符的 SQLSTATE 码。
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/error-codes.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


与 PostgreSQL 一样，AgensGraph 服务端产生的每条消息都带有一个五个字符的 SQLSTATE 码。前两个字符标示错误*类别*，后三个字符标示类别内的具体条件。因此，即使应用程序不认识某个码，仍可根据类别采取行动。

**AgensGraph 没有定义自己的错误码。**它的错误码表与 PostgreSQL 18 的逐字节相同；图语句失败时，抛出的是 PostgreSQL 既有错误码之一。包含 PL/pgSQL 为每个条件所用条件名的完整码表见 PostgreSQL 的 [Error Codes](https://www.postgresql.org/docs/18/errcodes-appendix.html) 附录，本文不重复。

对客户端而言，实际结果是图特有的失败不能靠错误码识别。`multiple types for relationship not supported` 和 `Cypher query must end with RETURN, FINISH or update clause` 分别以 `0A000` 和 `42601` 到达。这两个码也分别用于不受支持的 SQL 特性和 SQL 语法错误。需要区分它们时，请匹配消息文本，并把类别当作可靠部分。

## 读取错误码 {#reading-a-code}

在 `psql` 中运行 `\set VERBOSITY verbose`，之后每条错误都会带 SQLSTATE 和抛出它的源码位置：

```psql
\set VERBOSITY verbose
```

```cypher
MATCH (m:movie {year: 1999}) WHERE m.title RETURN count(m);
```

```
ERROR:  42846: cannot cast "The Matrix" (jsonb type string) to boolean
LOCATION:  ExecEvalCypherTypeCast, execExprInterp.c:5900
```

把 `VERBOSITY` 设为 `sqlstate` 会只打印错误码。在驱动中，错误码是错误对象的一个字段；大多数 PostgreSQL 客户端称之为 `sqlstate`。

## 图语句常见错误码 {#codes-a-graph-statement-commonly-raises}

下表列出图操作中应预期的错误码，并为每个码给出一条真实消息。条件名是 PL/pgSQL 和大多数驱动使用的名称。

| 码 | 条件名 | 例如由以下情况抛出 |
| --- | --- | --- |
| `0A000` | `feature_not_supported` | `multiple types for relationship not supported`——关系模式带有多个类型。 |
| `22023` | `invalid_parameter_value` | `labid out of range: 65536`——超出[限制](/zh/agensgraph/appendix/limits/)所列范围的 `graphid`。 |
| `3F000` | `invalid_schema_name` | `graph_path is NULL`——未设置工作图。图是模式，所以错误类别是这个。 |
| `42601` | `syntax_error` | `Cypher query must end with RETURN, FINISH or update clause`，以及所有解析失败。 |
| `42703` | `undefined_column` | `variable does not exist`——名称不在作用域内。 |
| `42712` | `duplicate_alias` | `WITH passes on "t" more than once`，以及其他名称冲突拒绝。 |
| `42846` | `cannot_coerce` | `cannot cast "…" (jsonb type string) to boolean`——条件的取值不是布尔值。 |
| `42P07` | `duplicate_table` | `label "movie" already exists`——标签是表，所以重复标签就是重复表。 |
| `54000` | `program_limit_exceeded` | `no more new labels are available`——图的标签 id 已耗尽。 |
| `55000` | `object_not_in_prerequisite_state` | `Vertex with connected edges cannot be removed`——`DELETE` 会留下悬空边。 |

其中三行说明了可预期的模式：图是模式，标签是表，属性是 `jsonb` 值。因此，图错误会归入它实际涉及的 PostgreSQL 对象所在类别。

## 另见 {#see-also}

- [Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/)——从其他 Cypher 实现移植的查询会遇到的错误及其文本
- [限制](/zh/agensgraph/appendix/limits/)——会产生 `22023` 和 `54000` 的两个限制
- [术语表](/zh/agensgraph/appendix/glossary/)——这些消息使用的术语
