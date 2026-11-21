# Content and dependency notice

Original text written for PG.CENTER at doc.pg.center is licensed under Creative Commons
Attribution 4.0 International. The full license is in `LICENSE`. Imported manuals
and third-party assets retain their own copyright and license terms.

The first collection was imported on 2026-08-15 from the English `pigsty.io` and
Simplified Chinese `pigsty.cc` documentation maintained by PGSTY. Those imported
adaptations use CC BY 4.0, subject to the original upstream terms identified below.

## Upstream documentation

The English edition was updated on 2026-11-21, and its Chinese incremental updates
completed three-pass self-review on 2026-11-22. Other translated editions retain their
prior source baselines pending synchronization. Existing draft and missing-translation
notices remain. `data/upstreams.yaml` records language-specific baselines; the update
inventory records completed Chinese work and the pending language tasks.

| Collection | English source edition | Upstream copyright and license |
| --- | --- | --- |
| Patroni | v4.1.5 | Copyright (c) 2025 Compose, Zalando SE, Patroni Contributors; MIT |
| pgBackRest | v2.60.1, commit `7aeba299c49abd768ca741506569007a5cab0870` | Copyright (c) 2015-2026 The PostgreSQL Global Development Group and David Steele; MIT |
| PgBouncer | v1.26.1, tag `pgbouncer_1_26_1` | Copyright (c) 2007-2009 Marko Kreen, Skype Technologies OÜ; ISC |
| pgBadger | v13.3, commit `0514893e97296695c77755fa36c59288c3afef3e` | Copyright (c) 2012-2026 Gilles Darold; PostgreSQL License |
| HAProxy | v3.4.8 LTS | Copyright 2000-2026 Willy Tarreau; GPL-2.0-only |
| etcd | v3.7 docs, website commit `e60635a46b57b7d74ca80c52c59aa0d37bed01a8`; updated for release v3.7.4 | Copyright 2013-present etcd Authors; CC BY 4.0 for prose, Apache 2.0 for code and samples |
| Apache Cloudberry | 2.x docs (`versioned_docs/version-2.x`), website commit `e3a102d15d0e85928a0cb5aaec24e67e6b40be7c`; release 2.2.0-incubating | Copyright 2024-2025 The Apache Software Foundation; Apache-2.0 |
| Apache Cloudberry PXF | `docs/`, commit `6683faa38ce4e2d146a77197991518aacb4b24e8`; release 2.2.0-incubating | Copyright 2024-2026 The Apache Software Foundation; Apache-2.0 |
| Apache Cloudberry Core Internals | `doc/core-internals/`, main commit `c2baef068a6f9f8b3c8110f9fdf5758306207693`; 3.0.0-devel / PostgreSQL 16.9 | Copyright 2024-2026 The Apache Software Foundation; Apache-2.0 and PostgreSQL License for cited PostgreSQL material |
| Halo Database MySQL compatibility documentation | Halo Database 1.0.16, captured 2026-11-07 | Copyright Halo Tech Co., Ltd.; no public documentation licence identified in the captured site |
| OpenHalo MySQL compatibility test report | OpenHalo 1.0.14.18, report commit `80a8d07` | Report contributors; repository licence not identified in the pinned snapshot |
| Citus | Microsoft Learn Citus 14, captured 2026-11-07; per-page commits in `data/imports/citus.json` | Copyright (c) Microsoft Corporation and contributors; CC BY 4.0 documentation, MIT code; retained original article links |

The etcd installation, Docker, and Kubernetes examples and release summary were
updated in English on 2026-11-21 for tag `v3.7.4`, release commit
`2e8a5c99e4982c8d4c521be15364ea4c5c68a489`, including its Go 1.26.11 toolchain.
The v3.7 documentation snapshot remains pinned separately from the software release.

Cloudberry 2.2.0-incubating uses PostgreSQL 14.10; 2.0 and 2.1 used 14.4. The
website documentation snapshot and software release are pinned separately in
`data/upstreams.yaml`. Exact website LICENSE and NOTICE texts are retained in
`static/third_party/cloudberry/`. Local corrections distinguish explicit Coordinator
activation from automatic Segment promotion and correct the AO compaction threshold
condition; both English and Chinese pages include these corrections.

