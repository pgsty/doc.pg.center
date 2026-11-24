---
title: "Attribution and Licensing"
linkTitle: "Attribution"
description: "Where every page on this site comes from, who holds it, which licence it carries, and where the complete notice is retained."
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

PG.CENTER republishes documentation for PostgreSQL tools and database variants. Every documentation page
carries a one-line credit at the end naming the work it is derived from, its copyright holder,
its licence, and a link back to the section of this page that covers it.

This page is that record. It states what was imported, when, from which pinned revision, under
which licence, and where the complete upstream notice is retained.

> [!NOTE]
> PG.CENTER is an independent community documentation project. It is not affiliated with, endorsed
> by, or an official publication of any of the projects below, nor of the PostgreSQL Global
> Development Group.

## Summary {#summary}

English updates below were reviewed on **November 21, 2026**. The Chinese incremental updates were completed with three-pass self-review on **November 22, 2026**. The other reviewed language editions include the operations-manual updates listed below. `data/upstreams.yaml` records the language-specific baselines; page-level links identify each source revision. The November 23 follow-up completed the 117 recorded Chinese translation tasks and restored the missing article text on four pgEdge section indexes.

| Component | Upstream work | Pinned at | Licence | Retained notice |
|---|---|---|---|---|
| [Patroni](/patroni/) | [Patroni documentation](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/pgbackrest/) | [pgBackRest documentation](https://pgbackrest.org/) | v2.60.1 | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/pgbouncer/) | [PgBouncer documentation](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [Upstream `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/pgbadger/) | [pgBadger documentation](https://pgbadger.darold.net/) | v13.3, commit `0514893` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/haproxy/) | [HAProxy 3.4 manuals](https://docs.haproxy.org/3.4/) | v3.4.8 LTS | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/etcd/) | [etcd v3.7 documentation](https://etcd.io/docs/v3.7/) | v3.7 docs, commit `e60635a`; release v3.7.4 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Upstream `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |
| [Apache Cloudberry](/cloudberry/) | [Apache Cloudberry 2.x documentation](https://cloudberry.apache.org/docs/) | 2.x docs, commit `e3a102d`; release 2.2.0-incubating | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [Upstream `LICENSE`](https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/LICENSE) and [`NOTICE`](https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/NOTICE) |
| [PXF](/cloudberry/pxf/) | [Apache Cloudberry PXF](https://cloudberry.apache.org/pxf/) | Docs `6683faa3`; release 2.2.0-incubating | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](/third_party/pxf/LICENSE), [NOTICE](/third_party/pxf/NOTICE) |
| [Core Internals](/cloudberry/core-internals/) | [Apache Cloudberry Core Internals](https://cloudberry.apache.org/core-internals/) | Main `c2baef0`; 3.0.0-devel / PostgreSQL 16.9 | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), PostgreSQL | [LICENSE](/third_party/core-internals/LICENSE), [NOTICE](/third_party/core-internals/NOTICE) |
| [PolarDB](/polardb/) | [PolarDB for PostgreSQL Documentation](https://github.com/polardb/polardb-pg-docs) | b4733b0 | Apache-2.0 | [Source and full notices](/polardb/site/attribution/) |
| [IvorySQL](/ivorysql/) | [IvorySQL Documentation](https://github.com/IvorySQL/ivorysql_docs) | v5.6 · 7c3f4a67e7d3 | LicenseRef-IvorySQL-Docs | [Source and full notices](/ivorysql/site/license/) |
| [OpenHalo 18](/openhalo/18/) | [PGSTY OpenHalo 18 source and acceptance](https://github.com/pgsty/openhalo) | v18.6.1 (`2627e6f`, aux_mysql 1.9); accepted at `6a93e8f` on 2026-11-10 | GPL-3.0-only | [Source and full notices](#openhalo) |
| [OpenHalo (PG14 historical)](/openhalo/quick-start/) | [OpenHalo documentation](https://github.com/HaloTech-Co-Ltd/openHalo) | master 90fc8d7 | GPL-3.0-only | [Source and full notices](/openhalo/assets/LICENSE.txt) |
| [Halo Database MySQL reference](/openhalo/mysql-compatibility/) | [Halo Database official documentation](https://doc.halodbtech.com/multi-mode-compatibility/mysql) | 1.0.16; snapshot 2026-11-07 | LicenseRef-HaloDB-Docs | [Source and terms](#halodb) |
| [OpenHalo test evidence](/openhalo/mysql-compatibility-gaps/) | [OpenHalo MySQL compatibility report](https://github.com/fxcollot/openHaloDocumentation) | OpenHalo 1.0.14.18; commit 80a8d07 | LicenseRef-OpenHalo-Test-Report | [Source and terms](#openhalo-tests) |
| [Babelfish](/babelfish/) | [Babelfish project website](https://github.com/babelfish-for-postgresql/babelfish_project_website) | main @ f468c5ed3d38 | LicenseRef-Babelfish-Website | [Source and full notices](/babelfish/site/attribution/) |
| [Percona TDE](/percona/) | [Percona pg_tde documentation](https://github.com/percona/pg_tde) | 2.3.0; docs 5dd7a9e4 | LicenseRef-pg-tde | [Source and full notices](/percona/assets/legal/pg_tde-COPYRIGHT.txt) |
| [AgensGraph](/agensgraph/) | [AgensGraph documentation](https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/index.html) | 2.18.6.1 | Apache-2.0 | [Source and full notices](/agensgraph/site/attribution/) |
| [pgEdge](/pgedge/) | [pgEdge extension documentation](https://github.com/pgEdge) | Spock beta.2; LOLOR development; SafeSession 1.1; Snowflake 2.6.1 | PostgreSQL | [Source and full notices](/pgedge/about/attribution/) |
| [DocumentDB](/documentdb/) | [DocumentDB documentation](https://github.com/documentdb/docs) | DocumentDB 1.2.0; docs 8fb7fda; website 4a83a07 | LicenseRef-DocumentDB-Docs | [Source and full notices](https://github.com/documentdb/docs/tree/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5) |
| [OrioleDB](/orioledb/) | [OrioleDB documentation and benchmarks](https://www.orioledb.com/docs) | Website snapshot 2026-11-06 | PostgreSQL; website materials retain upstream terms | [Source and full notices](/orioledb/attribution/) |
| [Citus](/citus/) | [Microsoft Learn Citus 14](https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14) | 2026-11-07; per-page revisions | CC BY 4.0; MIT code | [Sources and full notices](/citus/attribution/) |
{.wide .expand}

Every collection is **adapted**, not mirrored. Headings, anchors, cross-links, code signatures,
page grouping, and navigation are reworked for this edition; the upstream prose itself is
preserved. The page-end credit says so, and links to this site's change history for the page you
are reading.

## Patroni {#patroni}

Imported on 2026-08-15 from the [Patroni documentation](https://patroni.readthedocs.io/en/latest/)
for **v4.1.5**.

Patroni is copyright (c) 2025 Compose, Zalando SE, Patroni Contributors, and is distributed under
the [MIT License](https://opensource.org/license/mit). The complete licence text is retained
[upstream](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

Imported on 2026-08-15 from the [pgBackRest documentation site](https://pgbackrest.org/)
and refreshed in English on 2026-11-21 to **v2.60.1**, tag `release/2.60.1`, commit
[`7aeba29`](https://github.com/pgbackrest/pgbackrest/commit/7aeba299c49abd768ca741506569007a5cab0870).

pgBackRest is copyright (c) 2015-2026 The PostgreSQL Global Development Group and David Steele,
and is distributed under the [MIT License](https://opensource.org/license/mit). The complete
licence text is retained [upstream](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

Imported on 2026-08-15 from the [PgBouncer documentation site](https://www.pgbouncer.org/)
for **v1.25.2** and refreshed on 2026-10-23 to
[**v1.26.1**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_1).

PgBouncer is copyright (c) 2007-2009 Marko Kreen, Skype Technologies OÜ, and is distributed under
the [ISC License](https://opensource.org/license/isc-license-txt). The complete licence text is
retained [upstream](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT).

## pgBadger {#pgbadger}

Imported on 2026-08-15 from <https://pgbadger.darold.net/> and from
[`darold/pgbadger`](https://github.com/darold/pgbadger), and refreshed in English on 2026-11-21 for v13.3 at commit
[`0514893`](https://github.com/darold/pgbadger/commit/0514893e97296695c77755fa36c59288c3afef3e).
This is the published v13.3 release of November 3, 2026. Historical website excerpts and sample reports retain their own sources.

pgBadger is copyright (c) 2012-2026 Gilles Darold and is distributed under the
[PostgreSQL License](https://opensource.org/license/postgresql). The complete licence text is
retained beside the offline examples as
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) and in
`static/third_party/pgbadger/LICENSE` in the site repository.

> [!IMPORTANT]
> pgBadger embeds a modified `SQL::Beautify` module under Artistic License 2.0, and its
> generated-report resources include MIT, GPL-2.0, and SIL Open Font License 1.1 components. The
> complete upstream resource inventory is retained as
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> The [sample reports](/pgbadger/sample-reports/) published here are historical generated
> artifacts and keep their original embedded notices.

## HAProxy {#haproxy}

Imported on 2026-08-16 and updated in English on 2026-11-21 to the official [HAProxy v3.4.8 release](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8). The complete `doc/intro.txt`, `doc/configuration.txt`, and `doc/management.txt` scope is reorganized into 34 reading pages. The Starter and Management sources are unchanged from the preceding snapshot; Configuration changes are recorded in the update diff. The reviewed translations include the v3.4.8 updates.

HAProxy is copyright 2000-2026 Willy Tarreau and is distributed under the
[GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
HAProxy's own licence explanation, its OpenSSL exception, and the complete GPLv2 text are
published as [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) and
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> The HAProxy-derived pages are **not** covered by this site's CC BY 4.0 licence. They carry
> HAProxy's GPLv2 terms.

## etcd {#etcd}

The English v3.7 manual was refreshed on 2026-11-21 from [`etcd-io/website@e60635a46b57`](https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7). Installation examples and the release summary target [v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4), commit `2e8a5c99e4982c8d4c521be15364ea4c5c68a489`, built with Go 1.26.11. The separately pinned changelog remains headed “v3.7.4 (TBC)”; the release tag confirms publication. The documentation and software source checksums are recorded separately in `data/upstreams.yaml`.

The etcd documentation is copyright 2013-present etcd Authors. Its prose is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), while code and code samples are
licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). The complete notice is
retained [upstream](https://github.com/etcd-io/website/blob/main/LICENSE).

## Apache Cloudberry {#cloudberry}

Updated in English on 2026-11-21 from the Apache Cloudberry website repository at commit
[`e3a102d15d0e`](https://github.com/apache/cloudberry-site/commit/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c). The source is the 2.x
documentation in [`versioned_docs/version-2.x`](https://github.com/apache/cloudberry-site/tree/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x), which upstream publishes at
<https://cloudberry.apache.org/docs/> for the 2.2.0-incubating release.

The documentation snapshot and software release are recorded separately. Cloudberry
`2.2.0-incubating` uses PostgreSQL `14.10`; versions `2.0` and `2.1` used `14.4`. Older
recorded examples retain their original version output. Exact upstream copies of the
[LICENSE](/third_party/cloudberry/LICENSE) and [NOTICE](/third_party/cloudberry/NOTICE)
are retained with this edition.

Navigation follows the upstream 2.x sidebar. Docusaurus admonitions, tabs, and collapsible blocks
are rewritten as OINK callouts and tabs, and images live beside the pages that use them. Three pages
that upstream publishes outside its sidebar, the TPC-H and TPC-DS benchmarks and `pg_restore`, are
included. Nineteen links that are broken upstream (legacy Greenplum paths and typos) point to the
page they refer to, an unclosed note is closed, and a misspelled heading is corrected. Both editions now have 672 pages, including the 31 new pages and the updated PXF guides.
Chinese pages preserve code, commands, program output, and their source English heading anchors. Local corrections also
distinguish explicit Coordinator activation from automatic Segment promotion and
correct the AO compaction threshold condition against the 2.2 release source; both
language editions include these corrections.

The Apache Cloudberry website is Copyright 2024-2025 The Apache Software Foundation and is licensed
under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Its
[`NOTICE`](https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/NOTICE) states that the product contains significant parts originally based on
Greenplum Database from VMware, Inc. or its affiliates, Copyright (c) 2004-2020, also licensed under
the Apache License 2.0. The page-end credit and this section identify the pages as modified.

Apache Cloudberry, Apache, and the Apache feather logo are trademarks of The Apache Software
Foundation. Apache Cloudberry is an effort undergoing incubation at The Apache Software Foundation
(ASF), sponsored by the Apache Incubator. Incubation is required of all newly accepted projects until
a further review indicates that the infrastructure, communications, and decision making process have
stabilized in a manner consistent with other successful ASF projects. While incubation status is not
necessarily a reflection of the completeness or stability of the code, it does indicate that the
project has yet to be fully endorsed by the ASF.

## Apache Cloudberry PXF {#pxf}

The English PXF collection is sourced from [`apache/cloudberry-pxf@6683faa38ce4`](https://github.com/apache/cloudberry-pxf/commit/6683faa38ce4e2d146a77197991518aacb4b24e8), path `docs/`, as pinned by the current Cloudberry website. This development documentation includes Java 17/21 requirements and connector changes newer than the published [`2.2.0-incubating`](https://github.com/apache/cloudberry-pxf/releases/tag/2.2.0-incubating) release. The Chinese edition is synchronized with this snapshot.

The source is Copyright 2024-2026 The Apache Software Foundation and is licensed under Apache License 2.0. Its [NOTICE](https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/NOTICE) records software originally developed by Apache HAWQ, Copyright 2017 The Apache Software Foundation. The [LICENSE](https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/LICENSE) also retains the Greenplum Platform Extension Framework attribution, Copyright 2018-Present VMware, Inc. or its affiliates. The upstream [documentation index](https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/docs/index.md#L26-L32) identifies `greenplum-db/pxf-archive` 6.10.1 as the documentation's origin; the software fork is identified separately as 6.10.1-SNAPSHOT. This community edition adapts the formatting, navigation, and links while retaining upstream notices.

The exact upstream [LICENSE](/third_party/pxf/LICENSE) and [NOTICE](/third_party/pxf/NOTICE) are retained locally.

## Apache Cloudberry Core Internals {#core-internals}

Core Internals is sourced from [`apache/cloudberry@c2baef0`](https://github.com/apache/cloudberry/commit/c2baef068a6f9f8b3c8110f9fdf5758306207693), path `doc/core-internals`, as pinned by the Cloudberry website. It documents a `main` development snapshot: [configure.ac](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/configure.ac#L23-L24) identifies Cloudberry `3.0.0-devel` and PostgreSQL `16.9`. Its implementation details must be read against that revision. Cloudberry `2.2.0-incubating` follows the PostgreSQL `14.10` line.

The handbook carries ASF headers under Apache License 2.0. The repository [NOTICE](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/NOTICE) states Copyright 2024-2026 The Apache Software Foundation and preserves the Greenplum Database attribution, Copyright (c) 2004-2020 VMware, Inc. or its affiliates. The [LICENSE](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/LICENSE#L203-L206) separately identifies PostgreSQL-derived material under the [PostgreSQL License](https://github.com/apache/cloudberry/blob/c2baef068a6f9f8b3c8110f9fdf5758306207693/licenses/LICENSE-postgresql.txt), including the PostgreSQL Global Development Group and University of California notices. Code excerpts retain the licensing of their cited source files. This community edition adapts formatting, navigation, and links and retains the handbook's source citations and acknowledgments.

The exact [LICENSE](/third_party/core-internals/LICENSE), [NOTICE](/third_party/core-internals/NOTICE), and [PostgreSQL License](/third_party/core-internals/LICENSE-postgresql.txt) are retained locally.

## This site {#site}

Original text written for PG.CENTER is published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), except where an upstream licence
above applies to the page instead.


The PostgreSQL elephant (Slonik) shown on the home page is the PostgreSQL project's own mark,
taken from the [postgresql.org website repository](https://git.postgresql.org/gitweb/?p=pgweb.git)
and republished here unmodified under
[the PostgreSQL trademark and logo policy](https://www.postgresql.org/about/policies/trademarks/)
as a reference to PostgreSQL. It is a mark of the PostgreSQL Community Association of Canada and
its use here does not imply endorsement.

The collection marks that orbit the elephant are each project's own logo, reproduced only to refer
to that project's documentation; the DocumentDB collection is shown with the FerretDB mark and
AgensGraph with the "A" of the AGEDB wordmark. They remain trademarks of their respective owners,
and their use here does not imply endorsement. PgBouncer publishes no logo, so its mark is an
original drawing made for this site and is not an official PgBouncer logo. The individual sources
are listed in the repository [NOTICE](https://github.com/pgsty/doc.pg.center/blob/main/NOTICE.md).

The site is built with [OINK](https://oink.pgsty.com/) v1.5.1, a Hugo theme licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), which carries its own upstream
and bundled-dependency notices in the module source.

Corrections to any attribution on this page are welcome through the
[site repository](https://github.com/pgsty/doc.pg.center/issues).


## PolarDB {#polardb}

The existing OINK edition was recovered from the pinned `polardb/polardb-pg-docs` snapshot `b4733b0350888242afeba432a6837458c348a937`. It preserves 8 English upstream articles and 55 Chinese articles, plus the community Chinese translation of the coding-style guide and local section introductions. The upstream language editions are intentionally unequal. Copyright © Alibaba Group, Inc.; the upstream site declares Apache 2.0. Images retain their original bytes.

[Source and full notices](/polardb/site/attribution/).

## IvorySQL {#ivorysql}

Imported from the local IvorySQL edition, which pins `IvorySQL/ivorysql_docs` v5.6 at `7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1`. It includes 75 English and 80 Chinese upstream articles, plus indexes and source notices. These are independent upstream language editions. The documentation repository has no standalone LICENSE or NOTICE at this revision; the software Apache 2.0 licence is not presented as a blanket grant over all documentation or third-party images.

[Source and full notices](/ivorysql/site/license/).

## OpenHalo {#openhalo}

The collection homepage is a maintained version guide. The [OpenHalo 18 manual](/openhalo/18/) describes the [PGSTY fork](https://github.com/pgsty/openhalo) at source tag `v18.6.1` (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`, `aux_mysql 1.9`) together with the retained independent final acceptance evidence pinned to commit `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` (dated 2026-11-10; the four commits `6a93e8f..2627e6f` add only copyright headers, `.gitignore` rules, and documentation updates). Multi-platform binary packages for `v18.6.1` remain pending package acceptance, and no binary download URL is implied. New prose and translations are maintained by PGSTY; adapted material retains upstream rights.

The historical PG14 build guide derives from `HaloTech-Co-Ltd/openHalo` README at `90fc8d777c3f111d4c8d236625bb15b5d4b19d7c`, with original commands and two figures preserved. The initial PG18 review remains explicitly tied to `9dc937f`. The current manual does not replace their historical evidence or the separately attributed commercial Halo Database material.

Retained files include GPLv3, PostgreSQL copyright and third-party notices. PostgreSQL and the maintained protocol hooks use PostgreSQL License terms (Portions Copyright (c) 1996–2025, PostgreSQL Global Development Group); `aux_mysql` derives from GPLv3 OpenHalo (Copyright (c) 2025, Halo Tech Co., Ltd.; Portions Copyright (c) 2026, PGSTY PTE. LTD.), and builds including it are distributed under GPLv3. Product names remain their owners' trademarks. Source fingerprints and page provenance are recorded in `data/imports/openhalo.json` and `data/imports/openhalo-pgsty.json`.

[Source and full notices](/openhalo/assets/LICENSE.txt).

## Halo Database documentation {#halodb}

The MySQL compatibility guides summarize the official [Halo Database documentation](https://doc.halodbtech.com/multi-mode-compatibility/mysql) for product version **1.0.16**, captured on 2026-11-07. The source pages cover MySQL modes, SQL syntax, data types, functions, operators, other compatibility features, and engine parameters. The pages in this collection are short original guides with links to the complete upstream reference; they do not reproduce the full manual. No public documentation licence was identified on the captured official site, so the upstream rights holder and site terms remain authoritative.

[Source and terms](#halodb).

## OpenHalo test evidence {#openhalo-tests}

The compatibility-boundary page summarizes the independent [OpenHalo MySQL Compatibility Testing Report](https://github.com/fxcollot/openHaloDocumentation/blob/80a8d077b1d329e397b251fa8c64dbded303bba2/TestingReport/OpenHaloMySQLCompatibilityTestingReport.md) at commit `80a8d077b1d329e397b251fa8c64dbded303bba2`. It tested OpenHalo 1.0.14.18, not Halo Database 1.0.16. The report is linked as historical evidence; its repository licence was not identified in the pinned snapshot, and this site does not reproduce the report.

[Source and terms](#openhalo-tests).

## Babelfish {#babelfish}

Imported from the bilingual community edition of `babelfish-for-postgresql/babelfish_project_website` at `f468c5ed3d38849502ee924cb3e236357404d14d`: documentation, historical design material, release posts, contributors and source notices. The upstream website has its own licence records; these are kept distinct from the dual-licensed Babelfish software.

[Source and full notices](/babelfish/site/attribution/).

## Percona TDE {#percona}

The English Percona collection now contains pg_tde 2.3.0 documentation at `percona/pg_tde@5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a`, with the 2.3.0 release notes added to the previous 66 articles, section indexes, and PGSTY editorial guides. Chinese includes the reviewed 2.3.0 incremental updates. It is not the entire Percona product documentation. The complete pg_tde copyright text, including the PostgreSQL, University of California and Percona portions, is retained.

[Source and full notices](/percona/assets/legal/pg_tde-COPYRIGHT.txt).

## AgensGraph {#agensgraph}

Imported from the existing AgensGraph 2.18.6.1 edition. Documentation copyright is 2014–2026 SKAI Worldwide Co., Ltd., under Apache 2.0, with PostgreSQL notices retained. All 113 English pages have Chinese counterparts. The community translated the backup guide, upgrade walkthrough, and sixteen Cypher clause references against the maintained English edition.

[Source and full notices](/agensgraph/site/attribution/).

## pgEdge {#pgedge}

Includes Spock, LOLOR, SafeSession and Snowflake from their existing OINK edition. The English source set is Spock v6.0.0-beta.2, LOLOR 1.3.0 development, SafeSession v1.1, and Snowflake v2.6.1. The community added 66 Chinese pages, reviewed 32 earlier drafts against English and restored four section articles. All 118 routes have a Chinese counterpart. Security passages in the SafeSession manual and changelog and the LOLOR release notes are adapted for administrators. The PostgreSQL licence and project-specific copyright notices are retained. Source commits are listed below.

[Source and full notices](/pgedge/about/attribution/).

| Extension | Fixed commit |
| --- | --- |
| spock | [d05e2e2b6a82](https://github.com/pgEdge/spock/tree/d05e2e2b6a82) |
| lolor | [1548836b0df0](https://github.com/pgEdge/lolor/tree/1548836b0df0) |
| safesession | [d66225fcceef](https://github.com/pgEdge/pgedge-safesession/tree/d66225fcceef) |
| snowflake | [9506e1bd5c1f](https://github.com/pgEdge/snowflake/tree/9506e1bd5c1f) |

## DocumentDB {#documentdb}

Imported from the official `documentdb/docs` repository at `8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5` and the published website at `documentdb/documentdb.github.io` commit `4a83a0712149e101a2bbb38934bed36497cdf40f` (21 November 2026). The 306 documentation Markdown records and 20 website article bodies produce 310 English pages. All 310 pages have complete Simplified Chinese counterparts, including the ten additions. This includes the website-generated Docker, package, operations, and offline-install guides, the installation primer, category descriptions, and the upstream forthcoming architecture notice. Superseded source guides are retained with notices. The independently versioned Kubernetes Operator manual remains linked at its official site.

The original Chinese edition was translated and reviewed against the November 7 English edition with AI assistance. This update batch received three-pass self-review against the November 21 English changes, plus checks of examples, literals, links, and heading IDs. Code, commands, output, and upstream error messages are preserved. Forty pages include bilingual editorial notes identifying inconsistencies in the original prose or examples. The documentation and website repositories have no standalone documentation licence in these snapshots. DocumentDB software is MIT-licensed, which is not asserted here as a separate blanket licence grant for all documentation. The upstream sources and their rights notices remain authoritative.

[Documentation sources](https://github.com/documentdb/docs/tree/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5) · [Website sources](https://github.com/documentdb/documentdb.github.io/tree/4a83a0712149e101a2bbb38934bed36497cdf40f).

## OrioleDB {#orioledb}

Imported from PGSTY's bilingual OrioleDB community edition, based on the live website snapshot of **2026-11-06**. The collection contains all 18 documentation articles and two benchmark recipes, plus section indexes and source notes: 26 pages per language. Original HTML and Markdown checksums, code fingerprints, and asset hashes are recorded in `data/imports/orioledb.json`. The snapshot is not tied to one software release; the benchmark recipes use beta18. The English homepage additionally records the v1.10.3 release of November 9, 2026 without changing those historical benchmark versions.

Project documentation retains **Copyright (c) 2025-2026, Supabase Inc.**, under the PostgreSQL License selected by the source edition from the project's dual Apache-2.0 OR PostgreSQL license. The complete [license and warranty disclaimer](/third_party/orioledb/LICENSE-POSTGRESQL.txt) are retained. Website and benchmark materials retain **Copyright © 2026 Supabase Inc** and their original terms; no separate blanket website-content license was identified. Chinese translation and curation are credited to PGSTY. This import preserves the existing translation status.

[Coverage, rights, and source discrepancies](/orioledb/attribution/).


## Citus {#citus}

The [Citus 14 collection](/citus/) follows the Microsoft Learn snapshot of
2026-11-07: 59 imported pages, including ten technical articles, with local
figures and bilingual OINK navigation. Copyright (c) Microsoft Corporation and
contributors. Documentation is CC BY 4.0; code is MIT. The unchanged license and
trademark texts, per-page revisions, archived repository, and translation policy
are documented in [Sources and licensing](/citus/attribution/). English is
authoritative; the upstream Chinese machine translation is reference material.
