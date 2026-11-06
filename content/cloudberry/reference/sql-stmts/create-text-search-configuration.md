---
title: "CREATE TEXT SEARCH CONFIGURATION"
description: "Defines a new text search configuration."
weight: 850
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-text-search-configuration.md"
---

## Synopsis {#synopsis}

```sql
CREATE TEXT SEARCH CONFIGURATION <name> (
    PARSER = <parser_name> |
    COPY = <source_config>
)
```

## Description {#description}

`CREATE TEXT SEARCH CONFIGURATION` creates a new text search configuration. A text search configuration specifies a text search parser that can divide a string into tokens, plus dictionaries that can be used to determine which tokens are of interest for searching.

If only the parser is specified, then the new text search configuration initially has no mappings from token types to dictionaries, and therefore will ignore all words. Subsequent [ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/) commands must be used to create mappings to make the configuration useful. Alternatively, an existing text search configuration can be copied.

If a schema name is provided then the text search configuration is created in the specified schema. Otherwise it is created in the current schema.

The user who defines a text search configuration becomes its owner.

## Parameters {#parameters}

**`name`**

The name of the text search configuration to be created. The name can be schema-qualified.

**`parser_name`**

The name of the text search parser to use for this configuration.

**`source_config`**

The name of an existing text search configuration to copy.

## Notes {#notes}

The `PARSER` and `COPY` options are mutually exclusive, because when an existing configuration is copied, its parser selection is copied too.

## Compatibility {#compatibility}

There is no `CREATE TEXT SEARCH CONFIGURATION` statement in the SQL standard.

## See also {#see-also}

[ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/), [DROP TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/drop-text-search-configuration/)
