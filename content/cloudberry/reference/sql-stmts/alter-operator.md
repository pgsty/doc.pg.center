---
title: "ALTER OPERATOR"
description: "Changes the definition of an operator."
weight: 190
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-operator.md"
---

## Synopsis {#synopsis}

```sql
ALTER OPERATOR <name> ( {<left_type> | NONE} , {<right_type> | NONE} ) 
   OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER OPERATOR <name> ( {<left_type> | NONE} , {<right_type> | NONE} ) 
    SET SCHEMA <new_schema>

ALTER OPERATOR name ( { <left_type> | NONE } , { <right_type> | NONE } )
    SET ( {  RESTRICT = { <res_proc> | NONE }
           | JOIN = { <join_proc> | NONE }
         } [, ... ] )
```

## Description {#description}

`ALTER OPERATOR` changes the definition of an operator.

You must own the operator to use `ALTER OPERATOR`. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the operator's schema. (These restrictions enforce that altering the owner does not do anything you could not do by dropping and recreating the operator. However, a superuser can alter ownership of any operator anyway.)

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of an existing operator.

**`left_type`**

The data type of the operator's left operand; write `NONE` if the operator has no left operand.

**`right_type`**

The data type of the operator's right operand; write `NONE` if the operator has no right operand.

**`new_owner`**

The new owner of the operator.

**`new_schema`**

The new schema for the operator.

**`res_proc`**

The restriction selectivity estimator function for this operator; write `NONE` to remove the existing selectivity estimator.

**`join_proc`**

The join selectivity estimator function for this operator; write `NONE` to remove the existing selectivity estimator.

## Examples {#examples}

Change the owner of a custom operator `a @@ b` for type `text`:

```sql
ALTER OPERATOR @@ (text, text) OWNER TO joe;
```

Change the restriction and join selectivity estimator functions of a custom operator `a && b` for type `int[]`:

```sql
ALTER OPERATOR && (_int4, _int4) SET (RESTRICT = _int_contsel, JOIN = _int_contjoinsel);
```

## Compatibility {#compatibility}

There is no `ALTER OPERATOR` statement in the SQL standard.

## See also {#see-also}

[CREATE OPERATOR](/cloudberry/reference/sql-stmts/create-operator/), [DROP OPERATOR](/cloudberry/reference/sql-stmts/drop-operator/)
