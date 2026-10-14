# doc.pg.center

The component documentation site of [pg.center](https://pg.center/), with
multilingual manuals for the tools that run PostgreSQL in production. Built with
Hugo Extended and the OINK theme, and maintained by PGSTY.

| Component | Documentation |
| --- | --- |
| Patroni | PostgreSQL high availability and administration |
| pgBackRest | Backup, recovery, and archiving |
| PgBouncer | Connection pooling |
| pgBadger | Log analysis and sample reports |
| HAProxy | Starter, Configuration, and Management manuals |
| etcd | Operations, APIs, internals, and upgrades |

Every collection is available in English, Simplified Chinese, French, Japanese,
German, and Russian. English is the source for the other five editions.

Each component lives directly under `content/<component>/` and uses the `docs`
layout. Its URL starts with the component name, for example `/patroni/` or
`/pgbouncer/config/`. Translations prepend their language code, for example
`/zh/patroni/` or `/fr/pgbouncer/config/`. The homepage lists all six collections;
there is no `/docs/` index or URL prefix.

## Develop

Install Hugo Extended, Go, Python 3, and Node.js. CI uses Hugo 0.165.0 and Go 1.27.0.
The theme is pinned in `go.mod`; no local theme checkout is required.
The local checkout is `~/www/doc.pg.center`.

```sh
make check    # Validate sources, build, routes, links, and multilingual search
make serve    # Preview at http://localhost:1313
make build    # Generate the production site in public/
```

`make check` uses an external temporary directory and removes it when finished.
`make dev` uses `~/pgsty/oink` for theme development. Override the theme path with
`make dev OINK_DIR=/path/to/oink`.
Run `python3 scripts/report-coverage.py` to see the current page coverage.

See [AGENTS.md](AGENTS.md) for the repository layout and maintenance workflow:
update and review English first, then synchronize all five translations from
the English changes. Official sources and pinned revisions are recorded in
`data/upstreams.yaml`.

## Publish

The site is intended for <https://doc.pg.center/>. Its repository is
[pgsty/doc.pg.center](https://github.com/pgsty/doc.pg.center), with `main` as the
production branch. GitHub Actions validates changes; **Cloudflare Pages** will
build and publish the site through its GitHub integration.

Configure the Cloudflare Pages project with the repository root, build command
`make build`, and output directory `public`. Set `HUGO_VERSION=0.165.0`,
`GO_VERSION=1.27.0`, `GOWORK=off`, and `HUGO_MODULE_WORKSPACE=off`; leave
`HUGO_MODULE_REPLACEMENTS` unset. Add `doc.pg.center` as the custom domain.
The source configuration keeps that domain as the canonical production URL.
Production builds use the shared `pg.center` Google Analytics 4 property,
`G-D9E4B60JWX`. Development builds do not emit the analytics tag.

These are the intended deployment settings; Cloudflare project creation, domain
setup, and public verification are separate deployment steps. See Cloudflare's
[Hugo guide](https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/)
and [build environment reference](https://developers.cloudflare.com/pages/configuration/build-image/).

## Licensing

Original site text is licensed under [CC BY 4.0](LICENSE). Imported manuals and
third-party assets retain their respective licenses. See [NOTICE.md](NOTICE.md),
the six attribution pages in `content/`, and the notices in `static/third_party/`.
