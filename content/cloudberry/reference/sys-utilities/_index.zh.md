---
title: "工具概览"
linkTitle: "系统工具"
description: "Apache Cloudberry 提供的命令行工具。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/index.md"
---

Apache Cloudberry 使用标准的 PostgreSQL 客户端和服务器程序，并提供额外的管理工具，用于管理分布式 Apache Cloudberry 数据库管理系统。

安装 Apache Cloudberry 服务器时会一并安装若干工具。这些工具位于 `$GPHOME/bin`。

上标用于标识需要单独下载的工具，以及也随客户端和加载工具包安装的工具。除非以特殊上标标明，否则所有工具都会在安装 Apache Cloudberry 服务器时一并安装。

有关某个工具的更多信息，请参阅“系统工具”分区中列出的相应主题。

## 客户端应用程序参考 {#reference-for-client-applications}

- [clusterdb](/cloudberry/reference/sys-utilities/clusterdb/) — 对数据库进行聚簇
- [createdb](/cloudberry/reference/sys-utilities/createdb/) — 创建新数据库
- [createuser](/cloudberry/reference/sys-utilities/createuser/) — 定义新用户账户
- [dropdb](/cloudberry/reference/sys-utilities/dropdb/) — 删除数据库
- [dropuser](/cloudberry/reference/sys-utilities/dropuser/) — 删除用户账户
- [pg_config](/cloudberry/reference/sys-utilities/pg-config/) — 获取已安装 PostgreSQL 版本的信息
- [pg_dump](/cloudberry/reference/sys-utilities/pg-dump/) — 将数据库导出为脚本文件或其他归档文件
- [pg_dumpall](/cloudberry/reference/sys-utilities/pg-dumpall/) — 将数据库集群导出为脚本文件
- [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) — 从 pg_dump 创建的归档文件中恢复数据库
- [psql](/cloudberry/reference/sys-utilities/psql/) — 交互式终端
- [reindexdb](/cloudberry/reference/sys-utilities/reindexdb/) — 重建数据库索引
- [vacuumdb](/cloudberry/reference/sys-utilities/vacuumdb/) — 对数据库进行垃圾回收和分析

## 服务器应用程序参考 {#reference-for-server-applications}

- [pg_checksums](/cloudberry/reference/sys-utilities/pg-checksums/) — 启用、禁用或检查数据库集群中的数据校验和

## 管理员参考 {#reference-for-administrator}

- [analyzedb](/cloudberry/reference/sys-utilities/analyzedb/) - 以增量和并发方式对表执行 `ANALYZE` 操作
- [gpaddmirrors](/cloudberry/reference/sys-utilities/gpaddmirrors/) - 为最初未配置镜像的 Apache Cloudberry 系统添加镜像 Segment
- [gpbackup](/cloudberry/reference/sys-utilities/gpbackup/) - 创建供 gprestore 工具使用的 Apache Cloudberry 备份
- [gpcheckcat](/cloudberry/reference/sys-utilities/gpcheckcat/) - 检查 Apache Cloudberry 系统目录表是否存在不一致
- [gpcheckperf](/cloudberry/reference/sys-utilities/gpcheckperf/) - 验证指定主机的硬件基准性能
- [gpconfig](/cloudberry/reference/sys-utilities/gpconfig/) - 设置 Apache Cloudberry 系统中所有 Segment 的服务器配置参数
- [gpdeletesystem](/cloudberry/reference/sys-utilities/gpdeletesystem/) - 删除使用 gpinitsystem 初始化的 Apache Cloudberry 系统
- [gpdemo](/cloudberry/reference/sys-utilities/gpdemo/) - 部署一个 Segment 均位于单节点上的小型 Apache Cloudberry 集群，用于演示
- [gpexpand](/cloudberry/reference/sys-utilities/gpexpand/) - 将现有 Apache Cloudberry 扩展到系统中的新主机上
- [gpfdist](/cloudberry/reference/sys-utilities/gpfdist/) - 向 Apache Cloudberry Segment 提供数据文件，或将 Segment 数据写出为文件
- [gpinitstandby](/cloudberry/reference/sys-utilities/gpinitstandby/) - 为 Apache Cloudberry 系统添加和／或初始化 Standby Coordinator 主机
- [gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/) - 使用 gpinitsystem_config 文件中指定的配置参数初始化 Apache Cloudberry 系统
- [gpload](/cloudberry/reference/sys-utilities/gpload/) - 运行 YAML 格式控制文件中定义的加载作业
- [gplogfilter](/cloudberry/reference/sys-utilities/gplogfilter/) - 在 Apache Cloudberry 日志文件中搜索指定条目
- [gpmemreport](/cloudberry/reference/sys-utilities/gpmemreport/) - 解析 gpmemwatcher 工具创建的输出，并生成可读格式的输出文件
- [gpmemwatcher](/cloudberry/reference/sys-utilities/gpmemwatcher/) - 跟踪数据库集群中各进程的内存使用情况。
- [gpmovemirrors](/cloudberry/reference/sys-utilities/gpmovemirrors/) - 将镜像 Segment 实例移动到新位置
- [gppkg](/cloudberry/reference/sys-utilities/gppkg/) - 安装、升级、迁移和删除 `.gppkg` 格式扩展的包管理器
- [gprestore](/cloudberry/reference/sys-utilities/gprestore/) - 恢复使用 gpbackup 工具创建的数据库备份
- [gpreload](/cloudberry/reference/sys-utilities/gpreload/) - 按指定列排序并重新加载表数据
- [gprecoverseg](/cloudberry/reference/sys-utilities/gprecoverseg/) - 恢复标记为停机的主 Segment 或镜像 Segment 实例（启用镜像时）
- [gpshrink](/cloudberry/reference/sys-utilities/gpshrink/) - 使用 `gpshrink` 缩小集群规模，节省服务器资源
- [gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/) - 在主机之间交换 SSH 公钥
- [gpssh](/cloudberry/reference/sys-utilities/gpssh/) - 同时提供对多台主机的 SSH 访问
- [gpstart](/cloudberry/reference/sys-utilities/gpstart/) - 启动 Apache Cloudberry 系统
- [gpstate](/cloudberry/reference/sys-utilities/gpstate/) - 显示正在运行的 Apache Cloudberry 系统的状态
- [gpstop](/cloudberry/reference/sys-utilities/gpstop/) - 停止或重启 Apache Cloudberry 系统
- [gpsync](/cloudberry/reference/sys-utilities/gpsync/) - 同时在多台主机之间复制文件
- [gpactivatestandby](/cloudberry/reference/sys-utilities/gpactivatestandby/) - 激活 Standby Coordinator 主机，使其成为活动 Coordinator
