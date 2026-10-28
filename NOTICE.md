# Content and dependency notice

Original text written for PG.CENTER at doc.pg.center is licensed under Creative Commons
Attribution 4.0 International. The full license is in `LICENSE`. Imported manuals
and third-party assets retain their own copyright and license terms.

The first collection was imported on 2026-08-15 from the English `pigsty.io` and
Simplified Chinese `pigsty.cc` documentation maintained by PGSTY. Those imported
adaptations use CC BY 4.0, subject to the original upstream terms identified below.

## Upstream documentation

| Collection | English source edition | Upstream copyright and license |
| --- | --- | --- |
| Patroni | v4.1.5 | Copyright (c) 2025 Compose, Zalando SE, Patroni Contributors; MIT |
| pgBackRest | v2.60.0, commit `2e1c4f2ba727c45a0a23d4b326905088dc15b1a1` | Copyright (c) 2015-2026 The PostgreSQL Global Development Group and David Steele; MIT |
| PgBouncer | v1.26.1, tag `pgbouncer_1_26_1` | Copyright (c) 2007-2009 Marko Kreen, Skype Technologies OÜ; ISC |
| pgBadger | v13.2 development snapshot, commit `f373ac678c756f66a785c5ab4773d1f05f468d67` | Copyright (c) 2012-2026 Gilles Darold; PostgreSQL License |
| HAProxy | 3.4.7-57, commit `0faeaeda6cdbb65c0e0cedb9a20489581bd7d4c3` | Copyright 2000-2026 Willy Tarreau; GPL-2.0-only |
| etcd | v3.7 docs, website commit `d20f8ae346da60ab6eb6f24f200753b328aa9fcc`; updated for release v3.7.3 | Copyright 2013-present etcd Authors; CC BY 4.0 for prose, Apache 2.0 for code and samples |

The etcd installation, Docker, and Kubernetes examples and release summary were
updated on 2026-10-28 for tag `v3.7.3`, release commit
`0a173d0410a96d01091b484daae81365bbcde57e`, including its Go 1.26.10 toolchain.
The v3.7 documentation snapshot remains pinned separately from the software release.

The HAProxy edition follows a 3.4 maintenance-branch documentation snapshot after
stable release 3.4.7. It includes the complete Starter, Configuration, and
Management manual scope, with adapted headings, links, examples, and page grouping.
HAProxy-derived pages retain GPLv2 terms and are not covered by the site's CC BY 4.0
license. The upstream license explanation, OpenSSL exception, and complete GPLv2
text are published from `static/third_party/haproxy/LICENSE` and
`static/third_party/haproxy/GPL-2.0`.

The pgBadger source is a development documentation snapshot after v13.2, not a
new stable release. Historical website excerpts and sample reports retain their
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

The site uses OINK 1.3.0 as a pinned Hugo module. OINK is licensed under Apache
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
