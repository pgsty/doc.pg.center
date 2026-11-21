---
title: tablefunc
description: The tablefunc module provides various functions that return tables (that is, multiple rows), such as normal_rand(),
  crosstab(), and connectby().
weight: 250
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/tablefunc.md
---

The `tablefunc` module provides various functions that return tables (that is, multiple rows), such as `normal_rand()`, `crosstab()`, and `connectby()`.

The Apache Cloudberry `tablefunc` module is equivalent to the PostgreSQL `tablefunc` module. There are no MPP-specific considerations for the module.

## Install and register the module {#install-and-register-the-module}

`tablefunc` is built and installed by a default Apache Cloudberry build. Register the extension in each database in which you want to use it:

```sql
CREATE EXTENSION tablefunc;
```

## Module documentation {#module-documentation}

See [tablefunc](https://www.postgresql.org/docs/14/tablefunc.html) in the PostgreSQL documentation for details about the individual functions in this module.
