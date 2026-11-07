---
title: Quick start
description: A reading path for a two-node Spock cluster.
weight: 5
icon: fa-solid fa-rocket
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/4ac1aec2f0807dc7ee806ab99a6e99a4556186df
type: docs
---


Read the installation prerequisites, then follow the complete two-node procedure. Spock requires PostgreSQL server patches, compatible table definitions, and authenticated connections between nodes.

![Two PostgreSQL nodes accept reads and writes, with asynchronous bidirectional Spock replication.](/pgedge/assets/images/replication-light.svg)
{width="600" height="388" caption="Two-node replication. Commits complete locally; visibility on the other node depends on replication lag."}

- [Installation prerequisites](/pgedge/spock/installation/)
- [End-to-end installation](/pgedge/spock/getting-started/)
- [Two-node procedure](/pgedge/spock/two-node/)
- [Resource sizing](/pgedge/spock/sizing/)
- [Conflict types](/pgedge/spock/conflicts/)
- [Limitations](/pgedge/spock/limitations/)
{.cards}
