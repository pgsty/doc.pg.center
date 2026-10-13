# Content and dependency notice

The first pig.center documentation collection was imported on 2026-08-15 from the English `pigsty.io` and Simplified Chinese `pigsty.cc` documentation trees maintained by PGSTY. Individual manuals retain links to the Patroni, pgBackRest, and PgBouncer upstream sources from which those documentation snapshots were prepared.

The imported documentation is distributed under the Creative Commons Attribution 4.0 International license used by the source documentation sites. A copy is included as `LICENSE-CC-BY-4.0`.

The English and Simplified Chinese PgBouncer manuals were refreshed on 2026-10-04
to version 1.26.0 (`pgbouncer_1_26_0`), using the proofread `pigsty.io` commit
`fe0a9f08259fd6a55856d202609205606ba3c704` and `pigsty.cc` commit
`e22fbc56ec1631a4d56a15ffb2b7e8721f411184`. They include corrections to four kinds
of upstream reference errors, checked against the release implementation.
Other language editions retain the 1.25.2 snapshot.

The pgBadger collection was imported on 2026-08-15 from <https://pgbadger.darold.net/> and from `darold/pgbadger` commit `a1ad95a035a0c2d246fe632eb1c361d4bde0ddae`. Its source code and source documentation are distributed under the PostgreSQL License, copyright 2012-2026 Gilles Darold. The complete license is retained in `sources/pgbadger/upstream/LICENSE` and beside the offline examples in `static/third_party/pgbadger/LICENSE`.

pgBadger embeds a modified `SQL::Beautify` module under Artistic License 2.0. Its generated-report resources include MIT, GPL-2.0, and SIL Open Font License 1.1 components; the complete upstream resource inventory is retained in `sources/pgbadger/upstream/RESOURCE-LICENSES` and `static/third_party/pgbadger/THIRD-PARTY-LICENSES`. The original website HTML is stored only as a provenance snapshot under `sources/pgbadger/site` and is not part of the normal Hugo output.

The HAProxy 3.4 documentation collection was imported on 2026-08-16 and refreshed on 2026-08-30
from the official maintenance repository at tag `v3.4.4`, commit
`7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0`. Its English prose is
derived from the complete `doc/intro.txt`, `doc/configuration.txt`, and `doc/management.txt` manuals
and is distributed under the GNU General Public License version 2 terms stated by HAProxy. The local
edition changes presentation, links, headings, code-signature treatment, and page grouping; the
pinned originals remain under `sources/haproxy/upstream/`.

HAProxy's license explanation, OpenSSL exception, and complete GPLv2 text are retained under
`sources/haproxy/upstream/` and published beside the rendered guide under
`static/third_party/haproxy/`. These HAProxy-derived pages are not covered by the site's
`LICENSE-CC-BY-4.0`.

The website uses OINK 1.2.0 as a pinned Hugo Module. OINK is licensed under Apache License 2.0 and carries its own upstream and bundled-dependency notices in the module source.

The etcd 3.7 documentation collection was imported from the official etcd website repository and
refreshed on 2026-08-30 at commit `824597935df6e95992ef61c07e3222f4f796ca6c`. Its prose is distributed under the Creative
Commons Attribution 4.0 International license, while code and code samples are distributed under
the Apache License 2.0, copyright 2013-present etcd Authors.

Per-page attribution for every collection is published at <https://pig.center/attribution/> and is
generated from `data/upstreams.yaml` together with the `upstream_link` front matter each page
carries.

The PostgreSQL elephant (Slonik) published at `static/img/slonik.svg` is taken unmodified from the
postgresql.org website repository. It is a mark of the PostgreSQL Community Association of Canada
and is used here to refer to PostgreSQL under the project's trademark and logo policy; its use
does not imply endorsement.
