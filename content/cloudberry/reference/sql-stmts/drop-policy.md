---
title: "DROP POLICY"
description: "Removes a row-level security policy from a table."
weight: 1200
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-policy.md"
---

## Synopsis {#synopsis}

```sql
DROP POLICY [ IF EXISTS ] <name> ON <table_name> [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP POLICY` removes the specified policy from the table. Note that if the last policy is removed for a table and the table still has row-level security enabled via `ALTER TABLE`, then the default-deny policy will be used. `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` can be used to disable row-level security for a table, whether policies for the table exist or not.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the policy does not exist. A notice is issued in this case.

**`name`**

The name of the policy to drop.

**`table_name`**

The name (optionally schema-qualified) of the table that the policy is on.

CASCADE
**`RESTRICT`**

These key words have no effect, since there are no dependencies on policies.

## Examples {#examples}

To drop the policy called `p1` on the table named `my_table`:

```sql
DROP POLICY p1 ON my_table;
```

## Compatibility {#compatibility}

`DROP POLICY` is a Apache Cloudberry extension to the SQL standard.

## See also {#see-also}

[CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/), [ALTER POLICY](/cloudberry/reference/sql-stmts/alter-policy/)
