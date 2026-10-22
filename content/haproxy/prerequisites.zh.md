---
title: "1. 先决条件"
linkTitle: "1. 先决条件"
weight: 250
description: "读者应具备 Unix 系统管理与故障排查知识"
icon: fa-solid fa-list-check
module: [HAPROXY]
categories: [任务]
aliases:
  - /haproxy/management/prerequisites/
  - /haproxy/management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 1"
---

本文介绍如何启动、停止、管理 HAProxy 及排查其故障，也会说明一些已知限制和应避免的陷阱。本文不涉及 HAProxy 的配置方法；相关内容请参阅 [`configuration.txt`](/zh/haproxy/http-fundamentals/)。

本文假定读者在类 Unix 操作系统上具备足够的系统管理能力，日常使用 shell，并熟悉 strace、tcpdump 等故障排查工具。
