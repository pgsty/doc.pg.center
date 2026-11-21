---
title: hstore
description: The hstore module implements the hstore data type for storing sets of key/value pairs within a single value.
weight: 140
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/hstore.md
---

The `hstore` module implements the `hstore` data type for storing sets of key/value pairs within a single value. This can be useful in various scenarios, such as rows with many attributes that are rarely examined, or semi-structured data.

The Apache Cloudberry `hstore` module is equivalent to the PostgreSQL `hstore` module. There are no MPP-specific considerations for the module.

## Install and register the module {#install-and-register-the-module}

`hstore` is built and installed by a default Apache Cloudberry build. Register the extension in each database in which you want to use it:

```sql
CREATE EXTENSION hstore;
```

## Module documentation {#module-documentation}

See [hstore](https://www.postgresql.org/docs/14/hstore.html) in the PostgreSQL documentation for details about the data type, operators, and functions that this module defines.
