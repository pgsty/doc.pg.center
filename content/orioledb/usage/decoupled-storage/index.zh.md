---
title: 存储与计算分离
linkTitle: 存算分离
description: 使用实验性 S3 模式分离存储和计算，并从对象存储恢复实例。
weight: 40
type: docs
search_keywords: ["OrioleDB", "decoupled storage", "S3", "存算分离"]
upstream_link: https://www.orioledb.com/docs/usage/decoupled-storage
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-cloud
---


OrioleDB 提供存储与计算分离能力：将数据放在 S3 等独立存储层，在另一实例上运行计算层。这为数据和计算资源的管理提供了更好的扩展性与灵活性。

> [!WARNING]
>
> 此功能目前处于实验阶段，应谨慎使用。
>
> 使用 OrioleDB 并不要求 S3 存储。它是可选功能，通过相应配置参数启用。

## S3 数据库存储 {#s3-database-storage}

OrioleDB 实验性地支持将所有表和物化视图的数据存储在 S3 存储桶中。这有助于分离计算实例与数据存储、提高数据安全性，并在保留全部数据的同时扩缩计算实例或调整其架构。

> [!WARNING]
>
> S3 模式仅在开发构建（`IS_DEV=1`）中可用。生产构建无法开启 `orioledb.s3_mode`。

本地存储缓存最常访问的数据，并确保新增和更新以本地存储的写入速度进行，而不受 S3 传输速率限制。数据异步同步到 S3，但 S3 中的全部数据仍满足完整性要求。因此，可以用另一个空 PostgreSQL 实例连接该 S3 存储桶，取回上一次 PostgreSQL 检查点时的完整数据状态。这个空实例需要用下文的工具初始化，并将 OrioleDB 扩展配置为使用该存储桶。

使用 S3 功能前，应在创建 OrioleDB 表和物化视图之前设置以下参数：

- `orioledb.s3_mode`：是否使用 S3 模式，可设为 `on` 或 `off`，默认为 `off`。
- `archive_library = 'orioledb'`：使用 S3 模式时必须设置。
- `archive_mode = on`：使用 S3 模式时必须设置。
- `orioledb.s3_region`：S3 存储桶所在的区域。
- `orioledb.s3_host`：S3 存储桶的访问端点，不带 `https://` 前缀，例如 mybucket.s3-accelerate.amazonaws.com。
- `orioledb.s3_prefix`：添加在 S3 对象名称之前的前缀。如果端点中不包含存储桶名，可以在这里包含它。
- `orioledb.s3_use_https`：使用 HTTPS 连接 S3，否则使用 HTTP。默认为 `on`。请确保与服务器一致，尤其是连接 localhost 时。
- `orioledb.s3_accesskey`：用于存储桶认证的 AWS 访问密钥。
- `orioledb.s3_secretkey`：用于存储桶认证的 AWS 秘密密钥。
- `orioledb.s3_num_workers`：向 S3 存储桶同步数据的 AWS 工作进程数。更多工作进程可能加快同步，建议设为 20，通常已足够。
- `orioledb.s3_desired_size`：OrioleDB 表在本地存储上的目标总大小。超出此限制后，后台工作进程开始将本地数据逐出到 S3 存储桶，从而有效利用本地空间并平稳传输数据。要有效执行此限制，文件系统必须支持稀疏文件。
- `max_worker_processes`：PostgreSQL 工作进程数上限，必须容纳新增的 `orioledb.s3_num_workers` 和其他所有 PostgreSQL 工作进程。初始可设为 `orioledb.s3_num_workers` 加上原有的 `max_worker_processes` 值。

设置上述 GUC 参数后重启 postmaster。随后，所有使用 `using orioledb` 创建的表和物化视图都会与 S3 存储桶同步。

``` sql
CREATE TABLE s3_test
(
  id int8 NOT NULL,
  value1 float8 NOT NULL,
  value2 text NOT NULL,
  PRIMARY KEY(id)
)  USING orioledb
```

S3 模式下，所有表和物化视图都会增量同步到 S3，即只上传修改过的块。但对于未使用 `using orioledb` 创建的表和物化视图，OrioleDB 后台工作进程需要在每次检查点时计算文件校验和。因此，建议在大部分数据都使用 OrioleDB 引擎存储时采用 S3 模式。

为获得最佳效果，建议在 **General** 类型的 AWS S3 存储桶设置中启用 `Transfer acceleration`，其端点地址后缀为 `s3-accelerate.amazonaws.com`，并将存储桶与计算实例放在同一 AWS 区域。更好的选择是在与计算实例相同的 AWS 区域和子区域内使用 **Directory** 类型存储桶。

同一个 S3 存储桶只能连接一个数据库实例。实例启动时，会检查是否已有其他实例连接，以及存储桶是否兼容；检查不通过则无法启动。

如前所述，S3 模式仍处于实验阶段，主要限制如下。

1. OrioleDB 表和物化视图在 S3 存储桶中增量存储，但历史数据会永久保留。目前尚无安全移除旧数据的机制。
2. 主库与副本必须分别使用独立的 S3 存储桶。

以上限制都是暂时的，将在后续版本中消除。

## S3 加载工具 {#s3-loader-utility}

S3 加载工具可以将存储桶中的数据下载到任意本地机器的指定目录。

使用前需要为 Python 安装 `boto3` 和 `testgres`：

`pip install boto3 testgres`

运行脚本时，使用与 S3 PostgreSQL 集群配置一致的参数：

- `AWS_ACCESS_KEY_ID`：对应 `orioledb.s3_accesskey`。
- `AWS_SECRET_ACCESS_KEY`：对应 `orioledb.s3_secretkey`。
- `AWS_DEFAULT_REGION`：对应 `orioledb.s3_region`。
- `--endpoint`：对应 `orioledb.s3_host`，但应使用带 `https://` 或 `http://` 前缀的完整 URL，例如 `--endpoint=https://mybucket.s3-accelerate.amazonaws.com`、`--endpoint=https://mybucket.s3.amazonaws.com`，或本地实例的 `--endpoint=http://localhost:PORT`。
- `--prefix`：可选的对象路径前缀。如果端点中不含存储桶名，可以在这里包含它。端点示例为 `--endpoint=https://mybucket.s3-accelerate.amazonaws.com` 或 `--endpoint=https://mybucket.s3.amazonaws.com`。
- `--bucket-name`：`orioledb.s3_host` 中的 S3 存储桶名，例如 `--bucket-name=mybucket`。
- `--data-dir`：本地机器上接收数据的目标目录，例如 `--data-dir=mydata/`。
- `--verbose`：可选，输出详细信息。

`AWS_ACCESS_KEY_ID=<your access key> AWS_SECRET_ACCESS_KEY='<your secret key>' AWS_DEFAULT_REGION=<your region> python orioledb_s3_loader.py --endpoint=https://<your-bucket-endpoint> --data-dir='orioledb_data' --verbose`
