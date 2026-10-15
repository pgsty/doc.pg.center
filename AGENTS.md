# Repository Guide

## Purpose

This repository contains the source for the **PG.CENTER** component documentation
site at **doc.pg.center**, part of **[pg.center](https://pg.center/)**, for the tools used
to run PostgreSQL in production. PGSTY maintains this independent community
edition. PostgreSQL core manuals, reference material, and ecosystem resources
live on the parent site; this repository maintains the six component collections
listed below. It uses Hugo Extended and the OINK theme, pinned as a Go module in
`go.mod` and `go.sum`.

Use **PG.CENTER** as the site identity in the title, navigation, footer, and
metadata, with the PostgreSQL elephant as the logo and browser icon. Keep
`doc.pg.center` as the documentation hostname and repository name. The top-level
Home link points to `https://pg.center/zh/` in Chinese and `https://pg.center/`
in all other languages. The local checkout is `~/www/doc.pg.center`.

## Documentation and languages

Every collection is available in **English (`en`), Simplified Chinese (`zh`),
French (`fr`), Japanese (`ja`), German (`de`), and Russian (`ru`)**.

| Component | Documentation scope | Languages |
| --- | --- | --- |
| Patroni | PostgreSQL high availability, configuration, administration, and APIs | en, zh, fr, ja, de, ru |
| pgBackRest | Backup, recovery, archiving, commands, and configuration | en, zh, fr, ja, de, ru |
| PgBouncer | Connection pooling, installation, configuration, and administration | en, zh, fr, ja, de, ru |
| pgBadger | Log analysis, command reference, sample reports, and release history | en, zh, fr, ja, de, ru |
| HAProxy | Starter, Configuration, and Management manuals | en, zh, fr, ja, de, ru |
| etcd | Operations, APIs, development, internals, and upgrades | en, zh, fr, ja, de, ru |

English is the source language. Files without a language suffix are English;
translations use the same path with `.zh.md`, `.fr.md`, `.ja.md`, `.de.md`, or
`.ru.md`. For example, `content/pgbouncer/config.md` is the source for
`content/pgbouncer/config.fr.md`. Each component is a top-level section with
the `docs` content type. English URLs start with the component name, such as
`/patroni/`; translations prepend the language code, such as `/fr/patroni/`.
There is no `/docs/` section or index. Internal links, aliases, and generated
outputs must use the component routes without a `/docs/` prefix.

## Repository layout

- `content/<component>/`: maintained manuals and their required images.
- `content/`: localized home, search, and attribution pages.
- `data/`: homepage and footer content, plus the upstream source and license registry.
- `layouts/`, `assets/`, and `i18n/`: templates, styles, scripts, and interface translations.
- `static/`: published assets, third-party notices, and linked pgBadger sample reports.
- `scripts/`: reusable source, build, route, link, and search checks.
- `hugo.yaml`, `go.mod`, and `go.sum`: site configuration and the pinned theme dependency.
- `LICENSE` and `NOTICE.md`: site licensing, attribution, and upstream exceptions.

The Markdown under `content/` is the maintained edition. It does not depend on
an in-repository upstream checkout or generator. Keep upstream downloads,
translation scratch files, review logs, and build output outside the source tree.

## Updating an upstream release

1. **Establish the source.** Check the component's official documentation and
   release notes against the revision in `data/upstreams.yaml`. Choose a specific
   release tag or commit. Download reference sources outside this repository.
   Distinguish stable releases from maintenance-branch documentation snapshots.
2. **Update English first.** Apply the upstream changes to the English Markdown.
   Review added and removed material, commands, options, defaults, examples,
   warnings, and release notes. Preserve useful local corrections and stable
   anchors; update aliases when a URL changes. Finish and review the English diff
   before translating it.
3. **Update all five translations from the English diff.** Synchronize Chinese,
   French, Japanese, German, and Russian, including existing pages, additions,
   and removals. Use consistent terminology and natural prose. Keep commands,
   configuration keys, API identifiers, code, and actual program output exact.
   Translate explanatory prose without changing its meaning.
4. **Update shared metadata.** Record the selected upstream revision and relevant
   checksums in `data/upstreams.yaml`. Keep page attribution, version labels,
   navigation, `NOTICE.md`, and all six attribution pages consistent. Retain
   upstream copyright and license notices.
5. **Validate the complete change.** Run `make check` and inspect the affected
   pages in a local preview, including language switching, search, navigation,
   and narrow screens. Page coverage and a successful build do not prove that a
   translation is complete or accurate. Review the actual translated changes
   before publishing.

## Local development and checks

Use Hugo **Extended**, Go, Python 3, and Node.js. CI pins Hugo and Go in
`.github/workflows/check.yml`; Python and Node are used by the checks.

```sh
make check                    # Build and validate in an external temporary directory
make serve                    # Preview with the pinned theme at http://localhost:1313
make build                    # Build the production site into public/
python3 scripts/report-coverage.py
```

`make dev` uses `~/pgsty/oink` for theme development; override it with
`make dev OINK_DIR=/path/to/oink`. Release checks and builds must use the pinned
module: unset `HUGO_MODULE_REPLACEMENTS`
and set `GOWORK=off` and `HUGO_MODULE_WORKSPACE=off`. Keep generated files out of
Git; `public/`, `resources/`, and local caches are ignored.

## Repository and publishing

- GitHub repository: <https://github.com/pgsty/doc.pg.center>
- Production branch: `main`.
- Intended public URL: <https://doc.pg.center/>.
- Parent site: <https://pg.center/>. Keep its links distinct from local component
  documentation links, which must stay in the reader's selected language.
- Hosting and deployment: **Cloudflare Pages**, connected to the GitHub repository.
- Cloudflare build command: `make build`; output: `public`; root: the repository root.
- Set `HUGO_VERSION=0.166.0` and `GO_VERSION=1.27.0` in Cloudflare, matching CI.
  Set `GOWORK=off` and `HUGO_MODULE_WORKSPACE=off`. Apply the same toolchain
  settings to preview builds; leave `HUGO_MODULE_REPLACEMENTS` unset.
- Google Analytics 4: `G-D9E4B60JWX`, shared with `pg.center`. Keep the ID in
  `services.googleAnalytics.ID`. OINK emits the tag only for production builds;
  ordinary development previews must not send analytics.

GitHub Actions runs checks. Configure the Pages project and the `doc.pg.center`
custom domain in Cloudflare. Repository configuration alone does not establish
that hosting or DNS has been provisioned. The build uses the production base URL
from `hugo.yaml`. After an authorized deployment, verify the public site,
localized routes, search, redirects, and attribution. Report local validation,
Git changes, deployment, and public verification separately.

## File and Git discipline

Keep source code, configuration, maintained documentation, required site assets,
and small provenance records. Store downloads, archives, executable files,
database dumps, large raw datasets, and temporary work outside the repository.
If a generated path must be local, add an appropriate ignore rule and verify it
with `git check-ignore` before creating the files.

Before staging or committing, inspect changed paths and new file sizes and types.
Stage only the intended files; never force-add ignored output. Ask before adding
a new binary asset or dataset whose place in Git is unclear. Preserve unrelated
work. Do not stash, reset, rewrite history, or delete existing material without
authorization for that operation.
