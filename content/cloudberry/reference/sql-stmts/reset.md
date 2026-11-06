---
title: "RESET"
description: "Restores the value of a run-time system configuration parameter to the default value."
weight: 1610
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/reset.md"
---

## Synopsis {#synopsis}

```sql
RESET <configuration_parameter>

RESET ALL
```

## Description {#description}

`RESET` restores system configuration parameters to their default values. `RESET` is an equivalent command for

``` sql
SET <configuration_parameter> TO DEFAULT
```

Refer to [SET](/cloudberry/reference/sql-stmts/set/) for details.

The default value is defined as the value that the parameter would have had, had no `SET` ever been issued for it in the current session. The actual source of this value might be a compiled-in default, the coordinator `postgresql.conf` configuration file, command-line options, or per-database or per-user default settings. This is subtly different from defining it as "the value that the parameter had at session start", because if the value came from the configuration file, it will be reset to whatever is specified by the configuration file now. See Server Configuration Parameters for more information.

The transactional behavior of `RESET` is the same as `SET`: its effects will be undone by transaction rollback.

## Parameters {#parameters}

**`configuration_parameter`**

The name of a settable run-time system configuration parameter. See Server Configuration Parameters for details.

**`ALL`**

Resets all settable run-time configuration parameters to their default values.

## Examples {#examples}

Set the `statement_mem` configuration parameter to its default value:

```sql
RESET statement_mem; 
```

## Compatibility {#compatibility}

`RESET` is a Apache Cloudberry extension.

## See also {#see-also}

[SET](/cloudberry/reference/sql-stmts/set/), [SHOW](/cloudberry/reference/sql-stmts/show/)
