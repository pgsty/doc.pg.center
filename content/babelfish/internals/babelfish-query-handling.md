---
title: Babelfish query handling
linkTitle: Query handling
description: How the pltsql parser processes, executes, and materializes T-SQL queries.
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/babelfish-query-handling.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Babelfish query handling {#babelfish-query-handling}

Microsoft SQL Server and PostgreSQL handle queries quite 
differently. Babelfish utilizes protocol hooks and provides software
mechanisms that allow you to refine and influence how your queries are processed.


### Processing a query {#processing-a-query}

T-SQL has many syntactic differences from the version of SQL spoken by PostgreSQL. To 
accept queries written in T-SQL, Babelfish utilizes a parser that is distributed in 
the `pltsql` extension. 

Once a client has sent a query to Babelfish via the TDS protocol, parser hooks in the <code>pltsql</code> 
extension are employed to parse, analyze, and execute the query. The extension provides the proper datatype 
conversion from PostgreSQL types to TDS wire types. By taking this approach, processing, executing, 
and materializing query results are handled by the extension only, and we don't need to extend the 
PostgreSQL SQL parser to understand T-SQL and its semantics at all.
