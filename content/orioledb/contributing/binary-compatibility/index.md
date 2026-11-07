---
title: OrioleDB binary compatibility
linkTitle: Binary compatibility
description: Check storage-format compatibility before upgrading OrioleDB binaries.
weight: 40
type: docs
search_keywords: ["OrioleDB", "binary compatibility", "binary compatibility", "二进制兼容"]
upstream_link: https://www.orioledb.com/docs/contributing/binary-compatibility
upstream_source: orioledb
upstream_modified: true
upstream_notice: /orioledb/attribution/
icon: fa-solid fa-puzzle-piece
---


## Version variables {#version-variables}

The file `include/orioledb.h` contains several OrioleDB binary-compatibility related version variables. Currently it contains the following version variables:

- `ORIOLEDB_BINARY_VERSION` - version of a database instance
- `ORIOLEDB_SYS_TREE_VERSION` - version of system trees format
- `ORIOLEDB_PAGE_VERSION` - version of OrioleDB pages format
- `ORIOLEDB_COMPRESS_VERSION` - version of OrioleDB pages compression format

If you change the relevant format and its version wasn't incremented since the last release, you need to increment it. To check whether it was already bumped, compare `include/orioledb.h` against the last release tag, e.g. `git diff <last-tag> -- include/orioledb.h`.

## Cross-architecture support {#cross-architecture-support}

At this point, PostgreSQL and OrioleDB cannot promise that a database initialized on one machine/architecture will work on a machine with a different architecture. This includes physical replication and copying database files between machines. This might not work even if PostgreSQL and OrioleDB binaries were built using the same endianness, alignment, and float format.

On the other hand, we try to minimize architecture differences. When making changes to database file formats or the replication protocol, please use data types that have the same implementation on different architectures. For example, prefer fixed-width integer types (`uint32`, `uint64`) over `long` or raw pointers, and avoid relying on `struct` field padding/alignment, since these can differ between platforms.
