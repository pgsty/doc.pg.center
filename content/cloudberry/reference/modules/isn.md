---
title: isn
description: The isn module provides data types for the international product numbering standards EAN13, UPC, ISBN (books),
  ISMN (music), and ISSN (serials).
weight: 150
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/isn.md
---

The `isn` module provides data types for the international product numbering standards EAN13, UPC, ISBN (books), ISMN (music), and ISSN (serials).

The Apache Cloudberry `isn` module is equivalent to the PostgreSQL `isn` module. There are no MPP-specific considerations for the module.

## Install and register the module {#install-and-register-the-module}

`isn` is not part of the default build targets (`make` and `make install`) of Apache Cloudberry. If `CREATE EXTENSION` reports that the extension is not available, build and install the module from the Apache Cloudberry source tree that your installation was configured from:

```shell
make -C contrib/isn install
```

The module files must be present on every host of the cluster (coordinator, standby coordinator, and all segment hosts). The module is also installed by `make install-world`.

Then register the extension in each database in which you want to use it:

```sql
CREATE EXTENSION isn;
```

## Module documentation {#module-documentation}

See [isn](https://www.postgresql.org/docs/14/isn.html) in the PostgreSQL documentation for details about the data types, casts, and functions that this module defines.
