---
title: 报告缺陷
weight: 1400
description: 如何为 etcd 项目提交问题报告
icon: fa-solid fa-bug
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/reporting_bugs.md"
aliases: [/etcd/reporting_bugs/]
---

如果 etcd 项目任何部分存在缺陷或文档错误，请通过 [打开问题][etcd-issue]告知我们。我们高度重视缺陷和错误，认为任何问题都不算太小。创建缺陷报告前，请确认尚未存在报告相同问题的议题。

为了使错误报告准确且易于理解，请尽量编写如下格式的错误报告：

- 具体。尽可能提供详细信息：包括版本号、运行环境、配置信息等。若该问题与运行 etcd 服务器相关，请附上 etcd 日志（包含 etcd 配置的启动日志尤为重要）。

- 可复现。请提供复现问题的完整步骤。我们理解某些问题可能难以复现，请尽可能提供可能导致问题的步骤。如有可能，请在缺陷报告中附上受影响的 etcd 数据目录和堆栈跟踪信息。

- 独立。请尽量在依赖最少的情况下复现问题。若报告中涉及过多依赖，将显著降低问题修复速度。排查依赖 etcd 的外部系统不在支持范围内，但我们可以提供正确的指导方向，或协助使用 etcd 本身。

- 唯一。请勿重复提交现有错误报告。

- 作用域明确。每个报告仅针对一个缺陷。请勿在单个报告中跟进其他缺陷。

在创建错误报告前，阅读 [Elika Etemad 关于撰写优质错误报告的文章][filing-good-bugs] 可能会有所帮助。

我们可能需要进一步信息以定位问题。重复的错误报告将被关闭。

## 常见问题解答 {#frequently-asked-questions}

### 如何获取堆栈跟踪 {#how-to-get-a-stack-trace}

``` bash
$ kill -QUIT $PID
```

### 如何获取 etcd 版本 {#how-to-get-etcd-version}

``` bash
$ etcd --version
```

### 如何获取以 `etcd2.service` 运行的 systemd 服务的 etcd 配置和日志 {#how-to-get-etcd-configuration-and-log-when-it-runs-as-systemd-service-etcd2service}

``` bash
$ sudo systemctl cat etcd2
$ sudo journalctl -u etcd2
```

由于上游 systemd 的一个缺陷，当 journald 的进程退出时，可能会丢失最后几行日志。如果 journalctl 显示 etcd 停止但未出现致命错误或 panic 消息，请尝试 `sudo journalctl -f -t etcd2` 以获取完整日志。

[etcd-issue]: https://github.com/etcd-io/etcd/issues/new
[filing-good-bugs]: http://fantasai.inkedblade.net/style/talks/filing-good-bugs/
