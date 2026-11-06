---
title: "DROP TEXT SEARCH TEMPLATE"
description: "Remove a text search template and control dependent objects with DROP TEXT SEARCH TEMPLATE."
weight: 1370
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-template.md"
---

## Description {#description}

Removes a text search template.

## Synopsis {#synopsis}

```sql
DROP TEXT SEARCH TEMPLATE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Description {#description-1}

`DROP TEXT SEARCH TEMPLATE` drops an existing text search template. You must be a superuser to use this command.

You must be a superuser to use `ALTER TEXT SEARCH TEMPLATE`.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the text search template does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of an existing text search template.

**`CASCADE`**

Automatically drop objects that depend on the text search template, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the text search template if any objects depend on it. This is the default.

## Examples {#examples}

Remove the text search template `thesaurus`:

```sql
DROP TEXT SEARCH TEMPLATE thesaurus;
```

This command will not succeed if there are any existing text search dictionaries that use the template. Add `CASCADE` to drop such dictionaries along with the template.

## Compatibility {#compatibility}

There is no `DROP TEXT SEARCH TEMPLATE` statement in the SQL standard.

## See also {#see-also}

[ALTER TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/alter-text-search-template/), [CREATE TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/create-text-search-template/)
