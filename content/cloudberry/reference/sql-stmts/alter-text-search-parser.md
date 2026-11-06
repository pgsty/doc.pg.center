---
title: "ALTER TEXT SEARCH PARSER"
description: "Change the definition of a text search parser with ALTER TEXT SEARCH PARSER."
weight: 360
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-text-search-parser.md"
---

## Description {#description}

Changes the definition of a text search parser.

## Synopsis {#synopsis}

```sql
ALTER TEXT SEARCH PARSER <name> RENAME TO <new_name>
ALTER TEXT SEARCH PARSER <name> SET SCHEMA <new_schema>
```

## Description {#description-1}

`ALTER TEXT SEARCH PARSER` changes the definition of a text search parser. Currently, the only supported functionality is to change the parser's name.

You must be a superuser to use `ALTER TEXT SEARCH PARSER`.

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of an existing text search parser.

**`new_name`**

The new name of the text search parser.

**`new_schema`**

The new schema for the text search parser.

## Compatibility {#compatibility}

There is no `ALTER TEXT SEARCH PARSER` statement in the SQL standard.

## See also {#see-also}

[CREATE TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/create-text-search-parser/), [DROP TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/drop-text-search-parser/)
