# pig.center

[![Website](https://img.shields.io/badge/web-pig.center-336791?logo=postgresql&logoColor=white)](https://pig.center/)
[![GitHub Pages](https://github.com/pgsty/pig.center/actions/workflows/pages.yml/badge.svg)](https://github.com/pgsty/pig.center/actions/workflows/pages.yml)
[![Hugo](https://img.shields.io/badge/Hugo-extended%200.165.0-FF4088?logo=hugo)](https://gohugo.io/)

PostgreSQL Community Components is a documentation portal for the tools that run PostgreSQL in
production. The current collection covers Patroni, pgBackRest, PgBouncer, pgBadger, the complete
HAProxy 3.4 Starter, Configuration, and Management manuals, and the official etcd 3.7 documentation.
English, Simplified Chinese, and French have a localized page for every English route. Japanese,
German, and Russian publish partial collections and fall back to the English page for any missing
route. Page availability and synchronization with the current English edition are measured separately.

本站是 PostgreSQL 生态工具文档站。当前收录 Patroni、pgBackRest、PgBouncer、pgBadger、
HAProxy 3.4 与 etcd 3.7。英文、简体中文与法文覆盖全部页面路由；日文、德文和俄文提供
部分译文，尚未翻译的链接会自动回退到对应英文页面。页面存在不代表译文已与当前英文版本同步。

## Language coverage

Coverage is the number of localized pages divided by the corresponding English page count.
Counts include published directory indexes (`_index.md`) and exclude HAProxy's three non-rendered
sidebar dividers (`_div_*.md`). The six component collections contain 212 pages; the homepage,
documentation index, search, and attribution add four site pages. Generated redirects, alternate
output formats, and English fallback destinations do not count as translations.

| Collection | EN | ZH | FR | JA | DE | RU |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Patroni | 24 (100%) | 24 (100%) | 24 (100%) | 24 (100%) | 6 (25%) | 24 (100%) |
| pgBackRest | 29 (100%) | 29 (100%) | 29 (100%) | 29 (100%) | 29 (100%) | 29 (100%) |
| PgBouncer | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) |
| pgBadger | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) |
| HAProxy | 35 (100%) | 35 (100%) | 35 (100%) | 12 (34.3%) | 2 (5.7%) | 30 (85.7%) |
| etcd | 99 (100%) | 99 (100%) | 99 (100%) | 99 (100%) | 99 (100%) | 99 (100%) |
| **Component total** | 212 (100%) | 212 (100%) | 212 (100%) | 189 (89.2%) | 161 (75.9%) | 207 (97.6%) |
| Site pages | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) |
| **All publishable pages** | 216 (100%) | 216 (100%) | 216 (100%) | 193 (89.4%) | 165 (76.4%) | 211 (97.7%) |

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
and complete Markdown, print and LLMS bodies. The [acceptance record](data/translation-audits/pgbouncer.json)
records verified source corrections and separates semantic review from automated validation.
`scripts/check-pgbouncer-browser.cjs` additionally exercises all 54 pages at desktop and
mobile widths, real technical-parameter search, language switching and mobile navigation.
Serve the production build locally and provide external Playwright/Chromium paths plus
a report directory outside the repository, as shown in the script header.

Localized navigation resolves each route at build time. Existing translations stay in the selected
language; gaps link to the matching English page and are marked `EN` on the homepage.

## Build

The site requires Hugo Extended 0.160.1 or newer and Go 1.27 or newer. OINK is pinned as a Hugo Module at `github.com/pgsty/oink v1.2.0`. `make dev` uses the sibling `../oink` checkout; `make build`, `make serve`, and `make check` intentionally keep the published module path.

```sh
make build
make dev
make serve
make check
```

`make check` runs the source and rendered-output gates against a production build.
The pgBackRest gate always uses current English; its former French 2.59.1 source pin
has been removed after the 29 French pages were checked against 2.59.2. Other
components may declare historical source snapshots in `data/translation-sources.json`;
validation of such snapshots requires full Git history (CI uses `fetch-depth: 0`).

For pgBackRest, `python3 scripts/test-pgbackrest.py` exercises deliberate regressions
in source fingerprints, code, numeric facts, diagnostic strings, metadata and missing
translations. Existing German, Japanese and Russian gates remain complementary checks.
Their earlier per-language acceptance records are retained as review history; the
[current publication record](data/translation-audits/pgbackrest.json) supersedes their
fingerprints after the shared source corrections. It distinguishes prior full bilingual
review from this pass's complete technical checks and focused semantic review.
The record also separates browser observations from automated source/output checks.
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

The final acceptance includes a fresh complete reading of natural-language text in all 495 translated pages, plus current-source protected-content and rendered-output checks. The etcd-owned structural helpers keep these checks independent of other pending component work.

The generated site is written to `public/`. Local preview, a successful build, and deployment to `pig.center` are separate delivery stages.

## Deploy

The production domain is **`pig.center`**. `static/CNAME`, Hugo's `baseURL`, generated canonical URLs, and the GitHub Pages repository setting must all use that exact hostname. Pushing `main` runs the multilingual source and rendered-link checks, builds with Go 1.27.0 and Hugo Extended 0.165.0, and deploys the resulting artifact through GitHub Pages.

## Information architecture

Patroni, pgBackRest, PgBouncer, pgBadger, HAProxy, and etcd live under `content/docs/`.
The documentation index is `/docs/`, component roots use `/docs/<component>/`, and localized
editions use `/<language>/docs/<component>/` (for example, `/zh/docs/patroni/`).
The six components appear directly in the global navbar, and each keeps its own sidebar and
sequential pager. Existing root-level page URLs redirect to their new canonical addresses;
Hugo aliases omit the language prefix so each locale receives exactly one prefix.
The homepage keeps a three-line hero, six root cards, six detailed shortcut indexes, and a short FAQ.
English, Simplified Chinese, and French provide full same-route page availability. Partial locales expose
their completed pages and resolve untranslated destinations to the English route. HAProxy keeps all
34 reading pages directly under one root, with
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
offline report examples. HAProxy is generated from the official `v3.4.4` Starter, Configuration,
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
