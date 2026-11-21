---
title: tsm_system_rows
description: The tsm_system_rows module implements the SYSTEM_ROWS table sampling method, which you can use in the TABLESAMPLE
  clause of a SELECT command.
weight: 260
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/tsm-system-rows.md
---

The `tsm_system_rows` module implements the `SYSTEM_ROWS` table sampling method, which you can use in the `TABLESAMPLE` clause of a `SELECT` command.

## Install and register the module {#install-and-register-the-module}

`tsm_system_rows` is not part of the default build targets (`make` and `make install`) of Apache Cloudberry. If `CREATE EXTENSION` reports that the extension is not available, build and install the module from the Apache Cloudberry source tree that your installation was configured from:

```shell
make -C contrib/tsm_system_rows install
```

The module files must be present on every host of the cluster (coordinator, standby coordinator, and all segment hosts). The module is also installed by `make install-world`.

Then register the extension in each database in which you want to use it:

```sql
CREATE EXTENSION tsm_system_rows;
```

## Use the module {#use-the-module}

The `SYSTEM_ROWS` sampling method accepts a single integer (`bigint`) argument that is the maximum number of rows to read. If the table does not contain that many rows, the whole table is selected. A negative argument raises an error.

Like the built-in `SYSTEM` sampling method, `SYSTEM_ROWS` performs block-level sampling, so the sample is not completely random and might be subject to clustering effects, especially if only a small number of rows are requested.

`SYSTEM_ROWS` does not support the `REPEATABLE` clause.

> [!NOTE]
> In Apache Cloudberry, each segment samples its own part of a distributed table, and the limit applies to each segment separately. A query on a distributed table can therefore return up to the given number of rows from each segment. For example, `SYSTEM_ROWS(75)` on a cluster with three primary segments returns up to 225 rows.


## Example {#example}

The following command returns a sample of at most 75 rows from each segment for the table `tablea`:

```sql
SELECT * FROM tablea TABLESAMPLE SYSTEM_ROWS(75);
```

## Module documentation {#module-documentation}

See [tsm_system_rows](https://www.postgresql.org/docs/14/tsm-system-rows.html) in the PostgreSQL documentation.