The Apache Cloudberry collection, including PXF and Core Internals, is published
in English and Simplified Chinese. The Chinese edition translates explanatory text
while preserving source code, commands, program output, and upstream anchors. The upstream
`NOTICE` records that the product contains significant parts originally based on
Greenplum Database, Copyright (c) 2004-2020 VMware, Inc. or its affiliates, under
the Apache License 2.0. Apache Cloudberry is undergoing incubation at The Apache
Software Foundation; Apache Cloudberry and Apache are trademarks of the ASF.

The English PXF collection follows the development `docs/` snapshot at
`apache/cloudberry-pxf@6683faa38ce4e2d146a77197991518aacb4b24e8`.
The published release remains 2.2.0-incubating; the English snapshot includes later
Java and connector changes. Chinese is synchronized with this snapshot.
PXF retains Apache HAWQ and VMware attributions from the NOTICE and LICENSE files in
`static/third_party/pxf/`.

Core Internals follows Cloudberry `main` at `c2baef0`, a 3.0.0-devel / PostgreSQL
16.9 development snapshot. Its cited PostgreSQL-derived material retains the
PostgreSQL License and the exact PostgreSQL notice in
`static/third_party/core-internals/LICENSE-postgresql.txt`; the ASF LICENSE and
NOTICE are retained alongside it.

The English HAProxy edition follows stable release 3.4.8. It includes the complete Starter, Configuration, and
Management manual scope, with adapted headings, links, examples, and page grouping.
HAProxy-derived pages retain GPLv2 terms and are not covered by the site's CC BY 4.0
license. The upstream license explanation, OpenSSL exception, and complete GPLv2
text are published from `static/third_party/haproxy/LICENSE` and
`static/third_party/haproxy/GPL-2.0`.

The English pgBadger source is the stable v13.3 release of 2026-11-03. Historical website excerpts and sample reports retain their
original sources. The pgBadger license is retained in `static/third_party/pgbadger/LICENSE`.
pgBadger embeds a modified `SQL::Beautify` module under Artistic License 2.0.
Its report resources include MIT, GPL-2.0, and SIL Open Font License 1.1 components;
the upstream inventory is in `static/third_party/pgbadger/THIRD-PARTY-LICENSES`.
The linked historical sample reports retain their original scripts and notices.

Official source locations, pinned revisions, and available checksums are recorded
in `data/upstreams.yaml`. Each manual page identifies its source through
`upstream_link`. Full attribution is maintained in the eight localized
`content/attribution*.md` pages and published at
<https://doc.pg.center/attribution/>. Upstream downloads are kept outside the
repository; published license texts remain in `static/third_party/`.

## Theme and artwork

The site uses OINK 1.5.1 as a pinned Hugo module. OINK is licensed under Apache
License 2.0 and carries its upstream and bundled-dependency notices in the module.

The PostgreSQL elephant (Slonik) at `static/img/slonik.svg` and
`static/favicon.svg` is taken unmodified from the postgresql.org website
repository. The PNG at `static/images/postgresql.png` is its original
`media/img/about/press/elephant.png`, also used by the parent PG.CENTER site.
`static/favicon.ico` is the parent site's copy of `media/favicon.ico`;
the 32px and 256px PNG favicons and the touch icon are the original PNG entries
extracted from that ICO without changing their pixels. It is a mark of the PostgreSQL
Community Association of Canada and is used to refer to PostgreSQL under the
project's trademark and logo policy. Its use does not imply endorsement.

The collection marks that orbit Slonik on the home page are each project's
own logo, listed in `data/logos.yaml` and stored under `static/img/logo/`
(Patroni and pgBadger reuse the logos already shipped with their manuals under
`static/img/patroni/` and `static/img/pgbadger/`). pgBackRest's armchair is
`doc/resource/logo.svg` from the pgbackrest repository with its embedded
colour-scheme stylesheet removed; the HAProxy Community Edition sphere is a
downscaled raster of that logo; the etcd, PolarDB, IvorySQL, Babelfish,
Percona, Apache Cloudberry, Citus, pgEdge, FerretDB (shown for the DocumentDB
collection), and OrioleDB marks and the HaloTech mark shown for OpenHalo are
the copies collected for the Pigsty website (`static/img/icon/` in
`pgsty/pigsty.cc`), unmodified apart from scaling and the removal of
PolarDB's inline size attribute; the AgensGraph mark is the "A" glyph cropped
from the same copy of Bitnine's AGEDB wordmark. Each mark remains the
trademark of its owner, is used only to refer to that project's documentation,
and does not imply endorsement.

