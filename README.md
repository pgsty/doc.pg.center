# pgsql.cc

[![Website](https://img.shields.io/badge/web-pgsql.cc-336791?logo=postgresql&logoColor=white)](https://pgsql.cc/)
[![GitHub Pages](https://github.com/pgsty/pgsql.cc/actions/workflows/pages.yml/badge.svg)](https://github.com/pgsty/pgsql.cc/actions/workflows/pages.yml)
[![Hugo](https://img.shields.io/badge/Hugo-extended%200.165.0-FF4088?logo=hugo)](https://gohugo.io/)

PostgreSQL Community Components is a documentation portal for the tools that run PostgreSQL in
production. The current collection covers Patroni, pgBackRest, PgBouncer, pgBadger, the complete
HAProxy 3.4 Starter, Configuration, and Management manuals, and the official etcd 3.7 documentation.
English, Simplified Chinese, and French cover every page. Japanese, German, and Russian publish the
translations already completed and fall back to the English page for any missing route.

本站是 PostgreSQL 生态工具文档站。当前收录 Patroni、pgBackRest、PgBouncer、pgBadger、
HAProxy 3.4 与 etcd 3.7。英文、简体中文与法文完整覆盖全部页面；日文、德文和俄文发布
已经完成的译文，尚未翻译的链接会自动回退到对应英文页面。

## Language coverage

- **English / 简体中文 / Français:** all six collections, 218 pages per locale.
- **日本語:** complete Patroni, PgBouncer, and pgBadger documentation, translated subsets of pgBackRest, HAProxy, and etcd, and localized site pages, 108 pages total.
- **Deutsch:** complete pgBadger documentation and translated subsets of Patroni, PgBouncer, HAProxy, and etcd, 34 pages total.
- **Русский:** complete Patroni, PgBouncer, pgBadger, and etcd documentation, translated subsets of pgBackRest and HAProxy, and localized site pages, 190 pages total.

Localized navigation resolves each route at build time. Existing translations stay in the selected
language; gaps link to the matching English page and are marked `EN` on the homepage.

## Build

The site requires Hugo Extended 0.160.1 or newer and Go 1.27 or newer. OINK is pinned as a Hugo Module at `github.com/pgsty/oink v1.0.0`. `make dev` uses the sibling `../oink` checkout; `make build`, `make serve`, and `make check` intentionally keep the published module path.

```sh
make build
make dev
make serve
make check
```

The generated site is written to `public/`. Local preview, a successful build, and deployment to `pgsql.cc` are separate delivery stages.

## Deploy

The production domain is **`pgsql.cc`**. `static/CNAME`, Hugo's `baseURL`, generated canonical URLs, and the GitHub Pages repository setting must all use that exact hostname. Pushing `main` runs the multilingual source and rendered-link checks, builds with Go 1.27.0 and Hugo Extended 0.165.0, and deploys the resulting artifact through GitHub Pages.

## Information architecture

Patroni, pgBackRest, PgBouncer, pgBadger, HAProxy, and etcd are six independent documentation roots
directly under `content/`; there is no shared `content/docs/` wrapper or `/docs/` canonical URL prefix.
They appear directly in the global navbar, and each root owns its own sidebar and sequential pager.
The homepage keeps a three-line hero, six root cards, six detailed shortcut indexes, and a short FAQ.
English, Simplified Chinese, and French provide complete same-route editions. Partial locales expose
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
