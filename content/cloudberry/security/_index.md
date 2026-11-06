---
title: "Security and Permission"
description: "This section describes how to secure a Apache Cloudberry system."
weight: 80
icon: "fa-solid fa-shield-halved"
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/index.md"
---

The guide assumes knowledge of Linux/UNIX system administration and database management systems. Familiarity with structured query language (SQL) is helpful.

Because Apache Cloudberry is based on PostgreSQL, this guide assumes some familiarity with PostgreSQL. References to PostgreSQL documentation are provided throughout this guide for features that are similar to those in Apache Cloudberry.

This information is intended for system administrators responsible for administering a Apache Cloudberry system.

## About endpoint security software {#about-endpoint-security-software}

If you install any endpoint security software on your Apache Cloudberry hosts, such as anti-virus, data protection, network security, or other security related software, the additional CPU, IO, network or memory load can interfere with Apache Cloudberry operations and may affect database performance and stability.

Refer to your endpoint security vendor and perform careful testing in a non-production environment to ensure it does not have any negative impact on Apache Cloudberry operations.
