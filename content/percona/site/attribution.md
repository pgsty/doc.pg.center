---
title: Attribution and copyright
description: Sources, copyright holders, licence texts and the scope of this independent documentation site.
type: docs
translation_notice: false
upstream_source: percona
upstream_link: https://github.com/percona/pg_tde/tree/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
---


This is an **independent documentation and translation site maintained by PGSTY**. It is not Percona’s official documentation and does not imply Percona’s endorsement. The [official documentation](/percona/overview/) and [upstream project](https://github.com/percona/pg_tde) remain the primary sources.

## Documentation source {#documentation-source}

The 66 English documents and their complete Chinese translations are based on `documentation/docs` at commit [`1660e66a6a30`](https://github.com/percona/pg_tde/commit/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39) (documentation version **2.2.2**), retrieved on 2026-11-06. PGSTY maintains the Chinese translation and downstream presentation. The original author is Percona and the pg_tde contributors.

Read the [source manifest](/percona/assets/source-manifest.json) for file paths, hashes, supporting assets, and pinned source URLs. Each adapted page links to its original. The [errata](/percona/site/errata/) records corrections checked against this snapshot.

## Upstream copyright and licence {#upstream-licence}

The repository’s [COPYRIGHT](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/COPYRIGHT) contains the pg_tde licence, with PostgreSQL-style grants and warranty disclaimers. Its full, unmodified text is preserved in [pg_tde-COPYRIGHT.txt](/percona/assets/legal/pg_tde-COPYRIGHT.txt). It names:

- PostgreSQL Global Development Group — portions © 1996–2024.
- The Regents of the University of California — portions © 1994.
- Percona LLC and/or its affiliates — © 2024–2025.

The local identifier `LicenseRef-pg-tde` refers to that exact text. Permission covers use, copying, modification, and distribution of the software and its documentation subject to the stated notices and disclaimers. Percona and PostgreSQL names and logos remain the property of their respective holders.

## Downstream work {#downstream-work}

PGSTY converts MkDocs formatting to Hugo/Oink, maintains paired English and Chinese pages, and adds navigation, an original key-hierarchy diagram, a homepage and editorial reading notes. SQL, examples and heading IDs are compared between languages. Corrections are disclosed separately; the source manifest retains the original hashes.

Percona blog entries are **short editorial reading notes linking to the original articles**. They retain the original author and publication date. The pg_tde repository licence is not asserted to cover the Percona website’s blog articles.

## Site licence {#site-licence}

The site’s own configuration, styles, scripts, diagrams and original editorial text use the [MIT License](/percona/assets/legal/site-LICENSE.txt). [Oink 1.5.1](https://github.com/pgsty/oink/releases/tag/v1.5.1) supplies the theme under its own licence. Neither changes the upstream documentation licence.
