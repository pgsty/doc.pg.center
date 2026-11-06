---
title: "如何检测故障 Segment"
description: "启用 Segment 镜像后，当主 Segment 实例停止运行时，Apache Cloudberry 会自动进行故障切换，转到镜像 Segment 实例。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/detect-a-failed-segment.md"
---

只要每份数据都有一个在线的 Segment 实例，用户就可能察觉不到某个 Segment 已停止运行。如果故障发生时有事务正在执行，该事务会回滚，并在重新配置后的 Segment 集合上自动重新执行。可以使用 [`gpstate`](/cloudberry/reference/sys-utilities/gpstate/) 工具识别故障 Segment。该工具显示来自目录表的信息，包括 [`gp_segment_configuration`](/cloudberry/reference/sys-catalogs/sys-tables/gp-segment-configuration/)。

如果 Segment 故障导致整个 Apache Cloudberry 系统无法运行（例如，未启用镜像，或在线 Segment 不足以访问全部用户数据），用户尝试连接数据库时会看到错误。返回给客户端程序的错误可能指出故障。例如：

```
ERROR: All segment databases are unavailable
```

## 检测和处理 Segment 故障的过程 {#how-a-segment-failure-is-detected-and-managed}

在 Apache Cloudberry Coordinator 主机上，Postgres 的 `postmaster` 进程会派生一个故障探测进程 `ftsprobe`，也称为 FTS（Fault Tolerance Server，容错服务器）进程。如果 FTS 故障，`postmaster` 会将其重启。

FTS 循环运行，每轮之间有一个休眠间隔。每轮中，FTS 根据 `gp_segment_configuration` 表中登记的主机名和端口，与各主 Segment 实例建立 TCP 套接字连接，以探测实例状态。如果连接成功，Segment 会执行几项简单检查并向 FTS 报告。检查包括对 Segment 的关键目录执行 `stat` 系统调用，以及检查 Segment 实例的内部故障。如果未发现问题，就向 FTS 返回成功响应，不对该 Segment 实例采取操作。

如果无法建立连接，或在超时时间内未收到响应，就会重试探测该 Segment 实例。如果达到配置的最大探测次数后仍未成功，FTS 会探测该 Segment 的镜像，确认它正常运行，然后更新 `gp_segment_configuration` 表，将主 Segment 标记为“down”，并设置镜像承担主实例角色。FTS 将执行的操作记录到 [`gp_configuration_history`](/cloudberry/reference/sys-catalogs/sys-tables/gp-configuration-history/) 表中。

当仅有主 Segment 处于活动状态，而对应镜像已停止运行时，主实例会进入*未同步（Not In Sync）*状态，继续记录数据库变更，使镜像恢复时可以完成同步，而无需从主实例向镜像完整复制数据。

## 配置 FTS 行为 {#configure-fts-behavior}

以下服务器配置参数会影响 FTS 行为：

`gp_fts_probe_interval`：启动新一轮 FTS 循环的间隔，单位为秒。例如，设为 60 且一轮探测耗时 10 秒时，FTS 进程休眠 50 秒；设为 60 且一轮探测耗时 75 秒时，休眠 0 秒。默认值为 60，最大值为 3600。

`gp_fts_probe_timeout`：Coordinator 与 Segment 之间的探测超时时间，单位为秒。默认值为 20，最大值为 3600。

`gp_fts_probe_retries`：探测一个 Segment 的尝试次数。例如，设为 5 时，首次尝试失败后还会重试 4 次。默认值：5。

`gp_log_fts`：FTS 的日志级别。可取“off”“terse”“verbose”或“debug”。生产环境可以使用“verbose”，以提供有助于排查问题的数据；不应在生产环境使用“debug”。默认值：“terse”。

`gp_segment_connect_timeout`：等待镜像响应的最长时间，单位为秒。默认值：180（3 分钟）。

除了 FTS 执行的故障检查，无法向镜像发送数据的主 Segment 也可以将镜像状态改为 down。主实例会将数据加入队列，在经过 `gp_segment_connect_timeout` 秒后报告镜像故障，使镜像被标记为 down，主实例则进入 `Not In Sync` 模式。
