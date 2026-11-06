---
title: "Apache Cloudberry 功能概览"
linkTitle: "功能概览"
description: "Apache Cloudberry 基于最新的 PostgreSQL 14.4 内核构建，是现有开源 MPP 数据库中最先进、最成熟的产品之一。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/introduction/cbdb-overview.md"
---

> [!WARNING]
> 本版本文档仍在编写中！

Apache Cloudberry 具备高并发、高可用等多项特性，能够快速、高效地执行复杂计算，满足海量数据管理与计算的需求，广泛应用于多个领域。

本文概述 Apache Cloudberry 的功能。

## 面向不同场景的高效查询 {#efficient-queries-in-different-scenarios}

- Apache Cloudberry 支持在大数据分析环境和分布式环境中执行高效查询：

    - **大数据分析环境**：Apache Cloudberry 使用内置的 PostgreSQL 优化器，为分布式环境提供更好的支持，因此能够在处理大数据分析任务时生成更高效的查询计划。
    - **分布式环境**：Apache Cloudberry 内置了专门适配的开源 GPORCA 优化器，满足分布式环境中的查询优化需求。

- 采用静态和动态分区剪枝、聚合下推、连接过滤等多种技术，帮助你尽可能快速、准确地获得查询结果。
- 同时提供基于规则和基于代价的查询优化方法，帮助你生成更高效的查询执行计划。

## 多种数据存储形式 {#polymorphic-data-storage}

针对不同场景，Apache Cloudberry 支持多种存储格式，包括堆存储、AO 行存和 AOCS 列存。Apache Cloudberry 还支持分区表，你可以根据特定条件定义表分区。执行查询时，系统会自动排除查询不需要的子表，以提高查询效率。

> [!DETAILS] 点击查看详情
> - **均匀的数据分布**：通过 Hash 和随机两种数据分布方式，Apache Cloudberry 能更充分地发挥磁盘性能，解决 I/O 瓶颈问题。
> - **存储类型**：
>
>     - 行存储：适合经常查询大多数字段、存在大量随机行访问的场景。
>     - 列存储：在只需查询少量字段时，可大幅减少 I/O 操作，适合频繁访问大量数据的场景。
>
> - **专用存储模式**：Apache Cloudberry 提供堆存储、AO 行存、AOCS 列存等不同存储模式，以优化不同类型应用的性能。一张表可以在最细的分区粒度上选用不同的存储模式。
> - **支持分区表**：可以根据特定条件定义表分区。查询时，系统会自动排除不需要的子表，以提高查询效率。
> - **高效的数据压缩**：Apache Cloudberry 支持 Zlib 1-9、Zstandard 1~19 等多种压缩算法，以提升数据处理性能，并在 CPU 开销与压缩比之间取得平衡。
> - **小表优化**：建表时可以选择复制表，并指定自定义 Hash 算法，从而更灵活地控制数据分布。

## 多层数据安全 {#multi-layer-data-security}

Apache Cloudberry 支持使用函数加密数据，也支持透明数据加密（TDE），以加强对用户数据的保护。在 TDE 中，这些处理由 Apache Cloudberry 内核完成，对用户透明。TDE 支持的数据格式包括堆表、AO 行存和 AOCS 列存。除 AES 等常见加密算法外，Apache Cloudberry 还支持国密算法，允许将自有算法无缝集成到 TDE 流程中。

