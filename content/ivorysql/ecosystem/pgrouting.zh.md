---
title: pgRouting
linkTitle: pgrouting
description: IvorySQL v5.6 文档：pgRouting。
type: docs
weight: 440
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/5.9.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 概述 {#overview}

pgRouting 是一个基于 PostgreSQL/PostGIS 数据库构建的开源地理空间路由扩展库。它为数据库赋予了强大的网络分析功能，使其能够处理复杂的路径规划与图论计算问题，例如计算两点之间的最短路径、执行旅行推销员（TSP）分析或计算服务区范围等。它将路由算法直接嵌入到数据库中，从而避免了在应用层进行复杂的数据传输与计算。

该扩展的核心优势在于能够利用 PostgreSQL 强大的数据管理能力和 PostGIS 丰富的空间函数，直接在数据库内部对空间网络数据执行高效计算。这不仅简化了应用程序的开发流程，还通过减少数据移动大幅提升了大规模网络分析的性能。

pgRouting 广泛应用于物流配送、交通导航、网络分析、城市规划及供应链管理等多个领域。其开源特性吸引了全球开发者持续的贡献与完善，使其成为空间数据库领域进行路径分析和网络求解的首选工具之一。

## 2. 安装 {#installation}

> [!TIP]
>
> 环境中已经安装了IvorySQL5.6及以上版本，安装路径为/usr/local/ivorysql/ivorysql-5

### 2.1. 源码安装 {#source-installation}

- 安装依赖

对perl有依赖，perl一般在装IvorySQL时已经装上了，这里不用再装。 CMake版本要求 \>= 3.12, Boost版本 \>= 1.56

```
#安装依赖
sudo apt install cmake libboost-all-dev
```

- 编译安装

```
wget https://github.com/pgRouting/pgrouting/releases/download/v3.8.0/pgrouting-3.8.0.tar.gz
tar xvf pgrouting-3.8.0.tar.gz
cd pgrouting-3.8.0
mkdir build
cd build
cmake .. -DPOSTGRESQL_PG_CONFIG=/path/to/pg_config  # eg: /usr/local/ivorysql/ivorysql-5/bin/pg_config
make
sudo make install
```

## 3. 创建Extension并确认ddlx版本 {#create-extension-and-confirm-pgrouting-version}

psql 连接到数据库，执行如下命令：

```
ivorysql=# CREATE extension pgrouting;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'pgrouting';
   name    | default_version | installed_version |       comment
-----------+-----------------+-------------------+---------------------
 pgrouting | 3.8.0           |                   | pgRouting Extension
(1 row)
```

## 4. 使用 {#usage}

关于pgRouting的使用，请参阅 [pgRouting官方文档](https://docs.pgrouting.org/)
