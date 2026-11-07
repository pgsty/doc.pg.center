---
title: PostGIS
linkTitle: postgis
description: IvorySQL v5.6 文档：PostGIS。
type: docs
weight: 360
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/5.1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 概述 {#overview}

IvorySQL原生100%兼容PostgreSQL,因此，PostGIS可以完美适配IvorySQL。

## 2. 安装 {#installation}

根据开发环境，用户可从 [PostGIS安装](https://postgis.net/documentation/getting_started/#installing-postgis) 页面选择适合自己的方式进行安装PostGIS。

### 2.1. 源码安装 {#source-code-installation}

除PostGIS社区提供的安装方式以外，IvorySQL社区也提供了源码安装方式，源码安装环境为 Ubuntu 24.04(x86_64)。

> [!NOTE]
>
> 请确保环境中已安装了**IvorySQL5.6及以上版本**

- 安装依赖

```
sudo apt install \
    docbook-xsl-ns \
    gettext \
    libgdal-dev \
    libgeos-dev \
    libjson-c-dev \
    libproj-dev \
    libprotobuf-c-dev \
    libsfcgal-dev \
    libxml2-dev \
    libxml2-utils \
    protobuf-c-compiler \
    xsltproc
```

- 安装 PostGIS

  ```
  $ wget https://download.osgeo.org/postgis/source/postgis-3.5.4.tar.gz
  $ tar xvf postgis-3.5.4.tar.gz
  $ cd postgis-3.5.4
  $ ./configure  --with-pgconfig=/path/to/pg_config   eg: /usr/ivory-5/bin/pg_config，如果ivorysql安装目录在/usr/ivory-5.
  $ make
  $ sudo make install
  ```

  > [!TIP]
  >
  > 如出现PGXS报错, 请根据环境中IvorySQL安装路径, 修改—​with-pgconfig的参数值。

## 3. 创建Extension并确认PostGIS版本 {#create-extension-and-verify-postgis-version}

psql 连接到数据库，执行如下命令：

```
ivorysql=# CREATE extension postgis;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'postgis';
  name   | default_version | installed_version |                          comment
---------+-----------------+-------------------+------------------------------------------------------------
 postgis | 3.5.4           | 3.5.4             | PostGIS geometry and geography spatial types and functions
(1 row)
```

## 4. 使用 {#using}

关于PostGIS的使用，请参阅 [PostGIS3.5官方文档](https://postgis.net/docs/manual-3.5)
