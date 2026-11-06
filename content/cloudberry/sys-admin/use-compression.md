---
title: "Use Compression"
description: "You can configure Apache Cloudberry to use data compression with some database features and with some utilities.Compression reduces disk usage and improves I/O across the system, however, it adds some performance overhead when compressing and decompressing data."
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/use-compression.md"
---

You can configure support for data compression with these features and utilities. See the specific feature or utility for information about support for compression.

- Append-optimized tables support compressing table data. See [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/).
- User-defined data types can be defined to compress data. See [`CREATE TYPE`](/cloudberry/reference/sql-stmts/create-type/).
- The external table protocols [`gpfdist`](/cloudberry/data-loading/files/load-data-using-gpfdist/) ([`gpfdists`](/cloudberry/data-loading/files/load-data-using-gpfdists/)), [s3](/cloudberry/data-loading/cloud/load-data-from-s3/), and [pxf](/cloudberry/data-loading/cloud/load-data-using-pxf/) support compression when accessing external data. For information about external tables, see [`CREATE EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/create-external-table/).
- Workfiles (temporary spill files that are created when running a query that requires more memory than it is allocated) can be compressed. See the server configuration parameter `gp_workfile_compression`.
- The Apache Cloudberry utilities [`gpbackup`](/cloudberry/reference/sys-utilities/gpbackup/), [`gprestore`](/cloudberry/reference/sys-utilities/gprestore/), [`gpload`](/cloudberry/reference/sys-utilities/gpload/), and [`gplogfilter`](/cloudberry/reference/sys-utilities/gplogfilter/) support compression.

For some compression algorithms (such as zlib) Apache Cloudberry requires software packages installed on the host system. For information about required software packages, see the [Apache Cloudberry Installation Guide](/cloudberry/deployment/).
