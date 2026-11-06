---
title: "ALTER RULE"
description: "Changes the definition of a rule."
weight: 270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-rule.md"
---

## Synopsis {#synopsis}

```sql
ALTER RULE name ON <table_name> RENAME TO <new_name>
```

## Description {#description}

`ALTER RULE` changes properties of an existing rule. Currently, the only available action is to change the rule's name.

To use `ALTER RULE`, you must own the table or view that the rule applies to.

## Parameters {#parameters}

**`name`**

The name of an existing rule to alter.

**`table_name`**

The name (optionally schema-qualified) of the table or view that the rule applies to.

**`new_name`**

The new name for the rule.

## Examples {#examples}

To rename an existing rule:

```sql
ALTER RULE notify_all ON emp RENAME TO notify_me; 
```

## Compatibility {#compatibility}

`ALTER RULE` is a Apache Cloudberry extension, as is the entire query rewrite system.

## See also {#see-also}

[`CREATE RULE`](/cloudberry/reference/sql-stmts/create-rule/), [`DROP RULE`](/cloudberry/reference/sql-stmts/drop-rule/)
