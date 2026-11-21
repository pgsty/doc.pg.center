---
title: citext
description: The citext module provides a case-insensitive character string data type, citext.
weight: 30
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/citext.md
---

The `citext` module provides a case-insensitive character string data type, `citext`. Essentially, it internally calls the `lower()` function when comparing values. Otherwise, it behaves almost exactly like the `text` data type.

The Apache Cloudberry `citext` module is equivalent to the PostgreSQL `citext` module. There are no MPP-specific considerations for the module.

## Install and register the module {#install-and-register-the-module}

`citext` is built and installed by a default Apache Cloudberry build. Register the extension in each database in which you want to use it:

```sql
CREATE EXTENSION citext;
```

## Module documentation {#module-documentation}

See [citext](https://www.postgresql.org/docs/14/citext.html) in the PostgreSQL documentation for details about the data type, operators, and functions that this module defines.
