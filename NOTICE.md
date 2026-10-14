# Content and dependency notice

The first doc.pg.center documentation collection was imported on 2026-08-15 from the English `pigsty.io` and Simplified Chinese `pigsty.cc` documentation trees maintained by PGSTY. Individual manuals retain links to the Patroni, pgBackRest, and PgBouncer upstream sources from which those documentation snapshots were prepared.

The imported documentation is distributed under the Creative Commons Attribution 4.0 International license used by the source documentation sites. A copy is included as `LICENSE-CC-BY-4.0`.

The English and Simplified Chinese PgBouncer manuals were refreshed on 2026-10-04
to version 1.26.0 (`pgbouncer_1_26_0`), using the proofread `pigsty.io` commit
`fe0a9f08259fd6a55856d202609205606ba3c704` and `pigsty.cc` commit
`e22fbc56ec1631a4d56a15ffb2b7e8721f411184`. On 2026-10-13, all six editions were synchronized with the current English
manual for 1.26.0. Local corrections to upstream factual errors, spelling and
grammar were checked against the release implementation. Original diagnostic
messages are preserved verbatim. The page-level review and corrected source
fingerprints are recorded in `data/translation-audits/pgbouncer.json`.

The pgBadger collection was imported on 2026-08-15 from <https://pgbadger.darold.net/> and from `darold/pgbadger` commit `a1ad95a035a0c2d246fe632eb1c361d4bde0ddae`. Its source code and source documentation are distributed under the PostgreSQL License, copyright 2012-2026 Gilles Darold. The complete license is retained in `sources/pgbadger/upstream/LICENSE` and beside the offline examples in `static/third_party/pgbadger/LICENSE`.

pgBadger embeds a modified `SQL::Beautify` module under Artistic License 2.0. Its generated-report resources include MIT, GPL-2.0, and SIL Open Font License 1.1 components; the complete upstream resource inventory is retained in `sources/pgbadger/upstream/RESOURCE-LICENSES` and `static/third_party/pgbadger/THIRD-PARTY-LICENSES`. The original website HTML is stored only as a provenance snapshot under `sources/pgbadger/site` and is not part of the normal Hugo output.

The HAProxy 3.4 documentation collection was imported on 2026-08-16, refreshed on 2026-08-30,
and synchronized in all six languages on 2026-10-13 with the current official English
maintenance snapshot `3.4.6-66`, commit `16acce1dac1dcf1ad5d654204af3a5d45d0e3de8`.
The latest stable release is `3.4.6` (tag `v3.4.6`); this documentation snapshot includes
maintenance-branch changes made after that release. Its English prose is
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
refreshed on 2026-10-13 at commit `d20f8ae346da60ab6eb6f24f200753b328aa9fcc`. Its prose is distributed under the Creative
Commons Attribution 4.0 International license, while code and code samples are distributed under
the Apache License 2.0, copyright 2013-present etcd Authors.

Per-page attribution for every collection is published at <https://doc.pg.center/attribution/> and is
generated from `data/upstreams.yaml` together with the `upstream_link` front matter each page
carries.

The PostgreSQL elephant (Slonik) published at `static/img/slonik.svg` is taken unmodified from the
postgresql.org website repository. It is a mark of the PostgreSQL Community Association of Canada
and is used here to refer to PostgreSQL under the project's trademark and logo policy; its use
does not imply endorsement.
