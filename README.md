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
| pgBackRest | 29 (100%) | 29 (100%) | 29 (100%) | 6 (20.7%) | 0 (0%) | 6 (20.7%) |
| PgBouncer | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) | 9 (100%) |
| pgBadger | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) | 16 (100%) |
| HAProxy | 35 (100%) | 35 (100%) | 35 (100%) | 12 (34.3%) | 2 (5.7%) | 30 (85.7%) |
| etcd | 99 (100%) | 99 (100%) | 99 (100%) | 35 (35.4%) | 3 (3%) | 99 (100%) |
| **Component total** | 212 (100%) | 212 (100%) | 212 (100%) | 102 (48.1%) | 36 (17%) | 184 (86.8%) |
| Site pages | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) | 4 (100%) |
| **All publishable pages** | 216 (100%) | 216 (100%) | 216 (100%) | 106 (49.1%) | 40 (18.5%) | 188 (87%) |

EN = English; ZH = 简体中文; FR = Français; JA = 日本語; DE = Deutsch; RU = Русский.
Reproduce this matrix with `python3 scripts/report-coverage.py`.

These percentages measure page availability, not sentence-level translation completeness or
version freshness. pgBackRest's English and Chinese editions target 2.59.2, while its French,
Japanese, and Russian editions still target 2.59.1.
Those pgBackRest translations require an update even where page coverage is 100%.

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

`make check` validates the existing German and Russian translations against their declared English
source version. Older pgBackRest translation sources are pinned in
`data/translation-sources.json` and read from Git history, so validation requires the full repository
history (CI uses `fetch-depth: 0`). Passing this check does not establish synchronization with the
latest English edition. Add `--current-source` to the German or Russian parity checker to inspect
that synchronization gap explicitly.

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
