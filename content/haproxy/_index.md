---
title: "HAProxy 3.4.8 Documentation"
linkTitle: HAProxy
weight: 50
description: "Complete English Markdown edition of the HAProxy 3.4 Starter, Configuration, and Management manuals"
icon: fa-solid fa-network-wired
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
module: [HAPROXY]
categories: [Reference]
upstream_source: haproxy-20261121
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
cascade:
  upstream_source: haproxy-20261121
  type: docs
  module: [HAPROXY]
---

**HAProxy** is a free, fast, and reliable reverse proxy for high availability, TCP and HTTP load
balancing, and application traffic management. This component contains the complete English text of
the three core HAProxy 3.4 manuals, reorganized as one flat Markdown reading sequence for OINK.

This English edition follows the official **3.4.8 LTS** release of November 18, 2026,
pinned at [tag v3.4.8](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8).
Translations still follow the preceding `3.4.7-57` documentation snapshot pending synchronization.

## Choose a manual {#choose-a-manual}

- [Starter Guide](/haproxy/load-balancing/) — 9 topics on load-balancing concepts, HAProxy architecture, features, sizing, releases, and ecosystem.
- [Configuration Manual](/haproxy/http-fundamentals/) — 12 chapters covering proxies, ACLs, samples, logging, filters, and every option family.
- [Management Guide](/haproxy/prerequisites/) — 13 chapters on startup, reloads, resources, logging, statistics, runtime CLI, debugging, and security.
{.cards}

## Edition coverage {#edition-coverage}

| Manual | Upstream source | Local organization |
| --- | ---: | ---: |
| Starter Guide | 1,695 lines | 9 flat topic pages |
| Configuration Manual | 33,277 lines | 12 flat chapter pages |
| Management Guide | 5,305 lines | 13 flat chapter pages |

All 34 reading pages live directly under the HAProxy component root. Three non-linking divider
placeholders separate the manuals in the sidebar without adding directory levels or pager stops.

The complete original manuals are available at the pinned upstream revision linked above. The
[upstream license notice](/third_party/haproxy/LICENSE) and [GPLv2 text](/third_party/haproxy/GPL-2.0)
are published beside the manuals. The existing Simplified Chinese companion edition remains available while the 3.4.8 changes are translated.
