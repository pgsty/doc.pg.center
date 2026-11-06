---
title: "使用压缩"
description: "可以配置 Apache Cloudberry，在部分数据库功能和工具中使用数据压缩。压缩可以减少磁盘占用并提升整个系统的 I/O 性能，但会增加数据压缩和解压缩的额外开销。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/use-compression.md"
---

可以为以下功能和工具配置数据压缩支持。有关压缩支持的信息，请参见相应的功能或工具。

- 追加优化表支持压缩表数据。参见 [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/)。
- 用户定义的数据类型可以定义为压缩数据。参见 [`CREATE TYPE`](/cloudberry/reference/sql-stmts/create-type/)。
- 访问外部数据时，外部表协议 [`gpfdist`](/cloudberry/data-loading/files/load-data-using-gpfdist/)（[`gpfdists`](/cloudberry/data-loading/files/load-data-using-gpfdists/)）、[s3](/cloudberry/data-loading/cloud/load-data-from-s3/) 和 [pxf](/cloudberry/data-loading/cloud/load-data-using-pxf/) 支持压缩。有关外部表的信息，参见 [`CREATE EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/create-external-table/)。
- 可以压缩工作文件（运行所需内存超过分配内存的查询时创建的临时溢出文件）。参见服务器配置参数 `gp_workfile_compression`。
- Apache Cloudberry 工具 [`gpbackup`](/cloudberry/reference/sys-utilities/gpbackup/)、[`gprestore`](/cloudberry/reference/sys-utilities/gprestore/)、[`gpload`](/cloudberry/reference/sys-utilities/gpload/) 和 [`gplogfilter`](/cloudberry/reference/sys-utilities/gplogfilter/) 支持压缩。

对于某些压缩算法（如 zlib），Apache Cloudberry 要求主机系统安装相应软件包。有关所需软件包的信息，参见 [Apache Cloudberry 安装指南](/cloudberry/deployment/)。
