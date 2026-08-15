---
title: "Project Metrics"
linkTitle: "Metrics"
weight: 80
description: "pgBackRest project code coverage metrics and quality statistics."
icon: fa-solid fa-list-check
module: [PGBACKREST]
categories: [Concept]
---


--------

## Code Coverage

pgBackRest aims to have complete function/branch/line coverage for the core C code in `/src`.

Function/line coverage is complete with no exceptions.

Branch coverage excludes branches inside macros and `assert()` calls. Macros have their own unit tests so they do not need to be tested everywhere they appear. Asserts are not expected to have complete branch coverage since they test cases that should always be true.

| Directory            |           Functions |             Branches |                 Lines |
|----------------------|--------------------:|---------------------:|----------------------:|
| build/common         |     32/32 (100.00%) |      72/72 (100.00%) |     268/268 (100.00%) |
| build/config         |     39/39 (100.00%) |    564/564 (100.00%) |   1142/1142 (100.00%) |
| build/error          |       6/6 (100.00%) |      22/22 (100.00%) |       71/71 (100.00%) |
| build/help           |     13/13 (100.00%) |    138/138 (100.00%) |     265/265 (100.00%) |
| build/postgres       |       8/8 (100.00%) |      58/58 (100.00%) |     149/149 (100.00%) |
| command              |     17/17 (100.00%) |    104/104 (100.00%) |     210/210 (100.00%) |
| command/annotate     |       1/1 (100.00%) |      12/12 (100.00%) |       30/30 (100.00%) |
| command/archive      |     14/14 (100.00%) |      98/98 (100.00%) |     189/189 (100.00%) |
| command/archive/get  |     10/10 (100.00%) |    208/208 (100.00%) |     447/447 (100.00%) |
| command/archive/push |     12/12 (100.00%) |    142/142 (100.00%) |     359/359 (100.00%) |
| command/backup       |     50/50 (100.00%) |    786/786 (100.00%) |   1640/1640 (100.00%) |
| command/check        |     13/13 (100.00%) |    106/106 (100.00%) |     214/214 (100.00%) |
| command/control      |       4/4 (100.00%) |      34/34 (100.00%) |       48/48 (100.00%) |
| command/expire       |     11/11 (100.00%) |    274/274 (100.00%) |     392/392 (100.00%) |
| command/help         |       8/8 (100.00%) |    178/178 (100.00%) |     283/283 (100.00%) |
| command/info         |     16/16 (100.00%) |    430/430 (100.00%) |     748/748 (100.00%) |
| command/local        |       1/1 (100.00%) |                  --- |         4/4 (100.00%) |
| command/remote       |       1/1 (100.00%) |        6/6 (100.00%) |       18/18 (100.00%) |
| command/repo         |       9/9 (100.00%) |    110/110 (100.00%) |     195/195 (100.00%) |
| command/restore      |     37/37 (100.00%) |    726/726 (100.00%) |   1350/1350 (100.00%) |
| command/server       |       6/6 (100.00%) |      24/24 (100.00%) |       81/81 (100.00%) |
| command/stanza       |       5/5 (100.00%) |    106/106 (100.00%) |     125/125 (100.00%) |
| command/verify       |     22/22 (100.00%) |    366/366 (100.00%) |     733/733 (100.00%) |
| common               |   146/146 (100.00%) |    624/624 (100.00%) |   1350/1350 (100.00%) |
| common/compress      |     12/12 (100.00%) |      24/24 (100.00%) |       80/80 (100.00%) |
| common/compress/bz2  |     13/13 (100.00%) |      20/20 (100.00%) |     123/123 (100.00%) |
| common/compress/gz   |     13/13 (100.00%) |      26/26 (100.00%) |     118/118 (100.00%) |
| common/compress/lz4  |     15/15 (100.00%) |      24/24 (100.00%) |     116/116 (100.00%) |
| common/compress/zst  |     13/13 (100.00%) |      12/12 (100.00%) |       96/96 (100.00%) |
| common/crypto        |     32/32 (100.00%) |      88/88 (100.00%) |     424/424 (100.00%) |
| common/error         |     33/33 (100.00%) |      66/66 (100.00%) |     179/179 (100.00%) |
| common/io            |     61/61 (100.00%) |    182/182 (100.00%) |     523/523 (100.00%) |
| common/io/filter     |     31/31 (100.00%) |      92/92 (100.00%) |     276/276 (100.00%) |
| common/io/http       |     58/58 (100.00%) |    292/292 (100.00%) |     685/685 (100.00%) |
| common/io/socket     |     28/28 (100.00%) |    110/110 (100.00%) |     339/339 (100.00%) |
| common/io/tls        |     37/37 (100.00%) |    122/122 (100.00%) |     409/409 (100.00%) |
| common/type          |   335/335 (100.00%) |    922/922 (100.00%) |   3123/3123 (100.00%) |
| config               |     93/93 (100.00%) |   1025/1026 (99.90%) |   1649/1649 (100.00%) |
| db                   |     23/23 (100.00%) |      94/94 (100.00%) |     301/301 (100.00%) |
| info                 |     48/48 (100.00%) |    240/240 (100.00%) |     712/712 (100.00%) |
| info/manifest        |     10/10 (100.00%) |    132/132 (100.00%) |     303/303 (100.00%) |
| postgres             |     36/36 (100.00%) |    140/140 (100.00%) |     336/336 (100.00%) |
| postgres/interface   |       4/4 (100.00%) |      10/10 (100.00%) |       35/35 (100.00%) |
| protocol             |     60/60 (100.00%) |    266/266 (100.00%) |     860/860 (100.00%) |
| storage              |     68/68 (100.00%) |    298/298 (100.00%) |     754/754 (100.00%) |
| storage/azure        |     26/26 (100.00%) |    164/164 (100.00%) |     487/487 (100.00%) |
| storage/cifs         |       2/2 (100.00%) |                  --- |         6/6 (100.00%) |
| storage/gcs          |     34/34 (100.00%) |    176/176 (100.00%) |     574/574 (100.00%) |
| storage/posix        |     29/29 (100.00%) |     165/166 (99.40%) |     328/328 (100.00%) |
| storage/remote       |     40/40 (100.00%) |    128/128 (100.00%) |     568/568 (100.00%) |
| storage/s3           |     31/31 (100.00%) |    194/194 (100.00%) |     651/651 (100.00%) |
| storage/sftp         |     39/39 (100.00%) |    408/408 (100.00%) |     762/762 (100.00%) |
| TOTAL                | 1705/1705 (100.00%) | 10608/10610 (99.98%) | 25128/25128 (100.00%) |

The C unit test modules in `/test/src/module` also have complete function/line coverage but are not included in the report.