PgBouncer publishes no logo, so `static/img/logo/pgbouncer.png` is a
site-authored adaptation of the generated elephant artwork supplied for this
site. The asset keeps the blue-and-white elephant, removes its drop shadow,
and uses a transparent square canvas. It is not an official PgBouncer logo,
is provided under the site's CC BY 4.0 terms, and implies no endorsement by
the PgBouncer project.


# Database collections integrated on 2026-11-07

## PolarDB

The existing OINK edition was recovered from the pinned `polardb/polardb-pg-docs` snapshot `b4733b0350888242afeba432a6837458c348a937`. It preserves 8 English upstream articles and 55 Chinese articles, plus a Chinese translation notice and local section introductions. The upstream language editions are intentionally unequal. Copyright © Alibaba Group, Inc.; the upstream site declares Apache 2.0. Images retain their original bytes.

Source records: `data/imports/polardb.json`; registry: `data/upstreams.yaml`.

## IvorySQL

Imported from the local IvorySQL edition, which pins `IvorySQL/ivorysql_docs` v5.6 at `7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1`. It includes 75 English and 80 Chinese upstream articles, plus indexes and source notices. These are independent upstream language editions. The documentation repository has no standalone LICENSE or NOTICE at this revision; the software Apache 2.0 licence is not presented as a blanket grant over all documentation or third-party images.

Source records: `data/imports/ivorysql.json`; registry: `data/upstreams.yaml`.

## OpenHalo

Adapted and translated from `HaloTech-Co-Ltd/openHalo` README at `90fc8d777c3f111d4c8d236625bb15b5d4b19d7c`. The overview and installation guide retain the source commands and two original figures. This is the OpenHalo-specific introduction, not a second copy of the PostgreSQL core manual. Retained files include GPLv3, PostgreSQL copyright and third-party notices. Product names remain their owners’ trademarks.

Source records: `data/imports/openhalo.json`; registry: `data/upstreams.yaml`.

## Halo Database MySQL reference

