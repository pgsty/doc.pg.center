---
title: "DROP TEXT SEARCH PARSER"
description: "Remove a text search parser and control dependent objects with DROP TEXT SEARCH PARSER."
weight: 1360
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-parser.md"
---

## Description {#description}

Removes a text search parser.

## Synopsis {#synopsis}

```sql
DROP TEXT SEARCH PARSER [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Description {#description-1}

`DROP TEXT SEARCH PARSER` drops an existing text search parser. You must be a superuser to use this command.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the text search parser does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of an existing text search parser.

**`CASCADE`**

Automatically drop objects that depend on the text search parser, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the text search parser if any objects depend on it. This is the default.

## Examples {#examples}

Remove the text search parser `my_parser`:

```sql
DROP TEXT SEARCH PARSER my_parser;
```

This command will not succeed if there are any existing text search configurations that use the parser. Add `CASCADE` to drop such configurations along with the parser.

## Compatibility {#compatibility}

There is no `DROP TEXT SEARCH PARSER` statement in the SQL standard.

## See also {#see-also}

[ALTER TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/alter-text-search-parser/), [CREATE TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/create-text-search-parser/)
