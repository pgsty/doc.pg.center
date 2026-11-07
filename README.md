# PG.CENTER component documentation

The component documentation site of [pg.center](https://pg.center/), with
multilingual manuals for the tools that run PostgreSQL in production and direct
English/Chinese documentation for PostgreSQL database variants. Built with Hugo
Extended and the OINK theme, and maintained by PGSTY.

## Collections

### PostgreSQL operations tools

| Component | Documentation |
| --- | --- |
| Patroni | PostgreSQL high availability and administration |
| pgBackRest | Backup, recovery, and archiving |
| PgBouncer | Connection pooling |
| pgBadger | Log analysis and sample reports |
| HAProxy | Starter, Configuration, and Management manuals |
| etcd | Operations, APIs, internals, and upgrades |

### PostgreSQL database collections

| Collection | Documentation |
| --- | --- |
| PolarDB | PolarDB for PostgreSQL features, deployment, operations, and internals |
| IvorySQL | Oracle compatibility, administration, reference, and development |
| OpenHalo | MySQL compatibility reference, usage, boundaries, build, and configuration |
| Babelfish | SQL Server compatibility, usage, APIs, design, and releases |
| Percona TDE | Transparent data encryption architecture, commands, and operations |
| Apache Cloudberry | MPP database, administration, references, PXF, and Core Internals |
| AgensGraph | Graph concepts, SQL/Cypher querying, operations, and reference |
| pgEdge | Spock, LOLOR, SafeSession, Snowflake, and operations |
| DocumentDB | Installation, operations, PostgreSQL API, commands, operators, and reference |
| OrioleDB | PostgreSQL storage engine installation, configuration, architecture, development, and benchmarks |
| Citus | Citus 14 deployment, tutorials, distributed data modeling, operations, migration, SQL/API reference, and technical articles |

The six operations collections are available in English, Simplified Chinese,
French, Japanese, German, Russian, Arabic, and Spanish. The eleven database
collections use English and Simplified Chinese routes only. Cloudberry has 641
paired pages; the other collections preserve the source project's actual coverage,
including explicit notices for incomplete Chinese editions, placeholders, and
machine drafts. OrioleDB includes all 18 documentation articles and two benchmark
guides from the 2026-11-06 website snapshot: 26 paired pages including indexes
and source notices. Its architecture figures are shared page-bundle resources;
heading IDs and code blocks are checked for English/Chinese alignment. DocumentDB
has 300 English/Chinese pairs from the fixed docs and website snapshots. Its OINK
conversion includes website-generated guides, installation steps, platform tabs,
field tables, stable heading aliases, and complete code/output preservation.
Translation provenance records AI-assisted bilingual review and source hashes;
`python3 scripts/check-documentdb.py` checks the paired edition.

The site uses the **PG.CENTER** name and PostgreSQL elephant logo. The Home
navigation link returns to `https://pg.center/zh/` for Chinese and
`https://pg.center/` for the other languages. Documentation stays at
`https://doc.pg.center/`.

Each collection lives directly under `content/<component>/` and uses the `docs`
layout. Its URL starts with the collection name, for example `/patroni/` or
`/cloudberry/`. Existing translations prepend their language code, for example
`/zh/patroni/`; bilingual database pages use `/zh/<component>/` where a Chinese
page exists. The English and Chinese homepages start with a PostgreSQL version
guide, then the eleven kernels, then the six community components. The navigation
uses Home, Kernel, and Community Components groups. PXF and Core Internals stay
inside the Cloudberry sidebar. `/postgresql/` and `/zh/postgresql/` link supported,
preview, development, and historical PostgreSQL manuals on PG.CENTER and PGSQL.CC.
There is no `/docs/` index or URL prefix on this site.

## Develop

Install Hugo Extended, Go, Python 3, and Node.js. CI pins Hugo Extended 0.168.0 and follows stable Go releases; no external Sass is required.

CI sets `HUGO_MEMORYLIMIT=4` so shared build resources stay cached during the
eight-language build.
The theme is pinned in `go.mod`; no local theme checkout is required.
The local checkout is `~/www/doc.pg.center`.

```sh
make check    # Validate sources, build, routes, links, and multilingual search
make serve    # Production preview at http://localhost:1313
make build    # Generate the production site in public/
```

`make check` uses an external temporary directory and removes it when finished.
`make dev` uses `~/pgsty/oink` for theme development. Override the theme path with
`make dev OINK_LOCAL=/path/to/oink PORT=1314` (`OINK_DIR` remains supported).
Use Hugo Extended 0.168.0 for the current local theme. Development bypasses
OINK vendor files; both workspaces remain disabled. Production targets clear
inherited local replacements and keep the module pin.
Run `python3 scripts/report-coverage.py` to see the current page coverage.

See [AGENTS.md](AGENTS.md) for the repository layout and maintenance workflow:
update and review English first, then synchronize the available Chinese and
localized translations from the English changes. Official sources and pinned revisions are recorded in
`data/upstreams.yaml`.

## Publish

The site is published at <https://doc.pg.center/>. Its repository is
[pgsty/doc.pg.center](https://github.com/pgsty/doc.pg.center), with `main` as the
production branch. GitHub Actions validates changes; **Cloudflare Pages** builds
and publishes the site through its GitHub integration.

Configure the Cloudflare Pages project with the repository root, build command
`make build`, and output directory `public`. Set `HUGO_VERSION=0.168.0`,
`GO_VERSION=1.27.3`, `GOWORK=off`, and `HUGO_MODULE_WORKSPACE=off`; leave
`HUGO_MODULE_REPLACEMENTS` unset. Add `doc.pg.center` as the custom domain.
The source configuration keeps that domain as the canonical production URL.
Production builds use the shared `pg.center` Google Analytics 4 property,
`G-D9E4B60JWX`. Development builds do not emit the analytics tag.

Repository settings do not provision a Cloudflare Pages project or its custom
domain. Verify the deployment and public site after pushing. See Cloudflare's
[Hugo guide](https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/)
and [build environment reference](https://developers.cloudflare.com/pages/configuration/build-image/).

## Licensing

Original site text is licensed under [CC BY 4.0](LICENSE). Imported manuals and
third-party assets retain their respective licenses. See [NOTICE.md](NOTICE.md),
the attribution pages in `content/`, the per-collection manifests in `data/imports/`,
and the notices in `static/third_party/` and component asset directories.
