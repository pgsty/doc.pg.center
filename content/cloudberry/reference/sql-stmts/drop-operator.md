---
title: "DROP OPERATOR"
description: "Removes an operator."
weight: 1180
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-operator.md"
---

## Synopsis {#synopsis}

```sql
DROP OPERATOR [IF EXISTS] <name> ( {<left_type> | NONE} , 
    {<right_type> | NONE} ) [, ...] [CASCADE | RESTRICT]
```

## Description {#description}

`DROP OPERATOR` drops an existing operator from the database system. To run this command you must be the owner of the operator.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the operator does not exist. A notice is issued in this case.

**`name`**

The name (optionally schema-qualified) of an existing operator.

**`left_type`**

The data type of the operator's left operand; write `NONE` if the operator has no left operand.

**`right_type`**

The data type of the operator's right operand; write `NONE` if the operator has no right operand.

**`CASCADE`**

Automatically drop objects that depend on the operator (such as views using it), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the operator if any objects depend on it. This is the default.

## Examples {#examples}

Remove the power operator `a^b` for type `integer`:

```sql
DROP OPERATOR ^ (integer, integer);
```

Remove the left unary bitwise complement operator `~b` for type `bit`:

```sql
DROP OPERATOR ~ (none, bit);
```

Remove the right unary factorial operator `x!` for type `bigint`:

```sql
DROP OPERATOR ! (bigint, none);
```

Remove multiple operators in one command:

```sql
DROP OPERATOR ~ (none, bit), ! (bigint, none);
```

## Compatibility {#compatibility}

There is no `DROP OPERATOR` statement in the SQL standard.

## See also {#see-also}

[ALTER OPERATOR](/cloudberry/reference/sql-stmts/alter-operator/), [CREATE OPERATOR](/cloudberry/reference/sql-stmts/create-operator/)
