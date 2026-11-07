---
title: Oracle Compatible Empty String to NULL
linkTitle: Empty String to NULL
description: 'IvorySQL v5.6 documentation: Oracle Compatible Empty String to NULL.'
type: docs
weight: 300
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.21.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Purpose {#purpose}

- In IvorySQL’s Oracle compatibility mode, support converting empty strings to NULL for storage, providing behavior consistent with Oracle Database.

## 2. Feature Description {#feature-description}

- Oracle compatibility mode supports converting empty strings to NULL for storage.

- The feature is controlled by parameter `ivorysql.enable_emptystring_to_null`, with default value `on`.

- When this parameter is enabled, inserting an empty string will automatically convert it to NULL value for storage.

- NULL values after conversion can be queried using the `IS NULL` condition.

## 3. Test Cases {#test-cases}

```
-- Create test table
ivorysql=# create table abc (id int);
CREATE TABLE

-- Check empty string to NULL parameter status
ivorysql=# show ivorysql.enable_emptystring_to_null;
 ivorysql.enable_emptystring_to_NULL
-------------------------------------
 on
(1 row)

-- Insert empty string
ivorysql=# insert into abc values('');
INSERT 0 1

-- Query table data, displays as NULL
ivorysql=# select * from abc;
 id
\----

(1 row)

-- Query using IS NULL condition
ivorysql=# select * from abc where id is null;
 id
\----

(1 row)
```
