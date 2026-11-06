---
title: "使用资源组管理内存与资源"
description: "使用资源组管理 Apache Cloudberry 资源。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/resource-group-best-practices.md"
---

内存、CPU 和并发事务管理会显著影响 Apache Cloudberry 集群的性能。资源组是一种较新的资源管理方案，可以限制 Apache Cloudberry 中的内存、CPU 和并发事务。

- [为 Apache Cloudberry 配置内存](#configure-memory-for-apache-cloudberry)
- [使用资源组时考虑内存](#consider-memory-when-using-resource-groups)
- [配置资源组](#configure-resource-groups)
- [低内存查询](#low-memory-queries)
- [管理工具与 admin_group 并发](#administrative-utilities-and-admin_group-concurrency)

## 为 Apache Cloudberry 配置内存 {#configure-memory-for-apache-cloudberry}

虽然系统内存并不总是能够增加，但可以通过配置资源组管理预期的工作负载，避免许多内存不足情况。

使用资源组管理 Apache Cloudberry 资源时，以下操作系统和 Apache Cloudberry 内存设置很重要：

- **vm.overcommit_memory**

    这个 Linux 内核参数在 [`/etc/sysctl.conf`](/cloudberry/deployment/prepare-to-deploy/#the-sysctlconf-file) 中设置，用于确定操作系统判定进程可以分配多少内存的方法。Apache Cloudberry 系统必须始终将 `vm.overcommit_memory` 设为 2。

- **vm.overcommit_ratio**

    这个 Linux 内核参数在 `/etc/sysctl.conf` 中设置，用于确定 RAM 中供应用进程使用的百分比；剩余部分保留给操作系统。根据需要调整该设置。如果内存利用率过低，提高该值；如果内存或交换空间使用率过高，降低该值。

- **gp_workfile_limit_files_per_query**

    设置 `gp_workfile_limit_files_per_query`，限制每个查询允许的临时溢出文件（工作文件）最大数量。查询所需内存超过分配量时会创建溢出文件。超过上限后，查询会被终止。默认值为零，表示允许无限数量的溢出文件，这可能会填满文件系统。

- **gp_workfile_compression**

    如果溢出文件很多，可以设置 `gp_workfile_compression` 来压缩溢出文件。压缩溢出文件有助于避免 I/O 操作使磁盘子系统过载。

- **statement_mem**

    Apache Cloudberry 使用 `statement_mem` 设置确定为查询分配的内存量。

其他注意事项：

- 不要将操作系统配置为使用大页。参见 *Cloudberry 安装指南*中的[推荐操作系统参数设置](/cloudberry/deployment/prepare-to-deploy/#recommended-os-parameters-settings)。
- 配置资源组内存时，应考虑故障期间变为主 Segment 的镜像 Segment 的内存需求，确保主 Segment 或 Segment 主机故障时数据库操作仍能继续。

## 使用资源组时考虑内存 {#consider-memory-when-using-resource-groups}

在使用少量或不使用交换空间、并采用默认 `vm.overcommit_ratio` 的系统上，资源组可用的内存可能受到限制。为确保 Apache Cloudberry 获得合理的每个 Segment 主机内存上限，可能需要提高以下一个或多个配置设置：

1. 系统上的交换空间大小。
2. 系统的 `vm.overcommit_ratio` 设置。

## 配置资源组 {#configure-resource-groups}

Apache Cloudberry 资源组提供了管理集群工作负载的强大机制。为系统配置资源组时，请考虑以下通用准则：

- 任何具有 `SUPERUSER` 权限的 Apache Cloudberry 角色提交的事务，都会在名为 `admin_group` 的默认资源组下运行。安排和运行 Cloudberry 管理工具时，要注意这一点。
- 确保为每个非管理员角色分配资源组。如果没有为角色分配资源组，该角色提交的查询会由名为 `default_group` 的默认资源组处理。
- 使用资源组参数 `CONCURRENCY`，限制特定资源组成员可以并发运行的活动查询数量。
- 使用 `MEMORY_QUOTA` 参数，控制在资源组中运行的查询可以消耗的最大内存量。
- Apache Cloudberry 会将未保留的内存（100 减去所有资源组 `MEMORY_QUOTA` 的总和）分配到全局共享内存池。所有查询都可以按先到先得的方式使用这部分内存。
- 动态调整资源组，使其与该组在不同工作负载和时段的实际需求相匹配。
- 使用 `gp_toolkit` 视图检查资源组资源使用情况，并监控各组的运行状态。

## 低内存查询 {#low-memory-queries}

实践表明，较低的 `statement_mem` 设置（例如 10MB 左右）可以提高低内存需求查询的性能。使用服务器配置参数 `statement_mem` 按查询覆盖该设置。例如：

```sql
SET statement_mem='10 MB';
```

## 管理工具与 `admin_group` 并发 {#administrative-utilities-and-admin_group-concurrency}

Apache Cloudberry `SUPERUSER` 发起的数据库事务默认使用名为 `admin_group` 的资源组。`admin_group` 资源组的默认 `CONCURRENCY` 值为 10。

某些 Apache Cloudberry 管理工具在运行时可能使用多个 `CONCURRENCY` 槽，例如使用 `--jobs` 选项调用的 `gpbackup`。如果运行的工具所需并发事务数超过 `admin_group` 的配置值，可以临时提高该组的 `MEMORY_QUOTA` 和 `CONCURRENCY` 值以满足工具需求；工具完成后务必将这些参数恢复为原始设置。

> **注意** 使用 `ALTER RESOURCE GROUP` 发起的内存分配变更，可能因为当前运行查询消耗资源而不会立即生效。务必在维护窗口前提前修改资源组参数。
