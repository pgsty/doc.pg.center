# pgsql.cc

[![Website](https://img.shields.io/badge/web-pgsql.cc-336791?logo=postgresql&logoColor=white)](https://pgsql.cc/)
[![GitHub Pages](https://github.com/pgsty/pgsql.cc/actions/workflows/pages.yml/badge.svg)](https://github.com/pgsty/pgsql.cc/actions/workflows/pages.yml)
[![Hugo](https://img.shields.io/badge/Hugo-extended%200.164.0-FF4088?logo=hugo)](https://gohugo.io/)

PostgreSQL Community Components is a bilingual documentation portal for the tools that run PostgreSQL in production. The current collection covers Patroni, pgBackRest, PgBouncer, and pgBadger in English and Simplified Chinese.

本站是 PostgreSQL 生态工具的中英文双语文档站。当前收录 Patroni、pgBackRest、PgBouncer 与 pgBadger。

## Build

The site requires Hugo Extended 0.160.1 or newer and Go. OINK is pinned as a Hugo Module at `github.com/pgsty/oink v0.4.1`.

```sh
make build
make dev
make check
```

The generated site is written to `public/`. Local preview, a successful build, and deployment to `pgsql.cc` are separate delivery stages.

## Deploy

The production domain is **`pgsql.cc`**. `static/CNAME`, Hugo's `baseURL`, generated canonical URLs, and the GitHub Pages repository setting must all use that exact hostname. Pushing `main` runs the complete bilingual and rendered-link checks, builds with Hugo Extended 0.164.0, and deploys the resulting artifact through GitHub Pages.

## Information architecture

Patroni, pgBackRest, PgBouncer, and pgBadger are four independent documentation roots under `content/docs/`. They appear directly in the global navbar; each root owns its own sidebar and sequential pager. The homepage is intentionally limited to a three-line hero, four root cards, four detailed shortcut indexes, and a short FAQ. English and Simplified Chinese use the same order and routes.

## Content sources

The first import was assembled from paired documentation trees in `pigsty.io` and `pigsty.cc`. pgBadger was imported from a pinned upstream source commit together with a live website snapshot and offline report examples. Imported pages retain their upstream source notices. See [NOTICE.md](NOTICE.md) and [sources/pgbadger/SOURCE.md](sources/pgbadger/SOURCE.md) for provenance and licensing notes.
