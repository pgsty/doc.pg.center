# Repository Guide

## Purpose

This repository contains the source for **doc.pg.center**, a multilingual
reference site for the tools used to run PostgreSQL in production. It is an
independent community project maintained by PGSTY. The site uses Hugo Extended
and the OINK theme, pinned as a Go module in `go.mod` and `go.sum`.

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
`.ru.md`. For example, `content/docs/pgbouncer/config.md` is the source for
`content/docs/pgbouncer/config.fr.md`. English URLs start with `/docs/`;
translated URLs start with the language code, such as `/fr/docs/`.

## Repository layout

- `content/docs/<component>/`: maintained manuals and their required images.
- `content/`: localized home, documentation index, search, and attribution pages.
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

`make dev` uses the adjacent `../oink` checkout for theme development. Release
checks and builds must use the pinned module: unset `HUGO_MODULE_REPLACEMENTS`
and set `GOWORK=off` and `HUGO_MODULE_WORKSPACE=off`. Keep generated files out of
Git; `public/`, `resources/`, and local caches are ignored.

## Repository and publishing

- GitHub repository: <https://github.com/pgsty/doc.pg.center>
- Production branch: `main`.
- Intended public URL: <https://doc.pg.center/>.
- Hosting and deployment: **Cloudflare Pages**, connected to the GitHub repository.
- Cloudflare build command: `make build`; output: `public`; root: the repository root.
- Set `HUGO_VERSION=0.165.0` and `GO_VERSION=1.27.0` in Cloudflare, matching CI.
  Set `GOWORK=off` and `HUGO_MODULE_WORKSPACE=off`. Apply the same toolchain
  settings to preview builds; leave `HUGO_MODULE_REPLACEMENTS` unset.

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
