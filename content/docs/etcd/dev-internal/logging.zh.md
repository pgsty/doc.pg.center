---
title: 日志记录约定
weight: 1600
description: 日志级别类别
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-internal/logging.md"
aliases: [/etcd/dev-internal/logging/]
---

etcd 使用 [zap][zap] 库记录应用程序输出，输出按 *级别* 进行分类。日志消息的级别依据以下约定确定：

* DebugLevel 日志通常非常庞大，通常在生产环境中禁用。
  * 示例：
    * 向远程对等成员发送一条普通消息
    * 将日志条目写入磁盘

* InfoLevel 为默认的日志优先级。
  * 示例：
    * 启动配置
    * 开始创建快照
    * 向集群中添加新节点
    * 向认证子系统中添加新用户

* 警告级别日志比信息级别日志更为重要，但无需逐条人工审查。
  * 示例：
    * 无法向远程对等成员发送 Raft 消息
    * 在配置的选举超时时间内未收到心跳消息

* ErrorLevel 日志为高优先级。若应用程序运行正常，不应产生任何 ErrorLevel 日志。
  * 示例：
    * WAL 无法分配磁盘空间

* PanicLevel 会记录一条消息，然后触发 panic。
  * 示例：
    * Raft 消息编码失败

* FatalLevel 会记录一条消息，然后调用 os.Exit(1)。
  * 示例：
    * Raft 快照保存失败

[zap]: https://github.com/uber-go/zap
