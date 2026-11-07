---
type: docs
upstream_source: openhalo
upstream_link: https://github.com/HaloTech-Co-Ltd/openHalo/blob/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c/README.md
title: OpenHalo documentation
linkTitle: OpenHalo
description: 'MySQL protocol and SQL compatibility on PostgreSQL: configuration, syntax, data types, and migration boundaries.'
weight: -70
sidebar_root_for: self
sidebar_root_link_self: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: openhalo
no_list: true
icon: fa-solid fa-circle-nodes
---

openHalo provides the capability for PostgreSQL to work with applications written for MySQL but provides much more better performance than MySQL!

Migrating from legacy MySQL databases can be time-consuming and resource-intensive. When migrating your databases, you can automate the migration of your database schema and data using HMT (an opensource migration tool also opened by HaloLab, https://github.com/HaloLab001/hmt-web), but there is often more work to do to migrate the application itself, including re-writing application code that interacts with the database.

openHalo understands the SQL dialect of MySQL, and supports the same communications protocol, so your apps that were originally written for MySQL can work with openHalo with fewer code changes. As a result, the effort required to modify and move applications running on MySQL 5.7 or newer to openHalo is reduced, leading to faster, lower-risk, and more cost-effective migrations.

A student team at IMT Atlantique maintains [compatibility tests and performance benchmarks](https://github.com/fxcollot/openHaloDocumentation). Halo Database's official 1.0.16 manual contains a focused [MySQL compatibility reference](https://doc.halodbtech.com/multi-mode-compatibility/mysql).

## Benefits {#benefits}
### Reduce migration time and risk {#migration}
openHalo supports commonly used MySQL dialect and semantics which reduces the amount of code changes related to database calls in an application. As a result, the amount of application code you need to re-write is minimized, reducing the risk of any new application errors.

### Obtain better performance {#performance}
With openHalo, you can obtain better performance without any extra efforts and fees! Especially for complex SQL statements!

### Migrate at your own pace {#pace}
With openHalo, you can commonly-used MySQL query tools, commands, and drivers. As a result, you can continue developing with the tools you are familiar with.


## How it works {#how-it-works}
openHalo supports commonly used SQL dialect and communication protocol of MySQL. You can use openHalo as a MySQL and enabling your legacy applications to communicate with openHalo without extensive code re-writes but provides much more better performance than MySQL!
![OpenHalo protocol architecture](/openhalo/assets/how-it-works.png)



[Build and configure OpenHalo](/openhalo/quick-start/).

## MySQL compatibility reference {#mysql-compatibility}

Use the focused reference pages when the goal is to run an existing MySQL application through OpenHalo or Halo Database:

- [MySQL compatibility](/openhalo/mysql-compatibility/)
- [Configuration and connection](/openhalo/mysql-configuration/)
- [Compatible MySQL statements](/openhalo/mysql-statements/)
- [Compatible MySQL data types](/openhalo/mysql-data-types/)
- [Known compatibility boundaries](/openhalo/mysql-compatibility-gaps/)

{.cards}
