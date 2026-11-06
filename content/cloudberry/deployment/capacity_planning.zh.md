---
title: "估算存储容量"
description: "要估算 Apache Cloudberry 系统能容纳多少数据，可参考以下计算方法。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/capacity_planning.md"
---

还应考虑在每台 Segment 主机上预留额外空间，用于存放备份文件和数据加载文件。

> [!TIP] 提示
> 要快速获得初步配置建议，可以试用[容量计算器](https://cloudberry.apache.org/sizing/)。输入数据量和基础设施类型（物理机、虚拟机或云），即可获得节点数量和每个节点规格的建议。结果仅为估算值，确定最终配置前应通过概念验证（POC）加以验证。

## 计算可用磁盘容量 {#calculating-usable-disk-capacity}

首先计算 Segment 主机上可用于数据存储的物理磁盘原始容量：

要计算 Apache Cloudberry 系统能容纳多少数据，需要先计算每台 Segment 主机的可用磁盘容量，再乘以 Apache Cloudberry 阵列中的 Segment 主机数量。首先计算 Segment 主机上可用于数据存储的物理磁盘原始容量（raw\_capacity），即：

```
disk_size * number_of_disks = raw_capacity
```

需要考虑文件系统格式化的开销（约 10%）以及使用的 RAID 级别。例如，使用 RAID-10 时，计算公式为：

```
(raw_capacity * 0.9) / 2 = formatted_disk_space
```

为获得最佳性能，不要将磁盘完全写满，而应将使用率保持在 70% 或以下。因此，可按以下公式计算可用磁盘空间：

```
formatted_disk_space * 0.7 = usable_disk_space
```

只使用 70% 的磁盘空间，可以让 Apache Cloudberry 将同一磁盘上剩余的 30% 用于临时文件和事务文件。如果主机系统具有可用于临时文件和事务文件的独立磁盘系统，可以指定一个表空间，让 Apache Cloudberry 将这些文件存放其中。更改文件存放位置可能会提高性能，具体取决于该磁盘系统的性能。

格式化 RAID 磁盘阵列并按建议的容量上限算出可用空间（usable\_disk\_space）后，还需要计算实际可用于用户数据的存储空间（`U`）。如果使用 Apache Cloudberry 镜像实现数据冗余，用户数据所占的空间将加倍（`2 * U`）。Apache Cloudberry 还需要预留一定空间，作为活动查询的工作区。工作区大小应约为用户数据大小的三分之一（工作区 = `U/3`）：

```
With mirrors: (2 * U) + U/3 = usable_disk_space
Without mirrors: U + U/3 = usable_disk_space
```

临时文件空间和用户数据空间的上述建议以典型分析型负载为前提。对于高并发负载，或查询需要大量临时空间的负载，预留更大的工作区可能更有利。通常，通过合理的负载管理，可以在减少工作区使用量的同时提高系统整体吞吐量。此外，还可以将临时空间和用户空间指定到不同的表空间，从而将两者隔离。

## 计算用户数据大小 {#calculating-user-data-size}

与所有数据库一样，原始数据加载到数据库后，占用空间会略有增加。平均而言，加载到数据库后，数据在磁盘上占用的空间约为原始数据的 1.4 倍，但实际大小可能更小或更大，具体取决于所用的数据类型、表存储类型、数据库内压缩等因素。

-   页面开销 — 数据加载到 Apache Cloudberry 后，会被划分为大小为 32KB 的页面。每个页面有 20 字节的页面开销。
-   行开销 — 在普通的堆存储表中，每行数据有 24 字节的行开销。追加优化表（AO 表）的行开销则只有 4 字节。
-   属性开销 — 对于数据值本身，每个属性值占用的空间取决于所选的数据类型。一般来说，应尽可能选择能存储数据的最小数据类型（前提是已知某列的可能取值）。
-   索引 — 在 Apache Cloudberry 中，索引与表数据一样，分布在各台 Segment 主机上。Apache Cloudberry 的默认索引类型为 B-树。由于索引大小取决于索引中不同值的数量以及要插入的数据，因此无法预先精确计算索引大小。不过，可以使用以下公式粗略估算。

    ```
    B-tree: unique_values * (data_type_size + 24 bytes)
    
    Bitmap: (unique_values * =number_of_rows * 1 bit * compression_ratio / 8) + (unique_values * 32)
    ```

## 计算元数据和日志的空间需求 {#calculating-space-requirements-for-metadata-and-logs}

在每台 Segment 主机上，还需要考虑 Apache Cloudberry 日志文件和元数据所占的空间：

-   **系统元数据** — 对于主机上运行的每个 Apache Cloudberry Segment 实例（主实例或镜像实例）或 Coordinator 实例，系统目录和元数据大约需要 20 MB 空间。
-   **预写式日志** — 对于主机上运行的每个 Apache Cloudberry Segment（主实例或镜像实例）或 Coordinator 实例，都要为预写式日志（WAL）分配空间。WAL 被划分为大小为 64 MB 的段文件。WAL 文件的最大数量为：

    ```
    max_wal_size / 64MB
    ```

    可以据此估算 WAL 的空间需求。Apache Cloudberry 实例的 checkpoint\_segments 默认设置为 8，这意味着主机上的每个 Segment 或 Coordinator 实例会分配 1088 MB 的 WAL 空间。

-   **Apache Cloudberry 日志文件** — 每个 Segment 实例和 Coordinator 实例都会生成数据库日志文件，这些文件会随时间不断增长。应为这些日志文件分配足够的空间，并采用某种日志轮转机制，以确保日志文件不会过大。
