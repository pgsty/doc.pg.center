---
title: 实时查询分析
linkTitle: 实时查询分析
description: IvorySQL v5.6 文档：实时查询分析。
type: docs
weight: 320
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/realtime_query.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 概述 {#overview}

**ivy_mooncake** 是 [pg_mooncake](https://github.com/Mooncake-Labs/pg_mooncake) 的 IvorySQL 发行版。它是一个 Postgres 扩展，可在 [Apache Iceberg](https://iceberg.apache.org/) 中为 Postgres 表创建列存镜像，从而支持亚秒级新鲜度的快速分析（OLAP）查询。它让 IvorySQL 在事务表之上直接获得实时分析处理能力：

- **实时摄取**：由 [moonlink](https://github.com/IvorySQL/ivy_moonlink) 驱动，支持流式与批量的 INSERT/UPDATE/DELETE。

- **快速分析**：由 [DuckDB](https://github.com/IvorySQL/ivy_duckdb) 加速，在 [ClickBench](https://www.mooncake.dev/blog/clickbench-v0.1) 上排名前 10。

- **Postgres 原生**：可像查询普通 Postgres 表一样查询列存表。

- **Iceberg 原生**：数据可被其他查询引擎直接访问。

## 2. 文档下载 {#documents}

- [ivy_mooncake 技术白皮书（V1.0 beta1）](https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/attachments/ivy_mooncake%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6-v1.0beta1.docx)

- [ivy_mooncake 用户使用手册（V1.0 beta1）](https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/attachments/ivy_mooncake%E7%94%A8%E6%88%B7%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C-v1.0beta1.docx)

## 3. 安装 {#installation}

### 3.1. 使用 Docker 运行（预览版） {#run-with-docker-preview}

提供了预装 `pg_duckdb` 与 `pg_mooncake` 的 IvorySQL 预览镜像：

```
docker run --name ivy_mooncake \
  -e IVORYSQL_PASSWORD=password \
  -p 5432:5432 -p 1521:1521 \
  -v ivy_mooncake_data:/var/lib/ivorysql/data \
  -v ivy_mooncake_warehouse:/tmp/moonlink_iceberg \
  registry.highgo.com/mooncake/ivy_mooncake:0.1
```

## 4. 快速开始 {#quick-start}

- 创建 `pg_mooncake` 扩展

  ```
  CREATE EXTENSION pg_mooncake CASCADE;
  ```

- 创建普通 Postgres 表 `trades`

  ```
  CREATE TABLE trades(
    id bigint PRIMARY KEY,
    symbol text,
    time timestamp,
    price real
  );
  ```

- 创建与 `trades` 保持同步的列存镜像 `trades_iceberg`

  ```
  CALL mooncake.create_table('trades_iceberg', 'trades');
  ```

- 向 `trades` 插入数据

  ```
  INSERT INTO trades VALUES
    (1,  'AMD', '2024-06-05 10:00:00', 119),
    (2, 'AMZN', '2024-06-05 10:05:00', 207),
    (3, 'AAPL', '2024-06-05 10:10:00', 203),
    (4, 'AMZN', '2024-06-05 10:15:00', 210);
  ```

- 查询 `trades_iceberg`，它反映 `trades` 的最新状态

  ```
  SELECT avg(price) FROM trades_iceberg WHERE symbol = 'AMZN';
  ```
