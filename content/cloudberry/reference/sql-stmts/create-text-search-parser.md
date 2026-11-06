---
title: "CREATE TEXT SEARCH PARSER"
weight: 870
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-text-search-parser.md"
---

## Description {#description}

Defines a new text search parser.

## Synopsis {#synopsis}

```sql
CREATE TEXT SEARCH PARSER <name> (
    START = <start_function> ,
    GETTOKEN = <gettoken_function> ,
    END = <end_function> ,
    LEXTYPES = <lextypes_function>
    [, HEADLINE = <headline_function> ]
)
```

## Description {#description-1}

`CREATE TEXT SEARCH PARSER` creates a new text search parser. A text search parser defines a method for splitting a text string into tokens and assigning types (categories) to the tokens. A parser is not particularly useful by itself, but must be bound into a text search configuration along with some text search dictionaries to be used for searching.

If a schema name is given then the text search parser is created in the specified schema. Otherwise it is created in the current schema.

You must be a superuser to use `CREATE TEXT SEARCH PARSER`. (This restriction is made because an erroneous text search parser definition could confuse or even crash the server.)

## Parameters {#parameters}

**`name`**

The name of the text search parser to be created. The name can be schema-qualified.

**`start_function`**

The name of the start function for the parser.

**`gettoken_function`**

The name of the get-next-token function for the parser.

**`end_function`**

The name of the end function for the parser.

**`lextypes_function`**

The name of the lextypes function for the parser (a function that returns information about the set of token types it produces).

**`headline_function`**

The name of the headline function for the parser (a function that summarizes a set of tokens).

The function names can be schema-qualified if necessary. Argument types are not given, since the argument list for each type of function is predetermined. All except the headline function are required.

The arguments can appear in any order, not only the one shown above.

## Compatibility {#compatibility}

There is no `CREATE TEXT SEARCH PARSER` statement in the SQL standard.

## See also {#see-also}

[ALTER TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/alter-text-search-parser/), [DROP TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/drop-text-search-parser/)
