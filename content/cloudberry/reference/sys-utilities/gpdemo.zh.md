---
title: "gpdemo"
description: "使用内置的 `gpdemo` 脚本，只需一条命令即可快速部署具有指定数量 Segment 的集群。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpdemo.md"
---

`gpdemo` 与其他系统工具（如 `gpinitsystem`、`gpstart` 和 `gpstop`）一起安装在 `GPHOME/bin` 目录中。

> [!WARNING]
> 除部署单节点集群的情况外，不建议在生产环境中使用 `gpdemo`。

## 使用方法 {#how-to-use}

在目标服务器上安装 RPM 包并正确加载 `greenplum_path.sh` 后，即可运行 `gpdemo`。

### 使用默认设置部署 {#deploy-with-default-settings}

如果对数据目录位置、起始端口号或 Segment 数量没有特殊要求，可以直接运行不带参数的 `gpdemo`，快速部署集群：

```bash
gpdemo
```

运行此命令后，脚本会在当前路径下创建集群。集群的默认配置如下：

- Segment 数量：3
- 数据目录：`./datadirs`
- Coordinator 起始端口号：`7000`

> [!NOTE]
> 集群部署完成后，脚本会在当前目录中生成 `gpdemo-env.sh` 文件，其中包含集群的基本信息。使用 `gpdemo` 操作集群前，请运行 `source gpdemo-env.sh` 加载这些信息。
>
> 每次开启新的 shell 会话时都需要运行此命令。若要自动加载集群信息，可以将此命令加入 `~/.bashrc` 或 `~/.zshrc`。

### 使用自定义设置部署 {#deploy-with-customized-settings}

如果需要自定义集群的 Segment 数量、数据目录位置和起始端口号，请参阅以下说明。

#### 指定 Segment 数量 {#specify-segment-count}

默认部署时，集群包含 3 个 Segment。

要指定集群中的 Segment 数量，可以在 `gpdemo` 命令中添加 `NUM_PRIMARY_MIRROR_PAIRS` 参数。例如，要将 Segment 数量指定为 3，可以运行：

```bash
NUM_PRIMARY_MIRROR_PAIRS=3 gpdemo
```

> [!NOTE]
> - 每个 Segment 节点都由一个主节点和一个镜像节点组成。因此，参数值每增加 `1`，就会多创建 2 个节点。为便于发现数据分布问题，建议将该值设为奇数。
> - 参数值设为 0 时，将部署只有一个计算节点的集群。详情请参阅[部署单计算节点 Apache Cloudberry](/cloudberry/deployment/single-node/)。

#### 指定节点的数据目录 {#specify-the-data-directory-of-a-node}

集群中各节点的数据存储在当前目录的 `./datadirs` 子目录中。要设置集群的数据目录位置，可采用以下任一方法：

- 使用 `cd` 切换到目标目录，然后运行 `gpdemo`。
- 在 `gpdemo` 命令中指定 `DATADIRS` 参数来设置数据目录。例如：

    ```bash
    DATADIRS=/target/directory/ gpdemo
    ```

> [!NOTE]
> 集群部署完成后，如果要手动调整数据目录的位置（通过修改 `pg_hha.conf` 配置文件），可能需要了解 Coordinator 节点和 Segment 节点的默认目录。
>
> - 常规多节点模式（即 `NUM_PRIMARY_MIRROR_PAIRS` > 0）
>     - Coordinator：`./datadirs/qddir`
>     - Standby Coordinator：`./datadirs/standby`
>     - Segment
>         - 主实例：`./datadirs/dbfast<N>`，其中 `<N>` 为 Segment 编号。
>         - 镜像实例：`./datadirs/dbfast_mirror<N>`，其中 `<N>` 为 Segment 编号。
>
> - 单节点模式（即 `NUM_PRIMARY_MIRROR_PAIRS` = 0）
>     - Coordinator：`./datadirs/singlenodedir`
>     - Standby Coordinator：`./datadirs/standby`

#### 指定 Coordinator 节点的起始端口号 {#specify-the-initial-port-number-of-the-coordinator-node}

默认情况下，Coordinator 节点的端口号为 `7000`。从此端口号开始，集群中的所有其他节点依次分配连续的端口号。

要指定集群 Coordinator 节点的起始端口号，可以在 `gpdemo` 命令中添加 `PORT_BASE` 参数。例如：

```bash
PORT_BASE=7000 gpdemo
```

#### 为集群中的每个节点指定附加初始化参数 {#specify-additional-initialization-parameter-for-each-node-in-the-cluster}

`BLDWRAP_POSTGRES_CONF_ADDONS` 指定集群中每个节点的附加初始化参数。默认值 `fsync=off` 用于提高并发性能。

**在生产环境中，请使用 `export BLDWRAP_POSTGRES_CONF_ADDONS ="fsync=on"` 启用 fsync，否则数据库的 ACID 特性会受到影响。在单节点模式下，fsync 会自动启用。**

## 命令行选项 {#command-line-options}

`gpdemo` 提供以下命令行选项。也可以使用 `gpdemo -H` 查看。

| 选项 | 说明 |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-K` | 部署集群时跳过数据一致性检查。不建议使用此选项。 |
| `-c` | 检查端口占用情况，确认是否可以部署测试集群。<br /><br />运行 `gpdemo -c` 前，需要运行 `source gpdemo-env.sh` 加载集群的基本信息。该 `sh` 文件位于创建集群的目录中。 |
| `-d` | 删除测试集群。<br /><br />运行 `gpdemo -c` 前，需要运行 `source gpdemo-env.sh` 加载集群的基本信息。该 `sh` 文件位于创建集群的目录中。 |
| `-p` | 查看集群状态、Coordinator 和 Segment 节点的版本等信息。<br /><br />运行 `gpdemo -c` 前，需要运行 `source gpdemo-env.sh` 加载集群的基本信息。该 `sh` 文件位于创建集群的目录中。 |
| `-H ` 或 `-H` | `gpdemo -h` 输出简要帮助说明。`gpdemo -H` 输出更详细的帮助说明，包括环境变量等附加配置。 |
| `-v` | 检查当前 `gpdemo` 版本。 |
