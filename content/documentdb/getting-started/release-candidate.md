---
title: 1.0 Release Candidates
description: The DocumentDB 1.0 release candidates have ended. DocumentDB 1.0 is released; upgrading hosts and volumes
  that ran a release candidate isn't supported.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/getting-started/release-candidate.md
weight: 1010
---

The 1.0 release candidates have ended: [DocumentDB 1.0](/documentdb/getting-started/release-notes-1.0/) was released on 2026-10-19, from the same commit as v1.0-RC2.

Upgrading hosts and data volumes that ran a release candidate to 1.0 isn't supported, and the installer refuses such hosts. Install 1.0 on a fresh host or a new volume, following [Pre-built Packages](/documentdb/getting-started/prebuilt-packages/) or [DocumentDB Local](/documentdb/documentdb-local/), and move any data you need with `mongodump` and `mongorestore`.
