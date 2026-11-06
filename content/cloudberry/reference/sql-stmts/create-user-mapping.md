---
title: "CREATE USER MAPPING"
description: "Defines a new mapping of a user to a foreign server."
weight: 920
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-user-mapping.md"
---

## Synopsis {#synopsis}

```sql
CREATE USER MAPPING [ IF NOT EXISTS ] FOR { <user_name> | USER | CURRENT_USER | PUBLIC }
    SERVER <server_name>
    [ OPTIONS ( <option> '<value>' [, ... ] ) ]
```

## Description {#description}

`CREATE USER MAPPING` defines a mapping of a user to a foreign server. A user mapping typically encapsulates connection information that a foreign-data wrapper uses together with the information encapsulated by a foreign server to access an external data resource.

The owner of a foreign server can create user mappings for that server for any user. Also, a user can create a user mapping for their own user name if they have been granted `USAGE` privilege on the server.

## Parameters {#parameters}

**`IF NOT EXISTS`**

Do not throw an error if a mapping of the given user to the given foreign server already exists. Apache Cloudberry issues a notice in this case. Note that there is no guarantee that the existing user mapping is anything like the one that would have been created.

**`user_name`**

The name of an existing user that is mapped to the foreign server. `CURRENT_USER` and `USER` match the name of the current user. When `PUBLIC` is specified, Apache Cloudberry creates a so-called public mapping that is used when no user-specific mapping is applicable.

**`server_name`**

The name of an existing server for which Apache Cloudberry is to create the user mapping.

**`OPTIONS ( option 'value' [, ... ] )`**

The options for the new user mapping. The options typically define the actual user name and password of the mapping. Option names must be unique. The option names and values are specific to the server's foreign-data wrapper.

## Examples {#examples}

Create a user mapping for user `bob`, server `foo`:

```sql
CREATE USER MAPPING FOR bob SERVER foo OPTIONS (user 'bob', password 'secret');
```

## Compatibility {#compatibility}

`CREATE USER MAPPING` conforms to ISO/IEC 9075-9 (SQL/MED).

## See also {#see-also}

[ALTER USER MAPPING](/cloudberry/reference/sql-stmts/alter-user-mapping/), [DROP USER MAPPING](/cloudberry/reference/sql-stmts/drop-user-mapping/), [CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/), [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/)
