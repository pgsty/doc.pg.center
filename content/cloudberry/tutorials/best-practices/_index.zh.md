---
title: "最佳实践汇总"
linkTitle: "最佳实践"
description: "Apache Cloudberry 最佳实践汇总。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/index.md"
---

## 数据模型 {#data-model}

Apache Cloudberry 是一个采用无共享架构的分析型 MPP 数据库。这种模型与高度规范化的事务型 SMP 数据库有很大差异。因此，建议遵循以下最佳实践。

- Apache Cloudberry 最适合采用面向 MPP 分析处理的非规范化模式设计，例如星型模式或雪花模式：使用大型事实表连接多个较小的维度表。
- 表之间执行连接时，连接列应使用相同的数据类型。

参见[模式设计](/cloudberry/tutorials/best-practices/schema-design-best-practices/)。

## 堆存储与追加优化存储 {#heap-vs-append-optimized-storage}

- 对需要反复执行批量和单行 `UPDATE`、`DELETE`、`INSERT` 操作的表和分区，使用堆存储。
- 对需要并发执行 `UPDATE`、`DELETE`、`INSERT` 操作的表和分区，使用堆存储。
- 对初始加载后很少更新、后续仅以大批量方式插入数据的表和分区，使用 AO 表。
- 避免对 AO 表执行单行 `INSERT`、`UPDATE` 或 `DELETE` 操作。
- 避免对 AO 表并发执行批量 `UPDATE` 或 `DELETE` 操作。并发批量 `INSERT` 操作可以接受。

