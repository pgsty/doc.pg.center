---
title: Attribution and licenses
description: Source, copyright, license, and modification records for this migrated site.
type: docs
weight: 10
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/README.md
cascade:
  type: docs
  upstream_source: babelfish-site
upstream_notice: /babelfish/site/attribution/
---


This is a community edition of the [Babelfish upstream website](https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/README.md), adapted to Hugo / OINK and maintained by PGSTY in English and Chinese. It is not an official Babelfish, AWS, or Microsoft website. Project names and marks identify their respective upstream projects and do not imply endorsement.

> Copyright Babelfish for PostgreSQL Contributors.

## License records {#license-records}

The upstream contains two inconsistent statements. Both are preserved here; they are not interpreted as a dual-license grant:

- Its [`LICENSE`](/babelfish/assets/legal/upstream-LICENSE.txt) contains the complete Apache License 2.0 text.
- At the same revision, [README · Credits](https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/README.md#credits) describes the website as BSD-3-Clause. It credits a fork of the BSD-licensed [djangoproject.com](https://github.com/django/djangoproject.com), merged with [Just the Docs](https://github.com/pmarsceill/just-the-docs). The [original README copy](/babelfish/assets/legal/upstream-README.md) preserves this record in full.
- Babelfish **software components** use Apache 2.0 or the PostgreSQL License, as specified in each component repository. Those terms are recorded separately from the website statements.
- New site configuration, conversion scripts, and Chinese translations are provided under Apache 2.0 without changing the ownership or terms of upstream material.
- [OINK v1.5.1](https://github.com/pgsty/oink/releases/tag/v1.5.1) is used under its own Apache 2.0 license.

## Upstream third-party notices {#third-party}

The original [THIRD-PARTY file](/babelfish/assets/legal/upstream-THIRD-PARTY.txt) retains these records:

| Component | License | Original copyright |
| --- | --- | --- |
| Just the Docs 0.3.3 | MIT | Copyright (c) 2016 Patrick Marsceill |
| Jekyll Pure Liquid Table of Contents 1.1.0 | MIT | Copyright (c) 2017 Vladimir Jimenez |
| Bootstrap Icons 1.4.1 | MIT | Copyright (c) 2019-2020 The Bootstrap Authors |

These are historical dependencies of the upstream website. This adaptation builds with Hugo and OINK's locally bundled assets.

## Sources and modifications {#source-snapshot}

| Item | Record |
| --- | --- |
| Repository | [babelfish_project_website](https://github.com/babelfish-for-postgresql/babelfish_project_website) |
| Revision | `f468c5ed3d38849502ee924cb3e236357404d14d` |
| Retrieval date | 2026-11-06 |
| Site maintenance | PGSTY documentation project |
| Theme | Hugo Extended / OINK 1.5.1 |

Jekyll pages were converted to Hugo Markdown, navigation and internal links were adapted, and Chinese translations with aligned heading IDs were added. Original code blocks, identifiers, blog authors, and publication dates are retained. Contributor photos were resized and converted to WebP; logo colors were adapted for light and dark backgrounds. The original homepage principles and founding references appear under [development principles](/babelfish/site/principles/) and [About](/babelfish/site/).

Each imported page links to its source at the fixed revision. `data/upstream-manifest.json` records checksums, destinations, and structural counts. Upstream [announced its documentation move in 2023](/babelfish/blog/release/babelfish-website-announcement/); use [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) for current documentation. Early design files are marked as historical, not current support matrices.
