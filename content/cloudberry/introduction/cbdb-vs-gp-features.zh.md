---
title: "Apache Cloudberry 新特性"
description: "Apache Cloudberry 以 Greenplum Database 的开源版本为基础，并与 Greenplum **高度向后兼容**。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/introduction/cbdb-vs-gp-features.md"
---

如果你用过 Greenplum，就会对 Apache Cloudberry 感到熟悉：大多数 SQL 语法、工具和运维流程的使用方式都相同。

同时，Apache Cloudberry 在此基础上引入了许多新能力。它集成了更新的 PostgreSQL 内核，并在存储、查询优化、安全等方面提供了新特性。本页介绍其中的主要内容。

## 现代化的 PostgreSQL 内核 {#modern-postgresql-kernel}

Apache Cloudberry 的多个分支都紧密跟进 PostgreSQL 上游：

| 分支 | PostgreSQL 内核 | 状态 |
| ------ | ----------------- | ------ |
| `main` | PostgreSQL 16.x | 持续开发中 |
| `REL_2_STABLE` | PostgreSQL 14.x | 最新稳定版本，持续进行小版本升级；计划在后续 2.x 版本中引入更新的内核 |

此次内核升级带来了 Greenplum 原先不具备的一系列 PostgreSQL 上游能力，包括多范围类型、JSONB 下标访问、LZ4 TOAST 压缩、增量排序、`REINDEX CONCURRENTLY`、BRIN 索引、hash 分区、`UPSERT` 支持等。这些能力如同在上游 PostgreSQL 中一样开箱即用，同时保留了你所依赖的 MPP 架构。

## Apache Cloudberry 的主要特性 {#key-features-in-apache-cloudberry}

以下是 Apache Cloudberry 社区带来的新能力。

### 存储与数据格式 {#storage--data-formats}

| 特性 | 说明 |
| ------- | ----------- |
| [目录表](/cloudberry/operate-with-data/advanced-analytics/directory-tables/) | 一种用于统一管理本地存储或对象存储中非结构化数据的表类型。可以使用简单的 SQL 语句管理和分析非结构化数据对象。 |
| [PAX 存储格式](/cloudberry/operate-with-data/pax-table-format/) | 一种行列混合存储格式，结合了行存的批量写入性能与列存的读取性能，提高了缓存效率。支持 MVCC、Z 序排列、布隆过滤器、稀疏过滤，以及多种编码和压缩选项，同时适用于云对象存储和传统文件系统。 |

### 查询性能与优化 {#query-performance--optimization}

| 特性 | 说明 |
| ------- | ----------- |
| [增量物化视图](/cloudberry/performance/optimize-queries/use-incremental-materialized-view/) | 一种特殊的物化视图，在基表更新时仅刷新变化的数据，无需刷新整个视图。对于大型数据集，其速度比普通视图快数个数量级。 |
| [自动物化视图改写](/cloudberry/performance/optimize-queries/use-auto-materialized-view-to-answer-queries/) | 在查询规划阶段，Apache Cloudberry 可以自动使用增量物化视图满足部分或全部查询需求（AQUMV）。这对大表上的聚合查询和复杂计算尤其有效，可大幅缩短查询处理时间。 |
| [动态表](/cloudberry/performance/use-dynamic-tables/) | 类似物化视图的数据库对象，可按计划自动刷新。适用于加速湖仓环境中的查询，并自动处理数据管道，无需人工干预。 |
| [并行查询执行](/cloudberry/performance/optimize-queries/parallel-query-execution/) | 在单个 Segment 内，一条查询可使用多个 CPU 核并行扫描堆表和 AO/AOCO 表，提升每台主机仅部署少量 Segment 时的性能。 |
| [使用 RuntimeFilter 优化连接](/cloudberry/performance/optimize-queries/use-runtimefilter-to-optimize-queries/) | 在 HashJoin 之前使用布隆过滤器对大表进行预过滤，大幅降低内存访问开销。在适用场景中，RuntimeFilter 可将连接性能提高一倍。 |
| [在 AO 表上使用 IndexScan](/cloudberry/performance/optimize-queries/use-index-scan-on-ao-tables/) | 支持在追加优化表（AO 表）上使用 IndexScan，大幅减少含有 `ORDER BY` 和 `LIMIT` 子句的查询所需扫描的数据量。在最适合的场景中，原本需要数十分钟的查询可在 1 秒内返回。 |
| [AO 表上的唯一索引](/cloudberry/performance/optimize-queries/use-unique-index-on-ao-tables/) | 支持在 AO/AOCS 表上创建唯一索引和唯一约束，在存储引擎层保证数据唯一性。 |

### 安全 {#security}

| 特性 | 说明 |
| ------- | ----------- |
| [透明数据加密（TDE）](/cloudberry/security/transparent-data-encryption/) | 对静态存储的数据文件进行透明加密。采用两级密钥管理架构，支持 AES 和 SM4 算法，无需修改应用程序。 |
| [行级安全策略](/cloudberry/security/configure-row-level-security-policy/) | 表所有者可以定义细粒度访问策略，按用户过滤行。 |
| [密码策略](/cloudberry/security/set-password-profile/) | 使用命名的密码策略配置（profile）实施密码复杂度、有效期、登录失败后锁定及重复使用规则。这些配置可绑定到一个或多个数据库用户。 |

### 灵活部署 {#deployment-flexibility}

| 特性 | 说明 |
| ------- | ----------- |
| [单节点部署](/cloudberry/deployment/single-node/) | 无需 Segment 节点即可部署 Apache Cloudberry，用于开发、测试或轻量生产场景。在类似 PostgreSQL 的精简部署中使用 Cloudberry 的全部特性。 |
| [ARM 架构支持](/cloudberry/deployment/platform-requirements/) | 除 x86_64 之外，Apache Cloudberry 还全面支持 ARM/AARCH64 架构，可部署在更广泛的硬件上，包括云实例和 ARM 服务器。 |

### 运维与工具 {#operations--utilities}

| 特性 | 说明 |
| ------- | ----------- |
| [gpshrink](/cloudberry/reference/sys-utilities/gpshrink/) | 从利用率不足的主机上移除 Segment，对运行中的集群进行缩容，在集群容量超过需求时节省资源。 |
| [gpdemo](/cloudberry/reference/sys-utilities/gpdemo/) | 一条命令即可部署功能完整、包含多个 Segment 的集群，适合开发、测试和演示，无需处理完整生产部署的复杂性。 |

## 遵循 Apache 之道的开放治理 {#open-governance-with-the-apache-way}

以上成果离不开项目开放、由社区驱动的治理方式。Apache Cloudberry 在 Apache 软件基金会旗下开发，遵循 **Apache 之道（The Apache Way）**。这一经过实践验证的治理模式确保项目**保持厂商中立**，由社区驱动。贡献者来自多家组织，也包括独立开发者；决策在公开邮件列表上作出，而非闭门决定。

原来的 Greenplum Database 采用单一厂商治理模式，最终闭源，成为专有产品。Apache Cloudberry 属于社区，任何一家公司都无法将其关闭或转为私有。

完整的贡献者和提交者名单见[社区团队页面](https://cloudberry.apache.org/team)。

## 小结 {#summary}

Apache Cloudberry 并非停滞不前的分支，而是一个持续开发、不断现代化的 MPP 数据库。它在保持 Greenplum 兼容性的同时，持续引入更新的 PostgreSQL 内核、新存储引擎、更智能的查询优化、更强的安全性和灵活的部署选项。无论你是正在评估迁移的 Greenplum 用户，还是寻找强大开源 MPP 数据库的新用户，Apache Cloudberry 都值得考虑。