The MySQL compatibility guides summarize the official [Halo Database documentation](https://doc.halodbtech.com/multi-mode-compatibility/mysql), product version 1.0.16, captured on 2026-11-07. The complete official pages remain at the upstream site. No public documentation licence was identified in the captured site; these guides are original summaries with source links and are not presented as GPL material.

Source records: `data/imports/openhalo.json`; registry: `data/upstreams.yaml`.

## OpenHalo MySQL test report

The compatibility-boundary guide summarizes the independent [OpenHalo MySQL Compatibility Testing Report](https://github.com/fxcollot/openHaloDocumentation/blob/80a8d077b1d329e397b251fa8c64dbded303bba2/TestingReport/OpenHaloMySQLCompatibilityTestingReport.md) at commit `80a8d077b1d329e397b251fa8c64dbded303bba2`. It is historical evidence for OpenHalo 1.0.14.18, not a Halo Database 1.0.16 support matrix. The repository licence was not identified in the pinned snapshot; the report is linked and summarized rather than reproduced.

Source records: `data/imports/openhalo.json`; registry: `data/upstreams.yaml`.

## Babelfish

Imported from the bilingual community edition of `babelfish-for-postgresql/babelfish_project_website` at `f468c5ed3d38849502ee924cb3e236357404d14d`: documentation, historical design material, release posts, contributors and source notices. The upstream website has its own licence records; these are kept distinct from the dual-licensed Babelfish software.

Source records: `data/imports/babelfish.json`; registry: `data/upstreams.yaml`.

## Percona TDE

The English Percona collection now contains pg_tde 2.3.0 documentation at `percona/pg_tde@5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a`, with the 2.3.0 release notes added to the previous 66 articles, section indexes, and PGSTY editorial guides. Chinese includes the reviewed 2.3.0 incremental updates. It is not the entire Percona product documentation. The complete pg_tde copyright text, including the PostgreSQL, University of California and Percona portions, is retained.

Source records: `data/imports/percona.json`; registry: `data/upstreams.yaml`.

## AgensGraph

Imported from the existing AgensGraph 2.18.6.1 edition. Documentation copyright is 2014–2026 SKAI Worldwide Co., Ltd., under Apache 2.0, with PostgreSQL notices retained. The existing Chinese drafts and their review status are preserved. Sixteen guide-only pages are explicitly marked as untranslated placeholders; two additional English pages have no Chinese peer. A migration and successful build do not certify translation accuracy.

Source records: `data/imports/agensgraph.json`; registry: `data/upstreams.yaml`.

## pgEdge

Includes Spock, LOLOR, SafeSession and Snowflake from their existing OINK edition. The English source set is Spock v6.0.0-beta.2, LOLOR 1.3.0 development, SafeSession v1.1, and Snowflake v2.6.1. Chinese includes this batch's reviewed incremental updates and six newly translated articles; unchanged draft portions still await review. Of 108 imported upstream articles, 32 have Chinese machine drafts; their status and review notices remain visible. The PostgreSQL licence and project-specific copyright notices are retained. Source commits are listed below.

Source records: `data/imports/pgedge.json`; registry: `data/upstreams.yaml`.

## DocumentDB

Imported from the official `documentdb/docs` repository at `8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5` and the published website at `documentdb/documentdb.github.io` commit `4a83a0712149e101a2bbb38934bed36497cdf40f` (21 November 2026). The 306 documentation Markdown records and 20 website article bodies produce 310 English pages. All 310 pages have complete Simplified Chinese counterparts, including the ten additions. This includes the website-generated Docker, package, operations, and offline-install guides, the installation primer, category descriptions, and the upstream forthcoming architecture notice. Superseded source guides are retained with notices. The independently versioned Kubernetes Operator manual remains linked at its official site.

The original Chinese edition was translated and reviewed against the November 7 English edition with AI assistance. This update batch received three-pass self-review against the November 21 English changes, plus checks of examples, literals, links, and heading IDs. Code, commands, output, and upstream error messages are preserved. Forty pages include bilingual editorial notes identifying inconsistencies in the original prose or examples. The documentation and website repositories have no standalone documentation licence in these snapshots. DocumentDB software is MIT-licensed, which is not asserted here as a separate blanket licence grant for all documentation. The upstream sources and their rights notices remain authoritative.

Source records: `data/imports/documentdb.json`; registry: `data/upstreams.yaml`.

## OrioleDB

The OrioleDB collection is imported from PGSTY's existing bilingual community
edition, based on https://www.orioledb.com/ captured on 2026-11-06. It includes
18 documentation articles and two benchmark recipes, with 26 pages per language
including indexes and source notes. The source edition's blog, landing pages,
author profiles and taxonomy archives are not part of this collection.

Project documentation: Copyright (c) 2025-2026, Supabase Inc. The project offers
Apache-2.0 OR PostgreSQL; this documentation edition selects PostgreSQL. The full
notice and disclaimer are retained in static/third_party/orioledb/LICENSE-POSTGRESQL.txt.
Website and benchmark materials: Copyright © 2026 Supabase Inc. No separate
blanket website-content license was identified; these materials and marks retain
their original rights and are not relicensed under this site's license.
Chinese translation and community curation: PGSTY.

The import changes routes, navigation, page metadata and resource placement;
code, figures, heading identities and the source edition's editorial notes are
preserved. data/imports/orioledb.json records source and asset checksums. Detailed
coverage and source discrepancies are in content/orioledb/attribution/.


## Citus 14 documentation

The Citus collection imports all 59 articles in the Microsoft Learn Citus 14
navigation, including ten technical blog articles retained by upstream. It adds
native OINK category indexes and a bilingual homepage and source notice.
English and Chinese snapshots were captured on 2026-11-07; English is authoritative.
The upstream Chinese edition is machine translated and serves only as a reference.
All 59 imported Chinese pages have been edited against the English edition;
future unreviewed pages must keep explicit machine-draft notices.

Published per-page revisions and HTML/Markdown hashes are recorded in
`data/imports/citus.json`. The public MicrosoftDocs/azure-databases-docs repository
was unavailable at capture time. License texts are preserved from the fork
Kiranchandratrey/azure-databases-docs, commit
`ff9de504fdbe2b7aa9d06411e0f0472d39dc1f14`; this is distinct from the live Learn
page revisions. The unchanged `LICENSE`, `LICENSE-CODE`, and
`ThirdPartyNotices.md` are in `static/third_party/citus/`.

Copyright (c) Microsoft Corporation and contributors. Documentation is CC BY 4.0;
code is MIT. Original Citus publication links and historical notices are retained.
The licenses do not grant rights to Microsoft names, logos, or trademarks.
Local changes include navigation, cross-links, OINK callouts, page bundles,
Citus-14 moniker selection, and Chinese editorial corrections. The collection
source page explains coverage, translation status, and the original rights.
