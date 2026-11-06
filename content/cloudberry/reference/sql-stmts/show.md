---
title: "SHOW"
description: "Shows the value of a run-time system configuration parameter."
weight: 1740
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/show.md"
---

## Synopsis {#synopsis}

```sql
SHOW <name>

SHOW ALL
```

## Description {#description}

`SHOW` displays the current settings of Apache Cloudberry run-time system configuration parameters. You can set these parameters with the `SET` statement, by editing the `postgresql.conf` configuration file of the Apache Cloudberry coordinator, through the `PGOPTIONS` environment variable (when using libpq or a libpq-based application), or through command-line flags when starting the Apache Cloudberry server.

## Parameters {#parameters}

**`name`**

The name of a run-time system configuration parameter.

Some parameters viewable by `SHOW` are read-only — you can view their values but not set them:

**`SERVER_VERSION`**

Shows the version number of the Apache Cloudberry server.

**`SERVER_ENCODING`**

Shows the server-side character set encoding. You can show, but not set, this parameter because the encoding is determined at database creation time.

**`LC_COLLATE`**

Shows the database's locale setting for collation (text ordering). You can show, but not set, this parameter because the setting is determined at database creation time.

**`LC_CTYPE`**

Shows the database's locale setting for character classification; You can show, but not set, this parameter because the setting is determined at database creation time.

**`IS_SUPERUSER`**

True if the current role has superuser privileges.

**`ALL`**

Shows the current value of all configuration parameters, with descriptions.

## Notes {#notes}

The function `current_setting()` produces equivalent output; see [System Administration Functions](https://www.postgresql.org/docs/12/functions-admin.html) in the PostgreSQL documentation. Also, the [pg_settings](https://www.postgresql.org/docs/12/view-pg-settings.html) system view produces the same information.

## Examples {#examples}

Show the current setting of the parameter `DateStyle`:

```sql
SHOW DateStyle;
 DateStyle
-----------
 ISO, MDY
(1 row)
```

Show the current setting of the parameter `row_security`:

```sql
SHOW row_security;
 row_security
--------------
 on
(1 row)
```

Show the current setting of all parameters:

```sql
SHOW ALL;
       name       | setting |                  description
-----------------+---------+----------------------------------------------------
 application_name | psql    | Sets the application name to be reported in sta...

 ...

 xmlbinary        | base64  | Sets how binary values are to be encoded in XML.
 xmloption        | content | Sets whether XML data in implicit parsing and s...
(473 rows)
```

## Compatibility {#compatibility}

The `SHOW` command is a Apache Cloudberry extension.

## See also {#see-also}

[SET](/cloudberry/reference/sql-stmts/set/), [RESET](/cloudberry/reference/sql-stmts/reset/)
