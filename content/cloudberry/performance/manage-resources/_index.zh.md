---
title: "资源管理"
description: "Apache Cloudberry 提供多种功能，帮助你根据业务要求确定查询优先级并分配资源，同时在资源不足时阻止查询启动。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/manage-resources.md"
---

可以通过资源管理功能限制并发查询数量、执行查询使用的内存量，以及用于处理查询的相对 CPU 份额。Apache Cloudberry 提供两种资源管理方案：[资源队列](/cloudberry/performance/manage-resources/manage-resources-using-resource-queues/)和[资源组](/cloudberry/performance/manage-resources/manage-resources-using-resource-groups/)。

Apache Cloudberry 可以启用资源队列或资源组管理方案，但不能同时启用两者。设置服务器配置参数 `gp_resource_manager`，即可在 Apache Cloudberry 集群中启用所选方案。

下表概括了资源队列与资源组的部分区别。

|指标|资源队列|资源组|
|------|---------------|---------------|
|并发|定义同时可用的查询槽位数|定义同时可用的事务槽位数|
|CPU|指定查询优先级|指定 CPU 资源百分比或具体 CPU 核数；使用 Linux 控制组|
|内存|在队列和算子级管理；用户可以超额分配|在事务级管理，增强了分配和跟踪能力；用户可以超额分配|
|用户|仅对非管理员用户施加限制|对 `SUPERUSER`、非管理员用户以及非用户类别的系统进程施加限制|
|磁盘 I/O|无|限制最大磁盘读写 I/O 吞吐量，以及每秒最大读写 I/O 操作数|
|排队|没有可用槽位或可用内存不足时排队|仅在没有可用槽位时排队|
|查询失败|为查询分配的内存超过可用系统内存和溢出限制时，查询可能立即失败|为查询分配的内存超过可用系统内存和溢出限制时，查询可能失败|
|绕过限制|不限制 `SUPERUSER` 角色及某些算子和函数|不限制 `SET`、`RESET` 和 `SHOW` 命令。此外，可以配置某些查询绕过并发限制|
|外部组件|无|管理 PL/Container 的 CPU 资源|
