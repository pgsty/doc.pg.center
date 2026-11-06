---
title: "DROP CAST"
description: "Removes a cast."
weight: 1020
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-cast.md"
---

## Synopsis {#synopsis}

```sql
DROP CAST [IF EXISTS] (<sourcetype> AS <targettype>) [CASCADE | RESTRICT]
```

## Description {#description}

`DROP CAST` will delete a previously defined cast. To be able to drop a cast, you must own the source or the target data type. These are the same privileges that are required to create a cast.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the cast does not exist. A notice is issued in this case.

**`sourcetype`**

The name of the source data type of the cast.

**`targettype`**

The name of the target data type of the cast.

CASCADE
**`RESTRICT`**

These keywords have no effect since there are no dependencies on casts.

## Examples {#examples}

To drop the cast from type `text` to type `int`:

```sql
DROP CAST (text AS int);
```

## Compatibility {#compatibility}

There `DROP CAST` command conforms to the SQL standard.

## See also {#see-also}

[CREATE CAST](/cloudberry/reference/sql-stmts/create-cast/)