> [!DETAILS] 点击查看详情
> Apache Cloudberry 注重数据安全，提供多项安全保护措施，以满足不同数据库环境的需求，形成多层安全防护：
>
> - **数据库隔离**：Apache Cloudberry 的数据库之间不共享数据，从而在多数据库环境中实现隔离。如需跨数据库访问，可使用 DBLink 功能。
> - **内部数据组织**：数据库中数据的逻辑组织包含表、视图、索引、函数等数据对象，支持跨模式访问数据。
> - **数据存储安全**：Apache Cloudberry 提供不同存储模式以支持数据冗余，使用 AES 128、AES 192、AES 256、DES 及国密加密等方式保障数据存储安全。它还支持密文认证，包括 SCRAM-SHA-256、MD5、LDAP、RADIUS 等加密算法。
> - **用户数据保护**：Apache Cloudberry 支持通过函数加密和解密数据，也支持透明数据加密与解密。这些处理由 Apache Cloudberry 内核实现，无需用户交互，支持堆表、AO 行存和 AOCS 列存等数据格式。除 AES 等常见加密算法外，Apache Cloudberry 还支持国密算法，便于将自有算法加入透明数据加密流程。
> - **细粒度权限设置**：针对不同用户和对象（如模式、表、行、列、视图、函数）的需求，Apache Cloudberry 提供多种权限设置选项，包括 `SELECT`、`UPDATE`、执行权限和所有权。

## 数据加载 {#data-loading}

Apache Cloudberry 提供一系列高效、灵活的数据加载方案，满足不同的数据处理需求，包括并行、持续的数据加载，灵活的数据源和文件格式支持，多种 ETL 工具集成，以及流数据加载和高性能数据访问。

> [!DETAILS] 点击查看详情
> - **并行、持续的数据加载**：Apache Cloudberry 通过外部表技术支持大规模并行、持续的数据加载，并自动进行字符集转换，例如从 GBK 转为 UTF-8，使数据导入更加顺畅。
>
> - **灵活的数据源和文件格式支持**：Apache Cloudberry 支持外部文件服务器、Hive、HBase、HDFS、S3 等数据源，以及 CSV、Text、JSON、ORC、Parquet 等数据格式。数据库还可加载 Zip 等压缩数据文件。
>
> - **集成多种 ETL 工具**：Apache Cloudberry 集成了 DataStage、Informatica、Kettle 等 ETL 工具，便于处理数据。
>
> - **支持流数据加载**：Apache Cloudberry 可针对订阅的 Kafka 主题启动多个并行读取任务，将读取的记录缓存起来，在达到一定时间或记录数后通过 gpfdist 加载到数据库。这种方式能够保证数据完整、不重复、不丢失，适用于流数据采集和实时分析场景。Apache Cloudberry 支持每分钟数千万条记录的数据加载吞吐量。
>
> - **高性能数据访问**：PXF 是 Apache Cloudberry 的内置组件，可将外部数据源映射为 Apache Cloudberry 的外部表，实现并行、高速的数据访问。PXF 支持对混合数据生态的管理与访问，有助于实现数据编织（Data Fabric）架构。

## 多层容错 {#multi-layer-fault-tolerance}

为确保数据安全和服务连续性，Apache Cloudberry 采用了涵盖数据页、校验和、镜像节点配置及控制节点备份的多层容错机制。

> [!DETAILS] 点击查看详情
> - **数据页校验和**：在底层存储中，Apache Cloudberry 使用校验和机制检测坏块，确保数据完整性。
>
> - **镜像节点配置**：通过在 Segment（或数据节点）之间配置镜像节点，Apache Cloudberry 可以实现服务高可用和故障切换。一旦检测到主 Segment 故障，系统会自动将对应的镜像 Segment 提升为主 Segment。故障发生时正在执行的事务会回滚，需要重试。
>
> - **控制节点备份**：与 Segment 类似，Coordinator 节点（或控制节点）也可以配置备份节点或 Standby Coordinator，以应对 Coordinator 节点故障。如果主 Coordinator 发生故障，管理员必须使用 `gpactivatestandby` 激活 Standby Coordinator；该切换不会自动发生。

## 丰富的数据分析支持 {#rich-data-analysis-support}

Apache Cloudberry 提供强大的数据分析功能，提高数据处理、查询和分析的效率，满足多种复杂的数据处理、分析和查询需求。

