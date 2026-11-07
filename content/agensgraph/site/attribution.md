---
title: Attribution and source manifest
linkTitle: Attribution and source manifest
description: Copyright, licence, source version, and modification boundary for the AgensGraph material on this site.
type: docs
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/index.html
upstream_source: agensgraph
upstream_modified: true
---

This site adapts the **AgensGraph 2.18.6.1** documentation published by [SKAI Worldwide](https://skaiworldwide.com/), formerly Bitnine. The upstream manual is the authoritative source for product behavior, syntax, examples, compatibility, and release boundaries.

## Upstream material {#upstream-material}

| Field | Record |
| --- | --- |
| Work | AgensGraph documentation 2.18.6.1 |
| Copyright | Copyright 2014–2026 SKAI Worldwide Co., Ltd. |
| License | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Source | [Documentation portal](https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/) |
| Code | [skaiworldwide-oss/agensgraph](https://github.com/skaiworldwide-oss/agensgraph) |
| Retrieved | 2026-11-06, Asia/Shanghai |

Every imported page carries an Oink page-end attribution line with its original source URL, copyright holder, SPDX licence, and this notice page. Pages marked as adapted include a local modification note. The English manual is imported from the upstream Markdown views; section indexes are converted from upstream reStructuredText. Editorial blog posts are written for this site and link back to the relevant upstream pages.

The machine-readable [source manifest](/agensgraph/assets/source-manifest.json) records 90 leaf Markdown pages and 14 section index sources, plus the original property-graph illustration, with source URLs, byte counts, and SHA-256 checksums. All 104 text sources were verified against the version-specific 2.18.6.1 URLs on 2026-11-07.

## What this site changes {#change-boundary}

- The Hugo / Oink shell, visual design, navigation, search, footer, and landing data are original site work.
- English manual pages are converted to Oink Markdown routes, with relative links rewritten to local routes and upstream source links retained in front matter.
- This collection publishes English and the available Chinese pages. Chinese drafts retain their status; unfinished guide-only pages link to the English source and are excluded from translation coverage. Code, query keywords, product names, and version identifiers are preserved.
- Blog posts are PGSTY editorial summaries based on named upstream pages; they are not presented as SKAI Worldwide announcements.

## Upstream notice {#upstream-notice}

The upstream repository's notice is retained verbatim:

```text
AgensGraph
Copyright 2014-2026 SKAI Worldwide Co., Ltd.

This product is licensed under the Apache License, Version 2.0.
See the LICENSE file.

This product is based on PostgreSQL.
Portions Copyright (c) 1996-2026, PostgreSQL Global Development Group
Portions Copyright (c) 1994, The Regents of the University of California
The PostgreSQL copyright notice, permission notice and disclaimers
are contained in the COPYRIGHT file.
```

Download the preserved [Apache 2.0 license](/agensgraph/assets/licenses/agensgraph-Apache-2.0.txt), [AgensGraph NOTICE](/agensgraph/assets/licenses/agensgraph-NOTICE.txt), and [PostgreSQL COPYRIGHT](/agensgraph/assets/licenses/PostgreSQL-COPYRIGHT.txt). These files are kept in `static/agensgraph/assets/licenses/` in the site source.

AgensGraph and SKAI Worldwide names identify the upstream project. This is an independent community documentation site, not an official SKAI Worldwide publication.

## Contact and corrections {#corrections}

For product corrections, consult the upstream [issue tracker](https://github.com/skaiworldwide-oss/agensgraph/issues). For this site's route, translation, or provenance corrections, update the source files and rerun `make check`.
