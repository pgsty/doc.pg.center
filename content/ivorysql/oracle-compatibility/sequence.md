---
title: Compatible with Oracle sequence
linkTitle: sequence
description: 'IvorySQL v5.6 documentation: Compatible with Oracle sequence.'
type: docs
weight: 200
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.11.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Objective {#objective}

- This document is designed for compatibility with Oracle sequence functions, in order to use Oracle’s sequences in IvorySQL.

## 2. Function description {#function-description}

- Sequence is a database object, similar to tables and views, that represents an integer sequence that can be used by any table and view in the global database namespace. Sequence values can be accessed using NEXTVAL and CURRVAL. Sequences can be in ascending or descending order.

## 3. Test cases {#test-cases}

```
ivorysql=# CREATE sequence seq;
CREATE SEQUENCE
ivorysql=# SELECT seq.NEXTVAL FROM DUAL;
 nextval
---------
       1
(1 row)
ivorysql=# ALTER sequence seq restart start with 10;
ALTER SEQUENCE
ivorysql=# SELECT seq.NEXTVAL FROM DUAL;
 nextval
---------
       10
(1 row)
ivorysql=# DROP SEQUENCE seq;
DROP SEQUENCE
```
