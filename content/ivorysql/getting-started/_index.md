---
title: Get started
description: Start IvorySQL with system requirements and a quick installation.
type: docs
weight: 20
no_list: true
upstream_source: ivorysql
upstream_link: https://github.com/IvorySQL/ivorysql_docs/tree/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1
---


- [Quick Start](/ivorysql/getting-started/quick-start/)
{.cards}

## Get a container image {#container-images}

Users in China can use the community Harbor registry. After pulling the image, follow the quick start to run and connect to the database.

```bash {tab="Docker Hub" group="ivorysql-registry" value="docker-hub"}
docker pull ivorysql/ivorysql:5.6-ubi8
```

```bash {tab="Harbor" value="harbor"}
docker pull registry.highgo.com/ivorysql/ivorysql:5.6-ubi8
```
