---
title: Sources and licensing
description: Citus 14 upstream sources, snapshot coverage, copyright, licenses, and translation policy.
weight: 90
type: docs
icon: fa-solid fa-scale-balanced
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14
no_list: true
---

This is an independent PGSTY community edition of the [Citus 14 documentation on Microsoft Learn](https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14). It is published within **PG.CENTER**, using OINK **1.5.1** and Hugo Extended **0.168.0**. Microsoft and the Citus project do not maintain this edition.

## Sources and coverage {#sources}

The source snapshot was captured on **November 7, 2026**. It covers the upstream homepage and all **59 linked documentation pages**, including the ten technical articles retained in the manual. English and Chinese HTML and Markdown snapshots were downloaded for all 60 source URLs. Required figures are retained as 27 local page-bundle images.

The maintained edition has **67 pages per language**: 59 imported pages, six additional topic indexes, a collection homepage, and this source notice. Eight topic sections organize overview, installation, tutorials, modeling, administration, migration, reference, and articles. The original reference and guides indexes serve as two of those section indexes.

Microsoft Learn identifies [`MicrosoftDocs/azure-databases-docs`](https://github.com/MicrosoftDocs/azure-databases-docs) as its source repository. That public repository was unavailable at capture time. A [preserved repository snapshot](https://github.com/Kiranchandratrey/azure-databases-docs/tree/ff9de504fdbe2b7aa9d06411e0f0472d39dc1f14/citus), pinned to commit `ff9de504fdbe2b7aa9d06411e0f0472d39dc1f14`, retains the documentation source and license files. The published Learn pages can have newer individual revisions; the preserved commit is **not** a claim that all captured pages come from that revision.

The per-file [import manifest](https://github.com/pgsty/doc.pg.center/blob/main/data/imports/citus.json) records published source commits, source paths, capture hashes, heading IDs, code hashes, assets, and translation status. [The upstream registry](https://github.com/pgsty/doc.pg.center/blob/main/data/upstreams.yaml) records the edition and license checksums.

## Copyright and licenses {#licenses}

Copyright (c) Microsoft Corporation and contributors. Original Citus articles retain their authors' rights and links to their original publications.

The repository's documentation and other content are licensed under **[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)**. Code in that repository is licensed under **MIT**. The complete, unmodified texts are retained locally:

- [Documentation license — LICENSE](/third_party/citus/LICENSE)
- [Code license — LICENSE-CODE](/third_party/citus/LICENSE-CODE)
- [Legal and trademark notices — ThirdPartyNotices.md](/third_party/citus/ThirdPartyNotices.md)

These licenses do not grant rights to Microsoft's names, logos, or trademarks. PostgreSQL, Citus, Azure, and other product names remain the property of their respective owners. This edition's site-authored introductions, Chinese adaptations, and navigation use CC BY 4.0, subject to the original terms above.

## Articles and historical context {#articles}

The [article collection](/citus/articles/) contains the ten technical articles published in the Citus manual. It is not a mirror of the entire Citus corporate blog. Original-publication links are retained wherever the upstream manual supplies them. Examples, dates, benchmark results, and Citus Cloud retirement notices retain their historical context; a historical article's “latest version” does not describe the current Citus release.

## Editorial and translation policy {#editorial}

English is authoritative. The Chinese text published by Microsoft Learn is machine translated and is only a reference for this edition. PGSTY has edited all 59 imported Chinese pages against the English text, reviewed terminology and qualifications, and checked paired headings, examples, and links. The import manifest records the English revision used for each translation. Future unfinished pages must carry an explicit machine-draft notice.

This edition reorganizes navigation, rewrites internal links, preserves upstream heading anchors, stores figures locally, and converts Learn callouts to OINK callouts. It selects only content applicable to `citus-14`; older version blocks hidden in the Learn HTML are excluded. Code, commands, program output, SQL identifiers, and link destinations are preserved across languages. Markdown and complete-manual exports include source and rights notices.

Documented corrections include restoring exponent notation from the original Citus articles, repairing legacy cross-references, clarifying abbreviated tutorial examples and ports, and correcting a managed-service name. Seven program-output paragraphs retain their original line breaks in code blocks. These changes are recorded in the import manifest; the unmodified bilingual snapshots remain available in the local source archive.
