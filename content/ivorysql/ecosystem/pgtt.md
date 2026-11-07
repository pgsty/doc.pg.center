---
title: pgtt
linkTitle: pgtt
description: 'IvorySQL v5.6 documentation: pgtt.'
type: docs
weight: 460
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.11.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

pgtt is a PostgreSQL extension to create, manage and use Oracle-style Global Temporary Tables. The objective of this extension it to provide the Global Temporary Table feature to PostgreSQL waiting for an in core implementation

## 2. Installation {#installation}

> [!TIP]
>
> The source installation environment is Ubuntu 24.04 (x86_64), with IvorySQL already installed in the environment at /path-to/ivorysql

### 2.1. Source Installation {#source-installation}

```
# Download pgtt source code
wget https://github.com/darold/pgtt/archive/refs/tags/v4.5.tar.gz
tar zxvf v4.5.tar.gz
cd pgtt-4.5

# Compile and install
make PG_CONFIF=/path-to/ivorysql/bin/pg_config
make PG_CONFIF=/path-to/ivorysql/bin/pg_config install
```

## 3. Create Extension {#create-extension}

Connect to the database using psql and execute the following command:

```
-- create the extension
CREATE EXTENSION pgtt;
```

## 4. Load the Extension {#load-the-extension}

```
After creating the extension, it needs to be loaded before use
You can use one of the following three methods to load it:

1. Modify session_preload_libraries in the configuration file
session_preload_libraries = 'pgtt'

2. Enable at database level
ALTER DATABASE mydb SET session_preload_libraries = 'pgtt';

3. Load in session
LOAD 'pgtt';

After successfully loading the extension, you can see that the value of pgtt.enabled is on
ivorysql=# show pgtt.enabled;
 pgtt.enabled
--------------
 on
(1 row)

pgtt_schema is added to search_path
ivorysql=# SHOW search_path;
         search_path
------------------------------
 "$user", public, pgtt_schema
(1 row)
```

## 5. Usage {#usage}

```
Create temporary table:
Using this statement will produce a warning message, but it can be ignored.

ivorysql=# CREATE GLOBAL TEMPORARY TABLE test_gtt_table (
    id integer,
    lbl text
) ON COMMIT PRESERVE ROWS;
WARNING:  GLOBAL is deprecated in temporary table creation
LINE 1: CREATE GLOBAL TEMPORARY TABLE test_gtt_table (
               ^
CREATE TABLE

If you don't want to produce this warning message, you can use comment symbols:
CREATE /*GLOBAL*/ TEMPORARY TABLE test_gtt_table (
    id integer,
    lbl text
) ON COMMIT PRESERVE ROWS;


Temporary tables can also be created using the LIKE clause:
ivorysql=# CREATE /*GLOBAL*/ TEMPORARY TABLE test_gtt_table AS SELECT * FROM source_table WITH DATA;
CREATE TABLE AS

Create indexes on table columns:
ivorysql=# CREATE INDEX ON test_gtt_table (id);
CREATE INDEX

Drop temporary table:
ivorysql=# drop table test_gtt_table;
DROP TABLE

Add constraints (except foreign keys):
ivorysql=# CREATE /*GLOBAL*/ TEMPORARY TABLE t2 (
    c1 serial PRIMARY KEY,
    c2 VARCHAR (50) UNIQUE NOT NULL,
    c3 boolean DEFAULT false
);
CREATE TABLE

Creating tables with foreign keys is not allowed:
ivorysql=# CREATE /*GLOBAL*/ TEMPORARY TABLE t1 (c1 integer, FOREIGN KEY (c1) REFERENCES source (id));
ERROR:  attempt to create referential integrity constraint on global temporary table

ivorysql=# ALTER TABLE t2 ADD FOREIGN KEY (c1) REFERENCES source (id);
ERROR:  attempt to create referential integrity constraint on global temporary table
```

For more detailed usage and advanced features, please refer to <a href="https://github.com/darold/pgtt" class="bare">https://github.com/darold/pgtt</a> .
