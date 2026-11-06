---
title: "CREATE SERVER"
description: "Defines a new foreign server."
weight: 800
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-server.md"
---

## Synopsis {#synopsis}

```sql
CREATE SERVER [ IF NOT EXISTS ] <server_name> [ TYPE '<server_type>' ] [ VERSION '<server_version>' ]
    FOREIGN DATA WRAPPER <fdw_name>
    [ OPTIONS ( [ mpp_execute { 'coordinator' | 'any' | 'all segments' } [, ] ]
                [ num_segments '<num>' [, ] ]
                [ <option> '<value>' [, ... ]] ) ]
```

## Description {#description}

`CREATE SERVER` defines a new foreign server. The user who defines the server becomes its owner.

A foreign server typically encapsulates connection information that a foreign-data wrapper uses to access an external data source. Additional user-specific connection information may be specified by means of user mappings.

Creating a server requires the `USAGE` privilege on the foreign-data wrapper specified.

## Parameters {#parameters}

**`IF NOT EXISTS`**

Do not throw an error if a server with the same name already exists. Apache Cloudberry issues a notice in this case. Note that there is no guarantee that the existing server is anything like the one that would have been created.

**`server_name`**

The name of the foreign server to create. The server name must be unique within the database.

**`server_type`**

Optional server type, potentially useful to foreign-data wrappers.

**`server_version`**

Optional server version, potentially useful to foreign-data wrappers.

**`fdw_name`**

Name of the foreign-data wrapper that manages the server.

**`OPTIONS ( option 'value' [, ... ] )`**

The options for the new foreign server. The options typically define the connection details of the server, but the actual names and values are dependent upon the server's foreign-data wrapper.

**`mpp_execute { 'coordinator' | 'any' | 'all segments' }`**

A Apache Cloudberry-specific option that identifies the host from which the foreign-data wrapper reads or writes data:

- `coordinator` (the default)—Read or write data from the coordinator host.
- `any`—Read data from either the coordinator host or any one segment, depending on which path costs less.
- `all segments`—Read or write data from all segments. To support this option value, the foreign-data wrapper should have a policy that matches the segments to data.

> **Note** Apache Cloudberry supports parallel writes to foreign tables only when you set `mpp_execute 'all segments'`.

Support for the foreign server `mpp_execute` option, and the specific modes, is foreign-data wrapper-specific.

The `mpp_execute` option can be specified in multiple commands: `CREATE FOREIGN TABLE`, `CREATE SERVER`, and `CREATE FOREIGN DATA WRAPPER`. The foreign table setting takes precedence over the foreign server setting, followed by the foreign-data wrapper setting.

**`num_segments 'num'`**

When `mpp_execute` is set to `'all segments'`, the Apache Cloudberry-specific `num_segments` option identifies the number of query executors that Apache Cloudberry spawns on the source Apache Cloudberry cluster. If you do not provide a value, num defaults to the number of segments in the source cluster.

Support for the foreign server `num_segments` option is foreign-data wrapper-specific.

## Notes {#notes}

When using the dblink module (see dblink), you can use the foreign server name as an argument of the `dblink_connect()` function to provide the connection parameters. You must have the `USAGE` privilege on the foreign server to use it in this manner.

## Examples {#examples}

Create a foreign server named `myserver` that uses a foreign-data wrapper named `gpfdw1` and includes connection options:

```sql
CREATE SERVER myserver FOREIGN DATA WRAPPER gpfdw1 
    OPTIONS (host 'foo', dbname 'foodb', port '5432');
```

## Compatibility {#compatibility}

`CREATE SERVER` conforms to ISO/IEC 9075-9 (SQL/MED).

## See also {#see-also}

[ALTER SERVER](/cloudberry/reference/sql-stmts/alter-server/), [DROP SERVER](/cloudberry/reference/sql-stmts/drop-server/), [CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/), [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/), [CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/)
