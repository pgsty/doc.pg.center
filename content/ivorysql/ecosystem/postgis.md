---
title: PostGIS
linkTitle: postgis
description: 'IvorySQL v5.6 documentation: PostGIS.'
type: docs
weight: 360
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

IvorySQL is fully compatible with PostgreSQL, allowing for seamless integration with PostGIS.

## 2. Installation {#installation}

Users can select the installation method for PostGIS that best suits their development environment from the [PostGIS installation page](https://postgis.net/documentation/getting_started/#installing-postgis).

### 2.1. Source Code Installation {#source-code-installation}

In addition to the installation methods provided by the PostGIS community, the IvorySQL community also offers a source code installation method, with Ubuntu 24.04 (x86_64) as the installation environment.

> [!NOTE]
>
> Please ensure that **IvorySQL 5.6 or above** is installed in the environment.

- Install dependencies

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

- Install PostGIS

  ```
  $ wget https://download.osgeo.org/postgis/source/postgis-3.5.4.tar.gz
  $ tar xvf postgis-3.5.4.tar.gz
  $ cd postgis-3.5.4
  $ ./configure  --with-pgconfig=/path/to/pg_config   eg: /usr/ivory-5/bin/pg_config, if ivorysql installation directory is /usr/ivory-5.
  $ make
  $ sudo make install
  ```

  > [!TIP]
  >
  > If configure reports PGXS error, please change --with-pgconfig parameter value and confirm the parameter value based on the installation path of IvorySQL in the environment.

## 3. Create Extension and Verify PostGIS Version {#create-extension-and-verify-postgis-version}

Connect to the database with psql and execute the following commands:

```
ivorysql=# CREATE extension postgis;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'postgis';
  name   | default_version | installed_version |                          comment
---------+-----------------+-------------------+------------------------------------------------------------
 postgis | 3.5.4           | 3.5.4             | PostGIS geometry and geography spatial types and functions
(1 row)
```

## 4. Using {#using}

For information about using PostGIS, please refer to the [PostGIS 3.5 Official Documentation](https://postgis.net/docs/manual-3.5)
