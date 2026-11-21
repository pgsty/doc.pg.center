---
title: "安全与权限"
description: "本节介绍如何保障 Apache Cloudberry 系统的安全。"
weight: 80
icon: "fa-solid fa-shield-halved"
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/security/index.md"
---

本指南假定读者了解 Linux/UNIX 系统管理和数据库管理系统。熟悉结构化查询语言（SQL）会有所帮助。

由于 Apache Cloudberry 基于 PostgreSQL，本指南假定读者对 PostgreSQL 有一定了解。对于 Apache Cloudberry 中与 PostgreSQL 类似的功能，本指南在相关位置提供了 PostgreSQL 文档的引用。

本指南面向负责管理 Apache Cloudberry 系统的系统管理员。

## 关于终端安全软件 {#about-endpoint-security-software}

如果在 Apache Cloudberry 主机上安装终端安全软件，例如防病毒、数据保护、网络安全或其他与安全有关的软件，额外的 CPU、IO、网络或内存负载可能会干扰 Apache Cloudberry 的运行，并可能影响数据库的性能和稳定性。

请咨询终端安全软件供应商，并在非生产环境中仔细测试，确保该软件不会对 Apache Cloudberry 的运行产生任何不利影响。
