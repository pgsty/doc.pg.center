# Content and dependency notice

Original text written for doc.pg.center is licensed under Creative Commons
Attribution 4.0 International. The full license is in `LICENSE`. Imported manuals
and third-party assets retain their own copyright and license terms.

The first collection was imported on 2026-08-15 from the English `pigsty.io` and
Simplified Chinese `pigsty.cc` documentation maintained by PGSTY. Those imported
adaptations use CC BY 4.0, subject to the original upstream terms identified below.

## Upstream documentation

| Collection | Maintained edition | Upstream copyright and license |
| --- | --- | --- |
| Patroni | v4.1.5 | Copyright (c) 2025 Compose, Zalando SE, Patroni Contributors; MIT |
| pgBackRest | v2.59.3, commit `46cdca625a73403cad4774d97354a1fac1e91e51` | Copyright (c) 2015-2026 The PostgreSQL Global Development Group and David Steele; MIT |
| PgBouncer | v1.26.0, tag `pgbouncer_1_26_0` | Copyright (c) 2007-2009 Marko Kreen, Skype Technologies OÜ; ISC |
| pgBadger | v13.2, commit `a1ad95a035a0c2d246fe632eb1c361d4bde0ddae` | Copyright (c) 2012-2026 Gilles Darold; PostgreSQL License |
| HAProxy | 3.4.6-66, commit `16acce1dac1dcf1ad5d654204af3a5d45d0e3de8` | Copyright 2000-2026 Willy Tarreau; GPL-2.0-only |
| etcd | v3.7, website commit `d20f8ae346da60ab6eb6f24f200753b328aa9fcc` | Copyright 2013-present etcd Authors; CC BY 4.0 for prose, Apache 2.0 for code and samples |

The HAProxy edition follows a 3.4 maintenance-branch documentation snapshot after
stable release 3.4.6. It includes the complete Starter, Configuration, and
Management manual scope, with adapted headings, links, examples, and page grouping.
HAProxy-derived pages retain GPLv2 terms and are not covered by the site's CC BY 4.0
license. The upstream license explanation, OpenSSL exception, and complete GPLv2
text are published from `static/third_party/haproxy/LICENSE` and
`static/third_party/haproxy/GPL-2.0`.

The pgBadger license is retained in `static/third_party/pgbadger/LICENSE`.
pgBadger embeds a modified `SQL::Beautify` module under Artistic License 2.0.
Its report resources include MIT, GPL-2.0, and SIL Open Font License 1.1 components;
the upstream inventory is in `static/third_party/pgbadger/THIRD-PARTY-LICENSES`.
The linked historical sample reports retain their original scripts and notices.

Official source locations, pinned revisions, and available checksums are recorded
in `data/upstreams.yaml`. Each manual page identifies its source through
`upstream_link`. Full attribution is maintained in the six localized
`content/attribution*.md` pages and published at
<https://doc.pg.center/attribution/>. Upstream downloads are kept outside the
repository; published license texts remain in `static/third_party/`.

## Theme and artwork

The site uses OINK 1.2.0 as a pinned Hugo module. OINK is licensed under Apache
License 2.0 and carries its upstream and bundled-dependency notices in the module.

The PostgreSQL elephant (Slonik) at `static/img/slonik.svg` is taken unmodified
from the postgresql.org website repository. It is a mark of the PostgreSQL
Community Association of Canada and is used to refer to PostgreSQL under the
project's trademark and logo policy. Its use does not imply endorsement.
