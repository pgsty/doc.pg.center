# Repository Guide

## OINK build baseline

As of 2026-11-07, this site uses OINK v1.5.1 and Hugo Extended 0.168.0.
Keep CI and local builds on this baseline. Do not enable `--panicOnWarning`
or `HUGO_PANICONWARNING`; keep warnings visible and review them. The upstream
LibSass deprecation warning is accepted. No external Sass compiler is required.

## Purpose

This repository contains the source for the **PG.CENTER** component documentation
site at **doc.pg.center**, part of **[pg.center](https://pg.center/)**, for the tools used
to run PostgreSQL in production. PGSTY maintains this independent community
edition. PostgreSQL core manuals, reference material, and ecosystem resources
live on the parent site; `/postgresql/` and `/zh/postgresql/` provide a version
navigation page linking those manuals. This repository maintains seventeen documentation
collections: six PostgreSQL operations tools and eleven bilingual database collections.
It uses Hugo Extended and the OINK theme, pinned as a Go module in
`go.mod` and `go.sum`.

Use **PG.CENTER** as the site identity in the title, navigation, footer, and
metadata, with the PostgreSQL elephant as the logo and browser icon. Keep
`doc.pg.center` as the documentation hostname and repository name. The top-level
Home link points to `https://pg.center/zh/` in Chinese and `https://pg.center/`
in all other languages. The local checkout is `~/www/doc.pg.center`.

## Documentation and languages

The six PostgreSQL operations manuals are available in **English (`en`), Simplified
Chinese (`zh`), French (`fr`), Japanese (`ja`), German (`de`), Russian (`ru`),
Arabic (`ar`), and Spanish (`es`)**. The eleven database collections are published
in English and Simplified Chinese only. Their source projects do not all publish
matching language editions, so the imported coverage and translation status are
recorded per collection.

### PostgreSQL operations tools

| Component | Documentation scope | Languages |
| --- | --- | --- |
| Patroni | PostgreSQL high availability, configuration, administration, and APIs | en, zh, fr, ja, de, ru, ar, es |
| pgBackRest | Backup, recovery, archiving, commands, and configuration | en, zh, fr, ja, de, ru, ar, es |
| PgBouncer | Connection pooling, installation, configuration, and administration | en, zh, fr, ja, de, ru, ar, es |
| pgBadger | Log analysis, command reference, sample reports, and release history | en, zh, fr, ja, de, ru, ar, es |
| HAProxy | Starter, Configuration, and Management manuals | en, zh, fr, ja, de, ru, ar, es |
| etcd | Operations, APIs, development, internals, and upgrades | en, zh, fr, ja, de, ru, ar, es |

### PostgreSQL database collections

| Collection | Documentation scope | Languages |
| --- | --- | --- |
| PolarDB | PolarDB for PostgreSQL features, deployment, operations, development, and internals | en, zh |
| IvorySQL | IvorySQL administration, Oracle compatibility, reference, migration, ecosystem, and development | en, zh |
| OpenHalo | OpenHalo and Halo Database MySQL compatibility, usage, boundaries, build, and configuration | en, zh |
| Babelfish | Babelfish usage, installation, compatibility, APIs, design, release history, and project material | en, zh |
| Percona pg_tde | Transparent data encryption architecture, installation, configuration, commands, operations, and reference | en, zh |
| Apache Cloudberry | 2.x MPP database build, deployment, data, performance, security, administration, references, PXF, and Core Internals | en, zh |
| AgensGraph | Graph database concepts, SQL/Cypher querying, operations, search, reference, and release notes | en, zh |
| pgEdge | Spock, LOLOR, SafeSession, Snowflake, installation, operations, recovery, and reference | en, zh |
| DocumentDB | Installation, operations, PostgreSQL API, commands, operators, configuration, and reference | en, zh |
| OrioleDB | PostgreSQL storage engine installation, configuration, architecture, development, and benchmarks | en, zh |
| Citus | Citus 14 architecture, deployment, tutorials, modeling, operations, migration, SQL/API reference, and technical articles | en, zh |

English is the source language for the paired manuals. Files without a language
suffix are English; translations use the same path with `.zh.md`, `.fr.md`,
`.ja.md`, `.de.md`, `.ru.md`, `.ar.md`, or `.es.md`. For example,
`content/pgbouncer/config.md` is the source for `content/pgbouncer/config.fr.md`.
The new database collections use `.zh.md` for Chinese pages; when an upstream
edition has no matching Chinese page, the English page remains available at the
English route and the coverage report records the gap. Each collection is a
top-level section with the `docs` content type. English URLs start with the
component name, such as `/patroni/`; translations prepend the language code, such
as `/fr/patroni/`. There is no `/docs/` section or index. Internal links, aliases,
and generated outputs must use the component routes without a `/docs/` prefix.

### Apache Cloudberry

`content/cloudberry/` contains the Docusaurus 2.x docs in
`apache/cloudberry-site` (`versioned_docs/version-2.x`) plus the PXF and Core
Internals submanuals pinned in `data/upstreams.yaml`.
Both submanuals use the Cloudberry sidebar and are excluded from the global
section switcher; do not give them `sidebar_root_for: self`. The section tree
follows each upstream sidebar, not the upstream directory layout:
each sidebar category is a Hugo section, and a category's linked doc is that
section's `_index.md`. Page bundles hold images.
Every heading carries the explicit `{#id}` that Docusaurus generates, so upstream
anchors and future translations stay aligned.

The checkers know Cloudberry's languages (`en`, `zh`). Both editions contain
641 complete pages, including PXF and Core Internals. Chinese headings retain the
English `{#id}` sequence; `check-content.py` verifies it. Translate explanatory
prose, descriptions, callout titles, tab labels, image alt text, and visible HTML
figure/table text. Preserve code, commands, program output, Mermaid source, and
link targets. Do not put English prose in Chinese pages or mark unfinished pages
as translated. The checkers still recognize `translation_status: placeholder`
for future additions and count those pages as untranslated. Such a placeholder
must link to its English page with raw HTML, since the link hook localizes ordinary
Markdown links. Do not add database menus, home cards, or footer links to other languages until
those editions exist. Cloudberry and the other database collections are linked from
the English and Chinese `Kernel` / `内核` menu only.

Chinese terminology distinguishes external table (外部表) from foreign table
(外表); foreign data wrapper is 外部数据包装器. Use 故障切换 for failover,
分区剪枝 for partition pruning, 压实 for compaction, 模式 for schema, 表空间
for tablespace, and AO 表 for append-optimized table. Preserve Coordinator,
Segment, Standby Coordinator, GPORCA, Interconnect, PXF, gpfdist, and tool names.
Use 派发 for dispatch, 切片 for slice, 进程组 for gang, and 分布位置 for
planner locus; optimizer cost is 代价, cost model is 代价模型. Do not confuse storage/WAL segments (段) with the Cloudberry Segment role.

Upstream prose escapes brackets as `\(` and `\[`. The site's math passthrough
reads those as formula delimiters, so converted text uses plain brackets; keep it
that way when syncing upstream changes.


### OrioleDB

`content/orioledb/` contains 18 documentation articles and two benchmark guides
from the reviewed bilingual edition in `~/pgsty/oriole.pgsty.com`, based on the
upstream website snapshot of 2026-11-06. With section indexes and editorial
pages, both languages contain 26 pages. The original documentation introduction
lives at `introduction/`; the collection root is a native OINK cards index.
Usage, architecture, contributing, and benchmarks share one sidebar. Images
are shared page-bundle resources. Only the benchmark driver and retained license
are static assets; blogs, product landing pages, and taxonomies are not imported.

`scripts/import-orioledb.py` records Markdown, upstream HTML, code, and asset
checksums in `data/imports/orioledb.json` and refuses to overwrite maintained
content. Updates are reviewed directly in Markdown. The collection registry
requires matching English/Chinese heading IDs and code blocks. Preserve the
website snapshot label and the distinction between PostgreSQL-licensed project
documentation and benchmark/website materials with their original terms.
`layouts/_partials/pgsql/export-annotations.md` is a site adapter that reuses
OINK's validated annotation data in OrioleDB Markdown and LLMSFULL exports.
The HTML reading shell and visible attribution remain theme-owned.

### Citus

`content/citus/` contains the Citus 14 edition captured from Microsoft Learn on
2026-11-07: 59 upstream pages (including ten retained blog articles), six additional
category indexes, a collection homepage, and a source/rights page in each language.
The eight topic sections share the Citus sidebar. Keep original heading IDs, code,
commands, program output, historical blog context, and article source links.
The Learn HTML includes hidden Citus 12/13 moniker blocks even when `view=citus-14`
is selected; filter those blocks during import. Do not infer the version from the
URL alone. English is authoritative; the upstream Chinese machine translation is
reference material, not a reviewed edition. Mark unfinished translations explicitly.
The maintained Chinese edition has all 59 imported pages edited against English.
Keep the translation-basis hashes in the import manifest current after review.

`scripts/fetch-citus.py` downloads snapshots outside the source tree;
`scripts/import-citus.py` converts them once and refuses to overwrite maintained
pages. `data/imports/citus.json` records per-page source revisions, HTML/Markdown
checksums, heading IDs, code hashes, images, and translation status. The former
MicrosoftDocs repository is unavailable; a pinned preserved fork supplies retained
CC BY 4.0 documentation, MIT code, and trademark notices under `static/third_party/citus/`.
The Citus source page distinguishes that archive from the live Learn snapshot.
`check-citus.py` checks all 612 examples per language, source anchors, assets,
licenses, translation provenance, and exported notices; `check-citus-search.cjs`
checks bilingual scoped search and its heading destinations. Both run in `make check`.

### Bilingual database collections

The eleven database collections are integrated directly below the site root: each
uses `/component/` for English and `/zh/component/` for Chinese pages that exist.
The English and Chinese home panels, the `Kernel` navigation menu, and the
footer kernel column use these same routes. Navigation and home panels put
PostgreSQL first, then the eleven kernels, then the six community components.
The navbar has Home, Kernel, and Community Components groups; languages without
kernel editions show Home and their localized community component group.
The PostgreSQL navbar entry opens the 18.6 manual on `pg.center` (English) or
`pgsql.cc` (Chinese), while its home card, footer, and section-switcher entry open
the local version guide. Kernel section weights are negative to precede the
operations manuals; keep their icons consistent with the home cards and menus.
`data/collections.json` is the language and pairing registry used by the route,
content, and coverage checkers;
`data/upstreams.yaml`, `data/licenses.yaml`, and `data/imports/` hold source
revisions, notices, and per-file migration provenance. The PostgreSQL entry has
`kind: navigation`: it is a site-authored guide, not an imported eighteenth manual.
The checkers validate its bilingual routes and outputs without requiring upstream
import attribution.

The import preserves upstream asymmetry and incomplete translation honestly.
PolarDB and IvorySQL retain unequal source language editions; AgensGraph keeps
Chinese draft pages and guide-only placeholders; pgEdge keeps its Chinese draft
coverage. DocumentDB has 300 complete English/Chinese page pairs. OpenHalo,
Babelfish, Percona pg_tde, and Cloudberry also have paired English and Chinese pages
for the imported scope. Do not put English prose into a Chinese page or label a
placeholder or machine draft as reviewed translation.

### DocumentDB

The DocumentDB edition has 300 English/Chinese page pairs, including category
indexes and the upstream forthcoming architecture notice. Its fixed source is
`documentdb/docs` at `cf69384e6da9524cc0fc723e8ac5b6c0689af432` plus
`documentdb/documentdb.github.io` at `90cfa088351557cd618034dfc00ab817c35a5f76`.
The website generates and corrects guides, so the docs repository alone is not
the complete published edition. `scripts/export-documentdb-website.mjs` exports
that site's article service; `scripts/import-documentdb-site.py` prepares a new
external staging directory and never overwrites maintained content. Preserve
both source revisions and per-page provenance in `data/imports/documentdb.json`.

Use native OINK cards, steps, code tabs, field tables, and expandable wide tables.
Chinese keeps English heading IDs and website anchor aliases. Preserve code,
inline literals, links, and quoted program errors; `scripts/check-documentdb.py`
checks structure, translation source hashes, and provenance. After an intentional
edit, update the paired translation and its recorded hashes. The Chinese edition
has undergone AI-assisted bilingual review. Editorial annotations for 40 pages
are maintained in `data/imports/documentdb-notes.json`; preserve their source
context and bilingual text.
The Kubernetes Operator's independent manual remains an external link; do not
silently expand this collection's scope. Retain notices on superseded guides and
the forthcoming architecture page.

## Repository layout

- `content/<component>/`: maintained manuals and their required images.
- `content/`: localized home, search, and attribution pages.
- `data/`: homepage and footer content, plus the upstream source and license registry.
  `data/logos.yaml` maps each collection route to the brand mark the home-page
  orbit and manual cards show (resolved by `pgsql/logo.html`, files under
  `static/img/logo/`, sources in `NOTICE.md`), so the eight home files carry no
  per-language logo paths; a route without an entry falls back to its card's
  Font Awesome `icon`, and an entry's `dark` (`mono`/`invert`/`rim`) says how
  a card lifts a dark mark off the dark ground. The PgBouncer mark is
  site-authored (no upstream logo exists); every other file is a project's
  own mark. A footer column with `span: 2` is laid out as two sub-columns
  filled top to bottom, so the kernel column stays six rows tall.
- `data/home/<lang>.yaml` + `layouts/_partials/pgsql/`: the home page is three
  site partials: `hero-orbit.html` (title, the eight reading languages, orbit),
  `manuals.html` (twelve kernel panels in `en` and `zh`, listed in the order
  they fill a three-column, four-row grid top to bottom and column by column,
  followed by six community tool panels with versions and shortcuts),
  and `about.html`. Keep the eight files in the same shape, and keep manual
  descriptions in a row to the same line count in every language. The kernel
  section uses `#kernels`, with `#databases` retained as a legacy anchor.
  `.pgsql-icon-postgresql` reuses `static/img/slonik.svg` as a CSS mask in menus
  and the section switcher.
- `layouts/`, `assets/`, and `i18n/`: templates, styles, scripts, and interface translations.
- `static/`: published assets, third-party notices, and linked pgBadger sample reports.
- `scripts/`: reusable import, source, build, route, link, coverage, and search checks.
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
3. **Update translations from the English diff.** For the six operations manuals,
   synchronize Chinese, French, Japanese, German, Russian, Arabic, and Spanish,
   including existing pages, additions, and removals. For a bilingual database
   collection, update its Chinese pages only when a reviewed Chinese edition exists;
   retain explicit notices for source gaps, placeholders, and machine drafts. Use
   consistent terminology and natural prose. Keep commands, configuration keys,
   API identifiers, code, and actual program output exact. Translate explanatory
   prose without changing its meaning.
4. **Update shared metadata.** Record the selected upstream revision and relevant
   checksums in `data/upstreams.yaml`. Keep page attribution, version labels,
   navigation, `NOTICE.md`, the English/Chinese attribution pages, and existing
   localized attribution pages consistent. Retain upstream copyright and license
   notices.
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
make serve                    # Production preview at http://localhost:1313
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
- Set `HUGO_VERSION=0.168.0` and `GO_VERSION=1.27.3` in Cloudflare. CI pins Hugo Extended 0.168.0 and pins Go 1.27.3; no external Sass is required.
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
