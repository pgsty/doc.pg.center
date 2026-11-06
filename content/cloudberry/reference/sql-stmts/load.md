---
title: "LOAD"
description: "Loads or reloads a shared library file."
weight: 1520
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/load.md"
---

## Synopsis {#synopsis}

```sql
LOAD '<filename>'
```

## Description {#description}

This command loads a shared library file into the Apache Cloudberry server address space. If the file had been loaded previously, it is first unloaded. This command is primarily useful to unload and reload a shared library file that has been changed since the server first loaded it. To make use of the shared library, function(s) in it need to be declared using the `CREATE FUNCTION` command.

The library file name is typically given as just a bare file name, which is sought in the server's library search path (set by `dynamic_library_path`). Alternatively it can be given as a full path name. In either case the platform's standard shared library file name extension may be omitted.

Note that in Apache Cloudberry the shared library file (`.so` file) must reside in the same path location on every host in the Apache Cloudberry array (coordinators, segments, and mirrors).

Non-superusers can only apply `LOAD` to library files located in `$libdir/plugins/` — the specified `filename` must begin with exactly that string. You must ensure that only “safe” libraries are installed there.

## Parameters {#parameters}

**`filename`**

The path and file name of a shared library file. This file must exist in the same location on all hosts in your Apache Cloudberry array.

## Examples {#examples}

Load a shared library file:

```sql
LOAD '/usr/local/cloudberry/lib/myfuncs.so';
```

## Compatibility {#compatibility}

`LOAD` is a Apache Cloudberry extension.

## See also {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)
