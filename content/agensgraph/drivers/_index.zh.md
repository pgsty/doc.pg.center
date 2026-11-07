---
title: 驱动与客户端库
linkTitle: 驱动与客户端库
description: 通过 PostgreSQL 驱动、Python 驱动和 AI 集成包连接 AgensGraph。
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/drivers/index.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
cascade:
  type: docs
no_list: true
translation_status: complete
---


- [AI 与 LLM 集成](/zh/agensgraph/drivers/ai-integrations/)

AgensGraph 使用 PostgreSQL 线协议，因此**任何 PostgreSQL 驱动都能连接它并运行 Cypher**——从协议角度看，Cypher 语句只是一条语句。使用 AgensGraph 不需要图专用客户端。

驱动没有帮助时无法解码的是图类型。返回 `m.title` 的查询交回每个驱动都理解的 `jsonb`；返回 `m` 的查询交回 `vertex`，路径模式中的 `p` 则交回 `graphpath`。原生 PostgreSQL 驱动会把它们视为文本。为 AgensGraph 编写的驱动增加了类型处理，因此顶点会作为带有标签、id 和属性的对象到达。

这带来两种工作方式：

**使用你已有的 PostgreSQL 驱动。** 返回属性而不是整个元素，并在需要普通标量而不是 `jsonb` 的地方把 Cypher 包在 SQL 中——参见[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。这是代码和依赖最少的路线；除 Python 之外的任何语言，都应选择它。

**需要把顶点、边和路径作为原生对象，或要基于某个 AI 集成构建时，使用 Python 驱动。**

## Python 驱动 {#the-python-driver}

[AgensGraph for Python](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/python/) 是适合用来构建的驱动。它在 psycopg 3 之上增加了图类型处理，所有 [AI 集成](/zh/agensgraph/drivers/ai-integrations/)都运行在它之上。它的手册包含安装和用法。

LangChain、LlamaIndex、LightRAG、cognee 和 MCP 服务器都位于这个驱动之上。参见 [AI 与 LLM 集成](/zh/agensgraph/drivers/ai-integrations/)。

## 其他语言 {#other-languages}

Java、Node.js 和 Go 请使用原生 PostgreSQL 驱动——pgjdbc、node-postgres 或 pgx——并按上文读取属性而不是整个元素。这是当前适合作为基础的组合。

这三种语言的驱动确实存在，但每一个都保留给已经在使用它的项目，而不是新的起点：

- [Java / JDBC](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/jdbc/) **legacy**——pgjdbc 的分支，2023 年 1 月以 `net.bitnine:agensgraph-jdbc:1.4.3` 发布。
- [Node.js](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/nodejs/) **legacy**——包装 node-postgres，要求 `pg >= 6.1.2`。2025 年 9 月作为 `@skaiworldwide/ag-driver` 1.1.0 发布。
- [Go](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/go/) **legacy**——构建在 `lib/pq` 上，以 Go module 形式分发，标签为 `v0.1.1`。

## 连接与参数 {#connection-and-parameters}

**在连接上设置 `graph_path`。** 它是会话级设置，因此连接池中的连接每次交出时都需要设置；也可以为角色或数据库设置一次：

``` sql
ALTER ROLE appuser SET graph_path = moviekb;
```

Python 驱动的 `ConnectionPool` 接受 `graph=` 参数，并在它打开的每个连接上设置一次，而不是每次交出时重复设置。因此，借用者如果修改 `graph_path` 并提交，会把修改传给下一个借用者。

**给 Cypher 参数指定类型。** 驱动未指定类型的参数会被解析为 JSON，因此普通字符串会失败：

```
ERROR:  invalid input syntax for type json
DETAIL:  Token "The" is invalid.
CONTEXT:  JSON data, line 1: The...
```

可以通过驱动 API 声明参数类型，或者在语句中转换：

```
MATCH (m:movie {title: $1::text}) RETURN m.year;
```

转换是可移植形式，而且没有代价。在一个值可能被两种方式解读时，它最重要：没有类型时，`'123'` 会作为*数字* 123 到达，不再匹配保存字符串 `"123"` 的属性。

Python 驱动会替你声明类型。从 2.0 版开始，它把 Python `str` 作为 `text` 发送，因此字符串参数在那里不需要转换。如果语句要从字符串得到其他类型，例如 `%s::date`，仍然需要转换。
