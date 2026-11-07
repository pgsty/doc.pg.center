---
title: pgvector
linkTitle: pgvector
description: 'IvorySQL v5.6 documentation: pgvector.'
type: docs
weight: 370
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.2.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

The vector database is an important component of Generative Artificial Intelligence (GenAI). As a significant extension of PostgreSQL, pgvector not only supports vector calculations of up to 16000 dimensions but also provides powerful vector operations and indexing capabilities, enabling PostgreSQL to directly transform into an efficient vector database. IvorySQL, being developed based on PostgreSQL, inherits the seamless integration capability with pgvector extension, thereby offering users a wider range of data processing and analysis options. Additionally, in Oracle compatibility mode, the pgvector extension is also available, providing great convenience for Oracle users to use vector databases, allowing for easy migration and management of data and achieving more efficient business operations.

## 2. Principles {#principles}

PGVector has two indexing algorithms, IVFFLAT and HNSW.

### 2.1. IVFFLAT {#ivfflat}

The working principle of IVFFLAT is to cluster similar vectors into regions and build an inverted index mapping each region to its vectors. This allows queries to focus on a subset of the data, enabling fast searches. By adjusting the parameters of lists and probes, IVFFLAT can balance the speed and accuracy of the dataset, enabling PostgreSQL to perform rapid semantic similarity searches on complex data. Through simple queries, applications can find the nearest neighbors to a query vector among millions of high-dimensional vectors. For tasks such as natural language processing and information retrieval, IVFFLAT provides an effective solution.

When building an IVFFLAT index, you need to decide how many lists to include in the index. Each list represents a "center" which are computed using the k-means algorithm. Once all centers are determined, IVFFLAT determines which center each vector is closest to and adds it to the index. When querying vector data, you can decide how many centers to check, which is determined by the ivfflat.probes parameter. This results in a trade-off between ANN performance/recall: the more centers accessed, the more accurate the results, but at the expense of performance.

### 2.2. HNSW {#hnsw}

HNSW (Hierarchical Navigating Small World) is a graph-based indexing algorithm consisting of multiple layers of neighborhood graphs, hence the name "hierarchical" NSW method. It constructs multiple layers of navigation graphs for a given graph according to certain rules, with the upper layers of the graph being sparser and the distances between nodes farther apart; and the lower layers of the graph being denser and the distances between nodes closer together. HNSW algorithm is a classic trade-off between space and time, as it achieves high search quality and speed, but at the cost of significant memory overhead. This is because it not only requires storing all vectors in memory but also maintaining the structure of the graph, which also needs to be stored.

## 3. Installation {#installation}

> [!TIP]
>
> The IvorySQL 5(above version) has been installed in the environment, and the installation path is /usr/local/ivorysql/ivorysql-5

### 3.1. Source Code Installation {#source-code-installation}

- Setting PG_CONFIG

  ```
  export PG_CONFIG=/usr/local/ivorysql/ivorysql-5/bin/pg_config
  ```

- Pull pg_vector source code

  ```
  git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git
  ```

- Install pgvector

  ```
  cd pgvector

  sudo --preserve-env=PG_CONFIG make
  sudo --preserve-env=PG_CONFIG make install
  ```

- Create pgvector extension

  ```
  [ivorysql@localhost ivorysql-5]$ psql
  psql (18.6)
  Type "help" for help.

  ivorysql=# create extension vector;
  CREATE EXTENSION
  ```

  Now, pgvector is installed completely. For more usage cases, please refer to [pgvector document](https://github.com/pgvector/pgvector?tab=readme-ov-file#getting-started)

## 4. Oracle Compatible {#oracle-compatible}

In IvorySQL’s Oracle compatibility mode, the pgvector extension can also work correctly.

> [!TIP]
>
> We suggest users to test using port 1521, using the command: psql -p 1521.

### 4.1. Data Type {#data-type}

```
ivorysql=# CREATE TABLE items5 (id bigserial PRIMARY KEY, name varchar2(20), num number(20), embedding bit(3));
CREATE TABLE
ivorysql=# INSERT INTO items5 (name, num, embedding) VALUES ('1st oracle data',0, '000'), ('2nd oracle data', 111, '111');
INSERT 0 2
ivorysql=# SELECT * FROM items5 ORDER BY bit_count(embedding # '101') LIMIT 5;
 id |      name       | num | embedding
----+-----------------+-----+-----------
  2 | 2nd oracle data | 111 | 111
  1 | 1st oracle data | 0   | 000
```

### 4.2. Anonymous Block {#anonymous-block}

```
ivorysql=# declare
i vector(3) := '[1,2,3]';
begin
raise notice '%', i;
end;
ivorysql-# /
NOTICE:  [1,2,3]
DO
```

### 4.3. PROCEDURE {#procedure}

```
ivorysql=# CREATE OR REPLACE PROCEDURE ora_procedure()
AS
p vector(3) := '[4,5,6]';
begin
raise notice '%', p;
end;
/
CREATE PROCEDURE
ivorysql=# call ora_procedure();
NOTICE:  [4,5,6]
CALL
```

### 4.4. FUNCTION {#function}

```
ivorysql=# CREATE OR REPLACE FUNCTION AddVector(a vector(3), b vector(3))
RETURN vector(3)
IS
BEGIN
RETURN a + b;
END;
/
CREATE FUNCTION
ivorysql=# SELECT AddVector('[1,2,3]','[4,5,6]') FROM DUAL;
 addvector
----------------
 [5,7,9]
(1 row)
```
