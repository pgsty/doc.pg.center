---
title: Reproducing the vehicle-tracking benchmark
linkTitle: Reproducing the vehicle-tracking benchmark
description: Reproduce the vehicle-tracking workload to compare OrioleDB beta18 and PostgreSQL heap storage and I/O.
weight: 20
type: docs
search_keywords: ["OrioleDB", "tracking"]
upstream_link: https://www.orioledb.com/tracking-benchmark
upstream_source: orioledb-website
upstream_modified: true
upstream_notice: /orioledb/attribution/
icon: fa-solid fa-location-dot
---


The two charts in the Efficiency section of the [upstream homepage](https://www.orioledb.com/) compare **OrioleDB-beta18** against **PostgreSQL 18.6 heap** on a write-heavy time-series workload: a fleet of tracked vehicles streaming position reports into a partitioned table while a reader looks up recent history. This page is a literal, step-by-step recipe for regenerating those numbers from scratch.

## Hardware {#hardware}

A `c5d.2xlarge` EC2 instance:

- 8 vCPU (4 physical cores × 2 threads), 1 socket, Intel Xeon Platinum 8275CL @ 3.00 GHz
- 16 GB RAM (15 GiB usable)
- 1 × local NVMe instance store (186 GiB) mounted at `/mnt`, ext4, `noatime`
- Ubuntu 26.04 LTS, kernel 7.0.0-1006-aws, Python 3.14

The instance size matters more here than for pgbench. The retained data is roughly twice the RAM for PostgreSQL and about the size of the RAM for OrioleDB, so a machine with much more memory keeps everything in the page cache and the comparison shifts.

## OS setup {#os-setup}

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

Log out and back in for the `ulimit` change to take effect. No huge pages are reserved: `huge_pages = try` falls back to regular pages, and memory left unreserved goes to the OS page cache, which both engines rely on here.

## Build dependencies {#build-dependencies}

``` bash
sudo apt-get -qq -y install \
    build-essential clang bison flex pkg-config git \
    libicu-dev libssl-dev libreadline-dev zlib1g-dev liblz4-dev libzstd-dev \
    libxml2-dev libxslt1-dev libperl-dev python3-dev python3-venv \
    libcurl4-openssl-dev
```

`libcurl4-openssl-dev` is required by OrioleDB for the decoupled-storage backends; skipping it makes the OrioleDB build fail.

## Build — OrioleDB beta18 on the patched PostgreSQL {#build--orioledb-beta18-on-the-patched-postgresql}

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

Unlike the [pgbench benchmark](/orioledb/benchmarks/pgbench/), both arms here run on this one build. The PostgreSQL arm starts the same binaries without `shared_preload_libraries = 'orioledb.so'`, so its tables use the built-in heap access method of the patched PostgreSQL 18.6.

## Driver {#driver}

The workload is driven by a single Python script with no dependencies beyond the standard library and the PostgreSQL client tools of the build above.

``` bash
mkdir -p ~/tracking && cd ~/tracking
curl -fsSLO https://www.orioledb.com/files/tracking-bench.py
```

[`tracking-bench.py`](/orioledb/assets/tracking-bench.py) creates a fresh cluster with `initdb`, loads the schema, runs the workload for `--duration` seconds, samples the block device once a second, and stops the cluster. Its defaults are the settings used for the homepage charts.

## Running the two arms {#running-the-two-arms}

Run the arms one after the other on the same machine. Each takes two hours; the driver wipes and re-creates `--pgdata` at the start of a run.

``` bash
PRE=~/oriole-bench/pgbin/beta18

python3 ~/tracking/tracking-bench.py --arm heap-idx \
    --pgbin $PRE --pgdata /mnt/pgdata --out-dir /mnt/results-heap

python3 ~/tracking/tracking-bench.py --arm oriole-pk \
    --pgbin $PRE --pgdata /mnt/pgdata --out-dir /mnt/results-oriole
```

`--iops-dev` defaults to `nvme1n1`; point it at the device that holds `--pgdata` if yours differs. Each output directory contains:

| file | contents |
|----|----|
| `resources.log` | one JSON line per second: read/write IOPS and bytes of the data device |
| `maint.log` | output of every maintenance cycle, including the head-partition size and each rotation |
| `summary.json` | medians and percentiles of the IOPS series, data size at the end of the run |
| `copy1.log` … `copy5.log`, `reader.log`, `pg.log` | stream, reader and server logs; `reader.log` should stay empty |

## What the workload does {#what-the-workload-does}

**Schema.** Each position report is one row:

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

The two arms differ only in how this table is indexed:

- `heap-idx` — a heap table with a covering B-tree index on `(object_id, ts, source, lonlat, heading, accuracy, speed, rcvd_ts)`.
- `oriole-pk` — an OrioleDB table with `PRIMARY KEY (object_id, ts)`. OrioleDB stores rows in the primary-key tree itself, so no secondary index is needed for the same lookups.

**Writers.** Five streams, each tracking 6,000 vehicles, send one report per vehicle per second — 30,000 rows per second in total. Every second each stream issues one `COPY … FROM STDIN` with its 6,000 rows, so the load is a steady sequence of short bulk inserts rather than one long-running `COPY`.

**Partitioning.** Writers always target `provider_tpv_stream_part_000`, the head partition. A view `provider_tpv_stream` unions all partitions. Once the head grows past 1 GB it is renamed to the next free `part_NNN`, tagged with the time range it covers, and replaced by an empty head with the same structure. Sealed partitions whose range ends more than 3,500 seconds ago are dropped. In steady state the table therefore holds roughly the last hour of reports.

**Maintenance.** Every 30 seconds a loop vacuums the head partition, runs the rotation above, and adds a `CHECK (ts BETWEEN min AND max)` constraint to one newly sealed partition.

**Reader.** A loop starts a fresh `psql` session, reads the recent history of one random vehicle, sleeps 0.2 seconds and repeats — about 4.5 queries a second:

``` sql
SELECT * FROM provider_tpv_stream
 WHERE object_id = (SELECT object_id FROM seen_provider_ids ORDER BY random() LIMIT 1)
   AND ts BETWEEN (SELECT now() - (random()*4*3600) * interval '1 second')
              AND (SELECT now());
```

`seen_provider_ids` is taken 20 seconds after the writers start, from the reports of the preceding 15 seconds, so it contains all 30,000 vehicle ids.

## Configuration summary {#configuration-summary}

| setting | value | why |
|----|----|----|
| `shared_buffers` | 512 MB (OrioleDB) / 3.5 GB (heap) | both engines get the same total engine cache: OrioleDB's 512 MB `shared_buffers` plus 3 GB `orioledb.main_buffers` equals the heap arm's 3.5 GB `shared_buffers` |
| `orioledb.main_buffers` | 3 GB | OrioleDB's page cache for its own tables |
| `orioledb.undo_buffers` | 512 MB | in-memory undo log |
| `orioledb.use_sparse_files` | on | OrioleDB arm only |
| `wal_buffers` | 256 MB | same for both engines |
| `max_wal_size` / `min_wal_size` | 32 GB / 4 GB | large enough that every checkpoint in both arms is started by `checkpoint_timeout`, none by WAL volume |
| `checkpoint_timeout` | 300 s | with `checkpoint_completion_target = 0.9` |
| `fsync`, `synchronous_commit`, `full_page_writes` | on | full durability for both engines |
| `wal_level` | replica |  |
| `autovacuum` | on | the default |
| `jit` | off | the workload has no analytical queries |
| `max_connections` | 200 | headroom for five writers, the reader and maintenance |
| writers | 5 streams × 6,000 vehicles | 30,000 rows per second |
| rotation | 1 GB head, 3,500 s retention | about one hour of data kept |
| duration | 7,200 s per arm | the first hour fills the retention window, the second is steady state |
{.wide .expand}
