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

pig.center republishes documentation written by six upstream projects. Every documentation page
carries a one-line credit at the end naming the work it is derived from, its copyright holder,
its licence, and a link back to the section of this page that covers it.

This page is that record. It states what was imported, when, from which pinned revision, under
which licence, and where the complete upstream notice is retained.

> [!NOTE]
> English, Simplified Chinese, and French cover all six collections. Japanese,
> German, and Russian publish the translations already completed; links to
> missing translations fall back to the corresponding English page.

> [!NOTE]
> pig.center is an independent community documentation project. It is not affiliated with, endorsed
> by, or an official publication of any of the projects below, nor of the PostgreSQL Global
> Development Group.

## Summary {#summary}

| Component | Upstream work | Pinned at | Licence | Retained notice |
|---|---|---|---|---|
| [Patroni](/docs/patroni/) | [Patroni documentation](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/docs/pgbackrest/) | [pgBackRest documentation](https://pgbackrest.org/) | v2.59.3 (all six languages) | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/docs/pgbouncer/) | [PgBouncer documentation](https://www.pgbouncer.org/) | v1.26.0 (all six languages) | [ISC](https://opensource.org/license/isc-license-txt) | [Upstream `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT) |
| [pgBadger](/docs/pgbadger/) | [pgBadger documentation](https://pgbadger.darold.net/) | v13.2, commit `a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/docs/haproxy/) | [HAProxy 3.4 manuals](https://docs.haproxy.org/3.4/) | v3.4.4, commit `7f03ae6` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/docs/etcd/) | [etcd v3.7 documentation](https://etcd.io/docs/v3.7/) | v3.7, commit `d20f8ae` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Upstream `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

Every collection is **adapted**, not mirrored. Headings, anchors, cross-links, code signatures,
page grouping, and navigation are reworked for this edition; the upstream prose itself is
preserved. The page-end credit says so, and links to this site's change history for the page you
are reading.

## Patroni {#patroni}

Imported on 2026-08-15 from the [Patroni documentation](https://patroni.readthedocs.io/en/latest/)
for **v4.1.5**, with a Simplified Chinese translation prepared alongside it.

Patroni is copyright (c) 2025 Compose, Zalando SE, Patroni Contributors, and is distributed under
the [MIT License](https://opensource.org/license/mit). The complete licence text is retained
[upstream](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

Imported on 2026-08-15 from the [pgBackRest documentation site](https://pgbackrest.org/).
The English and Simplified Chinese editions were refreshed on 2026-10-04 to **v2.59.2**.
All six language editions are aligned with the **v2.59.3** baseline as of 2026-10-13. The publication review corrects obsolete PITR selection guidance and a truncated historical warning using the pinned upstream implementation and XML; see `data/translation-audits/pgbackrest.json`.

pgBackRest is copyright (c) 2015-2026 The PostgreSQL Global Development Group and David Steele,
and is distributed under the [MIT License](https://opensource.org/license/mit). The complete
licence text is retained [upstream](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

Imported on 2026-08-15 from the [PgBouncer documentation site](https://www.pgbouncer.org/) for
**v1.25.2**, with a Simplified Chinese translation prepared alongside it.

The English and Simplified Chinese editions were refreshed on 2026-10-04 to
[**v1.26.0**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0),
using the proofread manuals from `pigsty.io` and `pigsty.cc`, respectively.

On 2026-10-13, all six editions were synchronized with the current English manual
for **v1.26.0**. Reference descriptions were checked against the release implementation;
local corrections address upstream factual errors, spelling and grammar. Original
diagnostic messages are retained verbatim, and each translation has a page-level review.

PgBouncer is copyright (c) 2007-2009 Marko Kreen, Skype Technologies OÜ, and is distributed under
the [ISC License](https://opensource.org/license/isc-license-txt). The complete licence text is
retained [upstream](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT).

## pgBadger {#pgbadger}

Imported on 2026-08-15 from <https://pgbadger.darold.net/> and from
[`darold/pgbadger`](https://github.com/darold/pgbadger) at commit
[`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae),
whose latest published release at the time was v13.2.

pgBadger is copyright (c) 2012-2026 Gilles Darold and is distributed under the
[PostgreSQL License](https://opensource.org/license/postgresql). The complete licence text is
retained beside the offline examples as
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) and in
`sources/pgbadger/upstream/LICENSE` in the site repository.

> [!IMPORTANT]
> pgBadger embeds a modified `SQL::Beautify` module under Artistic License 2.0, and its
> generated-report resources include MIT, GPL-2.0, and SIL Open Font License 1.1 components. The
> complete upstream resource inventory is retained as
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> The [sample reports](/docs/pgbadger/sample-reports/) published here are historical generated
> artifacts and keep their original embedded notices.

## HAProxy {#haproxy}

Imported on 2026-08-16 and refreshed on 2026-08-30 from the official HAProxy 3.4 maintenance
repository at tag `v3.4.4`, commit
[`7f03ae65c286`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0).
The English prose is derived from the complete `doc/intro.txt`, `doc/configuration.txt`, and
`doc/management.txt` manuals — 40,128 lines in total — reorganized into 34 reading pages.

HAProxy is copyright 2000-2026 Willy Tarreau and is distributed under the
[GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
HAProxy's own licence explanation, its OpenSSL exception, and the complete GPLv2 text are
published as [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) and
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> The HAProxy-derived pages are **not** covered by this site's CC BY 4.0 licence. They carry
> HAProxy's GPLv2 terms.

## etcd {#etcd}

Imported from the official etcd v3.7 documentation and refreshed on 2026-10-13 at commit
[`d20f8ae346da`](https://github.com/etcd-io/website/commit/d20f8ae346da60ab6eb6f24f200753b328aa9fcc).
The pinned source tree is
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7).

The etcd documentation is copyright 2013-present etcd Authors. Its prose is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), while code and code samples are
licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). The complete notice is
retained [upstream](https://github.com/etcd-io/website/blob/main/LICENSE).

## This site {#site}

Original text written for pig.center — orientation pages, the complete Simplified Chinese and French
editions, the published Japanese, German, and Russian translations, editorial notes, and the
landing pages — is published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), except where an upstream licence
above applies to the page instead.


The PostgreSQL elephant (Slonik) shown on the home page is the PostgreSQL project's own mark,
taken from the [postgresql.org website repository](https://git.postgresql.org/gitweb/?p=pgweb.git)
and republished here unmodified under
[the PostgreSQL trademark and logo policy](https://www.postgresql.org/about/policies/trademarks/)
as a reference to PostgreSQL. It is a mark of the PostgreSQL Community Association of Canada and
its use here does not imply endorsement.

The site is built with [OINK](https://oink.pgsty.com/) v1.2.0, a Hugo theme licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), which carries its own upstream
and bundled-dependency notices in the module source.

Corrections to any attribution on this page are welcome through the
[site repository](https://github.com/pgsty/pig.center/issues).
