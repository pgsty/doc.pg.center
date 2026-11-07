---
title: Site maintenance
description: Build, preview, validate, and update this community documentation site.
weight: 30
icon: fa-solid fa-wrench
upstream_source: polardb
upstream_link: https://github.com/polardb/polardb-pg-docs/tree/b4733b0350888242afeba432a6837458c348a937
type: docs
---


PG.CENTER uses [Hugo Extended](https://gohugo.io/) 0.168.0 and the pinned [OINK v1.5.1](https://github.com/pgsty/oink/tree/v1.5.1) module. Go 1.27.3 resolves the theme dependency.

## Preview {#preview}

```bash
make serve
```

The default address is `http://localhost:1313/`. Home-page data lives in `data/home/`, navigation in `hugo.yaml`, and PolarDB articles in `content/polardb/`. English is the default language; Chinese pages use the `.zh.md` suffix. The public routes are `/polardb/` and `/zh/polardb/`.

## Build and validate {#build}

```bash
make check
make build
```

The check command builds to a temporary directory and audits local links, images, anchors, and outputs. A production build writes to `public/`, ready for a static web host.

## Update upstream {#upstream}

The source records the upstream revision in `data/upstreams.yaml` and the import provenance in `data/imports/polardb.json`. Markdown under `content/polardb/` is the maintained edition. Review upstream changes and language coverage, apply the relevant diff, and run the checks. The one-time importer refuses to overwrite maintained content. Keep raw downloads outside the site directory.

Database issues and original documentation corrections belong to the [upstream project](https://github.com/polardb/polardb-pg-docs).
