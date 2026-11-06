---
title: "gpshrink"
description: "Apache Cloudberry 使用系统工具 `gpshrink` 对集群进行缩容。"
weight: 250
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpshrink.md"
---

当集群资源闲置时，例如磁盘空间使用率持续低于 20%，或 CPU 和内存使用率较低，可以使用 `gpshrink` 缩小集群规模，节省服务器资源。用户可通过 `gpshrink` 工具移除冗余服务器上的 Segment，实现集群缩容。

gpshrink 工具分两个阶段运行：

1. **准备阶段**：收集数据库中所有需要重分布的用户表的信息。

2. **数据重分布阶段**：重分布数据库集群中所有表的数据，以适应扩容或缩容后的集群规模。

## 使用 gpshrink 缩容集群的步骤 {#steps-to-scale-in-a-cluster-using-gpshrink}

1. 创建一个三节点集群：

    ```bash
    make create-demo-cluster
    ```

2. 创建测试表，并检查缩容前的状态：

    ```sql
    -- Create table and insert data
    CREATE TABLE test(a INT); 
    INSERT INTO test SELECT i FROM generate_series(1,100) i;
    -- Check data distribution of the test table
    SELECT gp_segment_id, COUNT(*) FROM test GROUP BY gp_segment_id;
    -- Check metadata status
    SELECT * FROM gp_distribution_policy;
    SELECT * FROM gp_segment_configuration;
    ```

3. 创建 shrinktest 文件，列出要删除的 Segment：

    ```bash
    touch shrinktest
    ```

    Segment 信息格式应为：hostname|address|port|datadir|dbid|content|role。必须包含主 Segment 和镜像 Segment 的信息。要删除多个 Segment，应先列出 content 编号较大的 Segment。确保首选角色与实际角色一致，先列主实例，再列镜像。

    删除一个 Segment 的格式示例：

    ```bash
    i-thd001y0|i-thd001y0|7004|/home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast3/demoDataDir2|4|2|p
    i-thd001y0|i-thd001y0|7007|/home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast_mirror3/demoDataDir2|7|2|m
    ```

4. 运行两次 `gpshrink` 命令：

    ```bash
    # Preparation phase
    gpshrink -i shrinktest
    # Redistribution phase
    gpshrink -i shrinktest
    ```

    |主要参数|说明|
    | ------------ | -----------------|
    | `-i` | 指定包含待删除 Segment 的文件。 |
    | `-c` | 清除已收集的表信息。 |
    | `-a` | 重分布后收集表统计信息。 |
    | `-d` | 设置重分布的最长执行时间，超时则终止。 |

    > [!TIP]
    > gpshrink 的两个运行阶段：
    >
    > - 第一条 `gpshrink -i shrinktest` 命令执行缩容准备：从 `shrinktest` 文件读取待删除的 Segment，创建表 `gpshrink.status`（记录 `gpshrink` 的状态）和 `gpshrink.status_detail`（记录各表的状态），并确定所有需要重分布的表。
    > - 第二条 `gpshrink -i shrinktest` 命令执行数据重分布，计算删除后的 Segment 规模，并在缩容后的集群中重分布数据。随后从 `gp_segment_configuration` 中移除相应 Segment。在此阶段，不建议创建新表，因为新表无法在缩容后的集群中重分布。部分语句可能因表被锁定而失败。

    > [!TIP]
    > - 如果第一次 `gpshrink -i shrinktest` 失败，可能是 `shrinktest` 文件存在错误。使用 `gpshrink -c` 清除已收集的数据，然后重新运行 `gpshrink -i shrinktest`。
    > - 如果第二次 `gpshrink -i shrinktest` 失败，请登录数据库检查表的状态，并根据需要继续重分布或回滚。

5. 检查缩容后的测试表状态：

    ```sql
    -- Check data distribution of the test table
    SELECT gp_segment_id, COUNT(*) FROM test GROUP BY gp_segment_id;
    -- Check metadata status
    SELECT * FROM gp_distribution_policy;
    SELECT * FROM gp_segment_configuration;
    ```
