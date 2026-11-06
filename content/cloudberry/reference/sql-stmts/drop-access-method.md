---
title: "DROP ACCESS METHOD"
description: "Removes an access method"
weight: 1000
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-access-method.md"
---

## Synopsis {#synopsis}

```sql
DROP ACCESS METHOD [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP ACCESS METHOD` removes an existing access method. Only superusers can drop access methods.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the access method does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name of an existing access method.

**`CASCADE`**

Automatically drop objects that depend on the access method (such as operator classes, operator families, and indexes), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the access method if any objects depend on it. This is the default.

## Examples {#examples}

Drop the access method `heptree`;

``` sql
DROP ACCESS METHOD heptree;
```

## Compatibility {#compatibility}

`DROP ACCESS METHOD` is a Apache Cloudberry extension.

## See also {#see-also}

[CREATE ACCESS METHOD](/cloudberry/reference/sql-stmts/create-access-method/)
