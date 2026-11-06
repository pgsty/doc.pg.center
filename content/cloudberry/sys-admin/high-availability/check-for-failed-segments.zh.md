---
title: "检查故障 Segment"
description: "启用镜像后，即使系统中存在故障 Segment 实例，服务也可能不中断，用户也可能察觉不到故障。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/check-for-failed-segments.md"
---

可以使用 `gpstate` 工具、查看 `gp_segment_configuration` 目录表的内容，或检查日志文件来验证系统状态。

## 使用 gpstate 检查故障 Segment {#check-for-failed-segments-using-gpstate}

`gpstate` 工具提供 Apache Cloudberry 各个组件的状态，包括主 Segment、镜像 Segment、Coordinator 和 Standby Coordinator。

在 Coordinator 主机上，使用 [`gpstate`](/cloudberry/reference/sys-utilities/gpstate/) 工具的 `-e` 选项，显示存在错误状况的 Segment 实例：

```shell
$ gpstate -e
```

如果工具列出 `Segments with Primary and Mirror Roles Switched`，说明 Segment 未处于其*首选角色*（系统初始化时分配的角色）。这意味着系统可能处于不均衡状态，因为某些 Segment 主机上的活动 Segment 数量可能超过实现最佳系统性能的理想数量。

如果某个 Segment 的 `Config status` 显示为 `Down`，表示对应镜像 Segment 已停止运行。

修复方法见[从 Segment 故障中恢复](/cloudberry/sys-admin/high-availability/recover-from-segment-failures/)。

## 使用 gp_segment_configuration 表检查故障 Segment {#check-for-failed-segments-using-the-gp_segment_configuration-table}

要获取故障 Segment 的详细信息，可以查看 [`gp_segment_configuration`](/cloudberry/reference/sys-catalogs/sys-tables/gp-segment-configuration/) 目录表。例如：

```shell
$ psql postgres -c "SELECT * FROM gp_segment_configuration WHERE status='d';"
```

对于故障 Segment 实例，记录其主机、端口、首选角色和数据目录。这些信息有助于确定需要排查的主机和 Segment 实例。要显示镜像 Segment 实例的信息，运行：

```shell
$ gpstate -m
```

## 通过日志文件检查故障 Segment {#check-for-failed-segments-by-examining-log-files}

日志文件有助于确定错误原因。Coordinator 和各 Segment 实例都有各自的日志文件，位于数据目录下的 `log` 目录中。Coordinator 日志包含的信息最多，应始终先检查它。

使用 [`gplogfilter`](/cloudberry/reference/sys-utilities/gplogfilter/) 工具检查 Apache Cloudberry 日志文件，获取更多信息。要检查 Segment 日志文件，可通过 [`gpssh`](/cloudberry/reference/sys-utilities/gpssh/) 在 Segment 主机上运行 `gplogfilter`。

## 检查日志文件 {#to-check-the-log-files}

1. 使用 `gplogfilter` 检查 Coordinator 日志文件中级别为 `WARNING`、`ERROR`、`FATAL` 或 `PANIC` 的消息：

    ```shell
    $ gplogfilter -t
    ```

2. 使用 `gpssh` 检查各 Segment 实例中级别为 `WARNING`、`ERROR`、`FATAL` 或 `PANIC` 的日志消息。例如：

    ```shell
    $ gpssh -f seg_hosts_file -e 'source 
    /usr/local/cloudberry-db/cloudberry-env.sh ; gplogfilter -t 
    /data1/primary/*/log/gpdb*.log' > seglog.out
    ```
