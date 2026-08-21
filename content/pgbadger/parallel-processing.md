---
title: "Parallel Processing"
linkTitle: "Parallel Processing"
weight: 50
description: "Choose between parallel chunks of one log and parallel processing of many logs"
icon: fa-solid fa-gauge-high
module: [PGBADGER]
categories: [Task]
aliases: [/docs/pgbadger/parallel-processing/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger has two complementary multiprocessing modes. Choose according to the shape of the input, not simply the number of CPUs.

| Option | Parallel unit | Best fit | Main constraint |
|---|---|---|---|
| `-j N` / `--jobs N` | chunks of one log file | one large, seekable log | chunk boundaries can duplicate or omit a small number of queries |
| `-J N` / `--Jobs N` | whole log files | many independent logs | useful only when enough files are available to keep workers busy |

## Split one large file with `-j` {#single-file-jobs}

```console
$ pgbadger -j 8 /var/log/postgresql/postgresql.log
```

The upstream algorithm divides each file into `N` byte ranges, forks one parser per range, writes temporary binary statistics, then merges those statistics into the final report.

```text
for each log file
    divide the file into N chunks
    find each chunk's start and end offsets
    fork N parsers at those offsets
    write one temporary binary statistics file per parser
wait for the workers
merge the binary files and build the report
```

Because log records and multi-line statements do not align perfectly with byte offsets, up to roughly `N` queries per file may be truncated, omitted, or—more commonly—counted twice at chunk boundaries. Use this mode for aggregate analysis of very large files, not for a workflow that requires an exact forensic count of every record.

## Process many files with `-J` {#multiple-file-jobs}

```console
$ pgbadger -J 8 /var/log/postgresql/postgresql-*.log
```

Each worker owns a complete file, so this mode avoids the chunk-boundary gap. It becomes most useful with hundreds of small files and enough CPU and I/O capacity. The upstream documentation also permits `-J` for independent compressed files; single-file chunking with `-j` requires seekable, uncompressed input.

## Upstream benchmark {#benchmark}

The upstream manual reports these measurements on an 8-CPU host. Treat them as a comparison of the two algorithms, not as a prediction for current hardware.

One 9.5 GB file:

| Option | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 1h41m18 | 50m25 | 25m39 | 15m58 |
| `-J` | 1h41m18 | 54m28 | 41m16 | 34m45 |

Two hundred 10 MB files, 2 GB total:

| Option | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 20m15 | 9m56 | 5m20 | 4m20 |
| `-J` | 20m15 | 9m49 | 5m00 | 2m40 |

The practical default is `-j` for a few large files and `-J` for many small files. Both modes can be combined when the input and platform support it, but benchmark the combination: log parsing may become limited by storage throughput before CPU.

## Limits and temporary files {#limits-and-temporary-files}

- `-j` is not available for compressed or CSV input and relies on process forking, so it is not a Windows mode.
- Remote CSV parsing is not supported by the upstream remote-input path.
- Parallel analysis creates temporary files named like `tmp_pgbadgerXXXX.bin` under the selected temporary directory (by default the system temporary directory).
- Do not clean those files while pgBadger is running. Use `--tempdir` to place them on storage with sufficient capacity.
- Start with a modest worker count and watch CPU, read throughput, temporary-space consumption, and elapsed time.

