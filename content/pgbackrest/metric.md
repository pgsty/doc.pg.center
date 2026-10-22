---
title: "Project Metrics"
linkTitle: "Metrics"
weight: 80
description: "pgBackRest project code coverage metrics and quality statistics."
icon: fa-solid fa-list-check
module: [PGBACKREST]
categories: [Concept]
upstream_link: "https://pgbackrest.org/metric.html"
---

--------

## Code Coverage

pgBackRest aims to have complete function/branch/line coverage for the core C code in `/src`.

Function/line coverage is complete with no exceptions.

Branch coverage excludes branches inside macros and `assert()` calls. Macros have their own unit tests so they do not need to be tested everywhere they appear. Asserts are not expected to have complete branch coverage since they test cases that should always be true.

| Directory            |            Functions |              Branches |                  Lines |
|----------------------|--------------------:|---------------------:|----------------------:|
| command              |      17/17 (100.00%) |     104/104 (100.00%) |      210/210 (100.00%) |
| command/annotate     |        1/1 (100.00%) |       12/12 (100.00%) |        30/30 (100.00%) |
| command/archive      |      14/14 (100.00%) |       98/98 (100.00%) |      191/191 (100.00%) |
| command/archive/get  |      10/10 (100.00%) |     208/208 (100.00%) |      441/441 (100.00%) |
| command/archive/push |      12/12 (100.00%) |     148/148 (100.00%) |      369/369 (100.00%) |
| command/backup       |      52/52 (100.00%) |     844/844 (100.00%) |    1716/1716 (100.00%) |
| command/check        |      13/13 (100.00%) |     108/108 (100.00%) |      216/216 (100.00%) |
| command/control      |        4/4 (100.00%) |       34/34 (100.00%) |        48/48 (100.00%) |
| command/expire       |      13/13 (100.00%) |     300/300 (100.00%) |      423/423 (100.00%) |
| command/help         |        8/8 (100.00%) |     178/178 (100.00%) |      283/283 (100.00%) |
| command/info         |      16/16 (100.00%) |     430/430 (100.00%) |      743/743 (100.00%) |
| command/local        |        1/1 (100.00%) |                   --- |          4/4 (100.00%) |
| command/remote       |        1/1 (100.00%) |         6/6 (100.00%) |        18/18 (100.00%) |
| command/repo         |        7/7 (100.00%) |     106/106 (100.00%) |      182/182 (100.00%) |
| command/restore      |      37/37 (100.00%) |     720/720 (100.00%) |    1337/1337 (100.00%) |
| command/server       |        6/6 (100.00%) |       24/24 (100.00%) |        81/81 (100.00%) |
| command/stanza       |        5/5 (100.00%) |     128/128 (100.00%) |      147/147 (100.00%) |
| command/verify       |      21/21 (100.00%) |     372/372 (100.00%) |      737/737 (100.00%) |
| common               |    160/160 (100.00%) |     690/690 (100.00%) |    1521/1521 (100.00%) |
| common/compress      |      12/12 (100.00%) |       24/24 (100.00%) |        80/80 (100.00%) |
| common/compress/bz2  |      13/13 (100.00%) |       20/20 (100.00%) |      123/123 (100.00%) |
| common/compress/gz   |      13/13 (100.00%) |       26/26 (100.00%) |      118/118 (100.00%) |
| common/compress/lz4  |      15/15 (100.00%) |       24/24 (100.00%) |      116/116 (100.00%) |
| common/compress/zst  |      13/13 (100.00%) |       12/12 (100.00%) |        96/96 (100.00%) |
| common/crypto        |      38/38 (100.00%) |       94/94 (100.00%) |      458/458 (100.00%) |
| common/error         |      33/33 (100.00%) |       66/66 (100.00%) |      179/179 (100.00%) |
| common/format        |      27/27 (100.00%) |       90/90 (100.00%) |      284/284 (100.00%) |
| common/io            |      61/61 (100.00%) |     182/182 (100.00%) |      523/523 (100.00%) |
| common/io/filter     |      31/31 (100.00%) |       92/92 (100.00%) |      276/276 (100.00%) |
| common/io/http       |      58/58 (100.00%) |     294/294 (100.00%) |      688/688 (100.00%) |
| common/io/socket     |      28/28 (100.00%) |     110/110 (100.00%) |      340/340 (100.00%) |
| common/io/tls        |      35/35 (100.00%) |     122/122 (100.00%) |      385/385 (100.00%) |
| common/type          |    335/335 (100.00%) |     936/936 (100.00%) |    3147/3147 (100.00%) |
| config               |      96/96 (100.00%) |    1035/1036 (99.90%) |    1675/1675 (100.00%) |
| db                   |      23/23 (100.00%) |       94/94 (100.00%) |      301/301 (100.00%) |
| info                 |      57/57 (100.00%) |     286/286 (100.00%) |      836/836 (100.00%) |
| info/manifest        |      46/46 (100.00%) |     696/696 (100.00%) |    1329/1329 (100.00%) |
| postgres             |      36/36 (100.00%) |     128/128 (100.00%) |      330/330 (100.00%) |
| postgres/interface   |        4/4 (100.00%) |       10/10 (100.00%) |        35/35 (100.00%) |
| protocol             |      61/61 (100.00%) |     268/268 (100.00%) |      865/865 (100.00%) |
| storage              |      84/84 (100.00%) |     382/382 (100.00%) |      948/948 (100.00%) |
| storage/azure        |      27/27 (100.00%) |     164/164 (100.00%) |      502/502 (100.00%) |
| storage/cifs         |        2/2 (100.00%) |                   --- |          6/6 (100.00%) |
| storage/gcs          |      36/36 (100.00%) |     198/198 (100.00%) |      685/685 (100.00%) |
| storage/posix        |      29/29 (100.00%) |      165/166 (99.40%) |      328/328 (100.00%) |
| storage/remote       |      51/51 (100.00%) |     148/148 (100.00%) |      671/671 (100.00%) |
| storage/s3           |      32/32 (100.00%) |     200/200 (100.00%) |      678/678 (100.00%) |
| storage/sftp         |      39/39 (100.00%) |     408/408 (100.00%) |      763/763 (100.00%) |
| TOTAL                |  1733/1733 (100.00%) |  10784/10786 (99.98%) |  25462/25462 (100.00%) |

The C unit test modules in `/test/src/module` also have complete function/line coverage but are not included in the report.
