---
title: Real-time query analytics
linkTitle: Real-time Query Analytics
description: 'IvorySQL v5.6 documentation: Real-time query analytics.'
type: docs
weight: 320
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/realtime_query.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

**ivy_mooncake** is the IvorySQL distribution of [pg_mooncake](https://github.com/Mooncake-Labs/pg_mooncake), a Postgres extension that creates a columnstore mirror of your Postgres tables in [Apache Iceberg](https://iceberg.apache.org/), enabling fast analytics (OLAP) queries with sub-second freshness. It gives IvorySQL real-time analytical processing capability directly on top of its transactional tables:

- **Real-time ingestion** powered by [moonlink](https://github.com/IvorySQL/ivy_moonlink) for streaming and batched INSERT/UPDATE/DELETE.

- **Fast analytics** accelerated by [DuckDB](https://github.com/IvorySQL/ivy_duckdb), ranking top 10 on [ClickBench](https://www.mooncake.dev/blog/clickbench-v0.1).

- **Postgres-native**, allowing you to query a columnstore table just like a regular Postgres table.

- **Iceberg-native**, making your data readily accessible by other query engines.

## 2. Documents {#documents}

- [ivy_mooncake Technical White Paper (V1.0 beta1)](https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/attachments/ivy_mooncake-technical-whitepaper-v1.0beta1.docx)

- [ivy_mooncake User Manual (V1.0 beta1)](https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/attachments/ivy_mooncake-user-manual-v1.0beta1.docx)

## 3. Installation {#installation}

### 3.1. Run with Docker (preview) {#run-with-docker-preview}

A preview image bundling IvorySQL with `pg_duckdb` and `pg_mooncake` preloaded is available:

```
docker run --name ivy_mooncake \
  -e IVORYSQL_PASSWORD=password \
  -p 5432:5432 -p 1521:1521 \
  -v ivy_mooncake_data:/var/lib/ivorysql/data \
  -v ivy_mooncake_warehouse:/tmp/moonlink_iceberg \
  registry.highgo.com/mooncake/ivy_mooncake:0.1
```

## 4. Quick Start {#quick-start}

- Create the `pg_mooncake` extension

  ```
  CREATE EXTENSION pg_mooncake CASCADE;
  ```

- Create a regular Postgres table `trades`

  ```
  CREATE TABLE trades(
    id bigint PRIMARY KEY,
    symbol text,
    time timestamp,
    price real
  );
  ```

- Create a columnstore mirror `trades_iceberg` that stays in sync with `trades`

  ```
  CALL mooncake.create_table('trades_iceberg', 'trades');
  ```

- Insert some data into `trades`

  ```
  INSERT INTO trades VALUES
    (1,  'AMD', '2024-06-05 10:00:00', 119),
    (2, 'AMZN', '2024-06-05 10:05:00', 207),
    (3, 'AAPL', '2024-06-05 10:10:00', 203),
    (4, 'AMZN', '2024-06-05 10:15:00', 210);
  ```

- Query `trades_iceberg`; it reflects the up-to-date state of `trades`

  ```
  SELECT avg(price) FROM trades_iceberg WHERE symbol = 'AMZN';
  ```
