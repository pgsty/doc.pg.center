---
title: "etcd 3.7 Documentation"
linkTitle: "etcd 3.7"
description: "Official etcd 3.7 guides for developers, operators, upgrades, APIs, and internals."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd
categories: [Concept]
search_keywords: [v3.7.3, "Go 1.26.10", NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7"
cascade:
  upstream_source: etcd
  type: docs
  module: [ETCD]
---

etcd is a strongly consistent, distributed key-value store. These guides cover installing and
operating etcd, building applications against its APIs, understanding its design, measuring
performance, and upgrading or downgrading clusters in the 3.7 release line.

Start with [Quickstart](/etcd/quickstart/) for a local single-member cluster, [Install](/etcd/install/)
for supported installation paths, or [Operations guide](/etcd/op-guide/) for production deployments.

## etcd v3.7.3 {#etcd-v3-7-3}

The current maintenance release is [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3).
The installation, Docker, and Kubernetes examples in this edition target this release.

- Fixes data races between `Hash` and `Restore` in the MVCC store and in keys-only `RangeStream` operations, plus a replication performance regression caused by the leader sending `MsgApp` messages in reverse order.
- Builds with Go 1.26.10 and updates OpenTelemetry and `golang.org/x/net` dependencies to address reported security issues.
- Deprecates `NewJournalWriter` in `client/pkg/v3/logutil`; removal is planned for v3.8.

See the [upstream changelog](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22) for the complete changes.
