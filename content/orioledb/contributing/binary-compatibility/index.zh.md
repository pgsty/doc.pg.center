---
title: 二进制兼容性
linkTitle: 二进制兼容性
description: 维护文件格式版本号，并减少跨架构差异。
weight: 40
type: docs
search_keywords: ["OrioleDB", "binary compatibility", "binary compatibility", "二进制兼容"]
upstream_link: https://www.orioledb.com/docs/contributing/binary-compatibility
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-puzzle-piece
---


## 版本变量 {#version-variables}

`include/orioledb.h` 包含若干与 OrioleDB 二进制兼容性相关的版本变量，目前包括：

- `ORIOLEDB_BINARY_VERSION`：数据库实例版本。
- `ORIOLEDB_SYS_TREE_VERSION`：系统树格式版本。
- `ORIOLEDB_PAGE_VERSION`：OrioleDB 页面格式版本。
- `ORIOLEDB_COMPRESS_VERSION`：OrioleDB 页面压缩格式版本。

如果修改了对应格式，且自上次发布以来版本号尚未递增，就需要递增它。可以将 `include/orioledb.h` 与上次发布标签比较，例如运行 `git diff <last-tag> -- include/orioledb.h`，检查是否已经提升版本号。

## 跨架构支持 {#cross-architecture-support}

目前 PostgreSQL 和 OrioleDB 都不能保证在一种机器或架构上初始化的数据库，能在另一种架构上正常工作。这包括物理复制以及跨机器复制数据库文件。即使构建 PostgreSQL 和 OrioleDB 二进制文件时采用相同的字节序、对齐方式和浮点格式，也可能无法工作。

不过，我们仍努力减少架构差异。修改数据库文件格式或复制协议时，请使用在不同架构上实现一致的数据类型。例如，优先使用固定宽度整数 `uint32`、`uint64`，而不是 `long` 或裸指针；避免依赖 `struct` 字段的填充和对齐，因为它们可能因平台而异。
