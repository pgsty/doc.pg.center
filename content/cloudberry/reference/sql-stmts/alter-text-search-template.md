---
title: "ALTER TEXT SEARCH TEMPLATE"
description: "Change the definition of a text search template with ALTER TEXT SEARCH TEMPLATE."
weight: 370
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-text-search-template.md"
---

## Description {#description}

Changes the definition of a text search template.

## Synopsis {#synopsis}

```sql
ALTER TEXT SEARCH TEMPLATE <name> RENAME TO <new_name>
ALTER TEXT SEARCH TEMPLATE <name> SET SCHEMA <new_schema>
```

## Description {#description-1}

`ALTER TEXT SEARCH TEMPLATE` changes the definition of a text search parser. Currently, the only supported functionality is to change the template's name.

You must be a superuser to use `ALTER TEXT SEARCH TEMPLATE`.

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of an existing text search template.

**`new_name`**

The new name of the text search template.

**`new_schema`**

The new schema for the text search template.

## Compatibility {#compatibility}

There is no `ALTER TEXT SEARCH TEMPLATE` statement in the SQL standard.

## See also {#see-also}

[CREATE TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/create-text-search-template/), [DROP TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/drop-text-search-template/)
