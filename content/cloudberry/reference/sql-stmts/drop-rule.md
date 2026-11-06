---
title: "DROP RULE"
description: "Removes a rewrite rule."
weight: 1270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-rule.md"
---

## Synopsis {#synopsis}

```sql
DROP RULE [IF EXISTS] <name> ON <table_name> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP RULE` drops a rewrite rule from a table or view.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the rule does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name of the rule to remove.

**`table_name`**

The name (optionally schema-qualified) of the table or view that the rule applies to.

**`CASCADE`**

Automatically drop objects that depend on the rule, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the rule if any objects depend on it. This is the default.

## Examples {#examples}

Remove the rewrite rule `sales_2006` on the table `sales`:

```sql
DROP RULE sales_2006 ON sales;
```

## Compatibility {#compatibility}

`DROP RULE` is a Apache Cloudberry extension, as is the entire query rewrite system.

## See also {#see-also}

[`ALTER RULE`](/cloudberry/reference/sql-stmts/alter-rule/), [`CREATE RULE`](/cloudberry/reference/sql-stmts/create-rule/)
