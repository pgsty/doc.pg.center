---
title: Added Oracle compatibility mode ports and IP
linkTitle: ports and IP
description: 'IvorySQL v5.6 documentation: Added Oracle compatibility mode ports and IP.'
type: docs
weight: 180
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.9.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Objective {#objective}

- In order to distinguish the Oracle port, IP and PG port IP. THERE IS NOW A NEED TO INCREASE THE PROCESSING OF ORAPORT AND ORAHOST;

## 2. Function {#function}

- Add ivoryhost: You need to add the parameter ivoryhost when connecting, and its function is similar to host;

- New ivoryport: Compared to host, the function of port is relatively complex. It involves specifying ports in the configure phase and connection phase;

## 3. Test method: {#test-method}

```
   ./configure --with-oraport=5555
   ./initdb ....
   ./pg_ctl -D ../data start

   ./pg_ctl -o "-p 5433 -o 1522" -D ../data
```
