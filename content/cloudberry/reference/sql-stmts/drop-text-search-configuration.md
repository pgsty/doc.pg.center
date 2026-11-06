---
title: "DROP TEXT SEARCH CONFIGURATION"
description: "Removes a text search configuration."
weight: 1340
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-configuration.md"
---

## Synopsis {#synopsis}

```sql
DROP TEXT SEARCH CONFIGURATION [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP TEXT SEARCH CONFIGURATION` drops an existing text search configuration. You must be the owner of the configuration to run this command.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the text search configuration does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of an existing text search configuration.

**`CASCADE`**

Automatically drop objects that depend on the text search configuration, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the text search configuration if any objects depend on it. This is the default.

## Examples {#examples}

Remove the text search configuration `my_english`:

```sql
DROP TEXT SEARCH CONFIGURATION my_english;
```

This command will not succeed if there are any existing indexes that reference the configuration in `to_tsvector` calls. Add `CASCADE` to drop such indexes along with the text search configuration.

## Compatibility {#compatibility}

There is no `DROP TEXT SEARCH CONFIGURATION` statement in the SQL standard.

## See also {#see-also}

[ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/), [CREATE TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/create-text-search-configuration/)
