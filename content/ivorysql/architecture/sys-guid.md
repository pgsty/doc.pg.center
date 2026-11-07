---
title: sysguid() function
linkTitle: sys_guid Function
description: 'IvorySQL v5.6 documentation: sysguid() function.'
type: docs
weight: 680
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/6.3.10.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Purpose {#purpose}

IvorySQL’s sys_guid() is a powerful random number generation function that generates and returns a 16-byte database-level unique identifier (raw value).

## 2. Implementation Description {#implementation-description}

The sys_guid() function of IvorySQL is implemented by modifying the code of the uuid-ossp plugin. To make full use of various underlying libraries of uuid, the following logic is adopted:

1.  If the uuid-ossp exists in the system, uuid_make() will be used;

2.  If the uuid-e2fs exists in the system, uuid_generate_random() will be used；

3.  Otherwise use arc4random()；

Meanwhile modify the code so that IvorySQL can load uuid-ossp extension automatically.
