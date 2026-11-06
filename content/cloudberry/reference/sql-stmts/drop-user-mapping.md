---
title: "DROP USER MAPPING"
description: "Removes a user mapping for a foreign server."
weight: 1410
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-user-mapping.md"
---

## Synopsis {#synopsis}

```sql
DROP USER MAPPING [ IF EXISTS ] { <user_name> | USER | CURRENT_USER | PUBLIC } 
    SERVER <server_name>
```

## Description {#description}

`DROP USER MAPPING` removes an existing user mapping from a foreign server.

The owner of a foreign server can drop user mappings for that server for any user. Also, a user can drop a user mapping for their own user name if they have been granted the `USAGE` privilege on the server.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the user mapping does not exist. Apache Cloudberry issues a notice in this case.

**`user_name`**

User name of the mapping. `CURRENT_USER` and `USER` match the name of the current user. `PUBLIC` is used to match all present and future user names in the system.

**`server_name`**

Server name of the user mapping.

## Examples {#examples}

Drop the user mapping named `bob`, server `foo` if it exists:

```sql
DROP USER MAPPING IF EXISTS FOR bob SERVER foo;
```

## Compatibility {#compatibility}

`DROP SERVER` conforms to ISO/IEC 9075-9 (SQL/MED). The `IF EXISTS` clause is a Apache Cloudberry extension.

## See also {#see-also}

[CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/), [ALTER USER MAPPING](/cloudberry/reference/sql-stmts/alter-user-mapping/)
