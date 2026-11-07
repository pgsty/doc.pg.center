---
title: pgsql-http
linkTitle: pgsql-http
description: 'IvorySQL v5.6 documentation: pgsql-http.'
type: docs
weight: 400
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.5.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

pgsql-http is an open-source extension designed for PostgreSQL databases that allows users to initiate HTTP requests directly within the database, acting as a built-in web client. The core purpose of this extension is to bridge the gap between databases and external web services, enabling interaction with external web services and API endpoints through simple SQL function calls without relying on external applications or middleware.

With this extension, developers can directly retrieve network data (GET), submit data (POST/PUT), update (PATCH), or delete (DELETE) remote resources in SQL queries, triggers, or stored procedures. It provides rich functionality, including setting request headers, automatic URL encoding, sending JSON data, and parsing response status, headers, and content, greatly simplifying the process of integrating external data into database operations.

Typical application scenarios include: real-time retrieval of external data (such as exchange rates, weather information) and storing it in tables; automatic notification of microservices through triggers when data changes; cleaning data in the database and directly submitting it to external APIs. It provides a powerful and flexible solution for building database-centric integrated applications.

## 2. Installation {#installation}

The pgsql-http plugin has been integrated into the IvorySQL installation package. If IvorySQL is installed using the installation package, pgsql-http can usually be used without manual installation. Other installation methods can refer to the source code installation steps below.

> [!TIP]
>
> The source installation environment is Ubuntu 24.04 (x86_64). IvorySQL 5 or higher version is already installed in the environment, with the installation path at /usr/local/ivorysql/ivorysql-5

### 2.1. Source Installation {#source-installation}

- Install Dependencies

It depends on libcurl, and libcurl development files (such as libcurl4-openssl-dev) need to be installed in advance

```
# Install dependencies
sudo apt install libcurl4-openssl-dev
```

- Compile and Install

Download the 1.7.0 source package pgsql-http-1.7.0.tar.gz from <a href="https://github.com/pramsey/pgsql-http/releases/tag/v1.7.0" class="bare">https://github.com/pramsey/pgsql-http/releases/tag/v1.7.0</a>

```
tar xvf pgsql-http-1.7.0.tar.gz
cd pgsql-http-1.7.0
# Ensure pg_config is accessible in PATH, e.g.: /usr/local/ivorysql/ivorysql-5/bin/pg_config
make
sudo make install
```

## 3. Create Extension and Confirm http Version {#create-extension-and-confirm-http-version}

Connect to the database with psql and execute the following commands:

```
ivorysql=# CREATE extension http;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'http';
   name    | default_version | installed_version |       comment
-----------+-----------------+-------------------+-------------------------------------------------------------------------
 http      | 1.7             |  1.7              | HTTP client for PostgreSQL, allows web page retrieval inside the database.
(1 row)
```

## 4. Usage {#usage}

For pgsql-http usage, please refer to [pgsql-http official documentation](https://github.com/pramsey/pgsql-http)
