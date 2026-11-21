---
title: pg_trgm
description: The pg_trgm module provides functions and operators for determining the similarity of alphanumeric text based
  on trigram matching.
weight: 200
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/pg-trgm.md
---

The `pg_trgm` module provides functions and operators for determining the similarity of alphanumeric text based on trigram matching. The module also provides GiST and GIN index operator classes that support fast searching for similar strings.

The Apache Cloudberry `pg_trgm` module is equivalent to the PostgreSQL `pg_trgm` module. There are no MPP-specific considerations for the module.

## Install and register the module {#install-and-register-the-module}

`pg_trgm` is built and installed by a default Apache Cloudberry build. Register the extension in each database in which you want to use it:

```sql
CREATE EXTENSION pg_trgm;
```

## Module documentation {#module-documentation}

See [pg_trgm](https://www.postgresql.org/docs/14/pgtrgm.html) in the PostgreSQL documentation for details about the functions, operators, and index operator classes in this module.