参见[堆存储或追加优化存储](/cloudberry/tutorials/best-practices/schema-design-best-practices/#heap-storage-or-append-optimized-storage)。

## 行存储与列存储 {#row-vs-column-oriented-storage}

- 对需要反复执行事务、需要更新并频繁插入数据的工作负载，使用行存储。
- 表查询需要读取大量列时，使用行存储。
- 对通用或混合型工作负载，使用行存储。
- 查询只读取少量列且在少数列上执行聚合时，使用列存储。
- 对经常单独更新、而不会修改行中其他列的列，使用列存储。

参见[行存储或列存储](/cloudberry/tutorials/best-practices/schema-design-best-practices/#row-or-column-orientation)。

## 压缩 {#compression}

- 对大型 AO 表和分区表使用压缩，以改善整个系统的 I/O。
- 在数据所在的层级设置列压缩选项。
- 在更高压缩级别带来的收益与压缩、解压所需的时间和 CPU 周期之间进行权衡。

参见[压缩](/cloudberry/tutorials/best-practices/schema-design-best-practices/)。

## 分布 {#distributions}

- 为所有表显式定义列分布或随机分布。不要使用默认值。
- 使用单个列，让数据在所有 Segment 之间均匀分布。
- 不要按查询 `WHERE` 子句中使用的列进行分布。
- 不要按日期或时间戳分布。
- 永远不要使用同一列进行表分布和分区。
- 对经常连接的大表按相同列进行分布，以实现本地连接，从而显著改善性能。
- 为确保没有数据倾斜，应在初始加载和增量加载后验证数据是否均匀分布。

参见[数据分布](/cloudberry/tutorials/best-practices/schema-design-best-practices/)。

## 资源队列内存管理 {#resource-queue-memory-management}

- 将 `vm.overcommit_memory` 设为 2。
- 不要将操作系统配置为使用大页。
- 使用 `gp_vmem_protect_limit` 设置每个 Segment 数据库实例可为*所有*工作分配的最大内存。
- 可以通过以下方式计算 gp_vmem，从而使用 `gp_vmem_protect_limit`：
    - `gp_vmem`——Apache Cloudberry 可用的总内存

        - 如果系统总内存小于 256 GB，使用以下公式：

            ```shell
            gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.7
            ```

        - 如果系统总内存大于或等于 256 GB，使用以下公式：

            ```shell
            gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM)) / 1.17
            ```

        其中，`SWAP` 是主机的交换空间，单位为 GB；`RAM` 是主机的 RAM，单位为 GB。

    - `max_acting_primary_segments`——由于主机或 Segment 故障而激活镜像 Segment 时，一台主机上可能运行的主 Segment 最大数量。
    - `gp_vmem_protect_limit`

        ```shell
        gp_vmem_protect_limit = gp_vmem / acting_primary_segments
        ```

        转换为 MB 后，将结果设置为配置参数的值。

- 在生成大量工作文件的场景中，使用以下公式计算 `gp_vmem` 因子，以计入工作文件：
    - 如果系统总内存小于 256 GB：

        ```shell
        gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM - (300KB *
              total_#_workfiles))) / 1.7
        ```

    - 如果系统总内存大于或等于 256 GB：

        ```shell
        gp_vmem = ((SWAP + RAM) – (7.5GB + 0.05 * RAM - (300KB *
              total_#_workfiles))) / 1.17
        ```

- 永远不要将 `gp_vmem_protect_limit` 设置得过高，也不要设置为大于系统物理 RAM 的值。
- 使用计算出的 `gp_vmem` 值计算操作系统参数 `vm.overcommit_ratio` 的设置值：

    ```shell
    vm.overcommit_ratio = (RAM - 0.026 * gp_vmem) / RAM
    ```

- 使用 `statement_mem` 为每个 Segment 数据库分配查询使用的内存。
- 使用资源队列设置队列中查询可使用的活动查询数量（`ACTIVE_STATEMENTS`）和内存量（`MEMORY_LIMIT`）。
- 将所有用户关联到资源队列。不要使用默认队列。
- 根据工作负载和时段的实际需求设置 `PRIORITY`。避免使用 MAX 优先级。
- 确保资源队列的内存分配不超过 `gp_vmem_protect_limit` 的设置值。
- 动态更新资源队列设置，使其与每日运行流程相匹配。

参见[设置 Cloudberry 推荐的操作系统参数](/cloudberry/build/source/system-settings/)。

## 分区 {#partitioning}

- 只对大型表进行分区。不要对小表分区。
- 仅当可以根据查询条件执行分区消除（分区剪枝）时，才使用分区。
- 优先使用范围分区，而不是列表分区。
- 根据常用列（例如日期列）对表进行分区。
- 永远不要使用同一列进行表分区和分布。
- 不要使用默认分区。
- 不要使用多级分区；应减少分区数量，并在每个分区中存储更多数据。
- 检查查询的 `EXPLAIN` 计划，验证查询是否只扫描分区表的必要部分（是否消除了分区）。
- 列存储会使每个 Segment 上的每一列都产生物理文件，因此不要创建过多的列存储分区：`physical files = segments x columns x partitions`

参见[模式设计](/cloudberry/tutorials/best-practices/schema-design-best-practices/)。

## 索引 {#indexes}

- 一般情况下，Apache Cloudberry 不需要索引。
- 对需要高选择性查询的高基数列存储表，为单列创建索引以支持深入查询。
- 不要为经常更新的列创建索引。
- 可以考虑在向表加载数据前删除索引。加载完成后，为表重新创建索引。
- 创建选择性较高的 B-树索引。
- 不要对会更新的列创建位图索引。
- 避免对唯一列、基数非常高或非常低的数据使用位图索引。列具有低基数（100 到 100,000 个不同值）时，位图索引的效果最佳。
- 不要将位图索引用于事务型工作负载。
- 一般不要为分区表创建索引。如果确实需要索引，索引列必须不同于分区列。

## 监控与维护 {#monitoring-and-maintenance}

- 执行“推荐的监控与维护任务”。
- 在安装时以及之后定期运行 `gpcheckperf`，保存输出，以便比较系统性能随时间的变化。
- 使用所有可用工具，了解系统在不同负载下的行为。
- 检查任何异常事件，确定其原因。
- 定期查看执行计划监控系统上的查询活动，确保查询以最佳方式运行。
- 检查计划，确定是否使用了索引，以及是否按预期执行了分区消除。
- 了解系统日志文件的位置和内容，并定期监控，而不是只在出现问题时查看。

参见[系统监控与维护](/cloudberry/tutorials/best-practices/system-monitor-and-maintain-best-practices/)、[查询分析](/cloudberry/performance/optimize-queries/analyze-query-performance/)。

## ANALYZE {#analyze}

- 确定是否确实需要分析数据库。如果 `gp_autostats_mode` 设为 `on_no_stats`（默认值）且表未分区，则不需要分析。
- 处理大量表时，优先使用 `analyzedb` 而不是 `ANALYZE`，因为前者不需要分析整个数据库。`analyzedb` 工具会增量并发地更新指定表的统计信息。对于 AO 表，只有统计信息不是最新时，`analyzedb` 才会增量更新统计信息；对于堆表，统计信息始终会更新。`ANALYZE` 不会更新 `analyzedb` 用来判断表统计信息是否最新的表元数据。
- 需要时，在表级别有选择地运行 `ANALYZE`。
- 在显著改变底层数据的 `INSERT`、`UPDATE` 和 `DELETE` 操作后，始终运行 `ANALYZE`。
- 执行 `CREATE INDEX` 操作后，始终运行 `ANALYZE`。
- 如果对超大表运行 `ANALYZE` 耗时过长，只对连接条件、`WHERE` 子句、`SORT`、`GROUP BY` 或 `HAVING` 子句中使用的列运行 `ANALYZE`。
- 处理大量表时，使用 `analyzedb` 而不是 `ANALYZE.`。
- 每次向分区表添加新分区时，在根分区上运行 `analyzedb`。此操作会并行分析叶子分区，并将更新的统计信息合并到根分区。

参见[使用 ANALYZE 更新统计信息](/cloudberry/performance/update-stats-using-analyze/)。

## VACUUM {#vacuum}

- 执行大量 `UPDATE` 和 `DELETE` 操作后运行 `VACUUM`。
- 不要运行 `VACUUM FULL`。应执行 `CREATE TABLE...AS` 操作，然后重命名并删除原表。
- 定期对系统目录运行 `VACUUM`，避免目录膨胀以及必须对目录表运行 `VACUUM FULL`。
- 永远不要对目录表中的 `VACUUM` 发出 `kill` 命令。

参见[管理数据库膨胀](/cloudberry/tutorials/best-practices/manage-bloat/)。

## 加载 {#loading}

- 随着 Segment 数量增加，最大化并行度。
- 将数据均匀分布到尽可能多的 ETL 节点上。
    - 将超大数据文件拆分成大小相等的部分，并将数据分散到尽可能多的文件系统中。
    - 每个文件系统运行两个 `gpfdist` 实例。
    - 尽可能在多个网络接口上运行 `gpfdist`。
    - 使用 `gp_external_max_segs` 控制从 `gpfdist` 进程请求数据的 Segment 数量。
    - 始终使 `gp_external_max_segs` 与 `gpfdist` 进程数构成整数倍关系。
- 向已有表加载数据前始终删除索引，加载后重新创建索引。
- 加载出错后运行 `VACUUM`，回收空间。

参见[加载数据](/cloudberry/tutorials/best-practices/load-data-best-practices/)。

## 安全 {#security}

- 保护 `gpadmin` 用户 ID，只允许必要的系统管理员访问该用户。
- 管理员只能在执行升级或扩容等特定系统维护任务时，以 `gpadmin` 身份登录 Cloudberry。
- 限制具有 `SUPERUSER` 角色属性的用户。超级用户角色会绕过 Apache Cloudberry 中的所有访问权限检查和资源排队；只有系统管理员才应获得超级用户权限。
- 数据库用户绝不能以 `gpadmin` 身份登录，ETL 或生产工作负载也绝不能以 `gpadmin` 身份运行。
- 为每个登录系统的用户、应用或服务分配独立的 Apache Cloudberry 角色。
- 对应用或 Web 服务，可以考虑为每个应用或服务创建独立角色。
- 使用组管理访问权限。
- 保护 root 密码。
- 为操作系统密码实施强密码策略。
- 确保重要的操作系统文件受到保护。

参见[安全](/cloudberry/tutorials/best-practices/security-best-practices/)。

## 加密 {#encryption}

- 加密和解密数据会产生性能开销；只加密确实需要加密的数据。
- 在生产系统实施任何加密方案前执行性能测试。
- 生产 Apache Cloudberry 系统中的服务器证书应由证书颁发机构（CA）签名，使客户端能够对服务器进行身份验证。如果所有客户端都位于同一组织内，CA 可以是本地 CA。
- 连接通过不安全链路时，客户端连接 Apache Cloudberry 应使用 SSL 加密。
- 对称加密方案使用同一个密钥进行加密和解密，性能优于非对称方案；只要能够安全共享密钥，就应使用对称加密。
- 使用加密函数加密磁盘上的数据。数据在数据库进程中加密和解密，因此必须使用 SSL 保护客户端连接，避免传输未加密的数据。
- 使用 gpfdists 协议保护 ETL 数据在加载到数据库或从数据库卸载时的安全。

参见[加密数据与数据库连接](/cloudberry/tutorials/best-practices/db-encryption-best-practices/)

## 高可用 {#high-availability}

> **注意** 以下准则适用于实际硬件部署，不适用于公有云基础设施，因为公有云中可能已经提供了高可用解决方案。

- 使用包含 8 到 24 块磁盘的硬件 RAID 存储方案。
- 使用 RAID 1、5 或 6，使磁盘阵列能够容忍一块磁盘故障。
- 在磁盘阵列中配置热备盘，使检测到磁盘故障后能够自动开始重建。
- 通过镜像 RAID 卷，防止整个磁盘阵列故障以及重建期间性能下降。
- 定期监控磁盘使用情况，并在需要时增加空间。
- 监控 Segment 数据倾斜，确保数据均匀分布，并且各 Segment 均匀消耗存储空间。
- 设置 Standby Coordinator，在主 Coordinator 故障时接管。
- 规划故障发生时如何将客户端切换到新的 Coordinator 实例，例如更新 DNS 中的 Coordinator 地址。
- 设置监控，在主实例故障时通过系统监控应用或电子邮件发送通知。
- 为所有 Segment 设置镜像。
- 将主 Segment 与其镜像放在不同主机上，以防范主机故障。
- 使用 `gprecoverseg` 工具及时恢复故障 Segment，恢复冗余并使系统重新达到最佳平衡。
- 考虑使用双集群配置，提供额外的冗余级别和查询处理吞吐量。
- 定期备份 Apache Cloudberry 数据库，除非数据可以轻易从源重新恢复。
- 如果备份保存在本地集群存储中，备份完成后将文件移到安全的集群外位置。
- 如果备份保存在 NFS 挂载中，使用 Dell EMC Isilon 等横向扩展 NFS 方案，防止 I/O 瓶颈。
- 考虑使用 Cloudberry 集成，将备份流式传输到 Dell EMC Data Domain 企业备份平台。

参见[高可用](/cloudberry/tutorials/best-practices/high-availability-best-practices/)。
