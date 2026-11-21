---
title: Babelfish documentation
linkTitle: Babelfish
description: Technical documentation for installation, usage, internals, clients, and troubleshooting.
weight: -60
type: docs
icon: fa-solid fa-fish
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website
sidebar_root_for: self
sidebar_root_link_self: true
cascade:
  type: docs
  upstream_source: babelfish
upstream_notice: /babelfish/site/attribution/
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
---


Install Babelfish, choose a migration mode, assess compatibility, then connect your application. This collection preserves the upstream website documentation alongside a complete Chinese translation.

> [!NOTE] Version scope
> Upstream announced the move to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. This site preserves a fixed source snapshot; check historical limitations against the release you use.

## Release channels {#release-channels}

As of November 21, 2026, the latest public GitHub release of the [Babelfish open-source extensions](https://github.com/babelfish-for-postgresql/babelfish_extensions/releases) is **6.1.0**. [Babelfish 6.2.0 for Amazon Aurora PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraPostgreSQLReleaseNotes/AuroraBabelfish.Updates.html), announced on September 29, is a separate distribution and release channel. The preserved website manual is not a version-matched reference for either channel; use the release notes for the binaries you deploy.

New to Babelfish? Begin with the [overview](/babelfish/overview/), [source installation](/babelfish/installation/compiling-babelfish-from-source/), and [migration guide](/babelfish/usage/migration/).
