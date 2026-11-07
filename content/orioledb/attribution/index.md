---
title: Sources and licensing
description: OrioleDB snapshot coverage, original copyright, translation provenance, and retained source discrepancies.
weight: 60
type: docs
search_keywords: ["OrioleDB", "attribution"]
icon: fa-solid fa-scale-balanced
upstream_source: orioledb
upstream_link: https://www.orioledb.com/docs
upstream_notice: /orioledb/attribution/
upstream_modified: true
---

This is an independent community documentation edition maintained by [PGSTY](https://pgsty.com/). Development, releases, and support remain with [OrioleDB](https://www.orioledb.com/).

## Sources and coverage {#sources-and-coverage}

The English text and Chinese translations come from PGSTY's OrioleDB community edition, based on the live upstream website captured on **2026-11-06**. This collection includes all **18 documentation articles** and **two benchmark recipes**, plus section indexes and these edition notes: **26 pages in each language**.

The documentation covers the introduction, five usage guides, eight architecture articles, and four development guides. The benchmarks cover pgbench and vehicle tracking. Product landing pages, blog articles, author profiles, and tag archives remain outside this documentation collection.

The import record in `data/imports/orioledb.json` preserves source paths, source Markdown checksums, original HTML checksums, code fingerprints, and copied asset checksums. Images are shared between the English and Chinese page bundles. The [vehicle-tracking driver](/orioledb/assets/tracking-bench.py) is retained as source text for the benchmark recipe.

## Copyright and licenses {#copyright-and-licenses}

The [OrioleDB repository](https://github.com/orioledb/orioledb) offers Apache License 2.0 or the PostgreSQL License. The imported community edition selects the **PostgreSQL License** for project documentation. The full notice, **Copyright (c) 2025-2026, Supabase Inc.**, and warranty disclaimer are retained in [LICENSE-POSTGRESQL.txt](/third_party/orioledb/LICENSE-POSTGRESQL.txt).

The website states **Copyright © 2026 Supabase Inc**. Benchmark material, website illustrations, and trademarks retain their original rights. The source edition did not identify a separate blanket reuse license for these materials; they are recorded as **Upstream terms**, without assigning them the site's license or the software license. See the upstream [Apache license](https://github.com/orioledb/orioledb/blob/main/LICENSE-APACHE.txt) and [PATENTS](https://github.com/orioledb/orioledb/blob/main/PATENTS.txt) for the software's additional terms.

Chinese translation and community curation are credited to **PGSTY**. English remains authoritative. This integration preserves the source edition's translation status; importing it does not constitute a new line-by-line technical review. [PG.CENTER attribution](/attribution/#orioledb) records the collection alongside the site's other manuals.

## Changes in this edition {#changes-in-this-edition}

The source edition converted Docusaurus HTML into Hugo Markdown. This integration retains its explanatory text, code, tables, diagrams, footnotes, and heading IDs, while moving the introduction to its own page and adding a reading index. Internal documentation links use `/orioledb/` and `/zh/orioledb/`. HTML pages use native OINK attribution. A small site adapter reuses that attribution in Markdown and LLMS exports; section introductions retain the source notices for printing.

All sections share one OrioleDB sidebar. Paired heading IDs support Duo View and synchronized scrolling. Navigation, search, image zoom, expandable tables, code copying, print, and Markdown/LLMS exports use OINK **1.5.1**.

## Version context and source discrepancies {#version-context-and-source-discrepancies}

This is a website snapshot, not a manual for one pinned software release. Installation examples, experimental features, and benchmark recipes can refer to different builds. The source edition records these unresolved differences:

- The configuration reference gives rewind defaults of `500` seconds and `86400` transactions; the rewind tutorial uses `3600` and `100000`. Both pages retain their source values. Check the running build's settings.
- The block-device guide introduces direct block-device access but says the main data remains in the filesystem. The source wording is retained.
- The recovery example names worker #2 on both sides of one ordering comparison. This ambiguity is retained.
- The Chinese free-space discussion interprets “can just read” in the context of variable-length extents as an inability to rely solely on sequential reads, and clarifies a repeated checkpoint caption. The page-merge discussion corrects repeated sibling and figure references; the checkpoint discussion interprets “release the log” as releasing the lock. These are existing editorial decisions in the source translation.

The benchmark recipes preserve the upstream environment and methodology. Vehicle tracking uses patched PostgreSQL for both engines; pgbench uses a separate stock PostgreSQL build as its baseline. PG.CENTER has not independently rerun these benchmarks.
