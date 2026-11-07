---
title: "Apache Cloudberry 2.x Documentation"
linkTitle: "Cloudberry"
description: "Apache Cloudberry (Incubating) 2.x guides and references for building, deploying, loading, querying, tuning, securing, and operating the MPP database."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: -40
icon: fa-solid fa-cubes-stacked
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
module: [CLOUDBERRY]
categories: [Concept]
upstream_source: cloudberry
search_keywords: [Greenplum, MPP, CBDB, "2.2.0", gpdb]
upstream_link: "https://github.com/apache/cloudberry-site/tree/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x"
cascade:
  upstream_source: cloudberry
  type: docs
  module: [CLOUDBERRY]
---

Apache Cloudberry (Incubating) is an open-source massively parallel processing (MPP) database
derived from Greenplum Database 7. Cloudberry 2.2.0-incubating uses PostgreSQL 14.10;
versions 2.0 and 2.1 used PostgreSQL 14.4. A Coordinator accepts client connections and dispatches
each query; Segments store the data and execute their part of the query in parallel.

This collection is the upstream 2.x documentation, which covers the current
[2.2.0-incubating](https://cloudberry.apache.org/releases/2.2.0-incubating) release. Start with the
[feature overview](/cloudberry/introduction/cbdb-overview/) and
[architecture](/cloudberry/introduction/cbdb-architecture/), try the
[sandbox](/cloudberry/build/sandbox/), or plan a [production deployment](/cloudberry/deployment/).
SQL syntax, utilities, configuration parameters, and system catalogs are under
[References](/cloudberry/reference/).

The upstream site publishes two related manuals separately:
[Platform Extension Framework (PXF)](/cloudberry/pxf/) and
[Apache Cloudberry Core Internals](/cloudberry/core-internals/).
