---
title: AgensGraph documentation
linkTitle: AgensGraph
description: 'The AgensGraph 2.18.6.1 manual: start with a graph, query it, search it, and operate it.'
type: docs
weight: -30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/index.html
upstream_source: agensgraph
upstream_modified: true
sidebar_root_for: self
sidebar_root_link_self: true
cascade:
  type: docs
  upstream_source: agensgraph
no_list: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
icon: fa-solid fa-diagram-project
---


AgensGraph is an open-source multi-model database built on PostgreSQL, developed and maintained by [SKAI Worldwide](https://skaiworldwide.com/) (formerly Bitnine) under the Apache License 2.0. It stores your data as a **property graph** and as relational tables at the same time. You query that data in **Cypher**, in **GQL** (ISO/IEC 39075), or in **SQL**, and you can combine two of them in one statement when that is the shortest way to the answer.

This manual covers AgensGraph 2.18.6.1. Release 2.18 is built on PostgreSQL 18 and adds a substantial part of the GQL standard. [AgensGraph 2.18](/agensgraph/release-notes/2.18/) lists what changed, including the changes your application needs to know about.

## How this manual is organized {#how-this-manual-is-organized}

[Get Started](/agensgraph/get-started/) installs the server, loads the small film graph that every example in this manual uses, and gets you to a result. Read it first.

[Concepts](/agensgraph/concepts/) explains the property-graph model, and how a graph is laid out in PostgreSQL. A graph is a schema and a label is a table. That is what lets one statement mix graph and relational work.

[Querying](/agensgraph/querying/) teaches the language in the order you meet it: reading, writing, composing pipelines, walking paths, indexing, and crossing between SQL and Cypher.

[Reference](/agensgraph/reference/) is the formal definition of the same language — the lexical rules, the types, and a page for each clause, statement and function. Look here when you know what you want and need the exact syntax.

[Guides](/agensgraph/guides/) covers loading data and the search features. [Drivers and client libraries](/agensgraph/drivers/) points at the client libraries. [Operations](/agensgraph/operations/) is for running a server. [System Catalogs](/agensgraph/system-catalogs/) documents the catalogs that describe a graph, and [Appendixes](/agensgraph/appendix/) holds the GQL conformance tables, the compatibility notes, the keyword and error-code lists, and a map from the 2.17 page names to these.

## Contents {#contents}

- [Get Started](/agensgraph/get-started/)
- [Concepts](/agensgraph/concepts/)
- [Querying](/agensgraph/querying/)
- [Reference](/agensgraph/reference/)
- [Guides](/agensgraph/guides/)
- [Drivers and client libraries](/agensgraph/drivers/)
- [Operations](/agensgraph/operations/)
- [System Catalogs](/agensgraph/system-catalogs/)
- [Release Notes](/agensgraph/release-notes/)
- [Appendixes](/agensgraph/appendix/)

{.cards}
