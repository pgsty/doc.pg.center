---
title: Sources and attribution
description: Pinned sources, copyright notices, adaptations, and translation status.
weight: 10
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/4ac1aec2f0807dc7ee806ab99a6e99a4556186df
type: docs
---


## Versions and sources {#versions}

This edition imports pinned snapshots of the four upstream `main` branches, retrieved on 2026-11-07. They can include changes newer than the versioned website. **These docs are not labeled as a stable Spock 6.0.0 manual or as an exact mirror of another release.** The original versioned entries—Spock 6.0.0 Beta, LOLOR 1.2.3, SafeSession 1.0, and Snowflake 2.6—remain linked for comparison with your installed binaries.

| Extension | Pinned commit | Versioned docs |
| --- | --- | --- |
| spock | [`4ac1aec2f080`](https://github.com/pgEdge/spock/tree/4ac1aec2f0807dc7ee806ab99a6e99a4556186df) | [Versioned docs](https://docs.pgedge.com/spock-v6/v6-0-0-beta/) |
| lolor | [`ac3893a7707a`](https://github.com/pgEdge/lolor/tree/ac3893a7707a65f71f494f260b1e3cd88f171770) | [Versioned docs](https://docs.pgedge.com/lolor/v1-2-3/) |
| safesession | [`b406cd1e82cf`](https://github.com/pgEdge/pgedge-safesession/tree/b406cd1e82cf21f30959351691c56de046562678) | [Versioned docs](https://docs.pgedge.com/pgedge-safesession/v1-0/) |
| snowflake | [`429a16803c8c`](https://github.com/pgEdge/snowflake/tree/429a16803c8c6336fcfede7cce0ccd3de05216d8) | [Versioned docs](https://docs.pgedge.com/snowflake/v2-6/) |

## Copyright and adaptations {#copyright}

Original notices credit pgEdge, Inc., the PostgreSQL Global Development Group, and The Regents of the University of California. Spock's LICENSE and COPYRIGHT files use different year ranges, as do Snowflake's notices. Each file is preserved separately and verbatim.

Adaptations include MkDocs admonition conversion, local link rewriting, stable heading IDs, navigation, Chinese translations, and editorial guides. Commands, conditions, limitations, and warnings retain their upstream meaning. No publication date is invented for undated material; snapshot_date in the manifest refers only to the pinned commit.

Every imported page links to its exact source commit. Credits are carried into HTML, print, Markdown, and LLMS outputs. See the [complete license texts](/pgedge/about/license/).

## Chinese translations {#translation}

GLM 5.3 assisted with Chinese drafts. The site workflow checks structure and code and samples technical meaning; a complete human sentence-by-sentence review is pending. Untranslated pages remain English, with clear links from Chinese indexes. Paired pages share heading IDs for Duo View.

## Independence {#independence}

This community site does not imply official pgEdge endorsement or stewardship of the upstream extensions. Product and company names identify their respective sources.
