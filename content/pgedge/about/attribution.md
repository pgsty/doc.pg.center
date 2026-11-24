---
title: Sources and attribution
description: Pinned sources, copyright notices, adaptations, and translation status.
weight: 10
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c
type: docs
---


## Versions and sources {#versions}

The English edition was updated on November 21, 2026. Spock follows a pre-release tag; SafeSession and Snowflake follow release tags; LOLOR follows unreleased 1.3.0 development. Chinese covers all four component snapshots.

| Extension | English source | Channel |
| --- | --- | --- |
| spock | [`d05e2e2b6a82`](https://github.com/pgEdge/spock/tree/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c) | v6.0.0-beta.2; pre-release |
| Spock 5.0 maintenance supplement | [`e710faa6fe21`](https://github.com/pgEdge/spock/tree/e710faa6fe21126d898fa660e9b6dc8ed0da9438) | [v5.0.15-rc.2 release notes](/pgedge/spock/spock-release-notes/#spock-5015-rc) and configuration changes |
| lolor | [`1548836b0df0`](https://github.com/pgEdge/lolor/tree/1548836b0df0819e5415a9d0574afd93e9a64f1d) | 1.3.0 development; latest stable v1.2.3 |
| safesession | [`d66225fcceef`](https://github.com/pgEdge/pgedge-safesession/tree/d66225fcceefa2b2cb2cdd7a0b8b84ccae8a4295) | v1.1 |
| snowflake | [`9506e1bd5c1f`](https://github.com/pgEdge/snowflake/tree/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8) | v2.6.1 |

## Copyright and adaptations {#copyright}

Original notices credit pgEdge, Inc., the PostgreSQL Global Development Group, and The Regents of the University of California. Spock's LICENSE and COPYRIGHT files use different year ranges, as do Snowflake's notices. Each file is preserved separately and verbatim.

Adaptations include MkDocs admonition conversion, local link rewriting, stable heading IDs, navigation, Chinese translations, and editorial guides. Commands, conditions, limitations, and warnings retain their upstream meaning. No publication date is invented for undated material; snapshot_date in the manifest refers only to the pinned commit.

Every imported page links to its exact source commit. Credits are carried into HTML, print, Markdown, and LLMS outputs. See the [complete license texts](/pgedge/about/license/).

## Chinese translations {#translation}

The community edition has 118 English/Chinese page pairs. This review added 66 Chinese pages, revised all 32 earlier GLM-assisted drafts against the English edition, and restored the article text on four Chinese section indexes. The SafeSession manual and changelog and the LOLOR release notes describe security issues from the administrator’s perspective, including affected behavior and fixes. The import manifest records the scope of the AI-assisted self-review for each page.

## Independence {#independence}

This community site does not imply official pgEdge endorsement or stewardship of the upstream extensions. Product and company names identify their respective sources.
