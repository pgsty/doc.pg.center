---
title: Reproducing the pgbench benchmark
linkTitle: Reproducing the pgbench benchmark
description: Reproduce the OrioleDB beta18 and stock PostgreSQL 18.6 throughput comparison on the same hardware.
weight: 10
type: docs
search_keywords: ["OrioleDB", "pgbench"]
upstream_link: https://www.orioledb.com/pgbench-benchmark
upstream_source: orioledb-website
upstream_modified: true
upstream_notice: /orioledb/attribution/
icon: fa-solid fa-gauge-high
---


The two charts on the [upstream homepage](https://www.orioledb.com/) compare **OrioleDB-beta18** against a stock **PostgreSQL 18.6** on the same hardware, running the same load. This page is a literal, step-by-step recipe for regenerating those numbers from scratch.

## Hardware {#hardware}

An `c5d.metal` EC2 instance:

- 96 vCPU (48 physical cores × 2 threads), 2 sockets, Intel Xeon Platinum 8275CL @ 3.00 GHz
- 188 GB RAM
- 1 × local NVMe (938 GB) mounted at `/mnt`, ext4, `noatime`

If you use a different instance type or another cloud, only the absolute TPS numbers change; the shape of the curves and the ratio between the engines stay representative.

## OS setup {#os-setup}

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

Log out and back in for the `ulimit` change to take effect.

## Build dependencies {#build-dependencies}

``` bash
sudo apt-get -qq -y install \
    build-essential clang bison flex pkg-config git \
    libicu-dev libssl-dev libreadline-dev zlib1g-dev liblz4-dev libzstd-dev \
    libxml2-dev libxslt1-dev libperl-dev python3-dev python3-venv \
    libcurl4-openssl-dev
```

`libcurl4-openssl-dev` is required by OrioleDB for the decoupled-storage backends; skipping it makes the OrioleDB build fail.

## Build A — OrioleDB beta18 on the patched PostgreSQL {#build-a--orioledb-beta18-on-the-patched-postgresql}

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

## Build B — stock upstream PostgreSQL 18.6 {#build-b--stock-upstream-postgresql-186}

To make the comparison fair, PostgreSQL is built from the plain upstream `REL_18_6` tag (no OrioleDB patches). Loading `shared_preload_libraries = 'orioledb'` is turned off for this build.

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

## Driver harness {#driver-harness}

The sweep is driven by `ci/pgbench.py` from the OrioleDB source tree. It uses [`testgres`](https://pypi.org/project/testgres/) to spin up a cluster, run `pgbench` at every client count, and collect resource samples.

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

## Running the sweep {#running-the-sweep}

`ci/pgbench.py` builds the `read-only-9` and `read-write-proc` `pgbench` scripts internally and runs them at every client count in the `--clients` list.

### The OrioleDB arm {#the-orioledb-arm}

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

### The heap arm — against stock PostgreSQL {#the-heap-arm--against-stock-postgresql}

Point `PATH` at the stock build and pass `--engines=builtin`; the harness will skip `shared_preload_libraries` and use only the `public` schema.

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

Each arm takes about three and a half hours: it initialises a scale-1000 cluster (roughly 15 minutes) once, then runs `pgbench -M prepared -T 300` across all 17 client counts for both tests, 34 measurements in total.

## What the two tests do {#what-the-two-tests-do}

Both scripts are defined in `ci/pgbench.py`, are used with `-M prepared`, and run for 300 seconds per client count.

**`read-only-9`** — a single-statement transaction that selects nine random accounts by primary key:

``` sql
\set aid1 random(1, 100000 * :scale)
\set aid2 random(1, 100000 * :scale)
-- ... aid3 … aid9
SELECT abalance FROM pgbench_accounts
 WHERE aid IN (:aid1, :aid2, :aid3, :aid4, :aid5, :aid6, :aid7, :aid8, :aid9);
```

**`read-write-proc`** — the classic pgbench transaction wrapped in a plpgsql function, so each client sends a single round-trip that performs four updates and an insert:

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

For OrioleDB the harness also adds `PRIMARY KEY (bid, mtime, tid, aid, delta)` to `pgbench_history`, so inserts are spread across the tree rather than serialised on the rightmost page.

## Configuration summary {#configuration-summary}

| setting | value | why |
|----|----|----|
| `shared_buffers` | 32 GB | both engines get the same total engine cache (OrioleDB splits the 32 GB into 1 GB `shared_buffers` for catalogs plus 31 GB `orioledb.main_buffers`) |
| `max_wal_size` | 4 GB | matches the reference; small enough that heap sees frequent checkpoints, large enough that OrioleDB does not run out of WAL |
| `max_connections` | 300 | headroom above the widest client count (280) |
| `scale` | 1000 | dataset roughly 15 GB, fits in `shared_buffers`; the workload is CPU-bound, not I/O-bound |
| `--time=300` | 5-minute runs | shorter runs overshoot at low client counts and miss steady state at high ones |
| `-M prepared` | always | otherwise the workload is dominated by query planning |
{.wide .expand}
