---
title: "管理查询生成的溢出文件"
description: "如果可用内存不足以执行 SQL 查询，Apache Cloudberry 会在磁盘上创建溢出文件，也称为工作文件。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/manage-spill-files.md"
---

单个查询允许生成的最大溢出文件数由服务器配置参数 `gp_workfile_limit_files_per_query` 控制。默认值 `100000` 足以满足大多数查询的需求。

如果查询生成的溢出文件数超过配置的限制，Apache Cloudberry 会返回以下错误：

```sql
ERROR: number of workfiles per query limit exceeded
```

以下情况可能导致 Apache Cloudberry 生成大量溢出文件：

- 查询的数据存在数据倾斜。
- 分配给查询的内存过少。可以通过 Apache Cloudberry 服务器配置参数 `max_statement_mem` 和 `statement_mem`，或通过资源组、资源队列配置，控制查询可使用的最大内存量。

修改查询、调整数据分布或更改系统内存配置后，查询可能就能成功执行。`gp_toolkit.gp_workfile_*` 视图显示溢出文件的使用情况，可用于查询排障和调优。关于 `gp_workfile_**` 视图的说明，请参阅[检查查询磁盘溢出空间使用情况](/cloudberry/reference/sys-catalogs/gp_toolkit/#check-query-disk-spill-space-usage)。

其他相关文档：

- [使用资源组](/cloudberry/performance/manage-resources/manage-resources-using-resource-groups/)介绍了启用基于资源组的资源管理时，内存和溢出方面的注意事项。
