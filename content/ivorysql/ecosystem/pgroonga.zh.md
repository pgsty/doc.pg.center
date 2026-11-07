---
title: PGroonga
linkTitle: pgroonga
description: IvorySQL v5.6 文档：PGroonga。
type: docs
weight: 420
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/5.7.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 概述 {#overview}

PostgreSQL 内置了全文搜索功能，但在处理​​大规模数据​​、​​复杂查询​​以及​​非英语语言（特别是中日韩等 CJK 语言）​​ 时，其功能和性能可能无法满足高性能应用的需求。

PGroonga 应运而生，它是一个 PostgreSQL 的扩展插件，将 ​​Groonga​​ 这款高性能的全功能全文搜索引擎与 PostgreSQL 数据库深度融合。Groonga 本身是一个优秀的开源搜索引擎，以其极致的速度和丰富的功能著称，尤其擅长处理多语言文本。PGroonga 的使命就是将 Groonga 的强大能力无缝地带入 PostgreSQL 的世界，为用户提供远超原生全文搜索的体验。

## 2. 安装 {#installation}

> [!NOTE]
>
> IvorySQL的安装包里已经集成了PGroonga插件，如果使用安装包安装的IvorySQL，通常不需要再手动安装PGroonga，直接跳过安装步骤即可。

用户可从 [PGroonga package安装](https://pgroonga.github.io/install) 页面选择适合自己的方式进行PGroonga安装。

IvorySQL社区提供了源码安装步骤，下面以PGroonga v4.0.4为例进行演示。

### 2.1. 安装依赖 {#dependencies}

环境

```
  操作系统：Ubuntu 24.04
  CPU架构：x86_64
  IvorySQL: v5.6
```

#### 2.1.1. 安装 msgpack-c {#install-msgpack-c}

编译PGroonga，有个配置选项：HAVE_MSGPACK=1，它是用于支持WAL，使用这个选项需要安装msgpack-c 1.4.1或者更高版本。

```
  sudo apt install libmsgpack-dev
```

#### 2.1.2. 安装 Groonga {#install-groonga}

确保Groonga \>= 14.0.0

```
  sudo apt install groonga libgroonga-dev
```

验证Groonga安装成功

``` bash
highgo@ubuntu:~/work/IvorySQL/inst$ groonga --version
  Groonga 15.1.7 [Linux,x86_64,utf8,match-escalation-threshold=0,nfkc,mecab,message-pack,mruby,onigmo,zlib,lz4,zstandard,epoll,apache-arrow,xxhash,blosc,h3,simdjson,llama.cpp]
```

### 2.2. 编译安装PGroonga {#compile-and-install-pgroonga}

#### 2.2.1. 下载解压源码 {#download-and-extract-the-pgroonga-source-code}

``` bash
  wget https://packages.groonga.org/source/pgroonga/pgroonga-4.0.4.tar.gz
  tar xvf pgroonga-4.0.4.tar.gz
  cd pgroonga-4.0.4
```

#### 2.2.2. 编译 {#compile}

运行make前确保\`pg_config\`命令的路径在\`PATH\`环境变量里，例如IvorySQL安装的路径是\`~/work/IvorySQL/inst\`，则环境变量设置如下：

``` bash
  export PGHOME=~/work/IvorySQL/inst
  export PGDATA=$PGHOME/data
  export PATH=$PGHOME/bin:$PATH
```

然后执行以下命令进行编译和安装：

``` bash
  make HAVE_MSGPACK=1
  make install
```

## 3. 创建Extension并确认PGroonga版本 {#create-extension-pgroonga-and-confirm-the-version}

psql 连接到数据库的pg模式下，执行命令：

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
 PostgreSQL (IvorySQL 5.6) 18.6 on x86_64-linux, compiled by gcc-13.3.0, 64-bit
(1 row)
```

## 4. 编码兼容性 {#encoding-compatibility}

PGroonga 依赖 [Groonga 支持的字符编码](https://groonga.org/docs/reference/api/util_8h.html#c.grn_encoding)，其中不包含 GB18030。因此，在 GB18030 编码的数据库中创建 PGroonga 索引时，索引可能没有生成词元，并导致查询无法返回匹配结果。

使用 PGroonga 的业务应创建 UTF-8 编码的数据库：

``` sql
CREATE DATABASE search_db
  WITH ENCODING 'UTF8'
       LC_COLLATE 'C'
       LC_CTYPE 'C'
       TEMPLATE template0;
```

修改 Groonga 的运行时编码或重建索引不会改变数据库编码。已有数据需要迁移或重新导入 UTF-8 数据库，再创建 PGroonga 索引。

## 5. 使用 {#usage}

关于PGroonga的使用，请参阅 [PGroonga官方文档](https://pgroonga.github.io/tutorial)