> [!DETAILS] 点击查看详情
> - **并行优化器与执行器**：Apache Cloudberry 内核内置并行优化器和执行器，不仅兼容 PostgreSQL 生态，还支持数据分区剪枝、多种索引技术（包括 B-树、位图、Hash、BRIN、GIN），以及 JIT（表达式即时编译处理）。
>
> - **机器学习组件 MADlib**：Apache Cloudberry 集成 MADlib 组件，提供完全由 SQL 驱动的机器学习能力，使算法、算力和数据深度融合。
>
> - **支持多种编程语言**：Apache Cloudberry 为开发者提供 R、Python、Perl、Java、PostgreSQL 等多种编程语言，便于编写自定义函数。
>
> - **基于 MPP 引擎的高性能并行计算**：Apache Cloudberry 的 MPP 引擎支持高性能并行计算，与 SQL 无缝集成，可对 SQL 执行结果进行快速计算和分析。
>
> - **PostGIS 地理数据处理**：Apache Cloudberry 引入了支持 MPP 架构的升级版 PostGIS 2.X，进一步增强了地理空间数据处理能力。主要特性包括：
>
>      - 支持对象存储：可将大容量地理空间数据直接从对象存储（OSS）加载到数据库。
>      - 全面的空间数据类型支持：包括 geometry、geography 和 raster。
>      - 时空索引：提供时空索引技术，可有效加速空间和时间查询。
>      - 复杂的空间与地理计算：包括球面长度计算和空间聚合函数（如包含、覆盖、相交）。
>
> - **Apache Cloudberry 文本组件**：该组件支持使用 Elasticsearch 加速文件检索，相较于传统 GIN 数据文本查询，性能提升了一个数量级。它支持多种分词方式、自然语言处理及查询结果渲染。

## 灵活的工作负载管理 {#flexible-workload-management}

Apache Cloudberry 提供全面的工作负载管理能力，以有效利用和优化数据库资源，确保系统高效、稳定运行。其工作负载管理包含连接级、会话级和 SQL 级三个控制层次。

> [!DETAILS] 点击查看详情
> - **连接池 PgBouncer（连接级管理）**：Apache Cloudberry 通过连接池统一管理用户访问，限制同时活跃的用户数量，以提高效率，避免频繁创建和销毁服务进程造成资源浪费。连接池内存占用小，支持高并发连接，并使用 libevent 进行套接字通信以提高通信效率。
>
> - **资源组（会话级管理）**：Apache Cloudberry 通过资源组分析和归类典型工作负载，量化各类负载所需的 CPU、内存、并发等资源。你可以按工作负载的实际需求设置合适的资源组，并动态调整资源使用，以确保整体运行效率。同时，可以使用规则清理空闲会话，释放不必要的资源。
>
> - **动态资源组分配（SQL 级管理）**：Apache Cloudberry 通过动态资源组分配，在 SQL 语句执行前或执行过程中灵活分配资源，优先处理特定查询，缩短执行时间。

## 多方面兼容性 {#multiple-compatibility}

Apache Cloudberry 的兼容性涵盖 SQL 语法、组件、工具与程序、硬件平台和操作系统等多个方面，因此能够灵活适配不同工具、平台和语言。

> [!DETAILS] 点击查看详情
> - **SQL 兼容性**：Apache Cloudberry 兼容 PostgreSQL 和 Greenplum 语法，支持 SQL-92、SQL-99 和 SQL 2003 标准，包括 SQL 2003 OLAP 扩展，如窗口函数、`rollup` 和 `cube`。
>
> - **组件兼容性**：Apache Cloudberry 基于 PostgreSQL 14.4 内核，兼容大多数常用 PostgreSQL 组件和扩展。
>
> - **工具与程序兼容性**：能很好地连接各类 BI 工具、挖掘预测工具、ETL 工具和 J2EE/.NET 应用。
>
> - **硬件平台兼容性**：可运行于多种硬件架构，包括 X86、ARM、飞腾、鲲鹏和海光。
>
> - **操作系统兼容性**：兼容 CentOS、Ubuntu、麒麟、BC-Linux 等多种操作系统环境。
