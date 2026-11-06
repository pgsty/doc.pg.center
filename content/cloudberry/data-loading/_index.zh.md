---
title: "数据加载概述"
linkTitle: "加载数据"
description: "Apache Cloudberry 主要通过加载工具将外部数据转换为外部表（或外表）来加载数据。"
weight: 50
icon: "fa-solid fa-file-import"
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/index.md"
---

然后，Apache Cloudberry 从这些外部表读取数据，或将数据写入这些外部表，以实现外部数据加载。

## 加载过程 {#loading-process}

将外部数据加载到 Apache Cloudberry 的一般过程如下：

1. 评估数据加载场景（例如数据源位置、数据类型和数据量），并选择适当的加载工具。
2. 设置并启用加载工具。
3. 创建外部表，在 `CREATE EXTERNAL TABLE` 语句中指定加载工具的协议、数据源地址、数据格式等信息。
4. 创建外部表后，可以直接使用 `SELECT` 语句查询外部表中的数据，也可以使用 `INSERT INTO SELECT` 从外部表导入数据。

## 加载方法和场景 {#loading-methods-and-scenarios}

Apache Cloudberry 提供多种数据加载方案，你可以根据不同的数据源选择不同的数据加载方法。

| 加载方法              | 数据源                                                 | 数据格式                                                  | 是否并行 |
| -------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------ | -------- |
| [`copy`](/cloudberry/data-loading/files/load-data-using-copy/)                     | 本地文件系统<br /><br />• Coordinator 节点主机（单个文件）<br />• Segment 节点主机（多个文件） | • TXT<br />• CSV<br />• 二进制                                             | 否       |
| [`file://` 协议](/cloudberry/data-loading/files/load-data-using-file-protocol/)         | 本地文件系统（本地 Segment 主机，只允许超级用户访问） | • TXT<br />• CSV                                             | 是      |
| [`gpfdist`](/cloudberry/data-loading/files/load-data-using-gpfdist/)    | 本地主机上的文件或可通过内部网络访问的文件   | • TXT<br />• CSV<br />• `FORMAT` 子句支持的任意分隔文本格式<br />• XML 和 JSON（需要通过 YAML 配置文件转换为文本格式） | 是      |
| [`gpfdists`](/cloudberry/data-loading/files/load-data-using-gpfdists/)（安全的 `gpfdist`） | 本地主机上的文件或可通过内部网络访问的文件（使用 SSL 加密）   | • TXT<br />• CSV<br />• `FORMAT` 子句支持的任意分隔文本格式<br />• XML 和 JSON（需要通过 YAML 配置文件转换为文本格式） | 是      |
| [使用 `gpload` 批量加载](/cloudberry/data-loading/files/load-data-using-gpload/)（底层工作进程为 `gpfdist`） | 本地主机上的文件或可通过内部网络访问的文件   | • TXT<br />• CSV<br />• `FORMAT` 子句支持的任意分隔文本格式<br />• XML 和 JSON（需要通过 YAML 配置文件转换为文本格式） | 是      |
| [`s3://` 协议](/cloudberry/data-loading/cloud/load-data-from-s3/)         | Amazon S3 和兼容 S3 的对象存储 | • TXT<br />• CSV<br />• `FORMAT` 子句支持的任意分隔文本格式                                             | 是      |
| [`pxf://` 协议](/cloudberry/data-loading/cloud/load-data-using-pxf/)         | 对象存储（S3、Azure、GCS）、Hadoop 系统（HDFS、Hive、HBase）、SQL 数据库 | • 文本<br />• Avro<br />• JSON<br />• Parquet<br />• ORC<br />• CSV                                             | 是      |
| [创建外部 Web 表](/cloudberry/data-loading/load-data-from-web-services/)         | 从网络服务或任何可通过命令行访问的来源提取的数据 | • TXT<br />• CSV                                             | 是      |
| [Kafka FDW](/cloudberry/data-loading/load-data-from-kafka-using-fdw/)         | 来自 Apache Kafka 的流数据 | • JSON<br />• CSV                                             | 否      |

## 进一步了解 {#learn-more}
