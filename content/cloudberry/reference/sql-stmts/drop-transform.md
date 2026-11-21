---
title: "DROP TRANSFORM"
description: "Removes a transform."
weight: 1380
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sql-stmts/drop-transform.md"
---

## Synopsis {#synopsis}

```sql
DROP TRANSFORM [IF EXISTS] FOR <type_name> LANGUAGE <lang_name> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP TRANSFORM` removes a previously defined transform.

To drop a transform, you must own the type and the language. These are the same privileges that are required to create a transform.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the transform does not exist. Apache Cloudberry issues a notice in this case.

**`type_name`**

The name of the data type of the transform.

**`lang_name`**

The name of the language of the transform.

**`CASCADE`**

Automatically drop objects that depend on the transform, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the transform if any objects depend on it. This is the default.

## Examples {#examples}

To drop the transform for type `hstore` and language `plpython3u`:

``` sql
DROP TRANSFORM FOR hstore LANGUAGE plpython3u;
```

## Compatibility {#compatibility}

This form of `DROP TRANSFORM` is a Apache Cloudberry extension. See [CREATE TRANSFORM](/cloudberry/reference/sql-stmts/create-transform/) for details.

## See also {#see-also}

[CREATE TRANSFORM](/cloudberry/reference/sql-stmts/create-transform/)
