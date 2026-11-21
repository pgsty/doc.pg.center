---
title: 1.0 Release Candidates
description: The DocumentDB 1.0 release candidates have ended. DocumentDB 1.0 is released; upgrading hosts and volumes
  that ran a release candidate isn't supported.
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/getting-started/release-candidate.md
weight: 1010
---

The 1.0 release candidates have ended: [DocumentDB 1.0](/documentdb/getting-started/release-notes-1.0/) was released on 2026-10-19, from the same commit as v1.0-RC2.

Upgrading hosts and data volumes that ran a release candidate to 1.0 isn't supported, and the installer refuses such hosts. Install 1.0 on a fresh host or a new volume, following [Pre-built Packages](/documentdb/getting-started/prebuilt-packages/) or [DocumentDB Local](/documentdb/documentdb-local/), and move any data you need with `mongodump` and `mongorestore`.
