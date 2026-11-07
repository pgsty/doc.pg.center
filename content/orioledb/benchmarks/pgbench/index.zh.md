---
title: 复现 pgbench 基准测试
linkTitle: 复现 pgbench 基准测试
description: 在相同硬件上复现 OrioleDB beta18 与原版 PostgreSQL 18.6 的吞吐量测试。
weight: 10
type: docs
search_keywords: ["OrioleDB", "pgbench"]
upstream_link: https://www.orioledb.com/pgbench-benchmark
upstream_source: orioledb-website
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-gauge-high
---


[上游首页](https://www.orioledb.com/)的两张图使用相同硬件与负载，对比 **OrioleDB beta18** 和未经修改的 **PostgreSQL 18.6**。本页逐步说明如何从零复现这些结果。

## 硬件 {#hardware}

一台 `c5d.metal` EC2 实例：

- 96 vCPU，48 个物理核心 × 2 线程，双路 Intel Xeon Platinum 8275CL @ 3.00 GHz。
- 188GB RAM。
- 一块 938GB 本地 NVMe，挂载于 `/mnt`，ext4，使用 `noatime`。

如果使用其他实例类型或云平台，绝对 TPS 会变化，但曲线形态与两引擎之间的比例仍具有代表性。

## 操作系统设置 {#os-setup}

``` bash
# format the local NVMe and mount at /mnt
sudo mkfs.ext4 -q -F -E nodiscard /dev/nvme1n1
sudo mount -o noatime /dev/nvme1n1 /mnt
sudo chown ubuntu:ubuntu /mnt

# 100 GiB of 2 MiB huge pages -- PostgreSQL uses them for shared_buffers
sudo sysctl -w vm.nr_hugepages=51200
echo "vm.nr_hugepages=51200" | sudo tee /etc/sysctl.d/99-oriole.conf

# raised file-descriptor limit
sudo tee /etc/security/limits.d/99-oriole.conf <<'EOF'
* soft nofile 65535
* hard nofile 65535
EOF

# core dumps go to /mnt so they don't fill the root filesystem
sudo sh -c 'echo "/mnt/%t_%p.core" > /proc/sys/kernel/core_pattern'
```

退出并重新登录，使 `ulimit` 变更生效。

## 构建依赖 {#build-dependencies}

``` bash
sudo apt-get -qq -y install \
    build-essential clang bison flex pkg-config git \
    libicu-dev libssl-dev libreadline-dev zlib1g-dev liblz4-dev libzstd-dev \
    libxml2-dev libxslt1-dev libperl-dev python3-dev python3-venv \
    libcurl4-openssl-dev
```

OrioleDB 的存算分离后端需要 `libcurl4-openssl-dev`，缺少它会导致构建失败。

## 构建 A：补丁版 PostgreSQL 上的 OrioleDB beta18 {#build-a--orioledb-beta18-on-the-patched-postgresql}

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

## 构建 B：上游原版 PostgreSQL 18.6 {#build-b--stock-upstream-postgresql-186}

为公平比较，PostgreSQL 从未应用 OrioleDB 补丁的上游 `REL_18_6` 标签构建，并关闭 `shared_preload_libraries = 'orioledb'`。

``` bash
git clone --branch REL_18_6 https://git.postgresql.org/git/postgresql.git \
    ~/postgres-stock
PRE=~/oriole-bench/pgbin/pg18-stock
cd ~/postgres-stock
./configure --enable-debug --disable-cassert --with-icu --with-ssl=openssl \
    --prefix=$PRE CC=clang CFLAGS="-O3 -fno-omit-frame-pointer"
make -j$(nproc) && make install
make -C contrib -j$(nproc) install
```

## 驱动框架 {#driver-harness}

OrioleDB 源码中的 `ci/pgbench.py` 驱动整组测试，使用 [`testgres`](https://pypi.org/project/testgres/) 启动集群，在每种客户端数下运行 pgbench，并采集资源样本。

``` bash
python3 -m venv ~/refbench-venv
~/refbench-venv/bin/pip install testgres psutil matplotlib

# `ci/pgbench.py` imports `telegram` unconditionally to (optionally) push status
# messages; stub it out if the bot isn't configured.
SITE=$(~/refbench-venv/bin/python -c "import site; print(site.getsitepackages()[0])")
cat > "$SITE/telegram.py" <<'PY'
class Bot:
    def __init__(self, *a, **k): pass
    def send_message(self, *a, **k): pass
    def send_document(self, *a, **k): pass
    def send_photo(self, *a, **k): pass
PY
```

## 运行整组测试 {#running-the-sweep}

`ci/pgbench.py` 在内部构建 `read-only-9` 和 `read-write-proc` 脚本，并对 `--clients` 列表中的每个客户端数执行。

### OrioleDB 组 {#the-orioledb-arm}

``` bash
PRE=~/oriole-bench/pgbin/beta18
mkdir -p /mnt/results-oriole

~/refbench-venv/bin/python \
    ~/oriole-bench/orioledb/ci/pgbench.py \
    --shared_buffers=32GB --max_wal_size=4GB \
    --clients=1,5,10,20,40,60,80,100,120,140,160,180,200,220,240,260,280 \
    --max_connections=300 --time=300 \
    --engines=orioledb --tests=read-only-9,read-write-proc \
    --scale=1000 --base_dir=/mnt/refbench-oriole \
    --results_dir=/mnt/results-oriole
```

### 原版 PostgreSQL heap 组 {#the-heap-arm--against-stock-postgresql}

将 `PATH` 指向原版构建，并传入 `--engines=builtin`。框架会跳过 `shared_preload_libraries`，只使用 `public` 模式。

``` bash
PRE=~/oriole-bench/pgbin/pg18-stock
mkdir -p /mnt/results-heap

~/refbench-venv/bin/python \
    ~/oriole-bench/orioledb/ci/pgbench.py \
    --shared_buffers=32GB --max_wal_size=4GB \
    --clients=1,5,10,20,40,60,80,100,120,140,160,180,200,220,240,260,280 \
    --max_connections=300 --time=300 \
    --engines=builtin --tests=read-only-9,read-write-proc \
    --scale=1000 --base_dir=/mnt/refbench-heap \
    --results_dir=/mnt/results-heap
```

每组约需三个半小时：先初始化一次 scale-1000 集群，约 15 分钟；然后对两项测试的全部 17 种客户端数运行 `pgbench -M prepared -T 300`，共 34 次测量。

## 两项测试的内容 {#what-the-two-tests-do}

两个脚本都定义在 `ci/pgbench.py`，使用 `-M prepared`，每种客户端数运行 300 秒。

**`read-only-9`**：单语句事务，按主键随机查询九个账户。

``` sql
\set aid1 random(1, 100000 * :scale)
\set aid2 random(1, 100000 * :scale)
-- ... aid3 … aid9
SELECT abalance FROM pgbench_accounts
 WHERE aid IN (:aid1, :aid2, :aid3, :aid4, :aid5, :aid6, :aid7, :aid8, :aid9);
```

**`read-write-proc`**：将经典 pgbench 事务包装在 PL/pgSQL 函数中，使每个客户端只需一次往返，即可完成四次更新和一次插入。

``` sql
CREATE FUNCTION pgbench_transaction(_aid int, _bid int, _tid int, _delta int)
    RETURNS void AS $$
BEGIN
    UPDATE pgbench_accounts SET abalance = abalance + _delta WHERE aid = _aid;
    PERFORM abalance FROM pgbench_accounts WHERE aid = _aid;
    UPDATE pgbench_tellers  SET tbalance = tbalance + _delta WHERE tid = _tid;
    UPDATE pgbench_branches SET bbalance = bbalance + _delta WHERE bid = _bid;
    INSERT INTO pgbench_history (tid, bid, aid, delta, mtime)
         VALUES (_tid, _bid, _aid, _delta, CURRENT_TIMESTAMP);
END;
$$ LANGUAGE plpgsql;
```

对于 OrioleDB，框架还会为 `pgbench_history` 添加 `PRIMARY KEY (bid, mtime, tid, aid, delta)`，将插入分散到整棵树，避免在最右页串行化。

## 配置汇总 {#configuration-summary}

| 设置 | 值 | 原因 |
|----|----|----|
| `shared_buffers` | 32 GB | 两引擎获得相同的引擎缓存总量；OrioleDB 将 32GB 分为目录使用的 1GB `shared_buffers` 和 31GB `orioledb.main_buffers` |
| `max_wal_size` | 4 GB | 与参考测试一致；足够小，使 heap 频繁执行检查点，又足够大，不致让 OrioleDB 耗尽 WAL 空间 |
| `max_connections` | 300 | 高于最大测试客户端数 280，留有余量 |
| `scale` | 1000 | 数据约 15GB，可放入 `shared_buffers`，负载受 CPU 而非 I/O 限制 |
| `--time=300` | 每次 5 分钟 | 更短测试会在低客户端数时高估表现，在高客户端数时未达到稳态 |
| `-M prepared` | 始终使用 | 否则查询规划会主导负载 |
{.wide .expand}
