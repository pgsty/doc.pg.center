---
title: 复现车辆跟踪基准测试
linkTitle: 复现车辆跟踪基准测试
description: 复现车辆位置上报负载，比较 OrioleDB beta18 与 PostgreSQL heap 的存储和 I/O。
weight: 20
type: docs
search_keywords: ["OrioleDB", "tracking"]
upstream_link: https://www.orioledb.com/tracking-benchmark
upstream_source: orioledb-website
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-location-dot
---


[上游首页](https://www.orioledb.com/)“效率”部分的两张图，在写入密集的时序负载下比较 **OrioleDB beta18** 与 **PostgreSQL 18.6 heap**：车队持续向分区表上报位置，同时读者查询近期历史。本页逐步说明如何从零复现这些结果。

## 硬件 {#hardware}

一台 `c5d.2xlarge` EC2 实例：

- 8 vCPU，4 个物理核心 × 2 线程，单路 Intel Xeon Platinum 8275CL @ 3.00 GHz。
- 16GB RAM，约 15GiB 可用。
- 一块 186GiB 本地 NVMe 实例存储，挂载于 `/mnt`，ext4，使用 `noatime`。
- Ubuntu 26.04 LTS，内核 7.0.0-1006-aws，Python 3.14。

这里实例大小比 pgbench 测试更重要。保留的数据量在 PostgreSQL 中约为内存的两倍，在 OrioleDB 中约等于内存。如果机器内存大得多，所有数据都能留在页缓存中，对比结果就会变化。

## 操作系统设置 {#os-setup}

``` bash
# format the local NVMe and mount at /mnt
sudo mkfs.ext4 -q -F -E nodiscard /dev/nvme1n1
sudo mount -o noatime /dev/nvme1n1 /mnt
sudo chown ubuntu:ubuntu /mnt

# raised file-descriptor limit
sudo tee /etc/security/limits.d/99-oriole.conf <<'EOF'
* soft nofile 65535
* hard nofile 65535
EOF
```

退出并重新登录，使 `ulimit` 生效。不预留大页：`huge_pages = try` 会回退到普通页，未预留内存交给操作系统页缓存，两引擎在此测试中都依赖它。

## 构建依赖 {#build-dependencies}

``` bash
sudo apt-get -qq -y install \
    build-essential clang bison flex pkg-config git \
    libicu-dev libssl-dev libreadline-dev zlib1g-dev liblz4-dev libzstd-dev \
    libxml2-dev libxslt1-dev libperl-dev python3-dev python3-venv \
    libcurl4-openssl-dev
```

OrioleDB 的存算分离后端需要 `libcurl4-openssl-dev`，缺少它会导致构建失败。

## 构建：补丁版 PostgreSQL 上的 OrioleDB beta18 {#build--orioledb-beta18-on-the-patched-postgresql}

``` bash
mkdir -p ~/oriole-bench/pgbin
git clone https://github.com/orioledb/postgres.git ~/oriole-bench/postgres-oriole
git clone https://github.com/orioledb/orioledb.git  ~/oriole-bench/orioledb

# beta18 requires the patches18_3 patch set
cd ~/oriole-bench/postgres-oriole && git checkout patches18_3
cd ~/oriole-bench/orioledb        && git checkout beta18

PRE=~/oriole-bench/pgbin/beta18
cd ~/oriole-bench/postgres-oriole
./configure --enable-debug --disable-cassert --with-icu --with-ssl=openssl \
    --prefix=$PRE CC=clang CFLAGS="-O3 -fno-omit-frame-pointer"
make -j$(nproc) && make install
make -C contrib -j$(nproc) install

cd ~/oriole-bench/orioledb
PATH=$PRE/bin:$PATH make -j$(nproc) USE_PGXS=1 ORIOLEDB_PATCHSET_VERSION=patches18_3
PATH=$PRE/bin:$PATH make install USE_PGXS=1 ORIOLEDB_PATCHSET_VERSION=patches18_3
```

与 [pgbench 测试](/zh/orioledb/benchmarks/pgbench/)不同，这里两组都使用同一构建。PostgreSQL 组以相同二进制文件启动，但不设置 `shared_preload_libraries = 'orioledb.so'`，因此使用补丁版 PostgreSQL 18.6 内置的 heap 访问方法。

## 驱动程序 {#driver}

负载由一个 Python 脚本驱动，除了标准库和上述构建的 PostgreSQL 客户端工具，没有其他依赖。

``` bash
mkdir -p ~/tracking && cd ~/tracking
curl -fsSLO https://www.orioledb.com/files/tracking-bench.py
```

[`tracking-bench.py`](/orioledb/assets/tracking-bench.py) 使用 `initdb` 创建新集群，加载表结构，运行 `--duration` 秒负载，每秒采样块设备，最后停止集群。默认参数即首页图表使用的设置。

## 依次运行两组 {#running-the-two-arms}

在同一台机器上依次运行，每组两小时。每次开始时，驱动程序都会清空并重建 `--pgdata`。

``` bash
PRE=~/oriole-bench/pgbin/beta18

python3 ~/tracking/tracking-bench.py --arm heap-idx \
    --pgbin $PRE --pgdata /mnt/pgdata --out-dir /mnt/results-heap

python3 ~/tracking/tracking-bench.py --arm oriole-pk \
    --pgbin $PRE --pgdata /mnt/pgdata --out-dir /mnt/results-oriole
```

`--iops-dev` 默认为 `nvme1n1`。如果你的设备不同，请指向保存 `--pgdata` 的设备。各输出目录包含：

| 文件 | 内容 |
|----|----|
| `resources.log` | 每秒一行 JSON，记录数据设备的读写 IOPS 和字节数 |
| `maint.log` | 每次维护循环输出，包括头部分区大小和各次轮转 |
| `summary.json` | IOPS 序列的中位数、百分位数，以及测试结束时的数据大小 |
| `copy1.log` … `copy5.log`、`reader.log`、`pg.log` | 写入流、读者和服务器日志；`reader.log` 应始终为空 |

## 负载内容 {#what-the-workload-does}

**表结构。** 每份位置报告是一行：

``` sql
CREATE TABLE provider_tpv_stream_part_000 (
    object_id uuid NOT NULL,
    source    text NOT NULL,
    lonlat    bytea NOT NULL,
    heading   double precision NOT NULL,
    accuracy  double precision NOT NULL,
    speed     double precision NOT NULL,
    ts        timestamp without time zone NOT NULL,
    rcvd_ts   timestamp without time zone NOT NULL
);
```

两组仅在索引方式上不同：

- `heap-idx`：堆表，在 `(object_id, ts, source, lonlat, heading, accuracy, speed, rcvd_ts)` 上建立覆盖 B 树索引。
- `oriole-pk`：OrioleDB 表，使用 `PRIMARY KEY (object_id, ts)`。行直接保存在主键树内，同样的查询无需二级索引。

**写入者。** 五条写入流，每条跟踪 6,000 辆车，每车每秒一份报告，总计每秒 30,000 行。每条流每秒用一次 `COPY … FROM STDIN` 写入 6,000 行，因此负载是一系列稳定的短批量插入，而非一次长时间 COPY。

**分区。** 写入始终指向头部分区 `provider_tpv_stream_part_000`，视图 `provider_tpv_stream` 合并全部分区。头部分区超过 1GB 后，重命名为下一个可用 `part_NNN`，记录覆盖的时间范围，再用结构相同的空头部分区替代。已封存分区的结束时间超过 3,500 秒前时，将其删除。因此稳态下大约保留最近一小时的报告。

**维护。** 每 30 秒执行一次循环，对头部分区 VACUUM，完成上述轮转，并向一个新封存分区添加 `CHECK (ts BETWEEN min AND max)` 约束。

**读者。** 循环启动新 `psql` 会话，读取随机车辆的近期历史，休眠 0.2 秒后重复，约每秒 4.5 次查询：

``` sql
SELECT * FROM provider_tpv_stream
 WHERE object_id = (SELECT object_id FROM seen_provider_ids ORDER BY random() LIMIT 1)
   AND ts BETWEEN (SELECT now() - (random()*4*3600) * interval '1 second')
              AND (SELECT now());
```

`seen_provider_ids` 在写入启动 20 秒后，从此前 15 秒的报告中取得，因此包含全部 30,000 个车辆 ID。

## 配置汇总 {#configuration-summary}

| 设置 | 值 | 原因 |
|----|----|----|
| `shared_buffers` | 512 MB（OrioleDB）/ 3.5 GB（heap） | 引擎缓存总量相同：OrioleDB 的 512MB `shared_buffers` 加 3GB `orioledb.main_buffers`，等于 heap 的 3.5GB |
| `orioledb.main_buffers` | 3 GB | OrioleDB 自身表的页缓存 |
| `orioledb.undo_buffers` | 512 MB | 内存撤销日志 |
| `orioledb.use_sparse_files` | on | 仅 OrioleDB 组 |
| `wal_buffers` | 256 MB | 两引擎相同 |
| `max_wal_size` / `min_wal_size` | 32 GB / 4 GB | 足够大，使两组检查点均由 `checkpoint_timeout` 而非 WAL 量触发 |
| `checkpoint_timeout` | 300 s | 配合 `checkpoint_completion_target = 0.9` |
| `fsync`、`synchronous_commit`、`full_page_writes` | on | 两引擎均保证完整持久性 |
| `wal_level` | replica | |
| `autovacuum` | on | 默认值 |
| `jit` | off | 负载没有分析查询 |
| `max_connections` | 200 | 为五个写入者、读者和维护连接留余量 |
| 写入者 | 5 条流 × 6,000 辆车 | 每秒 30,000 行 |
| 轮转 | 头部分区 1 GB，保留 3,500 s | 约保留一小时数据 |
| 时长 | 每组 7,200 s | 第一小时填满保留窗口，第二小时为稳态 |
{.wide .expand}
