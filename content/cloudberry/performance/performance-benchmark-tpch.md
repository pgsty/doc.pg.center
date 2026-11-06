---
title: "TPC-H: Decision Support Benchmark for Apache Cloudberry"
description: "Run the TPC-H benchmark automatically on an existing Apache Cloudberry cluster."
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/benchmark/performance-benchmark-tpch.md"
---

This tool is based on the benchmark tool [TPC-H](https://www.tpc.org/tpch/default5.asp).
This repo will guide you on how to run the TPC-H benchmark automatically on an existing Apache Cloudberry cluster in the Apache Cloudberry Sandbox.

> [!NOTE]
> The TPC-H is a decision support benchmark. It consists of a suite of business oriented ad-hoc queries and concurrent data modifications. The queries and the data populating the database have been chosen to have broad industry-wide relevance. This benchmark illustrates decision support systems that examine large volumes of data, execute queries with a high degree of complexity, and give answers to critical business questions. You can learn more from the [TPC-H official website](https://www.tpc.org/tpch/).

## Context {#context}

### Supported TPC-H Versions {#supported-tpc-h-versions}

TPC has published the following TPC-H standards over time:

| TPC-H Benchmark Version | Published Date | Standard Specification |
|-|-|-|
| 3.0.1 | 04/28, 2022| https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf |
| 3.0.0 | 02/18, 2021 | https://tpc.org/TPC_Documents_Current_Versions/pdf/tpc-h_v3.0.0.pdf|

## Setup {#setup}

### Prerequisites {#prerequisites}

This is a follow-up tutorial for previous bootcamp steps. Please make sure to have the environment ready for Apache Cloudberry Sandbox up and running.

### TPC-H Tools Dependencies {#tpc-h-tools-dependencies}

Make sure that `gcc` and `make` are installed on `cdw` for compiling the `dbgen` (data generation) and `qgen` (query generation).

You can install the dependencies on `cdw`:

```bash
docker exec -it $(docker ps -q) /bin/bash
yum -y install gcc make
```

The source code is from http://tpc.org/tpc_documents_current_versions/current_specifications5.asp.

### Packages {#packages}

TPC-H and TPC-DS packages are already placed under "cdw:/tmp/" folder.

```bash
[gpadmin@cdw tmp]$ ls -rlt
-rw-rw-r--  1 root    root    24520013 Jul 27 14:18 TPC-H-CBDB.tar.gz
-rw-rw-r--  1 root    root     7096941 Jul 27 14:18 TPC-DS-CBDB.tar.gz
```

### Execution {#execution}

To run the benchmark, login as `gpadmin` on `cdw` in the Apache Cloudberry Sandbox, and execute the following command:

```bash
su - gpadmin
tar xzf TPC-H-CBDB.tar.gz
cd ~/TPC-H-CBDB
./run.sh
```

The TPC-H benchmark needs a few minutes to run before you get the final report, which depends on your machine's hardware. You may check the TPC-H execution log information file under the same directory with a similar name as below.

```
tpch_20230727_145051.log
```
