---
title: IVORYSQL framework design
linkTitle: Ivorysql frame design
description: 'IvorySQL v5.6 documentation: IVORYSQL framework design.'
type: docs
weight: 740
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

- In order to minimize changes to the original PostgreSQL, it is compatible with Oracle. We need to implement a framework for dual-parser, dual-port, modal PL/PGSQL to implement PL/iSQL. The implementation flowchart is as follows:

![p18](/ivorysql/assets/images/upstream/b1302459264390e7d24d8062336c31dc767e59884c18044568a8c012ceed3b38.png)

## 1. Function {#function}

### 1.1. Dual-port design {#dual-port-design}

- The Ivorysql port 5432 is kept compatible with the original PostgreSQL situation, so Ivorysql uses another separate port to log in, which defaults to 1521. Log in from this port, and the Oracle compatibility mode is used by default. If you need to log in from port 5432 and also enter compatibility mode, you must configure it using `SET ivorysql.compatible_mode=oracle`.

### 1.2. Parser module design {#parser-module-design}

- In order to minimize the interference between Oracle syntax and PostgreSQL syntax, a parser module has been added to handle oracle-related syntax.

### 1.3. Added PL/iSQL procedural language {#added-plisql-procedural-language}

- Added PL/iSQL procedural language compatible with Oracle’s PL/SQL procedural language.
