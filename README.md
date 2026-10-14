# doc.pg.center

[![Website](https://img.shields.io/badge/web-doc.pg.center-336791?logo=postgresql&logoColor=white)](https://doc.pg.center/)
[![GitHub Pages](https://github.com/pgsty/doc.pg.center/actions/workflows/pages.yml/badge.svg)](https://github.com/pgsty/doc.pg.center/actions/workflows/pages.yml)
[![Hugo](https://img.shields.io/badge/Hugo-extended%200.165.0-FF4088?logo=hugo)](https://gohugo.io/)

PostgreSQL Community Components is a documentation portal for the tools that run PostgreSQL in
production. The current collection covers Patroni, pgBackRest, PgBouncer, pgBadger, the complete
HAProxy 3.4 Starter, Configuration, and Management manuals, and the official etcd 3.7 documentation.
English, Simplified Chinese, French, Japanese, German, and Russian have a localized page for every
English route. Page availability and synchronization with the current English edition are measured
separately.

本站是 PostgreSQL 生态工具文档站。当前收录 Patroni、pgBackRest、PgBouncer、pgBadger、
HAProxy 3.4 与 etcd 3.7。英文、简体中文、法文、日文、德文与俄文均覆盖全部页面路由；
页面存在不代表译文已与当前英文版本同步。

## Language coverage

Coverage is the number of localized pages divided by the corresponding English page count.
Counts include published directory indexes (`_index.md`) and exclude HAProxy's three non-rendered
sidebar dividers (`_div_*.md`). The six component collections contain 212 pages; the homepage,
documentation index, search, and attribution add four site pages. Generated redirects, alternate
output formats, and English fallback destinations do not count as translations.

| Collection | EN | ZH | FR | JA | DE | RU |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Patroni | 24 (100%) | 24 (100%) | 24 (100%) | 24 (100%) | 24 (100%) | 24 (100%) |
| pgBackRest | 29 (100%) | 29 (100%) | 29 (100%) | 29 (100%) | 29 (100%) | 29 (100%) |
| PgBouncer | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) |
| pgBadger | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) |
| HAProxy | 35 (100%) | 35 (100%) | 35 (100%) | 35 (100%) | 35 (100%) | 35 (100%) |
| etcd | 99 (100%) | 99 (100%) | 99 (100%) | 99 (100%) | 99 (100%) | 99 (100%) |
| **Component total** | 212 (100%) | 212 (100%) | 212 (100%) | 212 (100%) | 212 (100%) | 212 (100%) |
| Site pages | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) |
| **All publishable pages** | 216 (100%) | 216 (100%) | 216 (100%) | 216 (100%) | 216 (100%) | 216 (100%) |


EN = English; ZH = 简体中文; FR = Français; JA = 日本語; DE = Deutsch; RU = Русский.
Reproduce this matrix with `python3 scripts/report-coverage.py`.

These percentages measure page availability, not sentence-level translation completeness or
version freshness. All six pgBackRest editions target the same 2.59.3 stable-tag snapshot. The
[publication review](data/translation-audits/pgbackrest.json) records source corrections,
translation fixes, review scope and exact fingerprints for all 145 translation pairs.
`python3 scripts/check-pgbackrest.py --rendered-dir <production-build>` checks every
source pair and all 174 published pages, including technical content, search/navigation,
local links, aliases and complete Markdown, print and LLMS outputs. The source is
`release/2.59.3` (`46cdca625a73403cad4774d97354a1fac1e91e51`); the security advisory,
release notes and examples are synchronized to that tag, retaining the reviewed PITR
and historical-warning corrections. Development-branch changes are excluded.

PgBouncer 1.26.0 has nine pages in each of the six editions, with all 45 translation pairs
reviewed against current English and the release implementation.
`python3 scripts/check-pgbouncer.py --rendered-dir <production-build>` checks the exact
reviewed source fingerprints, technical content, routes, navigation, search, aliases, links,
and complete Markdown, print and LLMS bodies. The [acceptance metadata](data/translation-audits/pgbouncer.json)
records verified source corrections and binds each semantic review to its source and translation fingerprints.
`scripts/check-pgbouncer-browser.cjs` additionally exercises all 54 pages at desktop and
mobile widths, real technical-parameter search, language switching and mobile navigation.
Serve the production build locally and provide external Playwright/Chromium paths plus
a report directory outside the repository, as shown in the script header.

All five Patroni 4.1.5 translations have a complete semantic review against current English in the [current acceptance metadata](data/translation-audits/patroni.json).

The six-language HAProxy 3.4.6-66 publication gate is
`python3 scripts/check-haproxy.py --rendered-dir <production-build>`; `make check`
also runs it. It binds all 190 translation pairs to the current review fingerprints,
checks localized links, routes and navigation, and compares complete HTML, Markdown,
print and LLMS content. A separate temporary Hugo output renders source `.Content`
without the page templates, so matching omissions in HTML and print are rejected.
All literal fences must reach the rendered page unchanged and in order. Chinese and
French explanatory fences use narrowly classified review records; their explanations
and unfenced indented prose are included in untranslated-English screening. The
[aggregate review record](data/translation-audits/haproxy.json) states the semantic
review scope: the existing German, Japanese and Russian complete reviews were
revalidated against current changes; Chinese and French received complete explanation
translation and focused technical prose review. This is not a new sentence-by-sentence
review of every Chinese or French prose paragraph. Desktop and mobile interaction
checks use `scripts/check-haproxy-browser.cjs` with `HAPROXY_LANGUAGE` and external
Playwright, Chromium and report locations. Source-generator corrections and the pinned
upstream provenance are recorded in [sources/haproxy/SOURCE.md](sources/haproxy/SOURCE.md).
Mutation regressions are available with `python3 scripts/test-haproxy-publication.py
--rendered-dir <production-build> --output-dir <external-fixture-directory>`. They
use isolated copies and require explicit directories outside the repository.


The German HAProxy 3.4.6-66 collection contains all 35 published pages and three sidebar dividers.
Every body has a separate English/German semantic review. The current-source gate
`python3 scripts/check-german-parity.py --component haproxy --current-source
--rendered-dir <production-build>` requires all 38 pairs without `--allow-partial`.
`python3 scripts/check-haproxy-de-rendered.py --rendered-dir <production-build>`
also verifies exact semantic-review fingerprints, rendered anchors, aliases, sidebar/pager,
language switches, search, shared assets, Markdown, complete print bodies and LLMS outputs.
The [page-by-page acceptance record](data/translation-audits/haproxy-de.json) distinguishes
semantic evidence, protected English literals and source issues from script validation.

The Japanese HAProxy 3.4.6-66 collection contains all 35 published pages and three sidebar dividers.
`python3 scripts/check-haproxy-ja.py --require-review` compares every page with the current
English source, including exact semantic-review fingerprints, technical literals, numeric facts,
and individually classified code and explanation blocks. `python3 scripts/check-haproxy-ja-rendered.py
<production-build>` checks routes, aliases, English anchors, sidebar/pager order, language switches,
search entries, shared assets, Markdown, complete print bodies, LLMS and navigation outputs.
The [page-by-page acceptance metadata](data/translation-audits/haproxy-ja.json) records
the source baseline, semantic corrections and reviewed fingerprints. Desktop and narrow-screen
interactions are reproducible with `scripts/check-haproxy-ja-browser.cjs` using an external
Playwright runtime and a locally served production build.

The Russian HAProxy 3.4.6-66 collection contains all 35 published pages and three sidebar dividers.
The original 30 pages received a full current-English semantic review: 15 were corrected and
separately reviewed, and 15 passed unchanged. All five added reference pages were fully translated
and independently reviewed or checked again in a separate complete English/Russian comparison.
`python3 scripts/check-russian-parity.py --component haproxy --current-source --strict
--rendered-dir <production-build>` requires all 38 pairs without `--allow-partial`, exact final
semantic-review fingerprints, protected technical content, canonical routes and aliases, English
anchors, sidebar/pager order, language switches, search, shared assets, Markdown, complete print
bodies, complete LLMS bodies and navigation order. The
[page-by-page acceptance metadata](data/translation-audits/haproxy-ru.json) records semantic evidence,
source anomalies, legitimate English literals and reviewed fingerprints. Desktop and narrow
screen interaction checks are reproducible with `scripts/check-haproxy-ru-browser.cjs` using an
external Playwright runtime and an externally served production build.

The German PgBouncer 1.26.0 collection is complete, and all German pgBadger 13.2 pages have
been reviewed against the current English source. Their reviewed fingerprints are maintained
in the current [PgBouncer](data/translation-audits/pgbouncer.json) and
[pgBadger](data/translation-audits/pgbadger.json) acceptance metadata.

Localized navigation resolves each route at build time. Existing translations stay in the selected
language; gaps link to the matching English page and are marked `EN` on the homepage.

## Build

The site requires Hugo Extended 0.160.1 or newer and Go 1.27 or newer; `make check` also uses Node.js to validate search. OINK is pinned as a Hugo Module at `github.com/pgsty/oink v1.2.0`. `make dev` uses the sibling `../oink` checkout; `make build`, `make serve`, and `make check` intentionally keep the published module path.

```sh
make build
make dev
make serve
make check
```

`make check` runs the source and rendered-output gates against a production build.
The Patroni gate checks all 120 translations against current English, with the
[publication review](data/translation-audits/patroni.json) recording source corrections,
exact fingerprints, complete semantic review of all 24 page sets and 71 release
versions, and explained numeric notation variants.
`python3 scripts/check-patroni.py --rendered-dir <production-build>` also checks all
144 pages, command anchor destinations, navigation, search, aliases, language
switches, code and complete Markdown, print and LLMS bodies.
The source gate also uses Hugo's Goldmark parser to check release explanation/list
ownership. `python3 scripts/test-patroni.py` exercises translation and source
regressions, including detached French/Japanese release explanations.
The pgBackRest gate always uses current English; its former French 2.59.1 source pin
has been removed after the 29 French pages were checked against 2.59.2. Other
components may declare historical source snapshots in `data/translation-sources.json`;
validation of such snapshots requires full Git history (CI uses `fetch-depth: 0`).

For pgBackRest, `python3 scripts/test-pgbackrest.py` exercises deliberate regressions
in source fingerprints, code, numeric facts, diagnostic strings, metadata and missing
translations. Existing German, Japanese and Russian gates remain complementary checks.
The [current acceptance metadata](data/translation-audits/pgbackrest.json) contains the
reviewed fingerprints after the shared source corrections. It distinguishes prior full
bilingual review from this pass's complete technical checks and focused semantic review.
Repeat desktop and mobile browser checks of layout, search, same-page language
switching, fragment jumps and mobile navigation when changing the site's templates.

The guide examples come from `doc/resource/exe.cache` at the two stable tags, since
the distribution HTML suppresses some command outputs. Keep downloaded caches and
distribution archives outside this repository. To review a subsequent update, run
`python3 scripts/sync-pgbackrest-examples.py --from-cache <old-cache> --to-cache <new-cache> --from-version 2.59.2 --to-version 2.59.3`
against the old guide sources; add `--write` after checking the dry-run receipt.
The importer validates command identities, existing output blocks and all six code
copies before changing any files. It does not execute example commands. The audit
records the source and asset hashes and the actual replacement counts.
The local OINK search override retains Cyrillic queries.
`node scripts/test-pgbackrest-search.cjs <production-build>` checks security-advisory
search in all six languages and proves Latin/CJK results remain unchanged.

The complete Japanese etcd 3.7 collection is checked against current English with
`python3 scripts/check-japanese-parity.py --component etcd --rendered-dir <production-build>`
and `python3 scripts/check-etcd-ja-rendered.py --rendered-dir <production-build>`.
These gates require all 99 pages, exact protected content and English heading IDs,
Japanese display metadata, reviewed numeric facts, per-page semantic-review hashes,
and complete routes, aliases, navigation, pager, search, Markdown, print bodies and LLMS.
`python3 scripts/test-etcd-ja.py --rendered-dir <production-build>` exercises deliberate regressions.
The [page-by-page review](data/translation-reviews/etcd.ja.json) records 64 added pages,
9 corrected existing pages, 26 existing pages reviewed unchanged, and exact explained exceptions.

The complete German etcd 3.7 collection is checked against current English with
`python3 scripts/check-german-parity.py --component etcd --current-source
--rendered-dir <production-build>` and
`python3 scripts/check-etcd-german.py --rendered-dir <production-build>`.
These gates require all pages, preserve the reviewed source/translation fingerprints,
and check every canonical route, alias, heading, sidebar, pager, language switch,
search entry, shared asset, Markdown page, print bundle and LLMS output.
`python3 scripts/check-german-prose.py content/docs/etcd` checks for English prose residues.
The separate semantic review and per-page completion list are recorded in
`data/translation-audits/etcd-de.json`.

The [multilingual etcd publication record](data/translation-audits/etcd.json) binds all 495
translation pairs to current English and records the actual semantic review scope. Chinese,
French and Russian received complete fresh prose/table review; German and Japanese retain
their earlier full reviews, with 86 complete pages reread in this follow-up and every changed
paragraph checked. Verified source corrections include 3.7 flags and Go requirements,
consistency guarantees, snapshot defaults and storage-versus-binary version fields.
`python3 scripts/check-etcd.py --rendered-dir <production-build>` checks all 594 pages,
exact fingerprints, technical content, English heading IDs, aliases, navigation/pager,
search and complete Markdown, print and LLMS bodies. `python3 scripts/test-etcd.py`
exercises deliberate regressions; both run in `make check`. `scripts/check-etcd-browser.cjs`
checks every locale at desktop and mobile widths, real etcdctl search results, language
switching, fragment jumps and mobile navigation, using the external Playwright/Chrome
runtime and output directory described in its header. Search uses titles, headings and
summaries; flags appearing only inside code blocks are outside that configured scope.

The etcd v3.7 source snapshot is synchronized to website commit
`d20f8ae346da60ab6eb6f24f200753b328aa9fcc` (checked 2026-10-13). Current installation,
container and Kubernetes examples use released etcd v3.7.2 and its Go 1.26.8 toolchain;
the upstream documentation cascade still names v3.7.0. Historical versioned examples
retain their original context, and v3.8-DRAFT is excluded. The `upstream_sync` section
of the publication record separates body-preserving provenance changes, current
release adaptations, retained source corrections and fresh validation.

The generated site is written to `public/`. Local preview, a successful build, and deployment to `doc.pg.center` are separate delivery stages.

`data/translation-audits`, `data/translation-reviews`, `data/translation-checks` and
`data/translation-fences` contain the review fingerprints, scope and exact exceptions
required by the publication gates. Keep this validation metadata with the sources.
Use external temporary directories for generated reports, screenshots and downloaded
archives; remove intermediate review prompts, handoffs and progress files after acceptance.

## Deploy

The production domain is **`doc.pg.center`**. `static/CNAME`, Hugo's `baseURL`, generated canonical URLs, and the GitHub Pages repository setting must all use that exact hostname. Pushing `main` runs the multilingual source and rendered-link checks, builds with Go 1.27.0 and Hugo Extended 0.165.0, and deploys the resulting artifact through GitHub Pages.

## Information architecture

Patroni, pgBackRest, PgBouncer, pgBadger, HAProxy, and etcd live under `content/docs/`.
The documentation index is `/docs/`, component roots use `/docs/<component>/`, and localized
editions use `/<language>/docs/<component>/` (for example, `/zh/docs/patroni/`).
The six components appear directly in the global navbar, and each keeps its own sidebar and
sequential pager. Existing root-level page URLs redirect to their new canonical addresses;
Hugo aliases omit the language prefix so each locale receives exactly one prefix.
The homepage keeps a three-line hero, six root cards, six detailed shortcut indexes, and a short FAQ.
English, Simplified Chinese, French, Japanese, German, and Russian provide full same-route page
availability. The link resolver retains English fallback for any future untranslated destination.
HAProxy keeps all 34 reading pages directly under one root, with
`_div_intro.md`, `_div_configuration.md`, and `_div_management.md` providing non-linking sidebar
group labels in a single weighted reading sequence.

The site uses OINK's native landing-page sections and documentation shell. A focused local Hero
partial preserves the six-component navigator and animated Slonik orbit; focused link and
Capabilities partials add per-page English fallback while the Cards and FAQ retain the theme's
native structure. Static backlinks are enabled globally. Every page has
semantic Markdown output, each manual publishes a section-level `llms-full.txt`, and each language
publishes `llms.txt` plus a `navigation.json` view of the same navigation tree used by the sidebar
and pager.

## Content sources

The first import was assembled from paired documentation trees in `pigsty.io` and `pigsty.cc`.
pgBadger was imported from a pinned upstream source commit together with a live website snapshot and
offline report examples. HAProxy follows the official English `3.4.6-66` maintenance snapshot after stable release
`v3.4.6`, using the complete Starter, Configuration,
and Management texts and retains the upstream GPLv2 terms. etcd is adapted from a pinned official
3.7 website source tree. Imported pages retain their source notices. See
[NOTICE.md](NOTICE.md), [sources/pgbadger/SOURCE.md](sources/pgbadger/SOURCE.md), and
[sources/haproxy/SOURCE.md](sources/haproxy/SOURCE.md) for provenance and licensing notes.

## Documentation route maintenance

`scripts/migrate-docs-prefix.py` records the directory, link, and alias migration. It previews
changes by default, applies them with `--write`, and leaves already-moved trees alone.
The import generators and translation tools target `content/docs/`; page links in their output
use `/docs/` with any locale prefix before it. Fenced code, API endpoints, upstream URLs,
shared assets in `static/`, and pinned upstream snapshots retain their original paths.
Run `make check` after updating content or navigation to validate source parity, canonical
routes, legacy redirects, Markdown/print/agent outputs, and rendered links and anchors.
