---
title: "DROP TEXT SEARCH DICTIONARY"
description: "Removes a text search dictionary."
weight: 1350
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-dictionary.md"
---

## Synopsis {#synopsis}

```sql
DROP TEXT SEARCH DICTIONARY [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP TEXT SEARCH DICTIONARY` drops an existing text search dictionary. You must be the owner of the dictionary to run this command.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the text search dictionary does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of an existing text search dictionary.

**`CASCADE`**

Automatically drop objects that depend on the text search dictionary, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the text search dictionary if any objects depend on it. This is the default.

## Examples {#examples}

Remove the text search dictionary `english`:

```sql
DROP TEXT SEARCH DICTIONARY english;
```

This command will not succeed if there are any existing text search configurations that use the dictionary. Add `CASCADE` to drop such configurations along with the dictionary.

## Compatibility {#compatibility}

There is no `CREATE TEXT SEARCH DICTIONARY` statement in the SQL standard.

## See also {#see-also}

[ALTER TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/alter-text-search-dictionary/), [CREATE TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/create-text-search-dictionary/)
