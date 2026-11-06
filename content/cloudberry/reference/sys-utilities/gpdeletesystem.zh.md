---
title: "gpdeletesystem"
description: "删除使用 `gpinitsystem` 初始化的 Apache Cloudberry 系统。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpdeletesystem.md"
---

## 概要 {#synopsis}

```shell
gpdeletesystem [-d <coordinator_data_directory>] [-B <parallel_processes>] 
   [-f] [-l <logfile_directory>] [-D]

gpdeletesystem -? 

gpdeletesystem -v
```

## 说明 {#description}

`gpdeletesystem` 工具执行以下操作：

- 停止所有 `postgres` 进程（Segment 实例和 Coordinator 实例）。
- 删除所有数据目录。

运行 `gpdeletesystem` 前：

- 将所有备份文件移出 Coordinator 和 Segment 数据目录。
- 确认 Apache Cloudberry 正在运行。
- 如果当前位于 Segment 数据目录中，请切换到其他目录。在 Segment 数据目录内运行此工具会报错并失败。

此工具不会卸载 Apache Cloudberry 软件。

## 选项 {#options}

**`-d coordinator_data_directory`**

指定 Coordinator 主机的数据目录。如果未指定此选项，将使用环境变量 `COORDINATOR_DATA_DIRECTORY` 的设置。如果指定了此选项，它将覆盖 `COORDINATOR_DATA_DIRECTORY` 的任何设置。如果无法确定 coordinator_data_directory，此工具将返回错误。

**`-B parallel_processes`**

并行删除的 Segment 数量。如果未指定，此工具将根据需要删除的 Segment 实例数启动最多 60 个并行进程。

**`-f (force)`**

即使在数据目录中发现备份文件，也强制删除。默认情况下，只要存在备份文件，就不会删除 Apache Cloudberry 实例。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-D (debug)`**

将日志级别设为 debug。

**`-? (help)`**

显示在线帮助。

**`-v (show utility version)`**

显示此工具的版本、状态、最后更新日期和校验和。

## 示例 {#examples}

删除 Apache Cloudberry 系统：

```shell
gpdeletesystem -d /gpdata/gp-1
```

即使存在备份文件，也删除 Apache Cloudberry 系统：

```shell
gpdeletesystem -d /gpdata/gp-1 -f
```

## 另请参阅 {#see-also}

[gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/)
