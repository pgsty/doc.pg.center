---
title: PGroonga
linkTitle: pgroonga
description: 'IvorySQL v5.6 documentation: PGroonga.'
type: docs
weight: 420
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.7.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

PostgreSQL has built-in full-text search functionality, but when dealing with large-scale data, complex queries, and non-English languages (especially CJK languages like Chinese, Japanese, and Korean), its functionality and performance may not meet the requirements of high-performance applications.

PGroonga was created to address this need. It is a PostgreSQL extension that deeply integrates Groonga, a high-performance full-featured full-text search engine, with the PostgreSQL database. Groonga itself is an excellent open-source search engine, renowned for its extreme speed and rich functionality, particularly excelling at handling multilingual text. PGroonga’s mission is to seamlessly bring Groonga’s powerful capabilities into the PostgreSQL world, providing users with an experience that far exceeds native full-text search.

## 2. Installation {#installation}

> [!NOTE]
>
> The PGroonga plugin is already included in the IvorySQL installation package. If you installed IvorySQL using the official released package, you typically do not need to manually install PGroonga and can skip the installation steps.

You can choose their preferred installation method for PGroonga from the [PGroonga package installation](https://pgroonga.github.io/install) page.

The IvorySQL community provides source code installation steps, demonstrated below using PGroonga v4.0.4 as an example.

### 2.1. Dependencies {#dependencies}

Setup Environment

```
  Operating System: Ubuntu 24.04
  CPU Architecture: x86_64
  IvorySQL: v5.6
```

#### 2.1.1. Install msgpack-c {#install-msgpack-c}

When compile PGroonga, there is an option: `HAVE_MSGPACK=1`, which is used to support WAL. Enabling this option requires installing msgpack-c 1.4.1 or newer version.

``` bash
  sudo apt install libmsgpack-dev
```

#### 2.1.2. Install Groonga {#install-groonga}

Ensure Groonga \>= 14.0.0 is installed.

``` bash
  sudo apt install groonga libgroonga-dev
```

Verify Groonga installation:

``` bash
highgo@ubuntu:~/work/IvorySQL/inst$ groonga --version
  Groonga 15.1.7 [Linux,x86_64,utf8,match-escalation-threshold=0,nfkc,mecab,message-pack,mruby,onigmo,zlib,lz4,zstandard,epoll,apache-arrow,xxhash,blosc,h3,simdjson,llama.cpp]
```

### 2.2. Compile and Install PGroonga {#compile-and-install-pgroonga}

#### 2.2.1. Download and Extract the PGroonga Source Code {#download-and-extract-the-pgroonga-source-code}

``` bash
  wget https://packages.groonga.org/source/pgroonga/pgroonga-4.0.4.tar.gz
  tar xvf pgroonga-4.0.4.tar.gz
  cd pgroonga-4.0.4
```

#### 2.2.2. Compile {#compile}

Before running make , ensure that the `pg_config` command is in the `PATH` environment variable. For example, if IvorySQL is installed at `~/work/IvorySQL/inst` , set the environment variables as follows:

``` bash
  export PGHOME=~/work/IvorySQL/inst
  export PGDATA=$PGHOME/data
  export PATH=$PGHOME/bin:$PATH
```

Then execute the following commands to compile and install:

``` bash
  make HAVE_MSGPACK=1
  make install
```

## 3. Create Extension PGroonga and Confirm the version {#create-extension-pgroonga-and-confirm-the-version}

Connect to the database with `psql` in `pg` mode and execute the following commands:

``` sql
postgres=# CREATE extension pgroonga;
CREATE EXTENSION
postgres=# SELECT * FROM pg_available_extensions WHERE name = 'pgroonga';
   name   | default_version | installed_version |                                    comment
----------+-----------------+-------------------+--------------------------------------------------------------------------------
 pgroonga | 4.0.4           | 4.0.4             | Super fast and all languages supported full text search index based on Groonga
(1 row)

postgres=# select version();
                                    version
--------------------------------------------------------------------------------
 PostgreSQL (IvorySQL 5.6) 18.0 on x86_64-linux, compiled by gcc-13.3.0, 64-bit
(1 row)
```

## 4. Encoding Compatibility {#encoding-compatibility}

PGroonga relies on [Groonga’s supported encodings](https://groonga.org/docs/reference/api/util_8h.html#c.grn_encoding), which do not include GB18030. A PGroonga index created in a GB18030-encoded database may therefore contain no tokens and return no matches.

Create a UTF-8 database for workloads that use PGroonga:

``` sql
CREATE DATABASE search_db
  WITH ENCODING 'UTF8'
       LC_COLLATE 'C'
       LC_CTYPE 'C'
       TEMPLATE template0;
```

Changing Groonga’s runtime encoding or rebuilding the index does not change the database encoding. Existing data must be migrated or reloaded into a UTF-8 database before creating the PGroonga index.

## 5. Usage {#usage}

For PGroonga usage, please refer to the [PGroonga Official Documentation](https://pgroonga.github.io/tutorial)
