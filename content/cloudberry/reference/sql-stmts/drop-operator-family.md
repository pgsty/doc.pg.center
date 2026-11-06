---
title: "DROP OPERATOR FAMILY"
description: "Removes an operator family."
weight: 1170
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-operator-family.md"
---

## Synopsis {#synopsis}

```sql
DROP OPERATOR FAMILY [IF EXISTS] <name> USING <index_method> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP OPERATOR FAMILY` drops an existing operator family. To run this command you must be the owner of the operator family.

`DROP OPERATOR FAMILY` includes dropping any operator classes contained in the family, but it does not drop any of the operators or functions referenced by the family. If there are any indexes depending on operator classes within the family, you will need to specify `CASCADE` for the drop to complete.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the operator family does not exist. A notice is issued in this case.

**`name`**

The name (optionally schema-qualified) of an existing operator family.

**`index_method`**

The name of the index access method the operator family is for.

**`CASCADE`**

Automatically drop objects that depend on the operator family, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the operator family if any objects depend on it. This is the default.

## Examples {#examples}

Remove the B-tree operator family `float_ops`:

```sql
DROP OPERATOR FAMILY float_ops USING btree;
```

This command will not succeed if there are any existing indexes that use the operator family. Add `CASCADE` to drop such indexes along with the operator family.

## Compatibility {#compatibility}

There is no `DROP OPERATOR FAMILY` statement in the SQL standard.

## See also {#see-also}

[ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/), [CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/), [ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/), [CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/), [DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/)
