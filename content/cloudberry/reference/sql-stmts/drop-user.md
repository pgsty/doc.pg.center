---
title: "DROP USER"
description: "Removes a database role."
weight: 1420
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-user.md"
---

## Synopsis {#synopsis}

```sql
DROP USER [IF EXISTS] <name> [, ...]
```

## Description {#description}

`DROP USER` is an alias for [`DROP ROLE`](/cloudberry/reference/sql-stmts/drop-role/).

## Compatibility {#compatibility}

The `DROP USER` statement is a Apache Cloudberry extension. The SQL standard leaves the definition of users to the implementation.

## See also {#see-also}

[`DROP ROLE`](/cloudberry/reference/sql-stmts/drop-role/)
