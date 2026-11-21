---
title: tsm_system_time
description: The tsm_system_time module implements the SYSTEM_TIME table sampling method, which you can use in the TABLESAMPLE
  clause of a SELECT command.
weight: 270
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/tsm-system-time.md
---

The `tsm_system_time` module implements the `SYSTEM_TIME` table sampling method, which you can use in the `TABLESAMPLE` clause of a `SELECT` command.

## Install and register the module {#install-and-register-the-module}

`tsm_system_time` is not part of the default build targets (`make` and `make install`) of Apache Cloudberry. If `CREATE EXTENSION` reports that the extension is not available, build and install the module from the Apache Cloudberry source tree that your installation was configured from:

```shell
make -C contrib/tsm_system_time install
```

The module files must be present on every host of the cluster (coordinator, standby coordinator, and all segment hosts). The module is also installed by `make install-world`.

Then register the extension in each database in which you want to use it:

```sql
CREATE EXTENSION tsm_system_time;
```

## Use the module {#use-the-module}

The `SYSTEM_TIME` sampling method accepts a single floating-point argument that is the maximum number of milliseconds to spend reading the table. This lets you control how long the query takes; the tradeoff is that the size of the sample becomes hard to predict. The sample contains as many rows as could be read in the specified time, unless the whole table has been read first. A negative argument raises an error.

Like the built-in `SYSTEM` sampling method, `SYSTEM_TIME` performs block-level sampling, so the sample is not completely random and might be subject to clustering effects, especially if only a small number of rows are selected.

`SYSTEM_TIME` does not support the `REPEATABLE` clause.

> [!NOTE]
> In Apache Cloudberry, each segment samples its own part of a distributed table, and the time limit applies to each segment separately.


## Example {#example}

The following command returns as large a sample of `tablea` as each segment can read in 500 milliseconds. If the entire table can be read in less time, all of its rows are returned.

```sql
SELECT * FROM tablea TABLESAMPLE SYSTEM_TIME(500);
```

## Module documentation {#module-documentation}

See [tsm_system_time](https://www.postgresql.org/docs/14/tsm-system-time.html) in the PostgreSQL documentation.
