---
title: 进阶部署
description: 根据存储设备与文件系统，选择本地部署或共享存储部署路径。
weight: 30
upstream_link: https://github.com/polardb/polardb-pg-docs/blob/b4733b0350888242afeba432a6837458c348a937/docs/zh/deploying/deploy.md
upstream_source: polardb
upstream_modified: true
author: 棠羽
date: '2024-08-30'
type: docs
---


部署 PolarDB for PostgreSQL 需要在以下三个层面上做准备：

1. **块存储设备**：用于提供存储介质。可以是单个物理块存储设备（本地存储），也可以是多个物理块设备构成的分布式块存储。
2. **文件系统**：由于 PostgreSQL 将数据存储在文件中，因此需要在块存储设备上架设文件系统。根据底层块存储设备的不同，可以选用单机文件系统（如 ext4）或分布式文件系统 [PolarDB File System（PFS）](https://github.com/ApsaraDB/PolarDB-FileSystem)。
3. **数据库**：PolarDB for PostgreSQL 的编译和部署环境。

以下表格给出了三个层次排列组合出的的不同实践方式：

|                                                                                                                                                               | 块存储                 | 文件系统                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------- |
| [实践 1（极简本地部署）](/zh/polardb/deploying/db-localfs/)                                                                                                                     | 本地 SSD               | 单机文件系统（如 ext4） |
| [实践 2（生产环境最佳实践）](/zh/polardb/deploying/storage-aliyun-essd/) [视频](https://developer.aliyun.com/live/249628) | 阿里云 ECS + ESSD 云盘 | PFS                     |
